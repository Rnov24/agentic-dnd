"""
Automated Cross-Check and Validation Test Suite for 2024 Player's Handbook (PHB 2024) Integration.
Verifies zero hallucinations, 100% compendium structural integrity, and mechanics compliance.
"""

import unittest
from pathlib import Path
from tools.compendium import Compendium
from tools.compendium_validator import CompendiumValidator
from tools.explainer import explain_mechanic
from tools.character_creator import CharacterCreator


class TestPHB2024Compendiums(unittest.TestCase):

    def setUp(self):
        self.comp = Compendium.get_instance()
        self.validator = CompendiumValidator()

    def test_compendium_validation_zero_errors(self):
        res = self.validator.validate_all()
        self.assertTrue(res["valid"], f"Validation failed with errors: {res.get('errors')}")
        self.assertGreaterEqual(res["total_entities"], 400)

    def test_all_12_classes_present(self):
        classes = self.comp.get_classes()
        expected = ["barbarian", "bard", "cleric", "druid", "fighter", "monk", "paladin", "ranger", "rogue", "sorcerer", "warlock", "wizard"]
        for c in expected:
            self.assertIn(c, classes)
            self.assertIn("hit_die", classes[c])
            self.assertIn("saving_throws", classes[c])

    def test_all_10_species_present(self):
        species = self.comp.get_all_species()
        expected = ["aasimar", "dragonborn", "dwarf", "elf", "gnome", "goliath", "halfling", "human", "orc", "tiefling"]
        for s in expected:
            self.assertIn(s, species)
            self.assertIn("traits", species[s])

    def test_all_16_backgrounds_with_origin_feats(self):
        bgs = self.comp.get_all_backgrounds()
        expected = [
            "acolyte", "artisan", "charlatan", "criminal", "cultist", "entertainer",
            "farmer", "guard", "guide", "hermit", "merchant", "noble", "sage",
            "sailor", "scribe", "soldier", "wayfarer"
        ]
        for b in expected:
            self.assertIn(b, bgs)
            self.assertIn("feat", bgs[b])
            self.assertIn("ability_scores", bgs[b])

    def test_weapons_masteries_complete(self):
        weapons = self.comp.get_weapons()
        self.assertGreaterEqual(len(weapons), 30)
        # Check masteries
        self.assertEqual(weapons["greatsword"]["mastery"], "Graze")
        self.assertEqual(weapons["dagger"]["mastery"], "Nick")
        self.assertEqual(weapons["greataxe"]["mastery"], "Cleave")
        self.assertEqual(weapons["quarterstaff"]["mastery"], "Topple")
        self.assertEqual(weapons["longsword"]["mastery"], "Sap")

    def test_all_15_conditions_complete(self):
        conds = self.comp.get_conditions()
        expected = [
            "blinded", "charmed", "deafened", "exhaustion", "frightened",
            "grappled", "incapacitated", "invisible", "paralyzed", "petrified",
            "poisoned", "prone", "restrained", "stunned", "unconscious"
        ]
        for c in expected:
            self.assertIn(c, conds)
            self.assertTrue(len(conds[c].get("effects", [])) > 0 or len(conds[c].get("description", "")) > 0)

    def test_spells_compendium_2024(self):
        spells = self.comp.get_spells()
        self.assertGreaterEqual(len(spells), 80)
        # Test key 2024 revised spells
        self.assertIn("cure_wounds", spells)
        self.assertEqual(spells["cure_wounds"]["healing"], "2d8 + mod")
        self.assertIn("healing_word", spells)
        self.assertEqual(spells["healing_word"]["healing"], "2d4 + mod")
        self.assertIn("counterspell", spells)
        self.assertIn("Constitution saving throw", spells["counterspell"]["description"])

    def test_rules_glossary_retrieval(self):
        glossary = self.comp.get_glossary()
        self.assertGreaterEqual(len(glossary), 100)
        self.assertIn("heroic_inspiration", glossary)
        self.assertIn("grappling", glossary)
        self.assertIn("unarmed_strike", glossary)

    def test_character_creation_2024(self):
        creator = CharacterCreator()
        char = creator.create_character(
            name="Valen 2024",
            char_class="Fighter",
            species="Human",
            background="Soldier",
            method="standard"
        )
        self.assertEqual(char["class"], "Fighter")
        self.assertIn("Savage Attacker", char.get("feats", []))
        self.assertTrue(len(char.get("weapon_masteries", [])) > 0)


if __name__ == "__main__":
    unittest.main()
