from enum import Enum
from laws import mars_gravity, get_rotation_power_fraction
import random

max_rotation = 90
min_rotation = -90
max_power = 4
min_power = 0
max_x_speed = 500
max_y_speed = 500
max_rotation_change = 15
max_power_change = 1
fuel_cost = 10  # How much fuel gets consumed per value of power.


class Lander:
    x = 0
    y = 0
    fuel = 0
    power = 0
    rotation = 0
    x_speed = 0
    y_speed = 0
    actions = []

    def get_changes(self, new_rotation, new_power):
        if new_rotation > self.rotation + max_rotation_change:
            print("New rotation {0} over max rotation change. Clamping.".format(new_rotation))
            new_rotation = self.rotation + max_rotation_change
            if new_rotation > max_rotation:
                print("New rotation {0} over overall max value. Clamping.".format(new_rotation))
                new_rotation = max_rotation
        elif new_rotation < self.rotation - max_rotation_change:
            print("New rotation {0} over max rotation change. Clamping.".format(new_rotation))
            new_rotation = self.rotation - max_rotation_change
            if new_rotation < min_rotation:
                print("New rotation {0} under overall min value. Clamping.".format(new_rotation))
                new_rotation = min_rotation
        if new_power > self.power + max_power_change:
            print("New power {0} over max power change. Clamping.".format(new_power))
            new_power = self.power + max_power_change
            if new_power > max_power:
                print("New power {0} over overall max value. Clamping.".format(new_power))
                new_power = max_power
        elif new_power < self.power - max_power_change:
            print("New power {0} over max power change. Clamping.".format(new_power))
            new_power = self.power - max_power_change
            if new_power < min_power:
                print("New power {0} under overall min value. Clamping".format(new_power))
                new_power = min_power
        # Adjust to account for fuel
        new_fuel = self.fuel - new_power * fuel_cost
        while new_fuel < 0 and new_power > 0:
            new_power -= 1
            new_fuel = self.fuel - new_power * fuel_cost
        return [new_rotation, new_power]

    # Applies changes to the mars lander.
    # Rules based on max values and max changes get applied, so invalid values get clamped.
    # Also updates the fuel based on the new power.
    def apply_changes(self, new_rotation, new_power):
        self.rotation = new_rotation
        self.power = new_power
        self.fuel -= new_power * fuel_cost

    def get_new_parameters(self, rotation, power):
        rotation_fractions = get_rotation_power_fraction(rotation)
        applied_rotation_fractions = [rotation_fractions[0] * power, rotation_fractions[1] * power]
        new_y_speed = applied_rotation_fractions[0] + mars_gravity + self.y_speed
        new_x_speed = applied_rotation_fractions[1] + self.x_speed
        if new_y_speed > max_y_speed:
            print("New Y speed {0} over overall max value. Clamping".format(new_y_speed))
            new_y_speed = max_y_speed
        if new_x_speed > max_x_speed:
            print("New X speed {0} over overall max value. Clamping".format(new_x_speed))
            new_x_speed = max_x_speed
        new_y = self.y + new_y_speed
        new_x = self.x + new_x_speed
        return [new_x, new_y, new_x_speed, new_y_speed]

    def apply_new_parameters(self, new_x, new_y, new_x_speed, new_y_speed, turn):
        self.x = new_x
        self.y = new_y
        self.x_speed = new_x_speed
        self.y_speed = new_y_speed
        if len(self.actions) < turn + 1:
            self.actions.append([self.rotation, self.power, self.x, self.y])
        else:
            self.actions[turn] = [self.rotation, self.power, self.x, self.y]

    def print_stats(self):
        print("X={0}, Y={1}, HSpeed={2}m/s VSpeed={3}m/s".format(round(self.x),
                                                                 round(self.y),
                                                                 round(self.x_speed),
                                                                 round(self.y_speed)))
        print("Fuel={0}, Angle={1}, Power={2} ({2}m/s2)".format(self.fuel, self.rotation, self.power))

    def get_random_action(self):
        current_rotation = self.rotation
        current_power = self.power
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

    # Pls only call if we actually crashed into the landing zone.
    # This method is going to try and adjust its last action to allow for proper landing.
    def adjust_to_land(self):
        # Let's just try and set the rotation of the last action to 0 and see if that does the trick.
        self.actions[-1][0] = 0


class LanderState(Enum):
    LANDING = 1
    LANDED = 2
    CRASHED = 3
    ESCAPED = 4
    OUT_OF_RANGE = 5
