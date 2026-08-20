"""
Extractor for Part 2: Equipment, Weapons, Armor, and Tools (Chapter 6).
Creates rules/weapons.json, rules/armor.json, and rules/equipment.json based on PHB 2024.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

WEAPONS_2024 = {
    # Simple Melee
    "club": {
        "name": "Club",
        "category": "simple_melee",
        "cost": "1 SP",
        "damage": "1d4",
        "damage_type": "bludgeoning",
        "weight_lb": 2,
        "properties": ["Light"],
        "mastery": "Slow"
    },
    "dagger": {
        "name": "Dagger",
        "category": "simple_melee",
        "cost": "2 GP",
        "damage": "1d4",
        "damage_type": "piercing",
        "weight_lb": 1,
        "properties": ["Finesse", "Light", "Thrown (range 20/60)"],
        "mastery": "Nick"
    },
    "greatclub": {
        "name": "Greatclub",
        "category": "simple_melee",
        "cost": "2 SP",
        "damage": "1d8",
        "damage_type": "bludgeoning",
        "weight_lb": 10,
        "properties": ["Two-Handed"],
        "mastery": "Push"
    },
    "handaxe": {
        "name": "Handaxe",
        "category": "simple_melee",
        "cost": "5 GP",
        "damage": "1d6",
        "damage_type": "slashing",
        "weight_lb": 2,
        "properties": ["Light", "Thrown (range 20/60)"],
        "mastery": "Vex"
    },
    "javelin": {
        "name": "Javelin",
        "category": "simple_melee",
        "cost": "5 SP",
        "damage": "1d6",
        "damage_type": "piercing",
        "weight_lb": 2,
        "properties": ["Thrown (range 30/120)"],
        "mastery": "Slow"
    },
    "light_hammer": {
        "name": "Light Hammer",
        "category": "simple_melee",
        "cost": "2 GP",
        "damage": "1d4",
        "damage_type": "bludgeoning",
        "weight_lb": 2,
        "properties": ["Light", "Thrown (range 20/60)"],
        "mastery": "Nick"
    },
    "mace": {
        "name": "Mace",
        "category": "simple_melee",
        "cost": "5 GP",
        "damage": "1d6",
        "damage_type": "bludgeoning",
        "weight_lb": 4,
        "properties": [],
        "mastery": "Sap"
    },
    "quarterstaff": {
        "name": "Quarterstaff",
        "category": "simple_melee",
        "cost": "2 SP",
        "damage": "1d6",
        "damage_type": "bludgeoning",
        "weight_lb": 4,
        "properties": ["Versatile (1d8)"],
        "mastery": "Topple"
    },
    "sickle": {
        "name": "Sickle",
        "category": "simple_melee",
        "cost": "1 GP",
        "damage": "1d4",
        "damage_type": "slashing",
        "weight_lb": 2,
        "properties": ["Light"],
        "mastery": "Nick"
    },
    "spear": {
        "name": "Spear",
        "category": "simple_melee",
        "cost": "1 GP",
        "damage": "1d6",
        "damage_type": "piercing",
        "weight_lb": 3,
        "properties": ["Thrown (range 20/60)", "Versatile (1d8)"],
        "mastery": "Sap"
    },
    # Simple Ranged
    "dart": {
        "name": "Dart",
        "category": "simple_ranged",
        "cost": "5 CP",
        "damage": "1d4",
        "damage_type": "piercing",
        "weight_lb": 0.25,
        "properties": ["Finesse", "Thrown (range 20/60)"],
        "mastery": "Vex"
    },
    "light_crossbow": {
        "name": "Light Crossbow",
        "category": "simple_ranged",
        "cost": "25 GP",
        "damage": "1d8",
        "damage_type": "piercing",
        "weight_lb": 5,
        "properties": ["Ammunition (range 80/320)", "Loading", "Two-Handed"],
        "mastery": "Slow"
    },
    "shortbow": {
        "name": "Shortbow",
        "category": "simple_ranged",
        "cost": "25 GP",
        "damage": "1d6",
        "damage_type": "piercing",
        "weight_lb": 2,
        "properties": ["Ammunition (range 80/320)", "Two-Handed"],
        "mastery": "Vex"
    },
    "sling": {
        "name": "Sling",
        "category": "simple_ranged",
        "cost": "1 SP",
        "damage": "1d4",
        "damage_type": "bludgeoning",
        "weight_lb": 0,
        "properties": ["Ammunition (range 30/120)"],
        "mastery": "Slow"
    },
    # Martial Melee
    "battleaxe": {
        "name": "Battleaxe",
        "category": "martial_melee",
        "cost": "10 GP",
        "damage": "1d8",
        "damage_type": "slashing",
        "weight_lb": 4,
        "properties": ["Versatile (1d10)"],
        "mastery": "Topple"
    },
    "flail": {
        "name": "Flail",
        "category": "martial_melee",
        "cost": "10 GP",
        "damage": "1d8",
        "damage_type": "bludgeoning",
        "weight_lb": 2,
        "properties": [],
        "mastery": "Sap"
    },
    "glaive": {
        "name": "Glaive",
        "category": "martial_melee",
        "cost": "20 GP",
        "damage": "1d10",
        "damage_type": "slashing",
        "weight_lb": 6,
        "properties": ["Heavy", "Reach", "Two-Handed"],
        "mastery": "Graze"
    },
    "greataxe": {
        "name": "Greataxe",
        "category": "martial_melee",
        "cost": "30 GP",
        "damage": "1d12",
        "damage_type": "slashing",
        "weight_lb": 7,
        "properties": ["Heavy", "Two-Handed"],
        "mastery": "Cleave"
    },
    "greatsword": {
        "name": "Greatsword",
        "category": "martial_melee",
        "cost": "50 GP",
        "damage": "2d6",
        "damage_type": "slashing",
        "weight_lb": 6,
        "properties": ["Heavy", "Two-Handed"],
        "mastery": "Graze"
    },
    "halberd": {
        "name": "Halberd",
        "category": "martial_melee",
        "cost": "20 GP",
        "damage": "1d10",
        "damage_type": "slashing",
        "weight_lb": 6,
        "properties": ["Heavy", "Reach", "Two-Handed"],
        "mastery": "Cleave"
    },
    "lance": {
        "name": "Lance",
        "category": "martial_melee",
        "cost": "10 GP",
        "damage": "1d10",
        "damage_type": "piercing",
        "weight_lb": 6,
        "properties": ["Heavy", "Reach", "Two-Handed (unless mounted)"],
        "mastery": "Topple"
    },
    "longsword": {
        "name": "Longsword",
        "category": "martial_melee",
        "cost": "15 GP",
        "damage": "1d8",
        "damage_type": "slashing",
        "weight_lb": 3,
        "properties": ["Versatile (1d10)"],
        "mastery": "Sap"
    },
    "maul": {
        "name": "Maul",
        "category": "martial_melee",
        "cost": "10 GP",
        "damage": "2d6",
        "damage_type": "bludgeoning",
        "weight_lb": 10,
        "properties": ["Heavy", "Two-Handed"],
        "mastery": "Topple"
    },
    "morningstar": {
        "name": "Morningstar",
        "category": "martial_melee",
        "cost": "15 GP",
        "damage": "1d8",
        "damage_type": "piercing",
        "weight_lb": 4,
        "properties": [],
        "mastery": "Sap"
    },
    "pike": {
        "name": "Pike",
        "category": "martial_melee",
        "cost": "5 GP",
        "damage": "1d10",
        "damage_type": "piercing",
        "weight_lb": 18,
        "properties": ["Heavy", "Reach", "Two-Handed"],
        "mastery": "Push"
    },
    "rapier": {
        "name": "Rapier",
        "category": "martial_melee",
        "cost": "25 GP",
        "damage": "1d8",
        "damage_type": "piercing",
        "weight_lb": 2,
        "properties": ["Finesse"],
        "mastery": "Vex"
    },
    "scimitar": {
        "name": "Scimitar",
        "category": "martial_melee",
        "cost": "25 GP",
        "damage": "1d6",
        "damage_type": "slashing",
        "weight_lb": 3,
        "properties": ["Finesse", "Light"],
        "mastery": "Nick"
    },
    "shortsword": {
        "name": "Shortsword",
        "category": "martial_melee",
        "cost": "10 GP",
        "damage": "1d6",
        "damage_type": "piercing",
        "weight_lb": 2,
        "properties": ["Finesse", "Light"],
        "mastery": "Vex"
    },
    "trident": {
        "name": "Trident",
        "category": "martial_melee",
        "cost": "5 GP",
        "damage": "1d8",
        "damage_type": "piercing",
        "weight_lb": 4,
        "properties": ["Thrown (range 20/60)", "Versatile (1d10)"],
        "mastery": "Topple"
    },
    "war_pick": {
        "name": "War Pick",
        "category": "martial_melee",
        "cost": "5 GP",
        "damage": "1d8",
        "damage_type": "piercing",
        "weight_lb": 2,
        "properties": ["Versatile (1d10)"],
        "mastery": "Sap"
    },
    "warhammer": {
        "name": "Warhammer",
        "category": "martial_melee",
        "cost": "15 GP",
        "damage": "1d8",
        "damage_type": "bludgeoning",
        "weight_lb": 2,
        "properties": ["Versatile (1d10)"],
        "mastery": "Push"
    },
    "whip": {
        "name": "Whip",
        "category": "martial_melee",
        "cost": "2 GP",
        "damage": "1d4",
        "damage_type": "slashing",
        "weight_lb": 3,
        "properties": ["Finesse", "Reach"],
        "mastery": "Slow"
    },
    # Martial Ranged
    "blowgun": {
        "name": "Blowgun",
        "category": "martial_ranged",
        "cost": "10 GP",
        "damage": "1",
        "damage_type": "piercing",
        "weight_lb": 1,
        "properties": ["Ammunition (range 25/100)", "Loading"],
        "mastery": "Vex"
    },
    "heavy_crossbow": {
        "name": "Heavy Crossbow",
        "category": "martial_ranged",
        "cost": "50 GP",
        "damage": "1d10",
        "damage_type": "piercing",
        "weight_lb": 18,
        "properties": ["Ammunition (range 100/400)", "Heavy", "Loading", "Two-Handed"],
        "mastery": "Push"
    },
    "longbow": {
        "name": "Longbow",
        "category": "martial_ranged",
        "cost": "50 GP",
        "damage": "1d8",
        "damage_type": "piercing",
        "weight_lb": 2,
        "properties": ["Ammunition (range 150/600)", "Heavy", "Two-Handed"],
        "mastery": "Slow"
    },
    "musket": {
        "name": "Musket",
        "category": "martial_ranged",
        "cost": "500 GP",
        "damage": "1d12",
        "damage_type": "piercing",
        "weight_lb": 10,
        "properties": ["Ammunition (range 40/120)", "Loading", "Two-Handed"],
        "mastery": "Slow"
    },
    "pistol": {
        "name": "Pistol",
        "category": "martial_ranged",
        "cost": "250 GP",
        "damage": "1d10",
        "damage_type": "piercing",
        "weight_lb": 3,
        "properties": ["Ammunition (range 30/90)", "Loading"],
        "mastery": "Vex"
    }
}

ARMOR_2024 = {
    # Light Armor
    "padded_armor": {
        "name": "Padded Armor",
        "category": "light",
        "cost": "5 GP",
        "base_ac": 11,
        "dex_mod": "full",
        "strength_req": 0,
        "stealth_disadvantage": True,
        "weight_lb": 8,
        "don_time": "1 minute",
        "doff_time": "1 minute"
    },
    "leather_armor": {
        "name": "Leather Armor",
        "category": "light",
        "cost": "10 GP",
        "base_ac": 11,
        "dex_mod": "full",
        "strength_req": 0,
        "stealth_disadvantage": False,
        "weight_lb": 10,
        "don_time": "1 minute",
        "doff_time": "1 minute"
    },
    "studded_leather_armor": {
        "name": "Studded Leather Armor",
        "category": "light",
        "cost": "45 GP",
        "base_ac": 12,
        "dex_mod": "full",
        "strength_req": 0,
        "stealth_disadvantage": False,
        "weight_lb": 13,
        "don_time": "1 minute",
        "doff_time": "1 minute"
    },
    # Medium Armor
    "hide_armor": {
        "name": "Hide Armor",
        "category": "medium",
        "cost": "10 GP",
        "base_ac": 12,
        "dex_mod": "max_2",
        "strength_req": 0,
        "stealth_disadvantage": False,
        "weight_lb": 12,
        "don_time": "5 minutes",
        "doff_time": "1 minute"
    },
    "chain_shirt": {
        "name": "Chain Shirt",
        "category": "medium",
        "cost": "50 GP",
        "base_ac": 13,
        "dex_mod": "max_2",
        "strength_req": 0,
        "stealth_disadvantage": False,
        "weight_lb": 20,
        "don_time": "5 minutes",
        "doff_time": "1 minute"
    },
    "scale_mail": {
        "name": "Scale Mail",
        "category": "medium",
        "cost": "50 GP",
        "base_ac": 14,
        "dex_mod": "max_2",
        "strength_req": 0,
        "stealth_disadvantage": True,
        "weight_lb": 45,
        "don_time": "5 minutes",
        "doff_time": "1 minute"
    },
    "breastplate": {
        "name": "Breastplate",
        "category": "medium",
        "cost": "400 GP",
        "base_ac": 14,
        "dex_mod": "max_2",
        "strength_req": 0,
        "stealth_disadvantage": False,
        "weight_lb": 20,
        "don_time": "5 minutes",
        "doff_time": "1 minute"
    },
    "half_plate": {
        "name": "Half Plate Armor",
        "category": "medium",
        "cost": "750 GP",
        "base_ac": 15,
        "dex_mod": "max_2",
        "strength_req": 0,
        "stealth_disadvantage": True,
        "weight_lb": 40,
        "don_time": "5 minutes",
        "doff_time": "1 minute"
    },
    # Heavy Armor
    "ring_mail": {
        "name": "Ring Mail",
        "category": "heavy",
        "cost": "30 GP",
        "base_ac": 14,
        "dex_mod": "none",
        "strength_req": 0,
        "stealth_disadvantage": True,
        "weight_lb": 40,
        "don_time": "10 minutes",
        "doff_time": "5 minutes"
    },
    "chain_mail": {
        "name": "Chain Mail",
        "category": "heavy",
        "cost": "75 GP",
        "base_ac": 16,
        "dex_mod": "none",
        "strength_req": 13,
        "stealth_disadvantage": True,
        "weight_lb": 55,
        "don_time": "10 minutes",
        "doff_time": "5 minutes"
    },
    "splint_armor": {
        "name": "Splint Armor",
        "category": "heavy",
        "cost": "200 GP",
        "base_ac": 17,
        "dex_mod": "none",
        "strength_req": 15,
        "stealth_disadvantage": True,
        "weight_lb": 60,
        "don_time": "10 minutes",
        "doff_time": "5 minutes"
    },
    "plate_armor": {
        "name": "Plate Armor",
        "category": "heavy",
        "cost": "1500 GP",
        "base_ac": 18,
        "dex_mod": "none",
        "strength_req": 15,
        "stealth_disadvantage": True,
        "weight_lb": 65,
        "don_time": "10 minutes",
        "doff_time": "5 minutes"
    },
    # Shield
    "shield": {
        "name": "Shield",
        "category": "shield",
        "cost": "10 GP",
        "base_ac": 2,
        "dex_mod": "bonus",
        "strength_req": 0,
        "stealth_disadvantage": False,
        "weight_lb": 6,
        "don_time": "1 action",
        "doff_time": "1 action"
    }
}

EQUIPMENT_2024 = {
    # Artisan Tools
    "alchemists_supplies": {"name": "Alchemist's Supplies", "type": "artisan_tools", "cost": "50 GP", "weight_lb": 8, "ability": "intelligence", "utilize": "Identify a substance (DC 10) or start a fire (DC 15)"},
    "brewers_supplies": {"name": "Brewer's Supplies", "type": "artisan_tools", "cost": "20 GP", "weight_lb": 9, "ability": "wisdom", "utilize": "Purify water (DC 10)"},
    "calligraphers_supplies": {"name": "Calligrapher's Supplies", "type": "artisan_tools", "cost": "10 GP", "weight_lb": 5, "ability": "dexterity", "utilize": "Spot forgery (DC 15)"},
    "carpenters_tools": {"name": "Carpenter's Tools", "type": "artisan_tools", "cost": "8 GP", "weight_lb": 6, "ability": "strength", "utilize": "Seal door (DC 10)"},
    "cartographers_tools": {"name": "Cartographer's Tools", "type": "artisan_tools", "cost": "15 GP", "weight_lb": 6, "ability": "wisdom", "utilize": "Draft map (DC 15)"},
    "cobblers_tools": {"name": "Cobbler's Tools", "type": "artisan_tools", "cost": "5 GP", "weight_lb": 5, "ability": "dexterity", "utilize": "Find hidden compartment in boot (DC 10)"},
    "cooks_utensils": {"name": "Cook's Utensils", "type": "artisan_tools", "cost": "1 GP", "weight_lb": 8, "ability": "wisdom", "utilize": "Improve rest recovery (+1 HP per Hit Die)"},
    "glassblowers_tools": {"name": "Glassblower's Tools", "type": "artisan_tools", "cost": "30 GP", "weight_lb": 5, "ability": "dexterity", "utilize": "Identify glass (DC 10)"},
    "jewelers_tools": {"name": "Jeweler's Tools", "type": "artisan_tools", "cost": "25 GP", "weight_lb": 2, "ability": "dexterity", "utilize": "Appraise gem value (DC 15)"},
    "leatherworkers_tools": {"name": "Leatherworker's Tools", "type": "artisan_tools", "cost": "5 GP", "weight_lb": 5, "ability": "dexterity", "utilize": "Craft or patch leather (DC 10)"},
    "masons_tools": {"name": "Mason's Tools", "type": "artisan_tools", "cost": "10 GP", "weight_lb": 8, "ability": "strength", "utilize": "Chisel stone / find weak point (DC 15)"},
    "painters_supplies": {"name": "Painter's Supplies", "type": "artisan_tools", "cost": "10 GP", "weight_lb": 5, "ability": "dexterity", "utilize": "Paint portrait or symbol (DC 10)"},
    "potters_tools": {"name": "Potter's Tools", "type": "artisan_tools", "cost": "10 GP", "weight_lb": 3, "ability": "dexterity", "utilize": "Examine clay/ceramic (DC 10)"},
    "smiths_tools": {"name": "Smith's Tools", "type": "artisan_tools", "cost": "20 GP", "weight_lb": 8, "ability": "strength", "utilize": "Repair metal weapon or armor (DC 15)"},
    "tinkers_tools": {"name": "Tinker's Tools", "type": "artisan_tools", "cost": "50 GP", "weight_lb": 10, "ability": "dexterity", "utilize": "Mend clockwork / construct small device (DC 15)"},
    "weavers_tools": {"name": "Weaver's Tools", "type": "artisan_tools", "cost": "1 GP", "weight_lb": 5, "ability": "dexterity", "utilize": "Repair cloth/tapestry (DC 10)"},
    "woodcarvers_tools": {"name": "Woodcarver's Tools", "type": "artisan_tools", "cost": "1 GP", "weight_lb": 5, "ability": "dexterity", "utilize": "Carve wooden figurine or weapon (DC 10)"},
    # Other Tools
    "disguise_kit": {"name": "Disguise Kit", "type": "tool", "cost": "25 GP", "weight_lb": 3, "ability": "charisma", "utilize": "Create visual disguise (DC 10-15)"},
    "forgery_kit": {"name": "Forgery Kit", "type": "tool", "cost": "15 GP", "weight_lb": 5, "ability": "dexterity", "utilize": "Forge document or wax seal (DC 15)"},
    "herbalism_kit": {"name": "Herbalism Kit", "type": "tool", "cost": "5 GP", "weight_lb": 3, "ability": "wisdom", "utilize": "Identify plants / brew Potion of Healing (DC 15)"},
    "navigators_tools": {"name": "Navigator's Tools", "type": "tool", "cost": "25 GP", "weight_lb": 2, "ability": "wisdom", "utilize": "Determine course by stars / avoid getting lost (DC 15)"},
    "poisoners_kit": {"name": "Poisoner's Kit", "type": "tool", "cost": "50 GP", "weight_lb": 2, "ability": "intelligence", "utilize": "Harvest or craft poison (DC 15)"},
    "thieves_tools": {"name": "Thieves' Tools", "type": "tool", "cost": "25 GP", "weight_lb": 1, "ability": "dexterity", "utilize": "Pick a lock (DC 15) or disarm a trap (DC 15)"},
    # Adventuring Gear (Essential Core)
    "backpack": {"name": "Backpack", "type": "gear", "cost": "2 GP", "weight_lb": 5, "capacity_lb": 30},
    "bedroll": {"name": "Bedroll", "type": "gear", "cost": "1 GP", "weight_lb": 7},
    "crowbar": {"name": "Crowbar", "type": "gear", "cost": "2 GP", "weight_lb": 5, "description": "Grants Advantage on Strength checks where leverage applies."},
    "grappling_hook": {"name": "Grappling Hook", "type": "gear", "cost": "2 GP", "weight_lb": 4},
    "healers_kit": {"name": "Healer's Kit", "type": "gear", "cost": "5 GP", "weight_lb": 3, "uses": 10, "description": "Stabilize an unconscious creature at 0 HP without Medicine check."},
    "holy_symbol": {"name": "Holy Symbol", "type": "spellcasting_focus", "cost": "5 GP", "weight_lb": 1},
    "arcane_focus": {"name": "Arcane Focus", "type": "spellcasting_focus", "cost": "10 GP", "weight_lb": 1},
    "druidic_focus": {"name": "Druidic Focus", "type": "spellcasting_focus", "cost": "1 GP", "weight_lb": 1},
    "component_pouch": {"name": "Component Pouch", "type": "gear", "cost": "25 GP", "weight_lb": 2},
    "lantern_hooded": {"name": "Hooded Lantern", "type": "gear", "cost": "5 GP", "weight_lb": 2, "light": "30ft bright, 30ft dim"},
    "oil_flask": {"name": "Oil (Flask)", "type": "gear", "cost": "1 SP", "weight_lb": 1},
    "potion_of_healing": {"name": "Potion of Healing", "type": "potion", "cost": "50 GP", "weight_lb": 0.5, "healing": "2d4+2", "action": "Bonus Action to drink or Action to administer"},
    "rations_1_day": {"name": "Rations (1 Day)", "type": "gear", "cost": "5 SP", "weight_lb": 2},
    "rope_hempen_50ft": {"name": "Rope, Hempen (50 feet)", "type": "gear", "cost": "1 GP", "weight_lb": 10},
    "rope_silk_50ft": {"name": "Rope, Silk (50 feet)", "type": "gear", "cost": "10 GP", "weight_lb": 5},
    "spellbook": {"name": "Spellbook", "type": "gear", "cost": "50 GP", "weight_lb": 3},
    "tinderbox": {"name": "Tinderbox", "type": "gear", "cost": "5 SP", "weight_lb": 1},
    "torch": {"name": "Torch", "type": "gear", "cost": "1 CP", "weight_lb": 1, "light": "20ft bright, 20ft dim for 1 hour"},
    "waterskin": {"name": "Waterskin", "type": "gear", "cost": "2 SP", "weight_lb": 5}
}


def run():
    rules_dir = ROOT / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    
    with open(rules_dir / "weapons.json", "w", encoding="utf-8") as f:
        json.dump(WEAPONS_2024, f, indent=2)
    print(f"Saved {len(WEAPONS_2024)} weapons to rules/weapons.json")

    with open(rules_dir / "armor.json", "w", encoding="utf-8") as f:
        json.dump(ARMOR_2024, f, indent=2)
    print(f"Saved {len(ARMOR_2024)} armor/shield items to rules/armor.json")

    with open(rules_dir / "equipment.json", "w", encoding="utf-8") as f:
        json.dump(EQUIPMENT_2024, f, indent=2)
    print(f"Saved {len(EQUIPMENT_2024)} tools & equipment to rules/equipment.json")


if __name__ == "__main__":
    run()
