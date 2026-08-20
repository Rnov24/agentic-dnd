"""
Unit tests for 5e 2024 mechanics.
"""

import unittest
from tools.mechanics import (
    calculate_modifier,
    calculate_proficiency_bonus,
    calculate_dc,
    roll_check,
    roll_saving_throw,
    validate_action,
)


class TestMechanics(unittest.TestCase):

    def test_calculate_modifier(self):
        self.assertEqual(calculate_modifier(10), 0)
        self.assertEqual(calculate_modifier(11), 0)
        self.assertEqual(calculate_modifier(12), 1)
        self.assertEqual(calculate_modifier(18), 4)
        self.assertEqual(calculate_modifier(20), 5)
        self.assertEqual(calculate_modifier(8), -1)
        self.assertEqual(calculate_modifier(6), -2)

    def test_proficiency_bonus(self):
        self.assertEqual(calculate_proficiency_bonus(1), 2)
        self.assertEqual(calculate_proficiency_bonus(4), 2)
        self.assertEqual(calculate_proficiency_bonus(5), 3)
        self.assertEqual(calculate_proficiency_bonus(9), 4)
        self.assertEqual(calculate_proficiency_bonus(13), 5)
        self.assertEqual(calculate_proficiency_bonus(17), 6)

    def test_calculate_dc(self):
        self.assertEqual(calculate_dc("easy"), 10)
        self.assertEqual(calculate_dc("medium"), 15)
        self.assertEqual(calculate_dc("hard"), 20)
        self.assertEqual(calculate_dc(18), 18)

    def test_roll_check_proficiency_and_expertise(self):
        character = {
            "name": "Aria",
            "level": 3,
            "stats": {"dexterity": 18},  # mod +4
            "proficiencies": {
                "skills": ["acrobatics"],
                "expertise": ["stealth"]  # prof +2 * 2 = +4
            }
        }
        # Stealth: +4 (dex) + 4 (expertise) = +8
        res = roll_check(character, skill="stealth", dc=15, seed=10)
        self.assertEqual(res["total_modifier"], 8)
        self.assertTrue(res["has_expertise"])
        self.assertEqual(res["total"], res["natural_roll"] + 8)

    def test_roll_saving_throw(self):
        character = {
            "name": "Eldrin",
            "level": 3,
            "stats": {"intelligence": 16, "constitution": 12},
            "proficiencies": {
                "saving_throws": ["intelligence", "wisdom"]
            }
        }
        res_int = roll_saving_throw(character, ability="intelligence", dc=14, seed=5)
        self.assertTrue(res_int["is_proficient"])
        self.assertEqual(res_int["total_modifier"], 3 + 2)  # int mod + prof

        res_con = roll_saving_throw(character, ability="constitution", dc=14, seed=5)
        self.assertFalse(res_con["is_proficient"])
        self.assertEqual(res_con["total_modifier"], 1)

    def test_validate_action(self):
        healthy_char = {"name": "Hero", "hp": {"current": 20, "max": 20}, "conditions": []}
        valid, msg = validate_action(healthy_char, "attack")
        self.assertTrue(valid)

        unconscious_char = {"name": "Downed Hero", "hp": {"current": 0, "max": 20}, "conditions": ["unconscious"]}
        valid, msg = validate_action(unconscious_char, "attack")
        self.assertFalse(valid)


if __name__ == "__main__":
    unittest.main()
