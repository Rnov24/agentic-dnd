"""
Unit tests for Cover mechanics in combat (Half Cover, Three-Quarters Cover, Total Cover).
"""

import unittest
from tools.combat import roll_attack


class TestCoverMechanics(unittest.TestCase):
    def test_half_cover_bonus(self):
        """Half cover provides +2 AC bonus."""
        attacker = {"name": "Archer", "level": 1, "stats": {"dexterity": 16}, "attacks": [{"name": "Shortbow", "bonus": 5, "ability": "dexterity"}]}
        target = {"name": "Guard Behind Low Wall", "ac": 14}
        res = roll_attack(attacker, target, attack_name="Shortbow", cover="half", seed=42)
        self.assertEqual(res["target_ac"], 16) # 14 + 2

    def test_three_quarters_cover_bonus(self):
        """Three-quarters cover provides +5 AC bonus."""
        attacker = {"name": "Archer", "level": 1, "stats": {"dexterity": 16}, "attacks": [{"name": "Shortbow", "bonus": 5, "ability": "dexterity"}]}
        target = {"name": "Guard Behind Portcullis", "ac": 14}
        res = roll_attack(attacker, target, attack_name="Shortbow", cover="three_quarters", seed=42)
        self.assertEqual(res["target_ac"], 19) # 14 + 5

    def test_total_cover_blocked(self):
        """Total cover completely blocks the attack."""
        attacker = {"name": "Archer", "level": 1, "stats": {"dexterity": 16}, "attacks": [{"name": "Shortbow", "bonus": 5, "ability": "dexterity"}]}
        target = {"name": "Guard Behind Solid Wall", "ac": 14}
        res = roll_attack(attacker, target, attack_name="Shortbow", cover="total", seed=42)
        self.assertFalse(res["is_hit"])
        self.assertTrue(res["is_blocked_by_cover"])


if __name__ == "__main__":
    unittest.main()
