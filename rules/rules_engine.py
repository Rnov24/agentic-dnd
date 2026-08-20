"""
D&D 5e (2024 Revision & Basic Rules) Rules Engine.
Provides mechanical validation, action costs, conditions registry,
fear/sanity rules, encounter difficulty calculations, and monster/item lookups.
Loads action definitions and conditions dynamically from rules/*.json via Compendium.
"""

from typing import Dict, Any, List, Optional, Union
from tools.compendium import Compendium
from tools.encounters import calculate_encounter_difficulty, get_adventuring_day_budget, get_xp_by_cr
from tools.monsters import get_monster, load_monsters
from tools.magic_items import get_magic_item, load_magic_items


def get_rules_actions() -> Dict[str, Any]:
    return Compendium.get_instance().get_actions()

def get_conditions_registry() -> Dict[str, Any]:
    return Compendium.get_instance().get_conditions()

RULES_2024_ACTIONS = get_rules_actions()
CONDITIONS_REGISTRY = get_conditions_registry()


class RulesEngine:
    """
    Centralized D&D 5e (2024 Revision & Basic Rules) Arbiter.
    """

    def __init__(self, project_root: Optional[str] = None):
        self.compendium = Compendium.get_instance(project_root)

    @staticmethod
    def get_monster_info(name: str) -> Optional[Dict[str, Any]]:
        return get_monster(name)

    @staticmethod
    def get_magic_item_info(name: str) -> Optional[Dict[str, Any]]:
        return get_magic_item(name)

    def validate_action(self, action_name: str, actor: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates if an actor can perform a given action under D&D 5e rules.
        """
        actions = self.compendium.get_actions()
        action_key = action_name.lower().replace(" ", "_")
        
        # Check if action exists in rules
        if action_key not in actions:
            return {
                "valid": True,
                "action": action_name,
                "type": "custom",
                "message": f"Custom or DM-adjudicated action: '{action_name}'"
            }
            
        rule = actions[action_key]
        
        # Check actor conditions preventing actions
        conditions = actor.get("conditions", [])
        incapacitating = ["incapacitated", "paralyzed", "petrified", "stunned", "unconscious"]
        for cond in conditions:
            if cond.lower() in incapacitating:
                return {
                    "valid": False,
                    "action": action_name,
                    "reason": f"Actor is {cond} and cannot take actions or reactions."
                }
                
        return {
            "valid": True,
            "action": action_name,
            "type": rule["type"],
            "description": rule["description"]
        }

    def get_condition_effects(self, condition: str) -> Optional[str]:
        """Looks up the mechanical effects of a D&D 5e condition."""
        conditions = self.compendium.get_conditions()
        cond_data = conditions.get(condition.lower())
        return cond_data.get("effects") if cond_data else None

    def evaluate_fear_and_sanity(
        self,
        character: Dict[str, Any],
        dc: int = 13,
        stress_source: str = "horrific sight",
        stat: str = "wisdom"
    ) -> Dict[str, Any]:
        """
        Adjudicates fear or horror saving throws.
        """
        from tools.mechanics import roll_saving_throw
        
        # Check for immunity or advantage (e.g. Brave trait)
        species = character.get("species", "").lower()
        has_brave = "halfling" in species or any("brave" in f.lower() for f in character.get("features", []))
        
        res = roll_saving_throw(character, stat, dc, advantage=has_brave)
        
        passed = res["success"]
        consequence = None
        if not passed:
            consequence = f"Character is frightened by {stress_source} for 1 minute or until succeeding on a repeat save."
            
        return {
            "source": stress_source,
            "stat_used": stat,
            "dc": dc,
            "roll": res["total"],
            "success": passed,
            "had_advantage": has_brave,
            "consequence": consequence
        }
