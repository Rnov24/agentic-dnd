"""
Unit tests for Compendium Schema Validator & Homebrew Linter.
"""

import unittest
from tools.compendium_validator import CompendiumValidator


class TestCompendiumValidator(unittest.TestCase):

    def setUp(self):
        self.validator = CompendiumValidator()

    def test_rules_compendium_integrity(self):
        res = self.validator.validate_all()
        self.assertTrue(res["valid"], f"Validation failed with errors: {res['errors']}")
        self.assertEqual(len(res["errors"]), 0)
        self.assertGreater(res["total_entities"], 50)

    def test_compendium_stats(self):
        stats = self.validator.get_stats()
        self.assertTrue(stats["healthy"])
        self.assertIn("spells", stats["entity_counts"])
        self.assertIn("monsters", stats["entity_counts"])
        self.assertIn("magic_items", stats["entity_counts"])
        self.assertGreater(stats["entity_counts"]["spells"], 10)


if __name__ == "__main__":
    unittest.main()
