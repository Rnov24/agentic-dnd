"""
Git-Style Campaign Versioning & Rollback Engine for Agentic D&D.
Maintains persistent chronological commits, diffs, branch timelines, and rollback capabilities.
"""

import copy
import hashlib
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


class CampaignGitManager:
    """
    Manages snapshots, commits, history timelines, diffs, and rollback
    for the campaign and structured state.
    """

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = Path(__file__).resolve().parent.parent

        self.history_file = self.base_dir / "state" / "history.json"
        self.snapshots_dir = self.base_dir / "state" / "snapshots"
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_branch = "main"

    def _generate_commit_id(self, parent_id: Optional[str], state_data: Dict[str, Any]) -> str:
        payload = f"{parent_id}_{time.time()}_{json.dumps(state_data, sort_keys=True)}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:8]

    def load_history(self) -> Dict[str, Any]:
        if not self.history_file.exists():
            return {
                "active_branch": "main",
                "branches": {"main": []},
                "commits": {},
                "head": None
            }
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {
                "active_branch": "main",
                "branches": {"main": []},
                "commits": {},
                "head": None
            }

    def save_history(self, history: Dict[str, Any]) -> None:
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    def commit(
        self,
        full_state: Dict[str, Any],
        intent: str,
        reason: str,
        agent: str = "DM Agent",
        tool_calls: Optional[List[Dict[str, Any]]] = None,
        affected_files: Optional[List[str]] = None,
        approved_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Creates a new immutable commit snapshot.
        """
        history = self.load_history()
        branch = history.get("active_branch", "main")
        branch_commits = history.setdefault("branches", {}).setdefault(branch, [])
        parent_id = history.get("head")

        commit_id = self._generate_commit_id(parent_id, full_state)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Save state snapshot
        snapshot_path = self.snapshots_dir / f"{commit_id}.json"
        with open(snapshot_path, "w", encoding="utf-8") as f:
            json.dump(full_state, f, indent=2, ensure_ascii=False)

        commit_record = {
            "commit_id": commit_id,
            "parent_id": parent_id,
            "branch": branch,
            "timestamp": timestamp,
            "intent": intent,
            "reason": reason,
            "agent": agent,
            "tool_calls": tool_calls or [],
            "affected_files": affected_files or ["state/world.json", "state/party.json"],
            "approved_by": approved_by,
        }

        history["commits"][commit_id] = commit_record
        branch_commits.append(commit_id)
        history["head"] = commit_id
        self.save_history(history)

        return commit_record

    def get_commit(self, commit_id: str) -> Optional[Dict[str, Any]]:
        history = self.load_history()
        return history.get("commits", {}).get(commit_id)

    def get_commit_state(self, commit_id: str) -> Optional[Dict[str, Any]]:
        snapshot_path = self.snapshots_dir / f"{commit_id}.json"
        if not snapshot_path.exists():
            return None
        with open(snapshot_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_history_timeline(self, branch: Optional[str] = None) -> List[Dict[str, Any]]:
        history = self.load_history()
        target_branch = branch or history.get("active_branch", "main")
        commit_ids = history.get("branches", {}).get(target_branch, [])
        commits = [history["commits"][cid] for cid in commit_ids if cid in history.get("commits", {})]
        return list(reversed(commits))

    def compute_diff(self, commit_id_a: Optional[str], commit_id_b: str) -> Dict[str, Any]:
        """
        Computes a structured diff between two commits.
        """
        state_a = self.get_commit_state(commit_id_a) if commit_id_a else {}
        state_b = self.get_commit_state(commit_id_b) or {}

        diffs = {}
        all_keys = set((state_a or {}).keys()).union((state_b or {}).keys())

        for k in all_keys:
            val_a = (state_a or {}).get(k)
            val_b = (state_b or {}).get(k)
            if val_a != val_b:
                diffs[k] = {
                    "before": val_a,
                    "after": val_b
                }
        return {
            "commit_a": commit_id_a,
            "commit_b": commit_id_b,
            "changed_keys": list(diffs.keys()),
            "diffs": diffs
        }

    def rollback(self, commit_id: str) -> Optional[Dict[str, Any]]:
        """
        Rolls back the active campaign state to the snapshot at commit_id.
        """
        target_state = self.get_commit_state(commit_id)
        if not target_state:
            return None

        # Import StateManager dynamically to avoid circular import
        from tools.state_manager import StateManager
        sm = StateManager(str(self.base_dir))

        if "world" in target_state:
            sm.save_world(target_state["world"])
        if "party" in target_state:
            sm.save_party(target_state["party"])
        if "npcs" in target_state:
            sm.save_npcs(target_state["npcs"])
        if "combat" in target_state:
            sm.save_combat(target_state["combat"])
        if "quests" in target_state:
            sm.save_quests(target_state["quests"])
        if "relationships" in target_state:
            sm.save_relationships(target_state["relationships"])

        # Update HEAD in history
        history = self.load_history()
        history["head"] = commit_id
        self.save_history(history)

        return target_state

    def create_branch(self, branch_name: str) -> bool:
        history = self.load_history()
        clean_name = branch_name.strip().replace(" ", "-").lower()
        if clean_name in history.setdefault("branches", {}):
            return False
        # Copy current branch's commits as the starting history for the new branch
        active = history.get("active_branch", "main")
        current_commits = list(history["branches"].get(active, []))
        history["branches"][clean_name] = current_commits
        history["active_branch"] = clean_name
        self.save_history(history)
        return True

    def switch_branch(self, branch_name: str) -> Optional[Dict[str, Any]]:
        history = self.load_history()
        clean_name = branch_name.strip().replace(" ", "-").lower()
        if clean_name not in history.get("branches", {}):
            return None
        history["active_branch"] = clean_name
        branch_commits = history["branches"][clean_name]
        head_commit = branch_commits[-1] if branch_commits else None
        history["head"] = head_commit
        self.save_history(history)

        if head_commit:
            return self.rollback(head_commit)
        return {}
