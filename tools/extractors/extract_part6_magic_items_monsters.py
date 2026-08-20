"""
Extractor for Part 6: Magic Items and Monsters (Appendix B & Chapter 6).
Updates rules/magic_items.json and rules/monsters.json based on PHB 2024.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

MAGIC_ITEMS_2024 = {
    "potion_of_healing": {
        "name": "Potion of Healing",
        "type": "Potion",
        "rarity": "common",
        "attunement": False,
        "action": "Bonus Action to drink, or Action to administer",
        "healing": "2d4+2",
        "description": "You regain 2d4 + 2 Hit Points when you drink this potion. Drinking a potion yourself is a Bonus Action; administering it to another creature is an Action."
    },
    "potion_of_greater_healing": {
        "name": "Potion of Greater Healing",
        "type": "Potion",
        "rarity": "uncommon",
        "attunement": False,
        "action": "Bonus Action to drink, or Action to administer",
        "healing": "4d4+4",
        "description": "You regain 4d4 + 4 Hit Points when you drink this potion."
    },
    "potion_of_superior_healing": {
        "name": "Potion of Superior Healing",
        "type": "Potion",
        "rarity": "rare",
        "attunement": False,
        "action": "Bonus Action to drink, or Action to administer",
        "healing": "8d4+8",
        "description": "You regain 8d4 + 8 Hit Points when you drink this potion."
    },
    "spell_scroll": {
        "name": "Spell Scroll",
        "type": "Scroll",
        "rarity": "common",
        "attunement": False,
        "description": "A Spell Scroll bears the magical words of a single spell. If the spell is on your class's spell list, you can read the scroll and cast its spell without providing any material components."
    },
    "bag_of_holding": {
        "name": "Bag of Holding",
        "type": "Wondrous Item",
        "rarity": "uncommon",
        "attunement": False,
        "weight_lb": 15,
        "weight_capacity_lbs": 500,
        "capacity_lb": 500,
        "volume_cu_ft": 64,
        "description": "This bag has an interior space considerably larger than its outside dimensions. The bag can hold up to 500 pounds, not exceeding a volume of 64 cubic feet. The bag always weighs 15 pounds."
    },
    "boots_of_elvenkind": {
        "name": "Boots of Elvenkind",
        "type": "Wondrous Item",
        "rarity": "uncommon",
        "attunement": False,
        "description": "While you wear these boots, your steps make no sound, regardless of the surface you are moving across. You have Advantage on Dexterity (Stealth) checks that rely on moving silently."
    },
    "cloak_of_elvenkind": {
        "name": "Cloak of Elvenkind",
        "type": "Wondrous Item",
        "rarity": "uncommon",
        "attunement": True,
        "effects": {
            "stealth_advantage": True
        },
        "description": "While you wear this cloak with its hood up, Wisdom (Perception) checks made to see you have Disadvantage, and you have Advantage on Dexterity (Stealth) checks made to hide."
    },
    "ring_of_protection": {
        "name": "Ring of Protection",
        "type": "Ring",
        "rarity": "rare",
        "attunement": True,
        "ac_bonus": 1,
        "save_bonus": 1,
        "description": "You gain a +1 bonus to AC and saving throws while wearing this ring."
    },
    "weapon_plus_1": {
        "name": "Weapon, +1",
        "type": "Weapon",
        "rarity": "uncommon",
        "attunement": False,
        "attack_bonus": 1,
        "damage_bonus": 1,
        "description": "You have a +1 bonus to attack and damage rolls made with this magic weapon."
    },
    "weapon_plus_2": {
        "name": "Weapon, +2",
        "type": "Weapon",
        "rarity": "rare",
        "attunement": False,
        "attack_bonus": 2,
        "damage_bonus": 2,
        "description": "You have a +2 bonus to attack and damage rolls made with this magic weapon."
    },
    "armor_plus_1": {
        "name": "Armor, +1",
        "type": "Armor",
        "rarity": "rare",
        "attunement": False,
        "ac_bonus": 1,
        "description": "You have a +1 bonus to Armor Class while wearing this armor."
    },
    "wand_of_magic_missiles": {
        "name": "Wand of Magic Missiles",
        "type": "Wand",
        "rarity": "uncommon",
        "attunement": False,
        "charges": {"max": 7, "current": 7},
        "description": "This wand has 7 charges. While holding it, you can use an action to expend 1 or more of its charges to cast the Magic Missile spell from it. Regains 1d6 + 1 expended charges daily at dawn."
    }
}

MONSTERS_2024 = {
    "goblin": {
        "id": "goblin",
        "name": "Goblin",
        "size": "Small",
        "type": "Humanoid (Goblinoid)",
        "alignment": "Neutral Evil",
        "ac": 15,
        "hp": {"current": 7, "max": 7},
        "hit_dice": "2d6",
        "speed": "30 ft.",
        "stats": {"strength": 8, "dexterity": 14, "constitution": 10, "intelligence": 10, "wisdom": 8, "charisma": 8},
        "skills": {"stealth": 6},
        "senses": "Darkvision 60 ft., passive Perception 9",
        "cr": "1/4",
        "xp": 50,
        "traits": [
            "nimble_escape",
            {"name": "Nimble Escape", "id": "nimble_escape", "description": "The goblin can take the Disengage or Hide action as a bonus action on each of its turns."}
        ],
        "attacks": [
            {"name": "Scimitar", "type": "melee", "ability": "dexterity", "bonus": 4, "damage": "1d6+2", "damage_type": "slashing", "mastery": "Nick"},
            {"name": "Shortbow", "type": "ranged", "ability": "dexterity", "bonus": 4, "damage": "1d6+2", "damage_type": "piercing", "mastery": "Vex"}
        ]
    },
    "skeleton": {
        "id": "skeleton",
        "name": "Skeleton",
        "size": "Medium",
        "type": "Undead",
        "alignment": "Lawful Evil",
        "ac": 13,
        "hp": {"current": 13, "max": 13},
        "hit_dice": "2d8+4",
        "speed": "30 ft.",
        "stats": {"strength": 10, "dexterity": 14, "constitution": 15, "intelligence": 6, "wisdom": 8, "charisma": 5},
        "vulnerabilities": ["bludgeoning"],
        "damage_immunities": ["poison"],
        "condition_immunities": ["exhaustion", "poisoned"],
        "senses": "Darkvision 60 ft., passive Perception 9",
        "cr": "1/4",
        "xp": 50,
        "attacks": [
            {"name": "Shortsword", "type": "melee", "ability": "dexterity", "bonus": 4, "damage": "1d6+2", "damage_type": "piercing", "mastery": "Vex"},
            {"name": "Shortbow", "type": "ranged", "ability": "dexterity", "bonus": 4, "damage": "1d6+2", "damage_type": "piercing", "mastery": "Vex"}
        ]
    },
    "zombie": {
        "id": "zombie",
        "name": "Zombie",
        "size": "Medium",
        "type": "Undead",
        "alignment": "Neutral Evil",
        "ac": 8,
        "hp": {"current": 22, "max": 22},
        "hit_dice": "3d8+9",
        "speed": "20 ft.",
        "stats": {"strength": 13, "dexterity": 6, "constitution": 16, "intelligence": 3, "wisdom": 6, "charisma": 5},
        "saving_throws": {"wisdom": 0},
        "damage_immunities": ["poison"],
        "condition_immunities": ["poisoned"],
        "senses": "Darkvision 60 ft., passive Perception 8",
        "cr": "1/4",
        "xp": 50,
        "traits": [
            {"name": "Undead Fortitude", "description": "If damage reduces the zombie to 0 HP, it makes a CON save (DC 5 + damage taken) unless Radiant or critical. On success, it drops to 1 HP instead."}
        ],
        "attacks": [
            {"name": "Slam", "type": "melee", "ability": "strength", "bonus": 3, "damage": "1d6+1", "damage_type": "bludgeoning"}
        ]
    },
    "guard": {
        "id": "guard",
        "name": "Guard",
        "size": "Medium",
        "type": "Humanoid (Any Race)",
        "alignment": "Any Alignment",
        "ac": 16,
        "hp": {"current": 11, "max": 11},
        "hit_dice": "2d8+2",
        "speed": "30 ft.",
        "stats": {"strength": 13, "dexterity": 12, "constitution": 12, "intelligence": 10, "wisdom": 11, "charisma": 10},
        "skills": {"perception": 2},
        "senses": "passive Perception 12",
        "cr": "1/8",
        "xp": 25,
        "attacks": [
            {"name": "Spear", "type": "melee", "ability": "strength", "bonus": 3, "damage": "1d6+1", "damage_type": "piercing", "mastery": "Sap"}
        ]
    },
    "adult_red_dragon": {
        "id": "adult_red_dragon",
        "name": "Adult Red Dragon",
        "size": "Huge",
        "type": "Dragon",
        "alignment": "Chaotic Evil",
        "ac": 19,
        "hp": {"current": 256, "max": 256},
        "hit_dice": "19d12+133",
        "speed": "40 ft., climb 40 ft., fly 80 ft.",
        "stats": {"strength": 27, "dexterity": 10, "constitution": 25, "intelligence": 16, "wisdom": 13, "charisma": 21},
        "saving_throws": {"dexterity": 6, "constitution": 13, "wisdom": 7, "charisma": 11},
        "skills": {"perception": 13, "stealth": 6},
        "damage_immunities": ["fire"],
        "senses": "Blindsight 60 ft., Darkvision 120 ft., passive Perception 23",
        "cr": "17",
        "xp": 18000,
        "legendary_actions": ["Detect", "Tail Attack", "Wing Attack"],
        "attacks": [
            {"name": "Bite", "type": "melee", "ability": "strength", "bonus": 14, "damage": "2d10+8", "damage_type": "piercing"}
        ]
    }
}


def run():
    rules_dir = ROOT / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    
    with open(rules_dir / "magic_items.json", "w", encoding="utf-8") as f:
        json.dump(MAGIC_ITEMS_2024, f, indent=2)
    print(f"Saved {len(MAGIC_ITEMS_2024)} magic items to rules/magic_items.json")

    with open(rules_dir / "monsters.json", "w", encoding="utf-8") as f:
        json.dump(MONSTERS_2024, f, indent=2)
    print(f"Saved {len(MONSTERS_2024)} monsters to rules/monsters.json")


if __name__ == "__main__":
    run()
