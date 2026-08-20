"""
Unit tests for Universal Adventure Package Loader & Importer.
"""

import unittest
import tempfile
import json
from pathlib import Path
from tools.adventure_loader import AdventureLoader


class TestAdventureLoader(unittest.TestCase):
    def setUp(self):
        self.loader = AdventureLoader()

    def test_list_adventures(self):
        """Verifies discovery of packaged adventure modules."""
        adventures = self.loader.list_adventures()
        self.assertGreater(len(adventures), 0)
        lmop = next((a for a in adventures if a.get("id") == "lost_mine_of_phandelver"), None)
        self.assertIsNotNone(lmop)
        self.assertEqual(lmop.get("title"), "Lost Mine of Phandelver")

    def test_validate_lmop_package(self):
        """Verifies integrity validation of Lost Mine of Phandelver."""
        val = self.loader.validate_adventure("lost_mine_of_phandelver")
        self.assertTrue(val["valid"])
        self.assertEqual(len(val["errors"]), 0)

    def test_get_adventure_metadata(self):
        """Verifies manifest retrieval and chapter definitions."""
        adv = self.loader.get_adventure("lost_mine_of_phandelver")
        self.assertIsNotNone(adv)
        self.assertEqual(adv.get("starting_location"), "triboar_trail_ambush")
        self.assertEqual(len(adv.get("chapters", [])), 4)

    def test_load_adventure_into_campaign(self):
        """Verifies loading adventure into active campaign state."""
        res = self.loader.load_adventure_into_campaign("lost_mine_of_phandelver")
        self.assertTrue(res["success"])
        self.assertEqual(res["starting_location"], "triboar_trail_ambush")
        # Verify items.json and monsters.json were synced to state
        self.assertTrue((self.loader.state_dir / "items.json").exists())
        self.assertTrue((self.loader.state_dir / "monsters.json").exists())
        self.assertTrue((self.loader.state_dir / "encounters.json").exists())
        self.assertTrue((self.loader.state_dir / "locations.json").exists())

    def test_path_traversal_rejection(self):
        """Verifies path traversal attempts are rejected."""
        self.assertIsNone(self.loader.get_adventure("../../../outside"))
        val = self.loader.validate_adventure("../../secret")
        self.assertFalse(val["valid"])

    def test_scaffold_adventure(self):
        """Verifies scaffolding a new adventure package and validating its structure."""
        slug = "test_scaffold_sample"
        res = self.loader.scaffold_adventure(slug=slug, title="Sample Castle", recommended_levels="1-3")
        try:
            self.assertTrue(res["success"])
            val = self.loader.validate_adventure(slug)
            self.assertTrue(val["valid"])
        finally:
            import shutil
            test_dir = self.loader.adventures_dir / slug
            if test_dir.exists():
                shutil.rmtree(test_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
