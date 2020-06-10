import random
import math
from lander import Lander, LanderState, max_rotation_change, max_power_change, max_power, min_power, max_rotation, \
    min_rotation, max_x_speed, max_y_speed
from laws import get_distance

population = []

population_count = 40
graded_retention_value = 0.2
ungraded_retention_value = 0.1
mutation_rate = 0.1
weight_location = 25
weight_rotation = 0
weight_speed_x = 100
weight_speed_y = 100

winning_score = 100_000_000_000


def get_random_action(current_rotation, current_power):
    random_rotation = random.randrange(current_rotation - max_rotation_change,
                                       current_rotation + max_rotation_change + 1)
    random_power = random.randrange(current_power - max_power_change,
                                    current_power + max_power_change + 1)
    if random_rotation > max_rotation:
        random_rotation = max_rotation
    if random_rotation < min_rotation:
        random_rotation = min_rotation
    if random_power > max_power:
        random_power = max_power
    if random_power < min_power:
        random_power = min_power
    return [
        random_rotation,
        random_power
    ]


def get_score(lander: Lander, landing_zones, lander_state: LanderState):
    x_coord = round(lander.x)
    y_coord = round(lander.y)
    speed_x = math.fabs(lander.x_speed)
    speed_y = math.fabs(lander.y_speed)
    initial_x = lander.actions[0][2]
    initial_y = lander.actions[0][3]
    rotation = math.fabs(lander.rotation)
    # Score based on distance from landing zone,
    # Distance from acceptable x and y speeds,
    # And distance from acceptable rotation.
    # Normalized down to between 0 and 1.
    if lander_state is LanderState.LANDED:
        # This should do for max score.
        return winning_score
    location_score = 0
    for zone in landing_zones:
        start_x = zone[0][0]
        end_x = zone[-1][0]
        middle_x = (start_x + end_x) / 2  # Center of landing zone, the closer, the better.
        ground_y = zone[0][1]
        distance_to_landing_zone = get_distance(x_coord, middle_x, y_coord, ground_y)
        distance_to_starting_point = get_distance(initial_x, middle_x, initial_y, ground_y)
        # Normalization in comparison to where we started.
        # We want to be between 1 and 0, with 1 being the best possible.
        if distance_to_landing_zone <= 0:
            location_score_comparison = 1
            if location_score_comparison > location_score:
                location_score = location_score_comparison
            break
        achieved_distance_ratio = distance_to_landing_zone / distance_to_starting_point
        if achieved_distance_ratio > 1:
            location_score_comparison = 0
            if location_score_comparison > location_score:
                location_score = location_score_comparison
            break
        location_score_comparison = 1 - achieved_distance_ratio
        if location_score_comparison > location_score:
            location_score = location_score_comparison

    if rotation == 0:
        rotation_score = 1
    else:
        rotation_score = 1 - (rotation / (max_rotation / 2))
    if speed_x == 0:
        x_speed_score = 1
    else:
        x_speed_score = 1 - (speed_x / (max_x_speed / 4))
    if speed_y == 0:
        y_speed_score = 1
    else:
        y_speed_score = 1 - (speed_y / (max_y_speed / 4))
    score = location_score * weight_location + \
            rotation_score * weight_rotation + \
            x_speed_score * weight_speed_x + \
            y_speed_score * weight_speed_y
    return score


def create_child(parent1, parent2):
    parent1_actions = parent1[1].actions
    parent2_actions = parent2[1].actions
    child_actions = parent1_actions[:len(parent1_actions) // 2] + parent2_actions[len(parent2_actions) // 2:]
    for index in range(len(child_actions)):
        if index == 0:
            continue
        # Applying mutations
        if random.random() < mutation_rate:
            previous_action = child_actions[index - 1]
            child_actions[index] = get_random_action(previous_action[0],
                                                     previous_action[1])
    return child_actions


def select_parents(parents):
    return random.choices(parents, k=2)


def build_new_generation(sorted_landers):
    graded_amount = len(sorted_landers) * graded_retention_value
    ungraded_amount = len(sorted_landers) * ungraded_retention_value
    graded_landers = sorted_landers[:int(graded_amount)]
    remaining_landers = sorted_landers[int(graded_amount):]
    ungraded_landers = random.sample(remaining_landers, int(ungraded_amount))
    parents = graded_landers + ungraded_landers
    new_generation = []
    while len(new_generation) < population_count:
        selected_parents = select_parents(parents)
        new_generation.append(create_child(selected_parents[0], selected_parents[1]))
    return new_generation
