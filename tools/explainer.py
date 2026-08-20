"""
Interactive Rules & Mechanics Explainer for Agentic D&D.
Explains D&D 5e (2024 Revision) rules, weapon masteries, conditions,
spellcasting systems, combat actions, and DC calculation mechanics.
"""

from typing import Dict, Any, Optional, List
import difflib
from tools.compendium import Compendium


TOPIC_CATEGORIES = {
    "weapon_masteries": {
        "cleave": "If you hit a creature with a melee attack, you can make a second melee attack roll against a second creature within 5 feet of the first that is also within your reach. On a hit, the second creature takes the weapon's damage without your ability modifier.",
        "graze": "If your attack roll misses a creature, that creature still takes damage equal to the ability modifier you used for the attack roll (minimum 1).",
        "nick": "When you make the extra attack provided by the Light weapon property, you can make it as part of the Attack action instead of as a Bonus Action (once per turn).",
        "push": "When you hit a creature, you can push it up to 10 feet straight away from you if it is Large or smaller.",
        "sap": "When you hit a creature, that creature has Disadvantage on its next attack roll before the start of your next turn.",
        "slow": "When you hit a creature and deal damage, you can reduce its Speed by 10 feet until the start of your next turn (doesn't stack).",
        "topple": "When you hit a creature, you can force it to make a Constitution saving throw (DC 8 + your ability mod + proficiency bonus) or fall Prone.",
        "vex": "When you hit a creature and deal damage, you have Advantage on your next attack roll against that creature before the end of your next turn."
    },
    "core_mechanics": {
        "death_saves": "At 0 HP, roll a d20 at the start of your turn. 10+ is a success, 9 or lower is a failure. 3 successes = stabilized. 3 failures = permanent death. Natural 20 = regain 1 HP immediately and regain consciousness. Natural 1 = 2 failures.",
        "short_rest": "A period of downtime at least 1 hour long. Characters can spend one or more Hit Dice to regain HP (Roll Hit Die + CON mod per die spent).",
        "long_rest": "A period of downtime at least 8 hours long. Full HP recovery, full spell slot recovery, and recover up to half of total maximum Hit Dice.",
        "cover": "Half Cover: +2 AC and DEX saving throws. Three-Quarters Cover: +5 AC and DEX saving throws. Total Cover: Cannot be targeted directly by attacks or spells.",
        "initiative": "At the start of combat, every participant rolls 1d20 + DEX modifier to determine turn order from highest to lowest.",
        "ritual": "Casting a spell as a ritual adds 10 minutes to the casting time but does not expend a spell slot. The spell must have the ritual tag and be prepared (or in wizard spellbook).",
        "concentration": "Taking damage while concentrating requires a Constitution saving throw (DC 10 or half the damage taken, whichever is higher) to maintain the spell."
    }
}


def explain_mechanic(query: str) -> Dict[str, Any]:
    """
    Looks up and returns comprehensive explanation of a D&D 2024 mechanic,
    condition, weapon mastery, or rule.
    """
    comp = Compendium.get_instance()
    clean_q = query.strip().lower().replace(" ", "_").replace("-", "_")

    # 1. Check Weapon Masteries
    if clean_q in TOPIC_CATEGORIES["weapon_masteries"]:
        return {
            "found": True,
            "category": "Weapon Mastery (D&D 2024)",
            "topic": clean_q.title(),
            "explanation": TOPIC_CATEGORIES["weapon_masteries"][clean_q],
            "rule_source": "PHB 2024 Chapter 6 (Equipment)"
        }

    # 2. Check Core Mechanics
    if clean_q in TOPIC_CATEGORIES["core_mechanics"]:
        return {
            "found": True,
            "category": "Core Rules Engine",
            "topic": clean_q.replace("_", " ").title(),
            "explanation": TOPIC_CATEGORIES["core_mechanics"][clean_q],
            "rule_source": "D&D Basic Rules / 2024 Rules Engine"
        }

    # 3. Check Conditions from Compendium
    conditions = comp.get_conditions()
    if clean_q in conditions:
        c_data = conditions[clean_q]
        desc = c_data.get("description", "")
        effects = c_data.get("effects", [])
        effect_str = "\n".join(f"• {e}" for e in effects) if effects else desc
        return {
            "found": True,
            "category": "Condition",
            "topic": c_data.get("name", clean_q.title()),
            "explanation": effect_str or desc,
            "rule_source": "D&D 2024 Conditions Compendium"
        }

    # 4. Check Actions from Compendium
    actions = comp.get_actions()
    if clean_q in actions:
        a_data = actions[clean_q]
        return {
            "found": True,
            "category": "Action in Combat",
            "topic": a_data.get("name", clean_q.title()),
            "explanation": a_data.get("description", ""),
            "rule_source": "D&D 2024 Combat Actions"
        }

    # 5. Check Feats from Compendium
    feats = comp.get_feats()
    if clean_q in feats:
        f_data = feats[clean_q]
        benefits = "\n".join(f"• {b}" for b in f_data.get("benefits", []))
        return {
            "found": True,
            "category": f"Feat ({f_data.get('category', 'General').title()})",
            "topic": f_data.get("name", clean_q.title()),
            "explanation": f"Prerequisite: {f_data.get('prerequisite', 'None')}\n{benefits}",
            "rule_source": "PHB 2024 Chapter 5 (Feats)"
        }

    # 6. Check Weapons from Compendium
    weapons = comp.get_weapons()
    if clean_q in weapons:
        w_data = weapons[clean_q]
        props = ", ".join(w_data.get("properties", [])) or "None"
        return {
            "found": True,
            "category": "Weapon (Equipment)",
            "topic": w_data.get("name", clean_q.title()),
            "explanation": f"Damage: {w_data.get('damage')} {w_data.get('damage_type')} | Mastery: {w_data.get('mastery')} | Properties: {props} | Cost: {w_data.get('cost')}",
            "rule_source": "PHB 2024 Chapter 6 (Equipment)"
        }

    # 7. Check Rules Glossary from Compendium
    glossary = comp.get_glossary()
    if clean_q in glossary:
        g_data = glossary[clean_q]
        return {
            "found": True,
            "category": "Rules Glossary (D&D 2024)",
            "topic": g_data.get("name", clean_q.title()),
            "explanation": g_data.get("description", ""),
            "rule_source": "PHB 2024 Appendix C (Rules Glossary)"
        }

    # 8. Fuzzy Match across all catalogs
    all_keys = list(TOPIC_CATEGORIES["weapon_masteries"].keys()) + \
               list(TOPIC_CATEGORIES["core_mechanics"].keys()) + \
               list(conditions.keys()) + \
               list(actions.keys()) + \
               list(feats.keys()) + \
               list(weapons.keys()) + \
               list(glossary.keys())
    
    matches = difflib.get_close_matches(clean_q, all_keys, n=4, cutoff=0.45)
    return {
        "found": False,
        "query": query,
        "error": f"Mechanic '{query}' not found.",
        "suggestions": matches or ["topple", "vex", "stealth", "death_saves", "short_rest", "cover", "grapple", "alert", "greatsword"]
    }
