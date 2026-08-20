"""
Unit tests for the Unified Rules & Compendium Registry (Compendium).
Validates dynamic JSON loading, caching, querying, and schema retrieval.
"""

import unittest
from tools.compendium import Compendium, get_compendium


class TestCompendium(unittest.TestCase):
    def setUp(self):
        self.comp = Compendium.get_instance()

    def test_singleton_and_instance(self):
        c1 = Compendium.get_instance()
        c2 = get_compendium()
        self.assertIs(c1, c2)

    def test_classes_compendium(self):
        classes = self.comp.get_classes()
        self.assertIn("fighter", classes)
        self.assertIn("wizard", classes)
        self.assertIn("rogue", classes)
        self.assertIn("cleric", classes)
        self.assertEqual(len(classes), 12)

        fighter = self.comp.get_class("fighter")
        self.assertIsNotNone(fighter)
        self.assertIn("10", fighter["hit_die"])

    def test_species_compendium(self):
        all_species = self.comp.get_all_species()
        self.assertIn("human", all_species)
        self.assertIn("high_elf", all_species)
        self.assertIn("hill_dwarf", all_species)
        self.assertGreaterEqual(len(all_species), 10)

        dwarf = self.comp.get_species("Hill Dwarf")
        self.assertIsNotNone(dwarf)
        self.assertEqual(dwarf["bonuses"]["constitution"], 2)

    def test_backgrounds_compendium(self):
        bgs = self.comp.get_all_backgrounds()
        self.assertIn("soldier", bgs)
        self.assertIn("criminal", bgs)
        self.assertGreaterEqual(len(bgs), 8)

        soldier = self.comp.get_background("soldier")
        self.assertIsNotNone(soldier)
        self.assertEqual(soldier["feature"], "Military Rank")

    def test_presets_compendium(self):
        presets = self.comp.get_all_presets()
        self.assertIn("lmop_cleric_soldier", presets)
        self.assertIn("lmop_wizard_acolyte", presets)

        cleric = self.comp.get_preset("lmop_cleric_soldier")
        self.assertIsNotNone(cleric)
        self.assertEqual(cleric["name"], "Eberk Ironfist")

    def test_progression_tables(self):
        self.assertEqual(self.comp.get_proficiency_bonus(1), 2)
        self.assertEqual(self.comp.get_proficiency_bonus(5), 3)
        self.assertEqual(self.comp.get_proficiency_bonus(9), 4)

        wizard_slots = self.comp.get_spell_slots("Wizard", 3)
        self.assertEqual(wizard_slots["level_1"]["max"], 4)
        self.assertEqual(wizard_slots["level_2"]["max"], 2)

        fighter_feats = self.comp.get_class_features_for_level("Fighter", 2)
        self.assertTrue(any("Action Surge" in f for f in fighter_feats))

    def test_encounters_math(self):
        xp_lvl1 = self.comp.get_xp_thresholds(1)
        self.assertEqual(xp_lvl1["easy"], 25)
        self.assertEqual(xp_lvl1["deadly"], 100)

        day_xp = self.comp.get_adventuring_day_xp(1)
        self.assertEqual(day_xp, 300)

        cr_xp = self.comp.get_cr_to_xp()
        self.assertEqual(cr_xp.get("1/4"), 50)
        self.assertEqual(cr_xp.get("2"), 450)

    def test_actions_and_conditions(self):
        actions = self.comp.get_actions()
        self.assertIn("attack", actions)
        self.assertIn("dash", actions)

        conditions = self.comp.get_conditions()
        self.assertIn("blinded", conditions)
        self.assertIn("paralyzed", conditions)

    def test_spells_monsters_items(self):
        spell = self.comp.get_spell("fire_bolt")
        self.assertIsNotNone(spell)
        self.assertEqual(spell["name"], "Fire Bolt")

        monster = self.comp.get_monster("goblin")
        self.assertIsNotNone(monster)
        self.assertEqual(monster["cr"], "1/4")

        item = self.comp.get_magic_item("bag_of_holding")
        self.assertIsNotNone(item)
        self.assertEqual(item["rarity"], "uncommon")


if __name__ == "__main__":
    unittest.main()
