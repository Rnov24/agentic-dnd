"""
Unit tests for Spellcasting Engine, Upcasting, and Spell Compendium from PHB.
"""

import unittest
from tools.spells import get_spell, cast_spell, load_spells


class TestSpellcastingEngine(unittest.TestCase):
    def test_spell_compendium_lookup(self):
        """Verifies spell retrieval and properties from compendium."""
        fb = get_spell("fireball")
        self.assertIsNotNone(fb)
        self.assertEqual(fb["level"], 3)
        self.assertEqual(fb["school"], "Evocation")
        self.assertFalse(fb["concentration"])

        det = get_spell("detect_magic")
        self.assertIsNotNone(det)
        self.assertTrue(det["ritual"])
        self.assertTrue(det["concentration"])

    def test_cantrip_casting(self):
        """Verifies cantrips do not consume spell slots."""
        caster = {
            "name": "Eldrin",
            "class": "Wizard",
            "level": 3,
            "stats": {"intelligence": 16},
            "spell_slots": {"level_1": {"current": 4, "max": 4}}
        }
        target = {"name": "Goblin", "hp": {"current": 7, "max": 7}}
        res = cast_spell(caster, "fire_bolt", target=target, seed=42)
        self.assertTrue(res["success"])
        self.assertFalse(res["slot_expended"])
        self.assertEqual(caster["spell_slots"]["level_1"]["current"], 4)
        self.assertIn("damage", res)

    def test_leveled_spell_slot_deduction(self):
        """Verifies leveled spells deduct a spell slot."""
        caster = {
            "name": "Eldrin",
            "class": "Wizard",
            "level": 3,
            "stats": {"intelligence": 16},
            "spell_slots": {"level_1": {"current": 4, "max": 4}}
        }
        target = {"name": "Guard Karl", "hp": {"current": 11, "max": 11}}
        res = cast_spell(caster, "magic_missile", target=target, seed=42)
        self.assertTrue(res["success"])
        self.assertTrue(res["slot_expended"])
        self.assertEqual(caster["spell_slots"]["level_1"]["current"], 3)
        self.assertEqual(res["darts_count"], 3)

    def test_upcasting_scaling(self):
        """Verifies upcasting increases damage/effects."""
        caster = {
            "name": "Eldrin",
            "class": "Wizard",
            "level": 5,
            "stats": {"intelligence": 16},
            "spell_slots": {"level_2": {"current": 3, "max": 3}}
        }
        target = {"name": "Ogre", "hp": {"current": 59, "max": 59}}
        res = cast_spell(caster, "magic_missile", target=target, slot_level=2, seed=42)
        self.assertTrue(res["success"])
        self.assertEqual(res["level_cast"], 2)
        self.assertEqual(res["darts_count"], 4) # 3 + 1 extra dart
        self.assertEqual(caster["spell_slots"]["level_2"]["current"], 2)

    def test_ritual_casting_no_slots(self):
        """Verifies ritual casting uses 0 spell slots."""
        caster = {
            "name": "Eldrin",
            "class": "Wizard",
            "level": 3,
            "stats": {"intelligence": 16},
            "spell_slots": {"level_1": {"current": 4, "max": 4}}
        }
        res = cast_spell(caster, "detect_magic", is_ritual=True)
        self.assertTrue(res["success"])
        self.assertTrue(res["is_ritual"])
        self.assertFalse(res["slot_expended"])
        self.assertEqual(caster["spell_slots"]["level_1"]["current"], 4)


if __name__ == "__main__":
    unittest.main()
