"""
Global Character Vault for Agentic D&D.
Provides a persistent, cross-campaign character pool allowing players to
create, inspect, and reuse characters across any campaign run or adventure.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from tools.compendium import Compendium


class CharacterVault:
    """
    Manages the global character storage pool in `vault/characters/`.
    """

    def __init__(self, project_root: Optional[str] = None):
        if project_root:
            self.project_root = Path(project_root)
        else:
            self.project_root = Path(__file__).resolve().parent.parent

        self.vault_dir = self.project_root / "vault" / "characters"
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        self.compendium = Compendium.get_instance(self.project_root)
        self._ensure_preset_seeding()

    def _ensure_preset_seeding(self):
        """Seed default presets and auto-import existing legacy state characters into vault."""
        existing = list(self.vault_dir.glob("*.json"))
        if not existing:
            from tools.character_creator import CharacterCreator, LMOP_PRESETS
            creator = CharacterCreator(str(self.project_root))
            for preset_id in LMOP_PRESETS:
                try:
                    char = creator.create_character(preset=preset_id, save_to_state=False, save_to_vault=False)
                    if char:
                        self.save_character(char)
                except Exception:
                    pass

        # Auto-import any characters found in state/party.json
        state_party_file = self.project_root / "state" / "party.json"
        if state_party_file.exists():
            try:
                with open(state_party_file, "r", encoding="utf-8") as f:
                    p_data = json.load(f)
                    chars = p_data.get("party") or p_data.get("characters") or []
                    if isinstance(chars, list):
                        for c in chars:
                            if isinstance(c, dict) and (c.get("id") or c.get("name")):
                                cid = c.get("id") or c.get("name", "").lower().replace(" ", "_")
                                if not (self.vault_dir / f"{cid}.json").exists():
                                    self.save_character(c)
            except Exception:
                pass

    def save_character(self, character: Dict[str, Any]) -> Dict[str, Any]:
        """Saves or updates a character in the global vault."""
        char_id = character.get("id") or character.get("name", "hero").lower().replace(" ", "_").replace("'", "")
        character["id"] = char_id
        file_path = self.vault_dir / f"{char_id}.json"
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(character, f, indent=2)

        return {"success": True, "id": char_id, "name": character.get("name"), "path": str(file_path)}

    def get_character(self, char_id_or_name: str) -> Optional[Dict[str, Any]]:
        """Retrieves a character from the vault by ID or name (case-insensitive)."""
        clean_id = char_id_or_name.lower().replace(" ", "_").replace("'", "")
        file_path = self.vault_dir / f"{clean_id}.json"
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass

        # Fallback search across all files by name
        for f_path in self.vault_dir.glob("*.json"):
            try:
                with open(f_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if (data.get("id", "").lower() == clean_id or 
                        data.get("name", "").lower() == char_id_or_name.lower()):
                        return data
            except Exception:
                continue

        return None

    def list_characters(self) -> List[Dict[str, Any]]:
        """Returns all characters currently stored in the global vault."""
        characters = []
        for f_path in sorted(self.vault_dir.glob("*.json")):
            try:
                with open(f_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    characters.append(data)
            except Exception:
                continue
        return characters

    def delete_character(self, char_id_or_name: str) -> Dict[str, Any]:
        """Deletes a character from the vault."""
        char = self.get_character(char_id_or_name)
        if not char:
            return {"success": False, "error": f"Character '{char_id_or_name}' not found in vault."}

        char_id = char.get("id")
        file_path = self.vault_dir / f"{char_id}.json"
        if file_path.exists():
            file_path.unlink()
            return {"success": True, "deleted_id": char_id, "name": char.get("name")}

        return {"success": False, "error": "File not found."}
