import math

mars_gravity = -3.711


# Returns the amount of power distributed on the x and y axis, based on the rotation (trig).
# E.g. full power at 0 degrees will put all power up.
# Full power at 90 degrees will put all power to the right.
# Full power at 45 degrees will split up and right.
# The result will be returned as fractions of 1 in an array,
# with the first index meaning vertical, the second meaning horizontal
def get_rotation_power_fraction(rotation):
    radians = math.radians(rotation)
    x_fraction = math.sin(radians)
    y_fraction = math.cos(radians)
    if 0.00001 > x_fraction > -0.00001:
        x_fraction = 0
    if 0.00001 > y_fraction > -0.00001:
        y_fraction = 0
    return [y_fraction, x_fraction]


def get_distance(x1, x2, y1, y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance
