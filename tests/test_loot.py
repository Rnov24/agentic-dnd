"""
Unit tests for Deterministic 5e Loot & Treasure Generator.
"""

import unittest
from tools.loot import LootGenerator


class TestLootGenerator(unittest.TestCase):

    def setUp(self):
        self.lg = LootGenerator()

    def test_individual_treasure_cr_0_4(self):
        loot = self.lg.generate_individual_treasure(cr=2.0, seed=42)
        self.assertEqual(loot["type"], "individual_treasure")
        self.assertEqual(loot["tier"], "cr_0_4")
        self.assertGreater(loot["total_value_gp"], 0)
        self.assertIn("coins", loot)

    def test_hoard_treasure_cr_0_4(self):
        hoard = self.lg.generate_hoard_treasure(cr=3.0, seed=42)
        self.assertEqual(hoard["type"], "hoard_treasure")
        self.assertIn("coins", hoard)
        self.assertIn("gems_and_art", hoard)
        self.assertIn("magic_items", hoard)
        self.assertGreater(hoard["total_value_gp"], 0)

    def test_deterministic_seed(self):
        l1 = self.lg.generate_hoard_treasure(cr=5.0, seed=12345)
        l2 = self.lg.generate_hoard_treasure(cr=5.0, seed=12345)
        self.assertEqual(l1["coins"], l2["coins"])
        self.assertEqual(l1["total_value_gp"], l2["total_value_gp"])

    def test_adventure_items_in_compendium_pool(self):
        all_items = self.lg.compendium.get_magic_items()
        # Verify LMoP adventure items are in the loot pool
        self.assertIn("spider_staff", all_items)
        self.assertIn("staff_of_defense", all_items)
        self.assertIn("lightbringer", all_items)


if __name__ == "__main__":
    unittest.main()
