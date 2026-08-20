"""
Unit tests for Monsters Bestiary and Magic Items Compendiums from D&D Basic Rules.
"""

import unittest
from tools.monsters import get_monster, load_monsters
from tools.magic_items import get_magic_item, load_magic_items
from rules.rules_engine import RulesEngine


class TestMonstersAndMagicItems(unittest.TestCase):
    def test_monster_lookup(self):
        """Verifies retrieval and stat structure of monsters."""
        goblin = get_monster("goblin")
        self.assertIsNotNone(goblin)
        self.assertEqual(goblin["ac"], 15)
        self.assertEqual(goblin["cr"], "1/4")
        self.assertEqual(goblin["xp"], 50)
        self.assertIn("nimble_escape", goblin["traits"])

        dragon = get_monster("adult_red_dragon")
        self.assertIsNotNone(dragon)
        self.assertEqual(dragon["ac"], 19)
        self.assertEqual(dragon["cr"], "17")
        self.assertEqual(dragon["hp"]["current"], 256)
        self.assertEqual(len(dragon["legendary_actions"]), 3)

    def test_magic_item_lookup(self):
        """Verifies retrieval and properties of magic items."""
        bag = get_magic_item("bag_of_holding")
        self.assertIsNotNone(bag)
        self.assertEqual(bag["rarity"], "uncommon")
        self.assertFalse(bag["attunement"])
        self.assertEqual(bag["weight_capacity_lbs"], 500)

        cloak = get_magic_item("cloak_of_elvenkind")
        self.assertIsNotNone(cloak)
        self.assertTrue(cloak["attunement"])
        self.assertTrue(cloak["effects"]["stealth_advantage"])

        wand = get_magic_item("wand_of_magic_missiles")
        self.assertIsNotNone(wand)
        self.assertEqual(wand["charges"]["max"], 7)

    def test_rules_engine_delegation(self):
        """Tests RulesEngine static methods for monster and item lookup."""
        guard = RulesEngine.get_monster_info("guard")
        self.assertIsNotNone(guard)
        self.assertEqual(guard["ac"], 16)

        ring = RulesEngine.get_magic_item_info("ring_of_protection")
        self.assertIsNotNone(ring)
        self.assertTrue(ring["attunement"])
        self.assertEqual(ring["bonuses"]["ac"], 1)


if __name__ == "__main__":
    unittest.main()
