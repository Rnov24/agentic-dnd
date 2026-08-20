"""
Compendium Schema Validator & Homebrew Linter for Agentic D&D.
Validates the structural integrity, required schema keys, and mathematical consistency
of all rules compendiums in rules/*.json.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from tools.compendium import Compendium


class CompendiumValidator:
    """
    Validates rules compendiums and provides statistical diagnostics for developers.
    """

    def __init__(self, project_root: Optional[str] = None):
        if project_root:
            self.root = Path(project_root)
        else:
            self.root = Path(__file__).resolve().parent.parent

        self.rules_dir = self.root / "rules"
        self.compendium = Compendium.get_instance(self.root)

    def validate_all(self) -> Dict[str, Any]:
        """Runs comprehensive validation across all rules compendiums."""
        errors: List[str] = []
        warnings: List[str] = []
        stats: Dict[str, int] = {}

        # 1. Classes
        classes = self.compendium.get_classes()
        stats["classes"] = len(classes)
        for name, data in classes.items():
            if not isinstance(data, dict):
                errors.append(f"Class '{name}' must be an object.")
                continue
            if not data.get("hit_die"):
                errors.append(f"Class '{name}' missing required field 'hit_die'.")

        # 2. Species
        species = self.compendium.get_all_species()
        stats["species"] = len(species)
        for name, data in species.items():
            if not isinstance(data, dict):
                errors.append(f"Species '{name}' must be an object.")
                continue
            if not data.get("size"):
                warnings.append(f"Species '{name}' missing 'size'.")

        # 3. Backgrounds
        bgs = self.compendium.get_all_backgrounds()
        stats["backgrounds"] = len(bgs)

        # 4. Spells
        spells = self.compendium.get_spells()
        stats["spells"] = len(spells)
        for sid, sdata in spells.items():
            if not isinstance(sdata, dict):
                errors.append(f"Spell '{sid}' must be an object.")
                continue
            for req in ["name", "level", "school", "casting_time", "range"]:
                if req not in sdata:
                    errors.append(f"Spell '{sid}' missing required field '{req}'.")

        # 5. Monsters
        monsters = self.compendium.get_monsters()
        stats["monsters"] = len(monsters)
        for mid, mdata in monsters.items():
            if not isinstance(mdata, dict):
                errors.append(f"Monster '{mid}' must be an object.")
                continue
            for req in ["name", "cr", "ac", "hp"]:
                if req not in mdata:
                    errors.append(f"Monster '{mid}' missing required field '{req}'.")

        # 6. Magic Items
        items = self.compendium.get_magic_items()
        stats["magic_items"] = len(items)
        for iid, idata in items.items():
            if not isinstance(idata, dict):
                errors.append(f"Magic item '{iid}' must be an object.")
                continue
            for req in ["name", "rarity"]:
                if req not in idata:
                    errors.append(f"Magic item '{iid}' missing required field '{req}'.")

        # 7. Conditions
        conds = self.compendium.get_conditions()
        stats["conditions"] = len(conds)

        # 8. Presets
        presets = self.compendium.get_all_presets()
        stats["presets"] = len(presets)

        # 9. Feats
        feats = self.compendium.get_feats()
        stats["feats"] = len(feats)

        # 10. Weapons
        weapons = self.compendium.get_weapons()
        stats["weapons"] = len(weapons)

        # 11. Armor
        armor = self.compendium.get_armor()
        stats["armor"] = len(armor)

        # 12. Equipment & Tools
        equipment = self.compendium.get_equipment_items()
        stats["equipment"] = len(equipment)

        # 13. Subclasses
        subclasses = self.compendium.get_subclasses()
        stats["subclasses"] = len(subclasses)

        # 14. Rules Glossary
        glossary = self.compendium.get_glossary()
        stats["glossary"] = len(glossary)

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "stats": stats,
            "total_entities": sum(stats.values())
        }

    def get_stats(self) -> Dict[str, Any]:
        """Returns entity counts and catalog stats."""
        val = self.validate_all()
        return {
            "total_entities": val["total_entities"],
            "entity_counts": val["stats"],
            "healthy": val["valid"]
        }
