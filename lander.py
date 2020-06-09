from enum import Enum

from laws import mars_gravity, get_rotation_power_fraction

class Lander:
    max_rotation = 90
    min_rotation = -90
    max_power = 4
    min_power = 0
    max_x_speed = 500
    max_y_speed = 500
    max_rotation_change = 15
    max_power_change = 1
    fuel_cost = 10  # How much fuel gets consumed per value of power.

    x = 0
    y = 0
    fuel = 0
    power = 0
    rotation = 0
    x_speed = 0
    y_speed = 0
    actions = []

    # Applies changes to the mars lander.
    # Rules based on max values and max changes get applied, so invalid values get clamped.
    # Also updates the fuel based on the new power.
    def apply_changes(self, new_rotation, new_power):
        # For some reason positive rotation goes left and negative goes right.
        new_rotation = -new_rotation
        if new_rotation > self.rotation + self.max_rotation_change:
            print("New rotation {0} over max rotation change. Clamping.".format(new_rotation))
            new_rotation = self.rotation + self.max_rotation_change
            if new_rotation > self.max_rotation:
                print("New rotation {0} over overall max value. Clamping.".format(new_rotation))
                new_rotation = self.max_rotation
        elif new_rotation < self.rotation - self.max_rotation_change:
            print("New rotation {0} over max rotation change. Clamping.".format(new_rotation))
            new_rotation = self.rotation - self.max_rotation_change
            if new_rotation < self.min_rotation:
                print("New rotation {0} under overall min value. Clamping.".format(new_rotation))
                new_rotation = self.min_rotation
        if new_power > self.power + self.max_power_change:
            print("New power {0} over max power change. Clamping.".format(new_power))
            new_power = self.power + self.max_power_change
            if new_power > self.max_power:
                print("New power {0} over overall max value. Clamping.".format(new_power))
                new_power = self.max_power
        elif new_power < self.power - self.max_power_change:
            print("New power {0} over max power change. Clamping.".format(new_power))
            new_power = self.power - self.max_power_change
            if new_power < self.min_power:
                print("New power {0} under overall min value. Clamping".format(new_power))
                new_power = self.min_power
        self.rotation = new_rotation
        self.power = new_power
        self.fuel -= new_power * self.fuel_cost

    def apply_new_parameters(self, turn):
        rotation_fractions = get_rotation_power_fraction(self.rotation)
        applied_rotation_fractions = [rotation_fractions[0] * self.power, rotation_fractions[1] * self.power]
        new_y_speed = applied_rotation_fractions[0] + mars_gravity + self.y_speed
        new_x_speed = applied_rotation_fractions[1] + self.x_speed
        if new_y_speed > self.max_y_speed:
            print("New Y speed {0} over overall max value. Clamping".format(new_y_speed))
            new_y_speed = self.max_y_speed
        if new_x_speed > self.max_x_speed:
            print("New X speed {0} over overall max value. Clamping".format(new_x_speed))
            new_x_speed = self.max_x_speed
        new_y = self.y + new_y_speed
        new_x = self.x + new_x_speed
        self.x_speed = new_x_speed
        self.y_speed = new_y_speed
        self.x = new_x
        self.y = new_y
        if len(self.actions) < turn + 1:
            self.actions.append([self.rotation, self.power, self.x, self.y])
        else:
            self.actions[turn] = [self.rotation, self.power, self.x, self.y]
        # self.actions.append([self.x, self.y, self.rotation, self.power])

    def print_stats(self):
        print("X={0}, Y={1}, HSpeed={2}m/s VSpeed={3}m/s".format(round(self.x),
                                                                 round(self.y),
                                                                 round(self.x_speed),
                                                                 round(self.y_speed)))
        print("Fuel={0}, Angle={1}, Power={2} ({2}m/s2)".format(self.fuel, self.rotation, self.power))


class LanderState(Enum):
    LANDING = 1
    LANDED = 2
    CRASHED = 3
    ESCAPED = 4
    OUT_OF_RANGE = 5
