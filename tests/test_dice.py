"""
Unit tests for deterministic dice roller.
"""

import unittest
from tools.dice import parse_dice, roll_dice, roll_d20


class TestDice(unittest.TestCase):

    def test_parse_dice_standard(self):
        self.assertEqual(parse_dice("1d20"), (1, 20, 0))
        self.assertEqual(parse_dice("2d6+3"), (2, 6, 3))
        self.assertEqual(parse_dice("3d8-2"), (3, 8, -2))
        self.assertEqual(parse_dice("d20"), (1, 20, 0))
        self.assertEqual(parse_dice("5"), (0, 0, 5))

    def test_parse_dice_invalid(self):
        with self.assertRaises(ValueError):
            parse_dice("invalid_dice")
        with self.assertRaises(ValueError):
            parse_dice("1d0")

    def test_roll_dice_bounds(self):
        for _ in range(100):
            res = roll_dice("1d20+5")
            self.assertGreaterEqual(res["total"], 6)
            self.assertLessEqual(res["total"], 25)
            self.assertEqual(res["modifier"], 5)

    def test_advantage_and_disadvantage(self):
        res_adv = roll_dice("1d20", advantage=True, seed=42)
        self.assertEqual(res_adv["advantage_mode"], "ADVANTAGE")
        self.assertEqual(len(res_adv["individual_rolls"]), 1)
        self.assertEqual(len(res_adv["dropped_rolls"]), 1)

        res_disadv = roll_dice("1d20", disadvantage=True, seed=42)
        self.assertEqual(res_disadv["advantage_mode"], "DISADVANTAGE")

    def test_critical_damage_doubling(self):
        res = roll_dice("2d6+3", is_critical=True, seed=42)
        self.assertEqual(res["count"], 4)
        self.assertEqual(len(res["individual_rolls"]), 4)

    def test_roll_d20_helper(self):
        res = roll_d20(modifier=4, seed=123)
        self.assertEqual(res["modifier"], 4)
        self.assertEqual(res["total"], res["individual_rolls"][0] + 4)


if __name__ == "__main__":
    unittest.main()
