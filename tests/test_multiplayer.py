"""
Unit tests for Multiplayer Manager and Initiative Turn Order.
"""

import unittest
from tools.multiplayer import MultiplayerManager


class TestMultiplayerManager(unittest.TestCase):
    def setUp(self):
        self.mp = MultiplayerManager()

    def test_party_listing(self):
        party = self.mp.get_party()
        self.assertGreater(len(party), 0)

    def test_active_player_switch(self):
        res = self.mp.set_active_player("aria_nightwind")
        self.assertTrue(res["success"])
        active = self.mp.get_active_player()
        self.assertEqual(active["id"], "aria_nightwind")

    def test_initiative_flow(self):
        # Roll initiative
        monsters = [{"name": "Goblin Scout", "stats": {"dexterity": 14}, "ac": 13, "hp": {"current": 7, "max": 7}}]
        combat = self.mp.roll_initiative(monsters=monsters, seed=42)
        self.assertTrue(combat["in_combat"])
        self.assertEqual(combat["round"], 1)
        self.assertEqual(combat["turn_index"], 0)
        self.assertGreater(len(combat["order"]), 1)

        # Advance turn
        turn_res = self.mp.advance_turn()
        self.assertTrue(turn_res["success"])
        self.assertEqual(turn_res["turn_index"], 1)

        # End combat
        end_res = self.mp.end_combat()
        self.assertTrue(end_res["success"])
        combat_after = self.mp.get_initiative()
        self.assertFalse(combat_after["in_combat"])


if __name__ == "__main__":
    unittest.main()
