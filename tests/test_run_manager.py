"""
Unit tests for Multi-Campaign Run Manager and Difficulty Engine.
"""

import unittest
import shutil
import tempfile
from pathlib import Path
from tools.run_manager import RunManager, DIFFICULTY_PRESETS


class TestRunManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.rm = RunManager(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_difficulty_presets_defined(self):
        self.assertIn("story", DIFFICULTY_PRESETS)
        self.assertIn("normal", DIFFICULTY_PRESETS)
        self.assertIn("hardcore", DIFFICULTY_PRESETS)
        self.assertIn("deadly", DIFFICULTY_PRESETS)
        self.assertEqual(DIFFICULTY_PRESETS["story"]["death_save_dc"], 8)
        self.assertEqual(DIFFICULTY_PRESETS["normal"]["death_save_dc"], 10)
        self.assertEqual(DIFFICULTY_PRESETS["hardcore"]["death_save_dc"], 12)
        self.assertEqual(DIFFICULTY_PRESETS["deadly"]["death_save_dc"], 14)

    def test_create_and_switch_run(self):
        res = self.rm.create_run(
            name="Curse of Strahd Run",
            adventure="custom",
            difficulty="hardcore"
        )
        self.assertTrue(res["success"])
        run_id = res["run_id"]

        self.assertEqual(self.rm.get_active_run_id(), run_id)
        manifest = self.rm.get_active_run_manifest()
        self.assertIsNotNone(manifest)
        self.assertEqual(manifest["name"], "Curse of Strahd Run")
        self.assertEqual(manifest["difficulty"], "hardcore")

        # Test path isolation
        s_dir, c_dir = self.rm.get_active_run_paths()
        self.assertTrue(str(s_dir).endswith("state"))
        self.assertTrue(s_dir.exists())

    def test_list_and_delete_runs(self):
        self.rm.create_run(name="Run 1", difficulty="story")
        self.rm.create_run(name="Run 2", difficulty="deadly")

        runs = self.rm.list_runs()
        self.assertEqual(len(runs), 2)

        del_res = self.rm.delete_run("run_1")
        self.assertTrue(del_res["success"])
        self.assertEqual(len(self.rm.list_runs()), 1)


if __name__ == "__main__":
    unittest.main()
