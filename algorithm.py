import random
import math

from lander import Lander, LanderState
from laws import get_distance

population_count = 20
population = []

graded_retention_value = 0.3
ungraded_retention_value = 0.2


def get_random_action(lander: Lander):
    current_rotation = lander.rotation
    current_power = lander.power
    random_rotation = random.randrange(current_rotation - lander.max_rotation_change,
                                       current_rotation + lander.max_rotation_change + 1)
    random_power = random.randrange(current_power - lander.max_power_change,
                                    current_power + lander.max_power_change + 1)
    if random_rotation > lander.max_rotation:
        random_rotation = lander.max_rotation
    if random_rotation < lander.min_rotation:
        random_rotation = lander.min_rotation
    if random_power > lander.max_power:
        random_power = lander.max_power
    if random_power < lander.min_power:
        random_power = lander.min_power
    return [
        random_rotation,
        random_power
    ]


def get_score(lander: Lander, landing_zones, lander_state: LanderState):
    x_coord = round(lander.x)
    y_coord = round(lander.y)
    speed_x = math.fabs(lander.x_speed)
    speed_y = math.fabs(lander.y_speed)
    initial_x = lander.actions[0][0]
    initial_y = lander.actions[0][1]
    rotation = math.fabs(lander.rotation)
    # Score based on distance from landing zone,
    # Distance from acceptable x and y speeds,
    # And distance from acceptable rotation.
    # Normalized down to between 0 and 1.
    if lander_state is LanderState.LANDED:
        return 1
    location_score = 0
    for zone in landing_zones:
        start_x = zone[0][0]
        end_x = zone[-1][0]
        ground_y = zone[0][1]
        if x_coord < start_x:
            # Lander is to the left of landing zone.
            distance_to_landing_zone = get_distance(x_coord, start_x, y_coord, ground_y)
            distance_to_starting_point = get_distance(initial_x, start_x, initial_y, ground_y)
            pass
        elif x_coord > end_x:
            # Lander is to the right of landing zone.
            distance_to_landing_zone = get_distance(x_coord, end_x, y_coord, ground_y)
            distance_to_starting_point = get_distance(initial_x, end_x, initial_y, ground_y)
            pass
        else:
            # Lander must be in the landing zone.
            distance_to_landing_zone = get_distance(1, 1, y_coord, ground_y)
            distance_to_starting_point = get_distance(initial_x, x_coord, initial_y, ground_y)
            pass
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
        rotation_score = 1 - (rotation / (lander.max_rotation / 2))
    if speed_x == 0:
        x_speed_score = 1
    else:
        x_speed_score = 1 - (speed_x / (lander.max_x_speed / 2))
    if speed_y == 0:
        y_speed_score = 1
    else:
        y_speed_score = 1 - (speed_y / (lander.max_y_speed / 2))
    weight_location = 60
    weight_rotation = 20
    weight_speed_x = 20
    weight_speed_y = 20
    score = location_score * weight_location + \
            rotation_score * weight_rotation + \
            x_speed_score * weight_speed_x + \
            y_speed_score * weight_speed_y
    return score


def create_child(parent1, parent2):
    parent1_actions = parent1[1].actions
    parent2_actions = parent2[1].actions
    child_actions = parent1_actions[:len(parent1_actions) // 2] + parent2_actions[len(parent2_actions) // 2:]
    # No mutations yet
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
