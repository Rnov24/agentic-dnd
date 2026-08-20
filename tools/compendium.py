"""
Unified Rules & Compendium Registry for Agentic D&D.
Centralizes access, indexing, retrieval, and caching for all static JSON game rules,
classes, species, backgrounds, presets, progression matrices, encounter thresholds,
actions, conditions, spells, monsters, and magic items.

Eliminates embedded JSON/data dictionaries from code files.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union


class Compendium:
    """
    Registry and loader for all immutable static compendiums under rules/*.json.
    Caches loaded data for fast in-memory access during turn execution.
    """
    _instance: Optional['Compendium'] = None
    _cache: Dict[str, Any] = {}

    def __init__(self, project_root: Optional[Union[str, Path]] = None):
        repo_root = Path(__file__).resolve().parent.parent
        if project_root and (Path(project_root) / "rules").exists():
            self.project_root = Path(project_root)
            self.rules_dir = self.project_root / "rules"
        else:
            self.project_root = repo_root
            self.rules_dir = repo_root / "rules"

    @classmethod
    def get_instance(cls, project_root: Optional[Union[str, Path]] = None) -> 'Compendium':
        if cls._instance is None:
            cls._instance = Compendium(project_root)
        elif project_root and (Path(project_root) / "rules").exists() and cls._instance.project_root != Path(project_root):
            cls._instance = Compendium(project_root)
        return cls._instance

    def _load_json(self, filename: str) -> Dict[str, Any]:
        """Loads and caches a JSON file from the rules directory."""
        if filename in self._cache:
            return self._cache[filename]

        file_path = self.rules_dir / filename
        if not file_path.exists():
            return {}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._cache[filename] = data
                return data
        except Exception:
            return {}

    def reload(self):
        """Clears cache to reload rules from disk."""
        self._cache.clear()

    # 1. Classes
    def get_classes(self) -> Dict[str, Any]:
        return self._load_json("classes.json")

    def get_class(self, name: str) -> Optional[Dict[str, Any]]:
        classes = self.get_classes()
        if not classes:
            return None
        target = name.strip().lower().replace(" ", "_")
        if target in classes:
            return classes[target]
        for k, v in classes.items():
            if k.lower() == target or v.get("name", "").lower() == name.strip().lower():
                return v
        for k, v in classes.items():
            if target in k.lower() or target in v.get("name", "").lower():
                return v
        return None

    # 2. Species / Subraces
    def get_all_species(self) -> Dict[str, Any]:
        return self._load_json("species.json")

    def get_species(self, name: str) -> Optional[Dict[str, Any]]:
        all_spc = self.get_all_species()
        if not all_spc:
            return None
        target = name.strip().lower().replace(" ", "_")
        if target in all_spc:
            return all_spc[target]
        for k, v in all_spc.items():
            if k.lower() == target or v.get("name", "").lower() == name.strip().lower():
                return v
        for k, v in all_spc.items():
            if target in k.lower() or target in v.get("name", "").lower():
                return v
        return None

    # 3. Backgrounds
    def get_all_backgrounds(self) -> Dict[str, Any]:
        return self._load_json("backgrounds.json")

    def get_background(self, name: str) -> Optional[Dict[str, Any]]:
        bgs = self.get_all_backgrounds()
        if not bgs:
            return None
        target = name.strip().lower().replace(" ", "_")
        if target in bgs:
            return bgs[target]
        for k, v in bgs.items():
            if k.lower() == target or v.get("name", "").lower() == name.strip().lower():
                return v
        for k, v in bgs.items():
            if target in k.lower() or target in v.get("name", "").lower():
                return v
        return None

    # 4. Presets
    def get_all_presets(self) -> Dict[str, Any]:
        return self._load_json("presets.json")

    def get_preset(self, preset_id: str) -> Optional[Dict[str, Any]]:
        presets = self.get_all_presets()
        return presets.get(preset_id.strip().lower())

    # 5. Progression
    def get_progression(self) -> Dict[str, Any]:
        return self._load_json("progression.json")

    def get_proficiency_bonus(self, level: int) -> int:
        prog = self.get_progression()
        prof_map = prog.get("proficiency_bonus_by_level", {})
        return prof_map.get(str(level), 2 if level < 5 else (3 if level < 9 else (4 if level < 13 else (5 if level < 17 else 6))))

    def get_spell_slots(self, char_class: str, level: int) -> Dict[str, Dict[str, int]]:
        prog = self.get_progression()
        cls_lower = char_class.strip().lower()

        if cls_lower in ["wizard", "cleric", "druid", "bard", "sorcerer"]:
            slots_map = prog.get("full_caster_spell_slots", {}).get(str(level))
            if isinstance(slots_map, dict):
                spell_slots = {}
                for slvl, count in slots_map.items():
                    spell_slots[f"level_{slvl}"] = {"current": count, "max": count}
                return spell_slots
            slots_list = prog.get("full_caster_slots", {}).get(str(level), [2])
            spell_slots = {}
            for idx, count in enumerate(slots_list, 1):
                spell_slots[f"level_{idx}"] = {"current": count, "max": count}
            return spell_slots

        elif cls_lower in ["paladin", "ranger"]:
            slots_list = prog.get("half_caster_slots", {}).get(str(level), [])
            spell_slots = {}
            for idx, count in enumerate(slots_list, 1):
                spell_slots[f"level_{idx}"] = {"current": count, "max": count}
            return spell_slots

        elif cls_lower == "warlock":
            slot_info = prog.get("warlock_slots", {}).get(str(level), [1, 1])
            count, slot_lvl = slot_info[0], slot_info[1]
            return {f"level_{slot_lvl}": {"current": count, "max": count}}

        return {}

    def get_class_features_for_level(self, char_class: str, level: int) -> List[str]:
        cls_data = self.get_class(char_class)
        if cls_data and "features_by_level" in cls_data:
            return cls_data["features_by_level"].get(str(level), [])
        prog = self.get_progression()
        features_map = prog.get("class_features_by_level", {})
        cls_key = char_class.capitalize()
        return features_map.get(cls_key, {}).get(str(level), [])

    # 6. Encounters & XP
    def get_encounter_rules(self) -> Dict[str, Any]:
        return self._load_json("encounters.json")

    def get_xp_thresholds(self, level: int) -> Dict[str, int]:
        enc = self.get_encounter_rules()
        return enc.get("xp_thresholds_by_level", {}).get(str(level), {"easy": 25, "medium": 50, "hard": 75, "deadly": 100})

    def get_adventuring_day_xp(self, level: int) -> int:
        enc = self.get_encounter_rules()
        return enc.get("adventuring_day_xp", {}).get(str(level), 300)

    def get_cr_to_xp(self) -> Dict[str, int]:
        enc = self.get_encounter_rules()
        return enc.get("cr_to_xp", {})

    def get_multiplier_tiers(self) -> List[Tuple[int, float]]:
        enc = self.get_encounter_rules()
        tiers = enc.get("multiplier_tiers", [[1, 1.0], [2, 1.5], [6, 2.0], [10, 2.5], [14, 3.0], [999999, 4.0]])
        return [(t[0], float(t[1])) for t in tiers]

    # 7. Actions & Conditions
    def get_actions(self) -> Dict[str, Any]:
        return self._load_json("actions.json")

    def get_conditions(self) -> Dict[str, Any]:
        return self._load_json("conditions.json")

    # 8. Defaults
    def get_defaults(self, category: str) -> Dict[str, Any]:
        defaults = self._load_json("defaults.json")
        return defaults.get(category, {})

    def _get_active_adventure_dir(self) -> Optional[Path]:
        """Detects active adventure directory from state/world.json."""
        world_file = self.project_root / "state" / "world.json"
        if world_file.exists():
            try:
                with open(world_file, "r", encoding="utf-8") as f:
                    wdata = json.load(f)
                    cid = wdata.get("campaign_id")
                    if cid:
                        adv_dir = self.project_root / "adventures" / cid
                        if adv_dir.exists():
                            return adv_dir
            except Exception:
                pass
        
        # Fallback to default lost_mine_of_phandelver if present
        default_lmop = self.project_root / "adventures" / "lost_mine_of_phandelver"
        if default_lmop.exists():
            return default_lmop
        return None

    # 9. Spells, Monsters, Magic Items, Encounters, Locations (Multi-Tier Overlay)
    def get_spells(self) -> Dict[str, Any]:
        return self._load_json("spells.json")

    def get_spell(self, name_or_id: str) -> Optional[Dict[str, Any]]:
        spells = self.get_spells()
        target = name_or_id.strip().lower().replace(" ", "_")
        if target in spells:
            return spells[target]
        for k, v in spells.items():
            if v.get("name", "").lower() == name_or_id.strip().lower() or target in k:
                return v
        return None

    def get_monsters(self) -> Dict[str, Any]:
        """Returns core bestiary overlaid with active adventure monsters."""
        monsters = dict(self._load_json("monsters.json"))
        for k, v in monsters.items():
            if isinstance(v, dict):
                v["_source"] = "Core 5e Rules"

        # Check active adventure monsters
        adv_dir = self._get_active_adventure_dir()
        if adv_dir:
            adv_monsters_file = adv_dir / "monsters" / "monsters.json"
            if adv_monsters_file.exists():
                try:
                    with open(adv_monsters_file, "r", encoding="utf-8") as f:
                        adv_m = json.load(f)
                        adv_title = adv_dir.name.replace("_", " ").title()
                        for mk, mv in adv_m.items():
                            if isinstance(mv, dict):
                                mv["_source"] = f"Adventure: {adv_title}"
                                monsters[mk] = mv
                except Exception:
                    pass
        return monsters

    def get_monster(self, name_or_id: str) -> Optional[Dict[str, Any]]:
        monsters = self.get_monsters()
        target = name_or_id.strip().lower().replace(" ", "_")
        if target in monsters:
            return monsters[target]
        for k, v in monsters.items():
            if v.get("name", "").lower() == name_or_id.strip().lower() or target in k:
                return v
        # Fuzzy / partial match
        for k, v in monsters.items():
            if name_or_id.strip().lower() in v.get("name", "").lower():
                return v
        return None

    def get_magic_items(self) -> Dict[str, Any]:
        """Returns core magic items overlaid with active adventure unique relics."""
        items = dict(self._load_json("magic_items.json"))
        for k, v in items.items():
            if isinstance(v, dict):
                v["_source"] = "Core 5e Rules"

        # Check active adventure magic items
        adv_dir = self._get_active_adventure_dir()
        if adv_dir:
            adv_items_file = adv_dir / "items" / "magic_items.json"
            if adv_items_file.exists():
                try:
                    with open(adv_items_file, "r", encoding="utf-8") as f:
                        adv_it = json.load(f)
                        adv_title = adv_dir.name.replace("_", " ").title()
                        for ik, iv in adv_it.items():
                            if isinstance(iv, dict):
                                iv["_source"] = f"Adventure: {adv_title}"
                                items[ik] = iv
                except Exception:
                    pass
        return items

    def get_magic_item(self, name_or_id: str) -> Optional[Dict[str, Any]]:
        items = self.get_magic_items()
        target = name_or_id.strip().lower().replace(" ", "_").replace("+", "plus_")
        if target in items:
            return items[target]
        for k, v in items.items():
            if v.get("name", "").lower() == name_or_id.strip().lower() or target in k:
                return v
        for k, v in items.items():
            if name_or_id.strip().lower() in v.get("name", "").lower():
                return v
        return None

    def get_encounters(self) -> List[Dict[str, Any]]:
        """Returns core encounters and active adventure preset encounters."""
        encs = self._load_json("encounters.json")
        adv_dir = self._get_active_adventure_dir()
        if adv_dir:
            adv_enc_file = adv_dir / "encounters" / "encounters.json"
            if adv_enc_file.exists():
                try:
                    with open(adv_enc_file, "r", encoding="utf-8") as f:
                        adv_encs = json.load(f)
                        if isinstance(adv_encs, list):
                            return adv_encs
                except Exception:
                    pass
        return encs if isinstance(encs, list) else []

    def get_locations(self) -> List[Dict[str, Any]]:
        """Returns active adventure locations."""
        adv_dir = self._get_active_adventure_dir()
        if adv_dir:
            loc_file = adv_dir / "locations" / "locations.json"
            if loc_file.exists():
                try:
                    with open(loc_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            return data
                        if isinstance(data, dict):
                            if "locations" in data and isinstance(data["locations"], list):
                                return data["locations"]
                            return list(data.values())
                except Exception:
                    pass
        return []


    def get_feats(self) -> Dict[str, Any]:
        return self._load_json("feats.json")

    def get_feat(self, name_or_id: str) -> Optional[Dict[str, Any]]:
        feats = self.get_feats()
        target = name_or_id.strip().lower().replace(" ", "_").replace("-", "_")
        if target in feats:
            return feats[target]
        for k, v in feats.items():
            if v.get("name", "").lower() == name_or_id.strip().lower() or target in k:
                return v
        return None

    def get_weapons(self) -> Dict[str, Any]:
        return self._load_json("weapons.json")

    def get_weapon(self, name_or_id: str) -> Optional[Dict[str, Any]]:
        weapons = self.get_weapons()
        target = name_or_id.strip().lower().replace(" ", "_").replace("-", "_")
        if target in weapons:
            return weapons[target]
        for k, v in weapons.items():
            if v.get("name", "").lower() == name_or_id.strip().lower() or target in k:
                return v
        return None

    def get_armor(self) -> Dict[str, Any]:
        return self._load_json("armor.json")

    def get_armor_item(self, name_or_id: str) -> Optional[Dict[str, Any]]:
        armor = self.get_armor()
        target = name_or_id.strip().lower().replace(" ", "_").replace("-", "_")
        if target in armor:
            return armor[target]
        for k, v in armor.items():
            if v.get("name", "").lower() == name_or_id.strip().lower() or target in k:
                return v
        return None

    def get_equipment_items(self) -> Dict[str, Any]:
        return self._load_json("equipment.json")

    def get_subclasses(self) -> Dict[str, Any]:
        return self._load_json("subclasses.json")

    def get_glossary(self) -> Dict[str, Any]:
        return self._load_json("glossary.json")

    def get_glossary_term(self, term: str) -> Optional[Dict[str, Any]]:
        glossary = self.get_glossary()
        target = term.strip().lower().replace(" ", "_").replace("-", "_")
        if target in glossary:
            return glossary[target]
        for k, v in glossary.items():
            if v.get("name", "").lower() == term.strip().lower() or target in k:
                return v
        return None


# Helper instance functions for convenient global imports
def get_compendium(project_root: Optional[Union[str, Path]] = None) -> Compendium:
    return Compendium.get_instance(project_root)


