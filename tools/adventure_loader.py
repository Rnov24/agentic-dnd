"""
Universal Adventure Loader & Importer Engine for Agentic D&D.
Handles validation, metadata extraction, and loading of modular adventure packages
(e.g. Lost Mine of Phandelver, Curse of Strahd) into the active campaign.
"""

import json
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional


class AdventureLoader:
    """
    Manages discovery, validation, and loading of modular adventure packages.
    """

    def __init__(self, project_root: Optional[str] = None):
        if project_root:
            self.root = Path(project_root)
        else:
            self.root = Path(__file__).resolve().parent.parent
            
        self.adventures_dir = self.root / "adventures"
        self.state_dir = self.root / "state"
        self.campaign_dir = self.root / "campaign"

    def list_adventures(self) -> List[Dict[str, Any]]:
        """Scans the adventures directory for valid adventure packages."""
        if not self.adventures_dir.exists():
            return []
            
        adventures = []
        for d in self.adventures_dir.iterdir():
            if d.is_dir():
                manifest_file = d / "adventure.json"
                if manifest_file.exists():
                    try:
                        with open(manifest_file, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            data["directory"] = str(d)
                            adventures.append(data)
                    except Exception as e:
                        adventures.append({
                            "id": d.name,
                            "title": d.name.replace("_", " ").title(),
                            "error": f"Failed to parse manifest: {e}"
                        })
        return adventures

    def _safe_adv_dir(self, adventure_id: str) -> Optional[Path]:
        target_dir = (self.adventures_dir / adventure_id).resolve()
        adv_root_resolved = self.adventures_dir.resolve()
        try:
            target_dir.relative_to(adv_root_resolved)
        except ValueError:
            return None
        return target_dir if target_dir.exists() and target_dir.is_dir() else None

    def get_adventure(self, adventure_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves adventure manifest by slug/id."""
        adv_dir = self._safe_adv_dir(adventure_id)
        if not adv_dir:
            return None
        manifest_file = adv_dir / "adventure.json"
        if not manifest_file.exists():
            return None
        with open(manifest_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            data["directory"] = str(adv_dir)
            return data

    def validate_adventure(self, adventure_id: str) -> Dict[str, Any]:
        """Validates the directory structure and schemas of an adventure package."""
        adv_dir = self._safe_adv_dir(adventure_id)
        if not adv_dir:
            return {"valid": False, "errors": [f"Adventure directory '{adventure_id}' not found or invalid."]}

        errors = []
        warnings = []

        manifest_file = adv_dir / "adventure.json"
        if not manifest_file.exists():
            errors.append("Missing required 'adventure.json' manifest.")
        else:
            try:
                with open(manifest_file, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                    for req_key in ["id", "title", "recommended_levels", "starting_location", "starting_scene"]:
                        if req_key not in manifest:
                            errors.append(f"Manifest missing required field '{req_key}'.")
            except Exception as e:
                errors.append(f"Invalid JSON in 'adventure.json': {e}")

        # Check required sub-packages
        json_checks = [
            ("locations/locations.json", "Locations room graph"),
            ("npcs/npcs.json", "NPCs database"),
            ("quests/quests.json", "Quests tracker"),
            ("items/magic_items.json", "Magic items compendium"),
            ("monsters/monsters.json", "Monsters registry"),
            ("encounters/encounters.json", "Encounters list"),
            ("factions/factions.json", "Factions list")
        ]

        for rel_path, desc in json_checks:
            file_path = adv_dir / rel_path
            if not file_path.exists():
                warnings.append(f"Missing {desc} at '{rel_path}'.")
            else:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        json.load(f)
                except Exception as e:
                    errors.append(f"Invalid JSON in '{rel_path}': {e}")

        return {
            "valid": len(errors) == 0,
            "adventure_id": adventure_id,
            "errors": errors,
            "warnings": warnings
        }

    def load_adventure_into_campaign(self, adventure_id: str) -> Dict[str, Any]:
        """
        Loads an adventure package into active state/ and campaign/ directories.
        Preserves static rules/ and creates snapshot baseline.
        """
        validation = self.validate_adventure(adventure_id)
        if not validation["valid"]:
            return {"success": False, "errors": validation["errors"]}

        adv_dir = self._safe_adv_dir(adventure_id)
        manifest = self.get_adventure(adventure_id)
        if not adv_dir or not manifest:
            return {"success": False, "errors": [f"Could not load manifest for {adventure_id}"]}

        # 1. Update state/world.json with starting scene
        world_data = {
            "campaign_id": manifest.get("id"),
            "campaign_name": manifest.get("title"),
            "active_location": manifest.get("starting_location"),
            "time_of_day": manifest.get("starting_scene", {}).get("time_of_day", "Afternoon"),
            "weather": manifest.get("starting_scene", {}).get("weather", "Clear"),
            "lighting": manifest.get("starting_scene", {}).get("lighting", "Bright Light"),
            "tension_level": manifest.get("starting_scene", {}).get("tension_level", "Calm"),
            "current_scene": manifest.get("starting_scene", {})
        }
        self.state_dir.mkdir(parents=True, exist_ok=True)
        with open(self.state_dir / "world.json", "w", encoding="utf-8") as f:
            json.dump(world_data, f, indent=2)

        # 2. Copy/load state JSONs
        state_mappings = [
            ("npcs/npcs.json", "npcs.json"),
            ("quests/quests.json", "quests.json"),
            ("factions/factions.json", "factions.json"),
            ("items/magic_items.json", "items.json"),
            ("monsters/monsters.json", "monsters.json"),
            ("encounters/encounters.json", "encounters.json"),
            ("locations/locations.json", "locations.json")
        ]
        for src_rel, dest_filename in state_mappings:
            src_file = adv_dir / src_rel
            if src_file.exists():
                with open(src_file, "r", encoding="utf-8") as sf:
                    data = json.load(sf)
                with open(self.state_dir / dest_filename, "w", encoding="utf-8") as df:
                    json.dump(data, df, indent=2)

        # 3. Synchronize campaign Markdown documents
        self.campaign_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy chapters, locations, npcs, quests, items
        md_dirs = ["chapters", "locations", "npcs", "quests", "items", "lore"]
        copied_folders = []
        for folder in md_dirs:
            src_folder = adv_dir / folder
            dest_folder = self.campaign_dir / folder
            if src_folder.exists() and src_folder.is_dir():
                dest_folder.mkdir(parents=True, exist_ok=True)
                for item in src_folder.rglob("*.md"):
                    rel_to_folder = item.relative_to(src_folder)
                    dest_file = dest_folder / rel_to_folder
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(item), str(dest_file))
                copied_folders.append(folder)

        # Copy README to campaign/overview.md
        if (adv_dir / "README.md").exists():
            shutil.copy2(str(adv_dir / "README.md"), str(self.campaign_dir / "overview.md"))

        return {
            "success": True,
            "adventure_id": adventure_id,
            "title": manifest.get("title"),
            "starting_location": manifest.get("starting_location"),
            "copied_folders": copied_folders,
            "message": f"Successfully activated adventure '{manifest.get('title')}' into active campaign state!"
        }

    def scaffold_adventure(
        self,
        slug: str,
        title: Optional[str] = None,
        recommended_levels: str = "1-5",
        author: str = "Dungeon Master"
    ) -> Dict[str, Any]:
        """Scaffolds a new modular adventure package directory structure and boilerplate manifests."""
        clean_slug = slug.strip().lower().replace(" ", "_").replace("-", "_")
        adv_dir = self.adventures_dir / clean_slug

        if adv_dir.exists():
            return {
                "success": False,
                "error": f"Adventure directory '{clean_slug}' already exists at '{adv_dir}'."
            }

        adv_title = title or clean_slug.replace("_", " ").title()

        # 1. Create directory tree
        subdirs = [
            "locations", "npcs", "quests", "items", "monsters", "encounters", "factions", "chapters", "lore"
        ]
        adv_dir.mkdir(parents=True, exist_ok=True)
        for s in subdirs:
            (adv_dir / s).mkdir(parents=True, exist_ok=True)

        # 2. Boilerplate adventure.json
        manifest = {
            "id": clean_slug,
            "title": adv_title,
            "version": "1.0.0",
            "author": author,
            "recommended_levels": recommended_levels,
            "party_size": "3-5 players",
            "starting_location": "starting_room",
            "starting_scene": {
                "title": f"Beginning of {adv_title}",
                "description": f"The heroes gather at the threshold of {adv_title}.",
                "weather": "Clear",
                "time_of_day": "Morning",
                "lighting": "Bright Light",
                "tension_level": "Calm",
                "threats": [],
                "exits": ["Explore forward"]
            },
            "chapters": [
                {"id": "chapter_1", "title": "Chapter 1: The Adventure Begins", "file": "chapters/chapter_1.md"}
            ]
        }
        with open(adv_dir / "adventure.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        # 3. Boilerplate JSON files
        json_defaults = {
            "locations/locations.json": {"locations": [{"id": "starting_room", "name": "Starting Room", "description": "The initial chamber."}]},
            "npcs/npcs.json": {"npcs": []},
            "quests/quests.json": {"active_quests": [], "completed_quests": []},
            "items/magic_items.json": {"items": []},
            "monsters/monsters.json": {"monsters": []},
            "encounters/encounters.json": {"encounters": []},
            "factions/factions.json": {"factions": []}
        }
        for rel_path, data in json_defaults.items():
            with open(adv_dir / rel_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

        # 4. Boilerplate Markdown files
        with open(adv_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(f"# {adv_title}\n\n*Modular adventure package for Agentic D&D.*\n\n- **Recommended Levels**: {recommended_levels}\n- **Author**: {author}\n")

        with open(adv_dir / "chapters" / "chapter_1.md", "w", encoding="utf-8") as f:
            f.write(f"# Chapter 1: The Adventure Begins\n\nWelcome to **{adv_title}**.\n")

        return {
            "success": True,
            "adventure_id": clean_slug,
            "title": adv_title,
            "directory": str(adv_dir),
            "message": f"Successfully scaffolded new adventure package '{adv_title}' at '{adv_dir}'!"
        }
