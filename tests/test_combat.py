"""
Unit tests for deterministic combat engine.
"""

import unittest
from tools.combat import (
    roll_initiative,
    roll_attack,
    roll_damage,
    apply_damage,
    apply_healing,
    apply_condition,
    remove_condition,
    roll_death_save,
)


class TestCombat(unittest.TestCase):

    def test_roll_initiative(self):
        participants = [
            {"id": "hero", "name": "Hero", "stats": {"dexterity": 16}},
            {"id": "goblin", "name": "Goblin", "stats": {"dexterity": 14}},
            {"id": "ogre", "name": "Ogre", "stats": {"dexterity": 8}},
        ]
        tracker = roll_initiative(participants, seed=42)
        self.assertEqual(len(tracker), 3)
        # Verify sorted descending
        for i in range(len(tracker) - 1):
            self.assertGreaterEqual(tracker[i]["initiative"], tracker[i + 1]["initiative"])

    def test_roll_attack_and_damage(self):
        attacker = {
            "name": "Aria",
            "level": 3,
            "stats": {"dexterity": 16},
            "attacks": [{"name": "Dagger", "ability": "dexterity", "bonus": 1, "damage": "1d4"}]
        }
        target = {"name": "Guard", "ac": 12, "hp": {"current": 20, "max": 20}}

        atk = roll_attack(attacker, target, attack_name="Dagger", seed=10)
        self.assertIn("is_hit", atk)
        self.assertEqual(atk["target_ac"], 12)

        dmg = roll_damage(attacker, target, damage_formula="1d4+3", seed=10)
        self.assertGreaterEqual(dmg["final_damage"], 4)

    def test_apply_damage_and_temp_hp(self):
        target = {"name": "Warrior", "hp": {"current": 20, "max": 20, "temp": 5}, "conditions": []}
        
        # 8 damage: absorbs 5 temp, 3 to current HP (20 -> 17)
        res = apply_damage(target, 8)
        self.assertEqual(res["temp_hp_absorbed"], 5)
        self.assertEqual(res["hp_after"], 17)
        self.assertEqual(target["hp"]["temp"], 0)

        # 20 damage: drops to 0 and becomes unconscious
        res2 = apply_damage(target, 20)
        self.assertEqual(res2["hp_after"], 0)
        self.assertTrue(res2["is_unconscious"])
        self.assertIn("unconscious", target["conditions"])

    def test_apply_healing(self):
        target = {"name": "Downed Warrior", "hp": {"current": 0, "max": 25, "temp": 0}, "conditions": ["unconscious"]}
        res = apply_healing(target, 10)
        self.assertEqual(res["hp_after"], 10)
        self.assertTrue(res["recovered_from_unconscious"])
        self.assertNotIn("unconscious", target["conditions"])

    def test_condition_apply_and_remove(self):
        target = {"name": "Target", "conditions": []}
        apply_condition(target, "poisoned")
        self.assertIn("poisoned", target["conditions"])

        remove_condition(target, "poisoned")
        self.assertNotIn("poisoned", target["conditions"])

    def test_death_saving_throw(self):
        downed = {"name": "Fallen Hero", "hp": {"current": 0, "max": 15}, "conditions": ["unconscious"]}
        save_res = roll_death_save(downed, seed=42)
        self.assertIn("natural_roll", save_res)
        self.assertIn("successes", save_res)
        self.assertIn("failures", save_res)


if __name__ == "__main__":
    unittest.main()
