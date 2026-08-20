"""
Unit tests for Short and Long Rest recovery rules from Player'\''s Handbook.
"""

import unittest
from tools.resting import execute_short_rest, execute_long_rest


class TestRestingEngine(unittest.TestCase):
    def test_short_rest_healing(self):
        """Validates Hit Dice consumption and HP recovery during short rest."""
        character = {
            "name": "Aria Nightwind",
            "class": "Rogue",
            "level": 3,
            "stats": {"constitution": 14}, # +2 mod
            "hp": {"current": 10, "max": 24, "temp": 0},
            "hit_dice": {"current": 3, "max": 3, "die": "1d8"}
        }
        res = execute_short_rest(character, hit_dice_to_spend=1, seed=42)
        self.assertTrue(res["success"])
        self.assertEqual(res["hit_dice_spent"], 1)
        self.assertEqual(res["hit_dice_remaining"], 2)
        self.assertGreater(res["hp_after"], 10)
        self.assertLessEqual(res["hp_after"], 24)

    def test_short_rest_no_hit_dice(self):
        """Verifies error handling when attempting to short rest with 0 hit dice."""
        character = {
            "name": "Exhausted Rogue",
            "class": "Rogue",
            "level": 3,
            "hp": {"current": 5, "max": 20},
            "hit_dice": {"current": 0, "max": 3, "die": "1d8"}
        }
        res = execute_short_rest(character, hit_dice_to_spend=1)
        self.assertFalse(res["success"])
        self.assertIn("No remaining Hit Dice", res["error"])

    def test_long_rest_full_recovery(self):
        """Validates full HP reset, hit dice recovery, spell slot reset, and exhaustion reduction."""
        character = {
            "name": "Eldrin Shadowseeker",
            "class": "Wizard",
            "level": 4,
            "hp": {"current": 4, "max": 22, "temp": 3},
            "hit_dice": {"current": 1, "max": 4, "die": "1d6"},
            "spell_slots": {
                "level_1": {"current": 0, "max": 4},
                "level_2": {"current": 1, "max": 3}
            },
            "conditions": ["exhaustion_2", "unconscious"]
        }
        res = execute_long_rest(character)
        self.assertTrue(res["success"])
        self.assertEqual(res["hp_after"], 22)
        # Regain half total hit dice: 4 // 2 = 2 -> 1 + 2 = 3
        self.assertEqual(res["hit_dice_current"], 3)
        self.assertEqual(character["spell_slots"]["level_1"]["current"], 4)
        self.assertEqual(character["spell_slots"]["level_2"]["current"], 3)
        self.assertIn("exhaustion_1", res["conditions"])
        self.assertNotIn("unconscious", res["conditions"])


if __name__ == "__main__":
    unittest.main()
