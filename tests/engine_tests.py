import unittest
from engine import get_rotation_power_fraction


class EngineTests(unittest.TestCase):
    def test_rotation_fraction_power_up(self):
        rotation_power = get_rotation_power_fraction(0)
        self.assertEqual(rotation_power[0], 1)
        self.assertEqual(rotation_power[1], 0)

    def test_rotation_fraction_power_right(self):
        rotation_power = get_rotation_power_fraction(90)
        self.assertEqual(rotation_power[0], 0)
        self.assertEqual(rotation_power[1], 1)

    def test_rotation_fraction_power_left(self):
        rotation_power = get_rotation_power_fraction(-90)
        self.assertEqual(rotation_power[0], 0)
        self.assertEqual(rotation_power[1], -1)


if __name__ == '__main__':
    unittest.main()
