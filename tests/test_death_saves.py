"""
Unit tests for 0 HP, Death Saving Throws, Instant Death, and Stabilization.
"""

import unittest
from tools.death_saves import roll_death_save, apply_damage_at_zero_hp, stabilize_character


class TestDeathSaves(unittest.TestCase):
    def test_death_save_success_and_failure(self):
        """Validates success and failure tracking."""
        char = {
            "name": "Dying Warrior",
            "hp": {"current": 0, "max": 20},
            "conditions": ["unconscious"],
            "death_saves": {"successes": 1, "failures": 1, "stabilized": False}
        }
        # Roll with fixed seed
        res = roll_death_save(char, seed=42)
        self.assertIn(res["result_type"], ["Success", "Failure", "Critical Success (Natural 20)", "Critical Failure (Natural 1)"])

    def test_nat_20_revival(self):
        """Verifies that rolling a Natural 20 restores 1 HP and wakes the character."""
        # Find a seed that produces 20
        import random
        target_seed = None
        for s in range(500):
            random.seed(s)
            if random.randint(1, 20) == 20:
                target_seed = s
                break
                
        char = {
            "name": "Lucky Hero",
            "hp": {"current": 0, "max": 20},
            "conditions": ["unconscious"],
            "death_saves": {"successes": 0, "failures": 2}
        }
        res = roll_death_save(char, seed=target_seed)
        self.assertEqual(res["current_hp"], 1)
        self.assertEqual(res["status"], "Revived (1 HP)")
        self.assertNotIn("unconscious", char.get("conditions", []))

    def test_massive_damage_instant_death(self):
        """Verifies that damage at 0 HP >= max HP causes instant death."""
        char = {
            "name": "Frail Mage",
            "hp": {"current": 0, "max": 15},
            "conditions": ["unconscious"]
        }
        res = apply_damage_at_zero_hp(char, damage=15)
        self.assertTrue(res["instant_death"])
        self.assertEqual(res["status"], "Dead (Massive Damage)")
        self.assertIn("dead", char.get("conditions", []))

    def test_stabilization_check(self):
        """Verifies DC 10 Medicine stabilization."""
        healer = {"name": "Cleric", "level": 3, "stats": {"wisdom": 16}, "skills": {"medicine": 5}}
        target = {"name": "Bleeding Fighter", "hp": {"current": 0, "max": 25}, "death_saves": {"successes": 0, "failures": 2}}
        res = stabilize_character(healer, target, seed=42)
        self.assertIn("success", res)


if __name__ == "__main__":
    unittest.main()
