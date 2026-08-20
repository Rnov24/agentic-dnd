"""
Monster Bestiary & Statblock Registry for Agentic D&D.
Implements creature statistics from D&D Basic Rules / SRD.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MONSTERS_FILE = PROJECT_ROOT / "rules" / "monsters.json"

DEFAULT_MONSTERS = {
    "goblin": {
        "id": "goblin",
        "name": "Goblin",
        "size": "Small",
        "type": "humanoid (goblinoid)",
        "alignment": "neutral evil",
        "ac": 15,
        "armor_type": "leather armor, shield",
        "hp": {"current": 7, "max": 7, "formula": "2d6"},
        "speed": 30,
        "stats": {"strength": 8, "dexterity": 14, "constitution": 10, "intelligence": 10, "wisdom": 8, "charisma": 8},
        "skills": {"stealth": 6},
        "senses": "darkvision 60 ft., passive Perception 9",
        "languages": "Common, Goblin",
        "cr": "1/4",
        "xp": 50,
        "traits": {
            "nimble_escape": "The goblin can take the Disengage or Hide action as a bonus action on each of its turns."
        },
        "actions": [
            {"name": "Scimitar", "type": "melee", "bonus": 4, "reach": 5, "damage": "1d6+2", "damage_type": "slashing"},
            {"name": "Shortbow", "type": "ranged", "bonus": 4, "range": "80/320", "damage": "1d6+2", "damage_type": "piercing"}
        ]
    },
    "guard": {
        "id": "guard",
        "name": "Guard",
        "size": "Medium",
        "type": "humanoid (any race)",
        "alignment": "any alignment",
        "ac": 16,
        "armor_type": "chain shirt, shield",
        "hp": {"current": 11, "max": 11, "formula": "2d8+2"},
        "speed": 30,
        "stats": {"strength": 13, "dexterity": 12, "constitution": 12, "intelligence": 10, "wisdom": 11, "charisma": 10},
        "skills": {"perception": 2},
        "senses": "passive Perception 12",
        "languages": "any one language (usually Common)",
        "cr": "1/8",
        "xp": 25,
        "actions": [
            {"name": "Spear", "type": "melee/ranged", "bonus": 3, "reach": 5, "range": "20/60", "damage": "1d6+1", "damage_type": "piercing"}
        ]
    },
    "bandit": {
        "id": "bandit",
        "name": "Bandit",
        "size": "Medium",
        "type": "humanoid (any race)",
        "alignment": "any non-lawful alignment",
        "ac": 12,
        "armor_type": "leather armor",
        "hp": {"current": 11, "max": 11, "formula": "2d8+2"},
        "speed": 30,
        "stats": {"strength": 11, "dexterity": 12, "constitution": 12, "intelligence": 10, "wisdom": 10, "charisma": 10},
        "senses": "passive Perception 10",
        "languages": "any one language (usually Common)",
        "cr": "1/8",
        "xp": 25,
        "actions": [
            {"name": "Scimitar", "type": "melee", "bonus": 3, "reach": 5, "damage": "1d6+1", "damage_type": "slashing"},
            {"name": "Light Crossbow", "type": "ranged", "bonus": 3, "range": "80/320", "damage": "1d8+1", "damage_type": "piercing"}
        ]
    },
    "cultist": {
        "id": "cultist",
        "name": "Cultist",
        "size": "Medium",
        "type": "humanoid (any race)",
        "alignment": "any non-good alignment",
        "ac": 12,
        "armor_type": "leather armor",
        "hp": {"current": 9, "max": 9, "formula": "2d8"},
        "speed": 30,
        "stats": {"strength": 11, "dexterity": 12, "constitution": 10, "intelligence": 10, "wisdom": 11, "charisma": 10},
        "skills": {"deception": 2, "religion": 2},
        "senses": "passive Perception 10",
        "languages": "any one language (usually Common)",
        "cr": "1/8",
        "xp": 25,
        "traits": {
            "dark_devotion": "The cultist has advantage on saving throws against being charmed or frightened."
        },
        "actions": [
            {"name": "Scimitar", "type": "melee", "bonus": 3, "reach": 5, "damage": "1d6+1", "damage_type": "slashing"}
        ]
    },
    "bugbear": {
        "id": "bugbear",
        "name": "Bugbear",
        "size": "Medium",
        "type": "humanoid (goblinoid)",
        "alignment": "chaotic evil",
        "ac": 16,
        "armor_type": "hide armor, shield",
        "hp": {"current": 27, "max": 27, "formula": "5d8+5"},
        "speed": 30,
        "stats": {"strength": 15, "dexterity": 14, "constitution": 13, "intelligence": 8, "wisdom": 11, "charisma": 9},
        "skills": {"stealth": 6, "survival": 2},
        "senses": "darkvision 60 ft., passive Perception 10",
        "languages": "Common, Goblin",
        "cr": "1",
        "xp": 200,
        "traits": {
            "brute": "A melee weapon deals one extra die of its damage when the bugbear hits with it (included in attack).",
            "surprise_attack": "If the bugbear surprises a creature and hits it with an attack during the first round of combat, the target takes an extra 2d6 damage from the attack."
        },
        "actions": [
            {"name": "Morningstar", "type": "melee", "bonus": 4, "reach": 5, "damage": "2d8+2", "damage_type": "piercing"},
            {"name": "Javelin", "type": "melee/ranged", "bonus": 4, "reach": 5, "range": "30/120", "damage": "2d6+2", "damage_type": "piercing"}
        ]
    },
    "hobgoblin": {
        "id": "hobgoblin",
        "name": "Hobgoblin",
        "size": "Medium",
        "type": "humanoid (goblinoid)",
        "alignment": "lawful evil",
        "ac": 18,
        "armor_type": "chain mail, shield",
        "hp": {"current": 11, "max": 11, "formula": "2d8+2"},
        "speed": 30,
        "stats": {"strength": 13, "dexterity": 12, "constitution": 12, "intelligence": 10, "wisdom": 10, "charisma": 9},
        "senses": "darkvision 60 ft., passive Perception 10",
        "languages": "Common, Goblin",
        "cr": "1/2",
        "xp": 100,
        "traits": {
            "martial_advantage": "Once per turn, the hobgoblin can deal an extra 2d6 damage to a creature it hits with a weapon attack if that creature is within 5 feet of an ally of the hobgoblin that isn't incapacitated."
        },
        "actions": [
            {"name": "Longsword", "type": "melee", "bonus": 3, "reach": 5, "damage": "1d8+1", "damage_type": "slashing"},
            {"name": "Longbow", "type": "ranged", "bonus": 3, "range": "150/600", "damage": "1d8+1", "damage_type": "piercing"}
        ]
    },
    "ogre": {
        "id": "ogre",
        "name": "Ogre",
        "size": "Large",
        "type": "giant",
        "alignment": "chaotic evil",
        "ac": 11,
        "armor_type": "hide armor",
        "hp": {"current": 59, "max": 59, "formula": "7d10+21"},
        "speed": 40,
        "stats": {"strength": 19, "dexterity": 8, "constitution": 16, "intelligence": 5, "wisdom": 7, "charisma": 7},
        "senses": "darkvision 60 ft., passive Perception 8",
        "languages": "Common, Giant",
        "cr": "2",
        "xp": 450,
        "actions": [
            {"name": "Greatclub", "type": "melee", "bonus": 6, "reach": 5, "damage": "2d8+4", "damage_type": "bludgeoning"},
            {"name": "Javelin", "type": "melee/ranged", "bonus": 6, "reach": 5, "range": "30/120", "damage": "2d6+4", "damage_type": "piercing"}
        ]
    },
    "skeleton": {
        "id": "skeleton",
        "name": "Skeleton",
        "size": "Medium",
        "type": "undead",
        "alignment": "lawful evil",
        "ac": 13,
        "armor_type": "armor scraps",
        "hp": {"current": 13, "max": 13, "formula": "2d8+4"},
        "speed": 30,
        "stats": {"strength": 10, "dexterity": 14, "constitution": 15, "intelligence": 6, "wisdom": 8, "charisma": 5},
        "damage_vulnerabilities": ["bludgeoning"],
        "damage_immunities": ["poison"],
        "condition_immunities": ["exhaustion", "poisoned"],
        "senses": "darkvision 60 ft., passive Perception 9",
        "languages": "understands languages it knew in life but can't speak",
        "cr": "1/4",
        "xp": 50,
        "actions": [
            {"name": "Shortsword", "type": "melee", "bonus": 4, "reach": 5, "damage": "1d6+2", "damage_type": "piercing"},
            {"name": "Shortbow", "type": "ranged", "bonus": 4, "range": "80/320", "damage": "1d6+2", "damage_type": "piercing"}
        ]
    },
    "zombie": {
        "id": "zombie",
        "name": "Zombie",
        "size": "Medium",
        "type": "undead",
        "alignment": "neutral evil",
        "ac": 8,
        "hp": {"current": 22, "max": 22, "formula": "3d8+9"},
        "speed": 20,
        "stats": {"strength": 13, "dexterity": 6, "constitution": 16, "intelligence": 3, "wisdom": 6, "charisma": 5},
        "saving_throws": {"wisdom": 0},
        "damage_immunities": ["poison"],
        "condition_immunities": ["poisoned"],
        "senses": "darkvision 60 ft., passive Perception 8",
        "languages": "understands languages it knew in life but can't speak",
        "cr": "1/4",
        "xp": 50,
        "traits": {
            "undead_fortitude": "If damage reduces the zombie to 0 hit points, it must make a Constitution saving throw with a DC of 5 + the damage taken, unless the damage is radiant or from a critical hit. On a success, the zombie drops to 1 hit point instead."
        },
        "actions": [
            {"name": "Slam", "type": "melee", "bonus": 3, "reach": 5, "damage": "1d6+1", "damage_type": "bludgeoning"}
        ]
    },
    "adult_red_dragon": {
        "id": "adult_red_dragon",
        "name": "Adult Red Dragon",
        "size": "Huge",
        "type": "dragon",
        "alignment": "chaotic evil",
        "ac": 19,
        "armor_type": "natural armor",
        "hp": {"current": 256, "max": 256, "formula": "19d12+133"},
        "speed": 40,
        "fly_speed": 80,
        "stats": {"strength": 27, "dexterity": 10, "constitution": 25, "intelligence": 16, "wisdom": 13, "charisma": 21},
        "saving_throws": {"dexterity": 6, "constitution": 13, "wisdom": 7, "charisma": 11},
        "skills": {"perception": 13, "stealth": 6},
        "damage_immunities": ["fire"],
        "senses": "blindsight 60 ft., darkvision 120 ft., passive Perception 23",
        "languages": "Common, Draconic",
        "cr": "17",
        "xp": 18000,
        "traits": {
            "legendary_resistance": "3/Day. If the dragon fails a saving throw, it can choose to succeed instead."
        },
        "actions": [
            {"name": "Multiattack", "description": "Frightful Presence + Bite + 2 Claws"},
            {"name": "Bite", "type": "melee", "bonus": 14, "reach": 10, "damage": "2d10+8", "extra_damage": "2d6 fire", "damage_type": "piercing"},
            {"name": "Claw", "type": "melee", "bonus": 14, "reach": 5, "damage": "2d6+8", "damage_type": "slashing"},
            {"name": "Fire Breath", "recharge": "5-6", "area": "60 ft cone", "save": "DEX DC 21", "damage": "18d6", "damage_type": "fire"}
        ],
        "legendary_actions": [
            {"name": "Detect", "cost": 1, "description": "Wisdom (Perception) check"},
            {"name": "Tail Attack", "cost": 1, "description": "Melee attack (reach 15ft, 2d8+8 bludgeoning)"},
            {"name": "Wing Attack", "cost": 2, "description": "10ft radius DC 22 DEX save, 2d6+8 damage and knocked prone"}
        ]
    }
}


def load_monsters() -> Dict[str, Any]:
    from tools.compendium import Compendium
    comp = Compendium.get_instance(PROJECT_ROOT)
    return comp.get_monsters()


def get_monster(name_or_id: str) -> Optional[Dict[str, Any]]:
    from tools.compendium import Compendium
    comp = Compendium.get_instance(PROJECT_ROOT)
    return comp.get_monster(name_or_id)
