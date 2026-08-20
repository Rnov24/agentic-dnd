"""
Unit tests for Typed Domain Models and Schema Validation (Plan 017).
"""

import unittest
from tools.models import (
    AbilityScores,
    CharacterModel,
    MonsterModel,
    ItemModel,
    SpellModel,
    validate_character_dict
)


class TestDomainModels(unittest.TestCase):

    def test_ability_scores(self):
        stats = AbilityScores(strength=16, dexterity=14, constitution=12, intelligence=10, wisdom=8, charisma=18)
        self.assertEqual(stats.get_modifier("strength"), 3)
        self.assertEqual(stats.get_modifier("dexterity"), 2)
        self.assertEqual(stats.get_modifier("wisdom"), -1)
        self.assertEqual(stats.get_modifier("charisma"), 4)
        
        # Serialization
        s_dict = stats.to_dict()
        stats2 = AbilityScores.from_dict(s_dict)
        self.assertEqual(stats2.strength, 16)

    def test_character_model_roundtrip(self):
        raw = {
            "id": "eldrin_sunstrider",
            "name": "Eldrin Sunstrider",
            "species": "Elf",
            "class": "Wizard",
            "level": 3,
            "hp": {"current": 18, "max": 20},
            "ac": 13,
            "stats": {"intelligence": 16, "dexterity": 14}
        }
        char = CharacterModel.from_dict(raw)
        self.assertEqual(char.id, "eldrin_sunstrider")
        self.assertEqual(char.char_class, "Wizard")
        self.assertEqual(char.hp_current, 18)
        self.assertEqual(char.stats.intelligence, 16)
        
        # Round-trip to dict
        out = char.to_dict()
        self.assertEqual(out["class"], "Wizard")
        self.assertEqual(out["hp"]["current"], 18)

    def test_monster_model_source_tag(self):
        raw = {
            "id": "nezznar",
            "name": "Nezznar",
            "cr": "2",
            "xp": 450,
            "_source": "Adventure: Lost Mine Of Phandelver"
        }
        m = MonsterModel.from_dict(raw)
        self.assertEqual(m.id, "nezznar")
        self.assertEqual(m.source, "Adventure: Lost Mine Of Phandelver")
        self.assertEqual(m.to_dict()["_source"], "Adventure: Lost Mine Of Phandelver")

    def test_item_and_spell_models(self):
        item = ItemModel.from_dict({
            "id": "spider_staff",
            "name": "Spider Staff",
            "type": "Staff",
            "rarity": "rare",
            "attunement": True
        })
        self.assertTrue(item.attunement)
        self.assertEqual(item.rarity, "rare")

        spell = SpellModel.from_dict({
            "id": "fire_bolt",
            "name": "Fire Bolt",
            "level": 0,
            "damage": "1d10"
        })
        self.assertEqual(spell.name, "Fire Bolt")
        self.assertEqual(spell.damage, "1d10")

    def test_validate_character_dict(self):
        valid, errors = validate_character_dict({"id": "aria", "name": "Aria"})
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)

        invalid, errors = validate_character_dict({"id": "aria"})
        self.assertFalse(invalid)
        self.assertIn("name", errors[0])


if __name__ == "__main__":
    unittest.main()
