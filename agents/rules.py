"""
Rules Agent for Agentic D&D.
Interprets D&D 5e (2024 revision) rules, determines required skill checks,
difficulty classes (DCs), modifiers, and applicable conditions.
"""

from typing import Dict, Any, List, Optional
from rules.rules_engine import RulesEngine, RULES_2024_ACTIONS, CONDITIONS_REGISTRY


class RulesAgent:
    """
    Analyzes intended player actions against D&D 5e (2024) rules.
    """

    def __init__(self):
        self.engine = RulesEngine()

    def _extract_target(self, lower_intent: str, context: Dict[str, Any]) -> str:
        # 1. Check active threats in current room/scene
        threats = context.get("threats", [])
        for t in threats:
            t_str = t if isinstance(t, str) else t.get("name", "")
            t_lower = t_str.lower()
            for token in t_lower.replace("(", " ").replace(")", " ").split():
                if len(token) > 2 and token not in ["the", "and", "hiding", "behind", "with", "from"] and not token.isdigit():
                    if token in lower_intent:
                        return token

        # 2. Check active NPCs
        npcs = context.get("npcs", [])
        for n in npcs:
            n_str = n if isinstance(n, str) else n.get("name", n.get("id", ""))
            n_lower = n_str.lower()
            if n_lower in lower_intent:
                return n_str.lower().replace(" ", "_")

        # 3. Check Compendium bestiary monsters
        from tools.compendium import Compendium
        comp = Compendium.get_instance()
        monsters = comp.get_monsters()
        for m_id, m_data in monsters.items():
            m_name = m_data.get("name", m_id).lower()
            if m_name in lower_intent or m_id in lower_intent:
                return m_id

        # 4. Fallback heuristics for common creature types or target word
        for word in ["goblin", "bugbear", "hobgoblin", "redbrand", "wolf", "dragon", "spider", "zombie", "skeleton", "guard", "sentry", "bandit", "mage", "boss"]:
            if word in lower_intent:
                return word

        return threats[0].split()[0].lower() if threats and isinstance(threats[0], str) else "target"

    def _extract_weapon(self, lower_intent: str, actor: Dict[str, Any]) -> str:
        attacks = actor.get("attacks", [])
        for atk in attacks:
            name = atk.get("name", "")
            if name.lower() in lower_intent:
                return name

        equipment = actor.get("equipment", [])
        for eq in equipment:
            eq_name = eq if isinstance(eq, str) else eq.get("name", "")
            if eq_name.lower() in lower_intent:
                return eq_name

        if attacks and attacks[0].get("name"):
            return attacks[0].get("name")

        # Check for equipped weapons in equipment list
        for eq in equipment:
            eq_str = (eq if isinstance(eq, str) else eq.get("name", "")).lower()
            for w in [
                "dagger", "shortsword", "longsword", "greatsword", "shortbow", "crossbow",
                "mace", "quarterstaff", "scimitar", "handaxe", "spear", "warhammer",
                "battleaxe", "halberd", "glaive", "rapier", "morningstar", "flail",
                "pike", "trident", "whip", "blowgun", "dart", "sling", "heavy crossbow"
            ]:
                if w in eq_str:
                    return eq if isinstance(eq, str) else eq.get("name")

        if equipment:
            return equipment[0] if isinstance(equipment[0], str) else equipment[0].get("name", "Shortsword")

        return "Shortsword"

    def _extract_spell(self, lower_intent: str, actor: Dict[str, Any]) -> Optional[str]:
        known_spells = actor.get("spells_prepared", []) + actor.get("cantrips", [])
        for s in known_spells:
            if s.lower() in lower_intent:
                return s
        from tools.compendium import Compendium
        comp = Compendium.get_instance()
        all_spells = comp.get_spells()
        for s_id, s_data in all_spells.items():
            s_name = s_data.get("name", s_id).lower()
            if s_name in lower_intent or s_id in lower_intent:
                return s_data.get("name", s_id)
        if "cast " in lower_intent:
            parts = lower_intent.split("cast ", 1)[1].split(" at ")[0].split(" on ")[0].strip()
            if parts:
                return parts.title()
        return None

    def analyze_intent(self, intent: str, actor: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determines mechanical requirements (ability, skill, DC, advantage/disadvantage)
        for a given natural language intent based on D&D 5e (2024 revision).
        """
        lower_intent = intent.lower()
        actor_name = actor.get("name", "Hero")
        
        # 1. Spellcasting
        spell_name = self._extract_spell(lower_intent, actor)
        if spell_name or "cast " in lower_intent:
            target_name = self._extract_target(lower_intent, context)
            chosen_spell = spell_name or "Fire Bolt"
            return {
                "action_type": "spellcasting",
                "actor": actor_name,
                "spell_name": chosen_spell,
                "target": target_name,
                "requires_check": False,
                "requires_attack_roll": False,
                "rationale": f"{actor_name} is casting {chosen_spell} targeting {target_name}.",
            }

        # 2. Resting
        if any(w in lower_intent for w in ["short rest", "long rest", "take a rest", "bandage wounds", "sleep for the night", "camp", "take a breather"]):
            rest_type = "long" if any(w in lower_intent for w in ["long", "sleep", "camp", "night"]) else "short"
            return {
                "action_type": "resting",
                "actor": actor_name,
                "rest_type": rest_type,
                "requires_check": False,
                "rationale": f"Party is initiating a {rest_type} rest.",
            }
        
        # 3. Combat / Attack intents
        if any(w in lower_intent for w in ["attack", "strike", "stab", "shoot", "slash", "hit", "fire at"]):
            target_name = self._extract_target(lower_intent, context)
            weapon = self._extract_weapon(lower_intent, actor)
            return {
                "action_type": "combat_attack",
                "actor": actor_name,
                "target": target_name,
                "weapon": weapon,
                "requires_check": False,
                "requires_attack_roll": True,
                "rationale": f"{actor_name} initiates a weapon attack against {target_name} with {weapon}.",
            }
            
        # 4. Stealth / Sneak / Hide
        if any(w in lower_intent for w in ["sneak", "stealth", "creep", "slip past", "hide", "quietly"]):
            lighting = context.get("lighting", "").lower()
            weather = context.get("weather", "").lower()
            base_dc = 12 if "dim" in lighting or "dark" in lighting else 15
            has_adv = "thunder" in weather or "rain" in weather or "fog" in weather
            return {
                "action_type": "ability_check",
                "ability": "dexterity",
                "skill": "stealth",
                "dc": base_dc,
                "advantage": has_adv,
                "disadvantage": False,
                "rationale": f"Stealth check required to move silently through the area (DC {base_dc}" + (", Advantage from weather noise" if has_adv else "") + ").",
            }
            
        # 5. Pickpocket / Sleight of Hand / Steal Key
        if any(w in lower_intent for w in ["steal", "pickpocket", "take the key", "grab key", "snatch", "sleight of hand"]):
            return {
                "action_type": "ability_check",
                "ability": "dexterity",
                "skill": "sleight_of_hand",
                "dc": 13,
                "advantage": False,
                "disadvantage": False,
                "rationale": "Sleight of Hand check (DC 13) to perform fine manipulation unnoticed.",
            }
            
        # 6. Lockpicking / Pick Lock / Free Prisoner
        if any(w in lower_intent for w in ["pick lock", "pick the lock", "unlock", "open lock"]):
            return {
                "action_type": "ability_check",
                "ability": "dexterity",
                "skill": "sleight_of_hand",
                "dc": 14,
                "advantage": False,
                "disadvantage": False,
                "rationale": "Thieves' Tools / Dexterity check (DC 14) to pick the mechanism.",
            }
            
        # 7. Search / Investigate / Inspect
        if any(w in lower_intent for w in ["search", "investigate", "inspect", "examine", "look around", "study"]):
            return {
                "action_type": "ability_check",
                "ability": "intelligence",
                "skill": "investigation",
                "dc": 12,
                "advantage": False,
                "disadvantage": False,
                "rationale": "Investigation check (DC 12) to uncover hidden details, mechanisms, or clues.",
            }
            
        # 8. Social / Persuasion / Deception / Intimidation
        if any(w in lower_intent for w in ["convince", "persuade", "lie", "deceive", "bluff", "intimidate", "threaten", "talk to", "speak with"]):
            skill = "deception" if any(w in lower_intent for w in ["lie", "deceive", "bluff"]) else ("intimidation" if any(w in lower_intent for w in ["intimidate", "threaten"]) else "persuasion")
            return {
                "action_type": "ability_check",
                "ability": "charisma",
                "skill": skill,
                "dc": 14,
                "advantage": False,
                "disadvantage": False,
                "rationale": f"{skill.capitalize()} check (DC 14) to influence NPC reaction.",
            }
            
        # 9. Default routine action / exploration
        return {
            "action_type": "routine_action",
            "requires_check": False,
            "rationale": "Action is routine or narrative with no significant risk of failure.",
        }
