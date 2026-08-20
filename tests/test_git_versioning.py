"""
Unit tests for Git-style versioning and rollback.
"""

import unittest
import shutil
import tempfile
from tools.git_versioning import CampaignGitManager


class TestGitVersioning(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.git = CampaignGitManager(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_commit_and_history(self):
        state_1 = {"world": {"active_location": "entrance"}}
        commit_1 = self.git.commit(state_1, intent="Enter fortress", reason="Opening door")
        self.assertIsNotNone(commit_1["commit_id"])

        state_2 = {"world": {"active_location": "dungeon"}}
        commit_2 = self.git.commit(state_2, intent="Descend stairs", reason="Moving down")

        timeline = self.git.get_history_timeline()
        self.assertEqual(len(timeline), 2)
        self.assertEqual(timeline[0]["commit_id"], commit_2["commit_id"])

    def test_diff_computation(self):
        state_1 = {"world": {"hp": 20}}
        c1 = self.git.commit(state_1, intent="Turn 1", reason="Start")

        state_2 = {"world": {"hp": 15}}
        c2 = self.git.commit(state_2, intent="Turn 2", reason="Damage taken")

        diff = self.git.compute_diff(c1["commit_id"], c2["commit_id"])
        self.assertIn("world", diff["diffs"])
        self.assertEqual(diff["diffs"]["world"]["before"], {"hp": 20})
        self.assertEqual(diff["diffs"]["world"]["after"], {"hp": 15})

    def test_rollback(self):
        state_1 = {"world": {"active_location": "room_a"}}
        c1 = self.git.commit(state_1, intent="Turn 1", reason="Init")

        state_2 = {"world": {"active_location": "room_b"}}
        c2 = self.git.commit(state_2, intent="Turn 2", reason="Moved")

        restored = self.git.rollback(c1["commit_id"])
        self.assertIsNotNone(restored)
        self.assertEqual(restored["world"]["active_location"], "room_a")

    def test_rollback_with_relationships(self):
        state_1 = {
            "world": {"active_location": "room_a"},
            "relationships": {"factions": [{"id": "harpers", "standing": 5}]}
        }
        c1 = self.git.commit(state_1, intent="Met Harpers", reason="Formed alliance")

        state_2 = {
            "world": {"active_location": "room_b"},
            "relationships": {"factions": [{"id": "harpers", "standing": -2}]}
        }
        c2 = self.git.commit(state_2, intent="Betrayed Harpers", reason="Stole amulet")

        restored = self.git.rollback(c1["commit_id"])
        self.assertIsNotNone(restored)
        self.assertEqual(restored["relationships"]["factions"][0]["standing"], 5)


if __name__ == "__main__":
    unittest.main()
