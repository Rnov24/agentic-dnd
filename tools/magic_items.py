"""
Magic Items Compendium & Registry for Agentic D&D.
Implements magic items and attunement rules from D&D Basic Rules / DMG.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ITEMS_FILE = PROJECT_ROOT / "rules" / "magic_items.json"

DEFAULT_MAGIC_ITEMS = {
    "amulet_of_health": {
        "id": "amulet_of_health",
        "name": "Amulet of Health",
        "type": "Wondrous item",
        "rarity": "rare",
        "attunement": True,
        "description": "Your Constitution score is 19 while wearing this amulet. It has no effect if your Constitution is already 19 or higher.",
        "stat_override": {"constitution": 19}
    },
    "bag_of_holding": {
        "id": "bag_of_holding",
        "name": "Bag of Holding",
        "type": "Wondrous item",
        "rarity": "uncommon",
        "attunement": False,
        "weight_capacity_lbs": 500,
        "volume_capacity_cuft": 64,
        "bag_weight_lbs": 15,
        "description": "This bag has an interior space considerably larger than its outside dimensions. It can hold up to 500 pounds, not exceeding 64 cubic feet. The bag weighs 15 pounds regardless of its contents."
    },
    "cloak_of_elvenkind": {
        "id": "cloak_of_elvenkind",
        "name": "Cloak of Elvenkind",
        "type": "Wondrous item",
        "rarity": "uncommon",
        "attunement": True,
        "description": "While you wear this cloak with its hood up, Wisdom (Perception) checks made to see you have disadvantage, and you have advantage on Dexterity (Stealth) checks made to hide.",
        "effects": {
            "stealth_advantage": True,
            "enemy_perception_disadvantage": True
        }
    },
    "gauntlets_of_ogre_power": {
        "id": "gauntlets_of_ogre_power",
        "name": "Gauntlets of Ogre Power",
        "type": "Wondrous item",
        "rarity": "uncommon",
        "attunement": True,
        "description": "Your Strength score is 19 while wearing these gauntlets. They have no effect on you if your Strength is already 19 or higher.",
        "stat_override": {"strength": 19}
    },
    "goggles_of_night": {
        "id": "goggles_of_night",
        "name": "Goggles of Night",
        "type": "Wondrous item",
        "rarity": "uncommon",
        "attunement": False,
        "description": "While wearing these dark lenses, you have darkvision out to a range of 60 feet. If you already have darkvision, wearing the goggles increases its range by 60 feet.",
        "senses_grant": "darkvision +60ft"
    },
    "headband_of_intellect": {
        "id": "headband_of_intellect",
        "name": "Headband of Intellect",
        "type": "Wondrous item",
        "rarity": "uncommon",
        "attunement": True,
        "description": "Your Intelligence score is 19 while wearing this headband. It has no effect if your Intelligence is already 19 or higher.",
        "stat_override": {"intelligence": 19}
    },
    "ring_of_protection": {
        "id": "ring_of_protection",
        "name": "Ring of Protection",
        "type": "Ring",
        "rarity": "rare",
        "attunement": True,
        "description": "You gain a +1 bonus to AC and saving throws while wearing this ring.",
        "bonuses": {"ac": 1, "saving_throws": 1}
    },
    "ring_of_resistance": {
        "id": "ring_of_resistance",
        "name": "Ring of Resistance",
        "type": "Ring",
        "rarity": "rare",
        "attunement": True,
        "description": "You have resistance to one damage type (fire, cold, lightning, poison, acid, necrotic, radiant, or force) while wearing this ring."
    },
    "wand_of_magic_missiles": {
        "id": "wand_of_magic_missiles",
        "name": "Wand of Magic Missiles",
        "type": "Wand",
        "rarity": "uncommon",
        "attunement": False,
        "charges": {"max": 7, "current": 7, "recharge": "1d6+1 daily at dawn"},
        "description": "This wand has 7 charges. While holding it, you can use an action to expend 1 or more of its charges to cast the magic missile spell. For 1 charge, you cast the 1st-level version of the spell. You can increase the spell slot level by one for each additional charge you expend. If you expend the wand's last charge, roll a d20. On a 1, the wand crumbles into ashes."
    },
    "potion_of_healing": {
        "id": "potion_of_healing",
        "name": "Potion of Healing",
        "type": "Potion",
        "rarity": "common",
        "attunement": False,
        "healing_formula": "2d4+2",
        "description": "You regain 2d4 + 2 hit points when you drink this potion. The potion's red liquid glimmers when agitated."
    },
    "weapon_plus_1": {
        "id": "weapon_plus_1",
        "name": "Weapon, +1",
        "type": "Weapon (any)",
        "rarity": "uncommon",
        "attunement": False,
        "description": "You have a +1 bonus to attack and damage rolls made with this magic weapon.",
        "bonuses": {"attack": 1, "damage": 1}
    },
    "armor_plus_1": {
        "id": "armor_plus_1",
        "name": "Armor, +1",
        "type": "Armor (any)",
        "rarity": "rare",
        "attunement": False,
        "description": "You have a +1 bonus to AC while wearing this armor.",
        "bonuses": {"ac": 1}
    }
}


def load_magic_items() -> Dict[str, Any]:
    from tools.compendium import Compendium
    comp = Compendium.get_instance(PROJECT_ROOT)
    return comp.get_magic_items()


def get_magic_item(name_or_id: str) -> Optional[Dict[str, Any]]:
    from tools.compendium import Compendium
    comp = Compendium.get_instance(PROJECT_ROOT)
    return comp.get_magic_item(name_or_id)
