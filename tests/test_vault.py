"""
Unit tests for Global Character Vault.
"""

import unittest
import shutil
import tempfile
from pathlib import Path
from tools.vault import CharacterVault


class TestCharacterVault(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.vault = CharacterVault(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_preset_seeding(self):
        chars = self.vault.list_characters()
        self.assertGreaterEqual(len(chars), 1)

    def test_save_and_get_character(self):
        char = {
            "id": "valen_hero",
            "name": "Valen the Bold",
            "class": "Fighter",
            "level": 3,
            "hp": {"current": 28, "max": 28}
        }
        res = self.vault.save_character(char)
        self.assertTrue(res["success"])

        retrieved = self.vault.get_character("valen_hero")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["name"], "Valen the Bold")
        self.assertEqual(retrieved["level"], 3)

    def test_delete_character(self):
        char = {
            "id": "temp_char",
            "name": "Temporary Hero",
            "class": "Rogue"
        }
        self.vault.save_character(char)
        self.assertIsNotNone(self.vault.get_character("temp_char"))

        del_res = self.vault.delete_character("temp_char")
        self.assertTrue(del_res["success"])
        self.assertIsNone(self.vault.get_character("temp_char"))


if __name__ == "__main__":
    unittest.main()
