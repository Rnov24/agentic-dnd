"""
Unit tests for Unified Multi-Tier Compendium & Adventure Overlay.
"""

import unittest
from tools.compendium import Compendium


class TestCompendiumOverlay(unittest.TestCase):

    def setUp(self):
        self.comp = Compendium.get_instance()

    def test_core_and_adventure_magic_items(self):
        # 1. Core item lookup
        bag = self.comp.get_magic_item("bag_of_holding")
        self.assertIsNotNone(bag)
        self.assertEqual(bag.get("name"), "Bag of Holding")
        self.assertIn("Core 5e", bag.get("_source", ""))

        # 2. Adventure item lookup (Spider Staff from LMoP)
        spider_staff = self.comp.get_magic_item("spider_staff")
        self.assertIsNotNone(spider_staff)
        self.assertEqual(spider_staff.get("name"), "Spider Staff")
        self.assertIn("Adventure", spider_staff.get("_source", ""))

        # 3. Adventure item lookup (Staff of Defense from LMoP)
        staff_def = self.comp.get_magic_item("Staff of Defense")
        self.assertIsNotNone(staff_def)
        self.assertEqual(staff_def.get("name"), "Staff of Defense")

    def test_core_and_adventure_monsters(self):
        # 1. Core monster lookup (Goblin)
        goblin = self.comp.get_monster("goblin")
        self.assertIsNotNone(goblin)
        self.assertEqual(goblin.get("name"), "Goblin")
        self.assertIn("Core 5e", goblin.get("_source", ""))

        # 2. Adventure monster lookup (Nezznar from LMoP)
        nezznar = self.comp.get_monster("nezznar_black_spider")
        self.assertIsNotNone(nezznar)
        self.assertEqual(nezznar.get("name"), "Nezznar the Black Spider")
        self.assertIn("Adventure", nezznar.get("_source", ""))

        # 3. Adventure monster lookup (Redbrand Ruffian)
        redbrand = self.comp.get_monster("Redbrand Ruffian")
        self.assertIsNotNone(redbrand)
        self.assertEqual(redbrand.get("name"), "Redbrand Ruffian")

    def test_adventure_encounters_and_locations(self):
        encs = self.comp.get_encounters()
        self.assertGreater(len(encs), 0)
        goblin_ambush = next((e for e in encs if "goblin_ambush" in e.get("id", "")), None)
        self.assertIsNotNone(goblin_ambush)

        locs = self.comp.get_locations()
        self.assertGreater(len(locs), 0)


if __name__ == "__main__":
    unittest.main()
