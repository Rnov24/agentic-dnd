"""
Combat Agent for Agentic D&D.
Coordinates tactical encounters, initiative tracking, enemy actions, and combat resolution.
"""

from typing import Dict, Any, List, Optional
from tools.combat import roll_initiative, roll_attack, roll_damage, apply_damage, apply_condition


class CombatAgent:
    """
    Manages active combat encounters, enemy AI turns, and combat flow.
    """

    def initiate_combat(
        self,
        party: List[Dict[str, Any]],
        enemies: List[Dict[str, Any]],
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Rolls initiative for all combatants and creates the active combat state.
        """
        all_participants = []
        for p in party:
            char_copy = dict(p)
            char_copy["is_player"] = True
            all_participants.append(char_copy)
            
        for e in enemies:
            enemy_copy = dict(e)
            enemy_copy["is_player"] = False
            all_participants.append(enemy_copy)
            
        tracker = roll_initiative(all_participants, seed=seed)
        
        return {
            "is_active": True,
            "round": 1,
            "turn_index": 0,
            "initiative_order": tracker,
            "environmental_effects": ["Damp Stone (normal terrain)"],
            "log": [f"Combat initiated! Round 1 begins with {tracker[0]['name']}'s turn."]
        }

    def resolve_enemy_turn(
        self,
        enemy: Dict[str, Any],
        party: List[Dict[str, Any]],
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Executes an enemy AI turn using deterministic combat tools.
        """
        target = party[0] if party else {"name": "Player", "ac": 14, "hp": {"current": 20, "max": 20}}
        enemy_attacks = enemy.get("attacks", [{"name": "Basic Strike", "ability": "strength", "damage": "1d6+1"}])
        chosen_attack = enemy_attacks[0]
        
        atk_res = roll_attack(
            attacker=enemy,
            target=target,
            attack_name=chosen_attack.get("name"),
            seed=seed
        )
        
        dmg_res = None
        damage_applied = None
        
        if atk_res["is_hit"]:
            dmg_res = roll_damage(
                attacker=enemy,
                target=target,
                damage_formula=chosen_attack.get("damage", "1d6+1"),
                damage_type=chosen_attack.get("damage_type", "slashing"),
                is_critical=atk_res["is_critical_hit"],
                seed=seed
            )
            damage_applied = apply_damage(
                target=target,
                damage_amount=dmg_res["final_damage"],
                damage_type=dmg_res["damage_type"]
            )
            
        return {
            "enemy_name": enemy.get("name", "Enemy"),
            "target_name": target.get("name", "Target"),
            "attack_result": atk_res,
            "damage_result": dmg_res,
            "damage_applied": damage_applied,
            "narrative_action": f"{enemy.get('name')} lunges at {target.get('name')} with {chosen_attack.get('name')}!",
        }
