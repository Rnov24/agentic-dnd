"""
Unit tests for Theater of the Mind Zone-Based Spatial Combat Engine.
"""

import unittest
from tools.zones import SpatialCombatManager, TacticalZone


class TestSpatialCombat(unittest.TestCase):

    def setUp(self):
        self.mgr = SpatialCombatManager()
        self.mgr.assign_zone("fighter", TacticalZone.ENGAGED)
        self.mgr.assign_zone("goblin_melee", TacticalZone.ENGAGED)
        self.mgr.assign_zone("goblin_archer", TacticalZone.FAR)
        self.mgr.assign_zone("wizard", TacticalZone.NEAR)

    def test_melee_attack_same_zone(self):
        can_atk, msg = self.mgr.can_attack_target("fighter", "goblin_melee", weapon_type="melee", reach_or_range=5)
        self.assertTrue(can_atk)

    def test_melee_attack_different_zone_rejected(self):
        can_atk, msg = self.mgr.can_attack_target("fighter", "goblin_archer", weapon_type="melee", reach_or_range=5)
        self.assertFalse(can_atk)
        self.assertIn("out of 5ft melee reach", msg)

    def test_ranged_weapon_and_spell_ranges(self):
        # Fire Bolt (120ft range) hits from NEAR to FAR
        can_atk, msg = self.mgr.can_attack_target("wizard", "goblin_archer", weapon_type="spell", reach_or_range=120)
        self.assertTrue(can_atk)

        # Short range weapon (15ft) from ENGAGED to FAR fails
        can_atk, msg = self.mgr.can_attack_target("fighter", "goblin_archer", weapon_type="thrown", reach_or_range=15)
        self.assertFalse(can_atk)

    def test_movement_and_opportunity_attacks(self):
        # Moving from ENGAGED to NEAR provokes OA
        res = self.mgr.move_combatant("fighter", TacticalZone.NEAR, speed_ft=30)
        self.assertTrue(res["success"])
        self.assertTrue(res["provokes_opportunity_attack"])
        self.assertEqual(self.mgr.get_zone("fighter"), TacticalZone.NEAR)

        # Moving within range with dash
        res = self.mgr.move_combatant("fighter", TacticalZone.FAR, speed_ft=30)
        self.assertTrue(res["success"])
        self.assertFalse(res["provokes_opportunity_attack"])


if __name__ == "__main__":
    unittest.main()
