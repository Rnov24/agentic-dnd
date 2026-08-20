"""
Unit tests for Multiplayer and Vault cross-campaign party management.
"""

import unittest
import shutil
import tempfile
from pathlib import Path
from tools.multiplayer import MultiplayerManager
from tools.vault import CharacterVault
from tools.state_manager import StateManager


class TestMultiplayerVault(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.sm = StateManager(self.temp_dir)
        self.vault = CharacterVault(self.temp_dir)
        self.mp = MultiplayerManager(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_add_and_remove_party_member(self):
        # Create custom character in vault
        char = {
            "id": "shadow_monk",
            "name": "Kaelen Shadow",
            "class": "Monk",
            "level": 2,
            "hp": {"current": 16, "max": 16}
        }
        self.vault.save_character(char)

        # Initially party has 0
        self.assertEqual(len(self.mp.get_party()), 0)

        # Add to party from vault
        res_add = self.mp.add_member("shadow_monk")
        self.assertTrue(res_add["success"])
        self.assertEqual(len(self.mp.get_party()), 1)

        # Remove from party
        res_rem = self.mp.remove_member("shadow_monk")
        self.assertTrue(res_rem["success"])
        self.assertEqual(len(self.mp.get_party()), 0)

        # Character still exists in vault!
        self.assertIsNotNone(self.vault.get_character("shadow_monk"))

    def test_get_roster_overview(self):
        char1 = {"id": "hero_1", "name": "Hero 1", "class": "Fighter"}
        char2 = {"id": "hero_2", "name": "Hero 2", "class": "Wizard"}
        self.vault.save_character(char1)
        self.vault.save_character(char2)

        self.mp.add_member("hero_1")
        overview = self.mp.get_roster_overview()

        self.assertEqual(overview["party_count"], 1)
        self.assertEqual(overview["active_party"][0]["id"], "hero_1")
        bench_ids = [b["id"] for b in overview["bench_vault"]]
        self.assertIn("hero_2", bench_ids)


if __name__ == "__main__":
    unittest.main()
