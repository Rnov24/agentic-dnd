"""
Multi-Campaign Run Manager & Difficulty Engine for Agentic D&D.
Handles multiple campaign runs/save slots, isolated state directories,
and difficulty presets (Story, Normal, Hardcore, Deadly).
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


DIFFICULTY_PRESETS: Dict[str, Dict[str, Any]] = {
    "story": {
        "id": "story",
        "name": "Story Mode",
        "badge": "🟢 Story",
        "description": "Forgiving narrative adventure with generous recovery and easier saving throws.",
        "death_save_dc": 8,
        "player_save_bonus": 2,
        "monster_hp_multiplier": 0.9,
        "monster_attack_bonus": 0,
        "rest_type": "Standard",
        "permadeath": False
    },
    "normal": {
        "id": "normal",
        "name": "Normal (Core 2024)",
        "badge": "🔵 Normal",
        "description": "Authentic D&D 5e (2024 revision) rules, standard DCs, and balanced combat.",
        "death_save_dc": 10,
        "player_save_bonus": 0,
        "monster_hp_multiplier": 1.0,
        "monster_attack_bonus": 0,
        "rest_type": "Standard",
        "permadeath": False
    },
    "hardcore": {
        "id": "hardcore",
        "name": "Hardcore (Gritty Realism)",
        "badge": "🟠 Hardcore",
        "description": "High-stakes tactical survival with strict death saves, tougher enemies, and permanent consequences.",
        "death_save_dc": 12,
        "player_save_bonus": 0,
        "monster_hp_multiplier": 1.15,
        "monster_attack_bonus": 0,
        "rest_type": "Gritty Realism (8h short rest, 7d long rest)",
        "permadeath": True
    },
    "deadly": {
        "id": "deadly",
        "name": "Deadly (Nightmare)",
        "badge": "🔴 Deadly",
        "description": "Brutal dungeon crawl with empowered monsters, punishing DCs, and lethal traps.",
        "death_save_dc": 14,
        "player_save_bonus": -1,
        "monster_hp_multiplier": 1.3,
        "monster_attack_bonus": 1,
        "rest_type": "Gritty Realism",
        "permadeath": True
    }
}


class RunManager:
    """
    Orchestrates multiple campaign save slots and active run isolation.
    """

    def __init__(self, project_root: Optional[str] = None):
        if project_root:
            self.project_root = Path(project_root)
        else:
            self.project_root = Path(__file__).resolve().parent.parent

        self.runs_dir = self.project_root / "runs"
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        self.active_pointer_file = self.runs_dir / "active_run.json"

    def get_active_run_id(self) -> Optional[str]:
        """Returns the ID of the currently active campaign run, if any."""
        if self.active_pointer_file.exists():
            try:
                with open(self.active_pointer_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("active_run_id")
            except Exception:
                pass
        return None

    def get_active_run_manifest(self) -> Optional[Dict[str, Any]]:
        """Returns the manifest of the active campaign run."""
        run_id = self.get_active_run_id()
        if not run_id:
            return None
        return self.get_run_manifest(run_id)

    def get_run_manifest(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Returns the manifest for a specific run ID."""
        clean_id = run_id.lower().replace(" ", "_")
        manifest_file = self.runs_dir / clean_id / "run_manifest.json"
        if manifest_file.exists():
            try:
                with open(manifest_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return None

    def get_active_run_paths(self) -> Tuple[Path, Path]:
        """
        Returns (state_dir, campaign_dir).
        If an active run is configured in `runs/<run_id>`, returns its isolated paths.
        Otherwise falls back to root `state/` and `campaign/`.
        """
        run_id = self.get_active_run_id()
        if run_id:
            run_path = self.runs_dir / run_id
            if run_path.exists():
                s_dir = run_path / "state"
                c_dir = run_path / "campaign"
                s_dir.mkdir(parents=True, exist_ok=True)
                c_dir.mkdir(parents=True, exist_ok=True)
                return s_dir, c_dir

        # Fallback to root state and campaign directories
        return self.project_root / "state", self.project_root / "campaign"

    def create_run(
        self,
        name: str,
        adventure: str = "lost_mine_of_phandelver",
        difficulty: str = "normal",
        party_ids: Optional[List[str]] = None,
        run_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Initializes a brand new campaign run with isolated state and selected difficulty.
        """
        diff_key = difficulty.lower()
        if diff_key not in DIFFICULTY_PRESETS:
            diff_key = "normal"

        clean_id = run_id or name.lower().replace(" ", "_").replace("'", "")
        # Prevent collisions
        base_id = clean_id
        counter = 1
        while (self.runs_dir / clean_id).exists():
            clean_id = f"{base_id}_{counter}"
            counter += 1

        run_path = self.runs_dir / clean_id
        run_state_dir = run_path / "state"
        run_camp_dir = run_path / "campaign"
        run_state_dir.mkdir(parents=True, exist_ok=True)
        run_camp_dir.mkdir(parents=True, exist_ok=True)

        manifest = {
            "id": clean_id,
            "name": name,
            "adventure": adventure,
            "difficulty": diff_key,
            "difficulty_settings": DIFFICULTY_PRESETS[diff_key],
            "created_at": datetime.now().isoformat(),
            "turns_count": 0,
            "party_ids": party_ids or [],
            "active_character_id": party_ids[0] if party_ids else None
        }

        # Save manifest
        with open(run_path / "run_manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        # Populate party from Character Vault
        from tools.vault import CharacterVault
        vault = CharacterVault(str(self.project_root))
        party_list = []
        if party_ids:
            for pid in party_ids:
                c = vault.get_character(pid)
                if c:
                    party_list.append(c)
        else:
            # Seed with 3 default vault characters
            all_v = vault.list_characters()
            party_list = all_v[:3]
            manifest["party_ids"] = [c.get("id") for c in party_list]
            if party_list:
                manifest["active_character_id"] = party_list[0].get("id")

        with open(run_state_dir / "party.json", "w", encoding="utf-8") as f:
            json.dump({"party": party_list}, f, indent=2)

        # Scaffolding adventure data if adventure package exists
        from tools.adventure_loader import AdventureLoader
        adv_loader = AdventureLoader(str(self.project_root))
        if adventure and adv_loader.get_adventure(adventure):
            adv_data = adv_loader.get_adventure(adventure)
            # Initialize world state for run
            world_data = {
                "campaign_name": name,
                "adventure_slug": adventure,
                "active_location": adv_data.get("manifest", {}).get("starting_scene", {}).get("location_id", "wilderness"),
                "time_of_day": adv_data.get("manifest", {}).get("starting_scene", {}).get("time_of_day", "Late Afternoon"),
                "weather": adv_data.get("manifest", {}).get("starting_scene", {}).get("weather", "Overcast"),
                "lighting": adv_data.get("manifest", {}).get("starting_scene", {}).get("lighting", "Dim Light"),
                "tension_level": adv_data.get("manifest", {}).get("starting_scene", {}).get("tension", "Tense"),
                "active_character_id": manifest["active_character_id"],
                "current_scene": adv_data.get("manifest", {}).get("starting_scene", {}),
                "global_flags": {}
            }
            with open(run_state_dir / "world.json", "w", encoding="utf-8") as f:
                json.dump(world_data, f, indent=2)

            # Initialize NPCs and Quests
            npcs_data = {n.get("id"): n for n in adv_data.get("npcs", []) if isinstance(n, dict)}
            with open(run_state_dir / "npcs.json", "w", encoding="utf-8") as f:
                json.dump(npcs_data, f, indent=2)

            quests_data = {
                "active_quests": adv_data.get("quests", []),
                "completed_quests": []
            }
            with open(run_state_dir / "quests.json", "w", encoding="utf-8") as f:
                json.dump(quests_data, f, indent=2)
        else:
            # Generic starting world
            world_data = {
                "campaign_name": name,
                "adventure_slug": "custom",
                "active_location": "starting_tavern",
                "time_of_day": "Evening",
                "weather": "Clear",
                "lighting": "Warm Torchlight",
                "tension_level": "Calm",
                "active_character_id": manifest["active_character_id"],
                "current_scene": {
                    "title": "The Road Ahead",
                    "description": "Your adventuring party gathers at the tavern table, reviewing maps and sharpening blades."
                },
                "global_flags": {}
            }
            with open(run_state_dir / "world.json", "w", encoding="utf-8") as f:
                json.dump(world_data, f, indent=2)
            with open(run_state_dir / "npcs.json", "w", encoding="utf-8") as f:
                json.dump({}, f, indent=2)
            with open(run_state_dir / "quests.json", "w", encoding="utf-8") as f:
                json.dump({"active_quests": [], "completed_quests": []}, f, indent=2)

        # Initialize combat and history
        with open(run_state_dir / "combat.json", "w", encoding="utf-8") as f:
            json.dump({"in_combat": False, "round": 0, "turn_index": 0, "order": []}, f, indent=2)
        with open(run_state_dir / "history.json", "w", encoding="utf-8") as f:
            json.dump({"commits": [], "branches": {"main": {"head": None}}}, f, indent=2)

        # Auto-switch to newly created run
        self.switch_run(clean_id)

        return {
            "success": True,
            "run_id": clean_id,
            "name": name,
            "adventure": adventure,
            "difficulty": DIFFICULTY_PRESETS[diff_key]["name"],
            "party_size": len(party_list)
        }

    def switch_run(self, run_id: str) -> Dict[str, Any]:
        """Switches the active campaign run."""
        clean_id = run_id.lower().replace(" ", "_")
        run_path = self.runs_dir / clean_id
        if not run_path.exists():
            return {"success": False, "error": f"Campaign run '{run_id}' not found."}

        with open(self.active_pointer_file, "w", encoding="utf-8") as f:
            json.dump({"active_run_id": clean_id, "switched_at": datetime.now().isoformat()}, f, indent=2)

        manifest = self.get_run_manifest(clean_id)
        return {"success": True, "active_run_id": clean_id, "manifest": manifest}

    def list_runs(self) -> List[Dict[str, Any]]:
        """Returns all campaign runs/save slots."""
        active_id = self.get_active_run_id()
        runs = []
        for r_dir in sorted(self.runs_dir.iterdir()):
            if r_dir.is_dir() and (r_dir / "run_manifest.json").exists():
                try:
                    with open(r_dir / "run_manifest.json", "r", encoding="utf-8") as f:
                        data = json.load(f)
                        data["is_active"] = (data.get("id") == active_id)
                        runs.append(data)
                except Exception:
                    continue
        return runs

    def delete_run(self, run_id: str) -> Dict[str, Any]:
        """Deletes a campaign run."""
        clean_id = run_id.lower().replace(" ", "_")
        run_path = self.runs_dir / clean_id
        if not run_path.exists():
            return {"success": False, "error": f"Campaign run '{run_id}' not found."}

        is_active = (self.get_active_run_id() == clean_id)
        shutil.rmtree(run_path, ignore_errors=True)

        if is_active:
            if self.active_pointer_file.exists():
                self.active_pointer_file.unlink()

        return {"success": True, "deleted_run_id": clean_id}

    def get_difficulty_modifiers(self, difficulty: Optional[str] = None) -> Dict[str, Any]:
        """Returns the difficulty modifiers for the specified or active run."""
        if not difficulty:
            manifest = self.get_active_run_manifest()
            diff_key = manifest.get("difficulty", "normal") if manifest else "normal"
        else:
            diff_key = difficulty.lower()

        return DIFFICULTY_PRESETS.get(diff_key, DIFFICULTY_PRESETS["normal"])
