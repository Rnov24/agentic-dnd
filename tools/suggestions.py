"""
Fuzzy Suggestion & Error Recovery Engine for Agentic D&D.
Provides intelligent suggestions for typos in skill names, spell names,
actions, and monster queries to guide players and non-developers.
"""

import difflib
from typing import List, Optional


STANDARD_5E_SKILLS = [
    "acrobatics", "animal handling", "arcana", "athletics", "deception",
    "history", "insight", "intimidation", "investigation", "medicine",
    "nature", "perception", "performance", "persuasion", "religion",
    "sleight of hand", "stealth", "survival"
]

COMMON_5E_SPELLS = [
    "Fire Bolt", "Magic Missile", "Cure Wounds", "Shield", "Thunderwave",
    "Sleep", "Healing Word", "Mage Armor", "Burning Hands", "Sacred Flame",
    "Guiding Bolt", "Bless", "Elementalism", "Eldritch Blast", "Vicious Mockery",
    "Shocking Grasp", "Ray of Frost", "Acid Splash", "Light", "Prestidigitation",
    "Misty Step", "Invisibility", "Scorching Ray", "Hold Person", "Spiritual Weapon"
]


def suggest_closest(query: str, possibilities: List[str], n: int = 3, cutoff: float = 0.4) -> List[str]:
    """Returns top close string matches from possibilities."""
    clean_query = query.strip().lower()
    mapping = {p.lower(): p for p in possibilities}
    matches = difflib.get_close_matches(clean_query, list(mapping.keys()), n=n, cutoff=cutoff)
    return [mapping[m] for m in matches]


def suggest_skill(query: str) -> List[str]:
    """Suggests matching D&D 5e skill names for a query or typo."""
    matches = suggest_closest(query, STANDARD_5E_SKILLS, n=3, cutoff=0.35)
    if not matches:
        return ["Athletics", "Stealth", "Perception", "Insight"]
    return [m.title() for m in matches]


def suggest_spell(query: str, known_spells: Optional[List[str]] = None) -> List[str]:
    """Suggests matching spell names from known spells or standard compendium."""
    pool = known_spells if known_spells else COMMON_5E_SPELLS
    matches = suggest_closest(query, pool, n=3, cutoff=0.35)
    if not matches and known_spells:
        matches = suggest_closest(query, COMMON_5E_SPELLS, n=3, cutoff=0.35)
    if not matches:
        return ["Fire Bolt", "Magic Missile", "Cure Wounds"]
    return matches
