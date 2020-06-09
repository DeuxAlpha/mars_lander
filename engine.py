from lander import Lander, LanderState
from maps import get_maps
import matplotlib.pyplot as plt
import numpy as np
import math
import algorithm

max_height = 3000
max_width = 7000
ground = [[], []]

game_map = get_maps()[0]


def init(lander: Lander, x, y, power, rotation, fuel, initialize_actions):
    lander.x = x
    lander.y = y
    lander.power = power
    lander.rotation = rotation
    lander.fuel = fuel
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


def get_lander_state(lander: Lander):
    # For a landing to be successful, the ship must:
    # land on flat ground
    # land in a vertical position (tilt angle = 0°)
    # vertical speed must be limited ( ≤ 40m/s in absolute value)
    # horizontal speed must be limited ( ≤ 20m/s in absolute value)
    lander_x = lander.x
    lander_y = lander.y
    if lander_y > max_height or lander_y < 0:
        return LanderState.ESCAPED
    if lander_x > max_width or lander_x < 0:
        return LanderState.OUT_OF_RANGE
    x_ground = ground[1][round(lander_x)]
    if lander_y > x_ground:
        # We have not yet reached the ground.
        return LanderState.LANDING
    # Otherwise, calculate whether it was a smooth landing.
    if not is_flat_ground(lander_x) or \
            not lander.rotation == 0 or \
            math.fabs(lander.y_speed) > 40 or \
            math.fabs(lander.x_speed) > 20:
        return LanderState.CRASHED
    return LanderState.LANDED


define_map()
show_map()

landing_zones = get_landing_zones()

# TODO: It seems like there's a bug that switches the rotations after every generation

generations = 0
landed = False
while landed is False:
    lander_scores = []
    for pop in range(algorithm.population_count):
        if len(algorithm.population) - 1 > pop:
            lander = algorithm.population[pop]
            init(lander, 2500, 2700, 0, 0, 5501, False)
        else:
            lander = Lander()
            init(lander, 2500, 2700, 0, 0, 5501, True)
        lander.print_stats()
        turn = 0
        lander_state = get_lander_state(lander)
        while lander_state is LanderState.LANDING:
            turn += 1
            if len(lander.actions) > turn:
                actions = lander.actions[turn]
            else:
                # We never got this far, so we need new actions.
                actions = algorithm.get_random_action(lander)
            lander.apply_changes(actions[0], actions[1])
            lander.apply_new_parameters(turn)
            print("Turn {0}".format(turn))
            lander.print_stats()
            lander_state = get_lander_state(lander)
        lander.actions = lander.actions[:turn + 1]
        print(lander_state)
        add_lander_to_map(lander.actions)
        lander_score = algorithm.get_score(lander, landing_zones, lander_state)
        lander_scores.append([lander_score, lander])

    show_map()
    generations += 1
    sorted_scores = sorted(lander_scores, key=lambda score: score[0], reverse=True)
    new_generation = algorithm.build_new_generation(sorted_scores)
    algorithm.population = []
    for gen_actions in new_generation:
        new_lander = Lander()
        new_lander.actions = gen_actions
        algorithm.population.append(new_lander)
