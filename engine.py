from lander import Lander, LanderState
from params import get_maps, get_initial_state
import matplotlib.pyplot as plt
import numpy as np
import math
import algorithm
import time

initial_params = get_initial_state()[2]
game_map = get_maps()[2]

max_height = 3000
max_width = 7000
start_x = initial_params[0]
start_y = initial_params[1]
start_speed_x = initial_params[2]
start_speed_y = initial_params[3]
start_fuel = initial_params[4]
start_rotation = initial_params[5]
start_power = initial_params[6]
ground = [[], []]


def init(lander: Lander, x, y, power, rotation, fuel, x_speed, y_speed, initialize_actions):
    lander.x = x
    lander.y = y
    lander.power = power
    lander.rotation = rotation
    lander.fuel = fuel
    lander.x_speed = x_speed
    lander.y_speed = y_speed
    if initialize_actions:
        lander.actions = [[rotation, power, x, y]]


def fit_range(x_start, x_end, y_start, y_end):
    x_difference = x_end - x_start
    y_difference = y_end - y_start
    if y_difference == 0:
        return [np.arange(x_start, x_end, 1), np.full(x_difference, y_start)]
    else:
        fitted_range = [np.arange(x_start, x_end, 1), np.arange(y_start, y_end, y_difference / x_difference)]
        # There are times when np.arange creates too many items in comparison to the other array.
        # E.g. the first array has 500 items, the second one has 501.
        while len(fitted_range[0]) < len(fitted_range[1]):
            fitted_range[1] = fitted_range[1][:-1]  # Returns all but the last element (i.e. pop)
        return fitted_range


def add_lander_to_map(lander_history):
    x_values = [history[2] for history in lander_history]
    y_values = [history[3] for history in lander_history]
    plt.plot(x_values, y_values)


def show_map():
    plt.plot(max_width, max_height, ground[0], ground[1])
    plt.show()


def define_map():
    for index in range(len(game_map) - 1):
        this_zone = game_map[index]
        next_zone = game_map[index + 1]
        zone_range = fit_range(this_zone[0], next_zone[0], this_zone[1], next_zone[1])
        ground[0] += list(zone_range[0])
        ground[1] += list(zone_range[1])


def is_flat_ground(x):
    x_int = round(x)
    return ground[1][x_int - 1] == ground[1][x_int] == ground[1][x_int + 1]


def get_landing_zones():
    spots = len(ground[0])
    if spots != len(ground[1]):
        raise (Exception("X and Y coordinates do not match."))
    landing_zones = []
    flat_ground = []
    for location in range(spots):
        x_coordinate = ground[0][location]
        y_coordinate = ground[1][location]
        if is_flat_ground(x_coordinate):
            flat_ground.append([x_coordinate, y_coordinate])
        else:
            if len(flat_ground) > 0:
                landing_zones.append(flat_ground)
                flat_ground = []
    return landing_zones


def get_state(x, y, x_speed, y_speed, rotation):
    # For a landing to be successful, the ship must:
    # land on flat ground
    # land in a vertical position (tilt angle = 0°)
    # vertical speed must be limited ( ≤ 40m/s in absolute value)
    # horizontal speed must be limited ( ≤ 20m/s in absolute value)
    if y > max_height or y < 0:
        return LanderState.ESCAPED
    if x > max_width or x < 0:
        return LanderState.OUT_OF_RANGE
    x_ground = ground[1][round(x)]
    if y > x_ground:
        # We have not yet reached the ground.
        return LanderState.LANDING
    # Otherwise, calculate whether it was a smooth landing.
    if not is_flat_ground(x) or \
            not rotation == 0 or \
            math.fabs(y_speed) > 40 or \
            math.fabs(x_speed) > 20:
        return LanderState.CRASHED
    return LanderState.LANDED


define_map()
show_map()

landing_zones = get_landing_zones()

# TODO: It seems like there's a bug that switches the rotations after every generation

sorted_scores = []
generations = 0
landed = False
alg_start = time.time()
while landed is False:
    lander_scores = []
    for pop in range(algorithm.population_count):
        if len(algorithm.population) - 1 > pop:
            lander = algorithm.population[pop]
            init(lander, start_x, start_y, start_power, start_rotation, start_fuel, start_speed_x, start_speed_y, False)
        else:
            lander = Lander()
            init(lander, start_x, start_y, start_power, start_rotation, start_fuel, start_speed_x, start_speed_y, True)
        lander.print_stats()
        turn = 0
        lander_state = get_state(lander.x, lander.y, lander.x_speed, lander.y_speed, lander.rotation)
        while lander_state is LanderState.LANDING:
            turn += 1
            if len(lander.actions) > turn:
                actions = lander.actions[turn]
            else:
                # We never got this far, so we need new actions.
                actions = lander.get_random_action()
            # This section gets what the new parameters of the lander WOULD be.
            new_changes = lander.get_changes(actions[0], actions[1])
            new_parameters = lander.get_new_parameters(new_changes[0], new_changes[1])
            new_state = get_state(new_parameters[0],
                                  new_parameters[1],
                                  new_parameters[2],
                                  new_parameters[3],
                                  new_changes[0])
            if new_state != LanderState.LANDING:
                # Trying to land this thing safely.
                # Simply setting rotation to 0 for now to see if that does the trick.
                new_changes = lander.get_changes(0, actions[1])
                new_parameters = lander.get_new_parameters(new_changes[0], new_changes[1])
            # This section actually applies the changes. This allows
            lander.apply_changes(new_changes[0], new_changes[1])
            lander.apply_new_parameters(new_parameters[0],
                                        new_parameters[1],
                                        new_parameters[2],
                                        new_parameters[3],
                                        turn)
            print("Turn {0}".format(turn))
            lander.print_stats()
            lander_state = get_state(lander.x, lander.y, lander.x_speed, lander.y_speed, lander.rotation)
        # Chopping actions so none are left from the last generation of we crashed earlier this time.
        lander.actions = lander.actions[:turn + 1]
        print(lander_state)
        if lander_state is LanderState.LANDED:
            print("We fucking landed dis shit")
            landed = True
        add_lander_to_map(lander.actions)
        lander_score = algorithm.get_score(lander, landing_zones, lander_state)
        lander_scores.append([lander_score, lander])

    # TODO: Give scores for good coasting, e.g. Keeping overall vertical and horizontal speed within desired parameters.
    show_map()
    generations += 1
    sorted_scores = sorted(lander_scores, key=lambda score: score[0], reverse=True)
    new_generation = algorithm.build_new_generation(sorted_scores)
    algorithm.population = []
    for gen_actions in new_generation:
        new_lander = Lander()
        new_lander.actions = gen_actions
        algorithm.population.append(new_lander)

alg_stop = time.time()
alg_total = alg_stop - alg_start

successful_landers = list(filter(lambda score: score[0] == algorithm.winning_score, sorted_scores))
print("Landed after {0} generations.".format(generations))
print("Successful landers: {0}".format(len(successful_landers)))
print("Total time: {0}".format(alg_total))
for lander in successful_landers:
    add_lander_to_map(lander[1].actions)
show_map()
