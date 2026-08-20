"""
Extractor for Part 4: Character Classes & Progression (Chapter 3).
Creates rules/classes.json, rules/subclasses.json, and rules/progression.json based on PHB 2024.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

CLASSES_2024 = {
    "barbarian": {
        "name": "Barbarian",
        "hit_die": "d12",
        "primary_ability": ["strength"],
        "saving_throws": ["strength", "constitution"],
        "armor_training": ["light", "medium", "shields"],
        "weapon_training": ["simple", "martial"],
        "weapon_mastery_slots": 2,
        "spellcaster": False,
        "features_by_level": {
            "1": ["Rage", "Unarmored Defense", "Weapon Mastery (2)"],
            "2": ["Danger Sense", "Reckless Attack"],
            "3": ["Barbarian Subclass", "Primal Knowledge"],
            "4": ["Ability Score Improvement"],
            "5": ["Extra Attack", "Fast Movement"],
            "6": ["Subclass Feature"],
            "7": ["Feral Instinct", "Instinctive Pounce"],
            "8": ["Ability Score Improvement"],
            "9": ["Brutal Strike"],
            "10": ["Subclass Feature"],
            "11": ["Relentless Rage"],
            "12": ["Ability Score Improvement"],
            "13": ["Improved Brutal Strike"],
            "14": ["Subclass Feature"],
            "15": ["Persistent Rage"],
            "16": ["Ability Score Improvement"],
            "17": ["Brutal Strike Upgrade"],
            "18": ["Indomitable Might"],
            "19": ["Epic Boon"],
            "20": ["Primal Champion"]
        }
    },
    "bard": {
        "name": "Bard",
        "hit_die": "d8",
        "primary_ability": ["charisma"],
        "saving_throws": ["dexterity", "charisma"],
        "armor_training": ["light"],
        "weapon_training": ["simple"],
        "weapon_mastery_slots": 0,
        "spellcaster": True,
        "spellcasting_ability": "charisma",
        "features_by_level": {
            "1": ["Spellcasting", "Bardic Inspiration (d6)"],
            "2": ["Expertise", "Jack of All Trades"],
            "3": ["Bard College Subclass"],
            "4": ["Ability Score Improvement"],
            "5": ["Bardic Inspiration (d8)", "Font of Inspiration"],
            "6": ["Countercharm", "Subclass Feature"],
            "7": ["Level 4 Spells"],
            "8": ["Ability Score Improvement"],
            "9": ["Level 5 Spells"],
            "10": ["Bardic Inspiration (d10)", "Magical Secrets"],
            "11": ["Level 6 Spells"],
            "12": ["Ability Score Improvement"],
            "13": ["Level 7 Spells"],
            "14": ["Subclass Feature"],
            "15": ["Bardic Inspiration (d12)"],
            "16": ["Ability Score Improvement"],
            "17": ["Level 9 Spells"],
            "18": ["Superior Inspiration"],
            "19": ["Epic Boon"],
            "20": ["Words of Creation"]
        }
    },
    "cleric": {
        "name": "Cleric",
        "hit_die": "d8",
        "primary_ability": ["wisdom"],
        "saving_throws": ["wisdom", "charisma"],
        "armor_training": ["light", "medium", "shields"],
        "weapon_training": ["simple"],
        "weapon_mastery_slots": 0,
        "spellcaster": True,
        "spellcasting_ability": "wisdom",
        "features_by_level": {
            "1": ["Spellcasting", "Divine Order (Protector or Thaumaturge)"],
            "2": ["Channel Divinity", "Divine Spark", "Turn Undead"],
            "3": ["Cleric Domain Subclass"],
            "4": ["Ability Score Improvement"],
            "5": ["Smite Undead"],
            "6": ["Subclass Feature"],
            "7": ["Blessed Strikes"],
            "8": ["Ability Score Improvement"],
            "9": ["Level 5 Spells"],
            "10": ["Divine Intervention"],
            "11": ["Level 6 Spells"],
            "12": ["Ability Score Improvement"],
            "13": ["Level 7 Spells"],
            "14": ["Improved Blessed Strikes"],
            "15": ["Level 8 Spells"],
            "16": ["Ability Score Improvement"],
            "17": ["Subclass Feature"],
            "18": ["Level 9 Spells"],
            "19": ["Epic Boon"],
            "20": ["Greater Divine Intervention"]
        }
    },
    "druid": {
        "name": "Druid",
        "hit_die": "d8",
        "primary_ability": ["wisdom"],
        "saving_throws": ["intelligence", "wisdom"],
        "armor_training": ["light", "shields"],
        "weapon_training": ["simple"],
        "weapon_mastery_slots": 0,
        "spellcaster": True,
        "spellcasting_ability": "wisdom",
        "features_by_level": {
            "1": ["Spellcasting", "Druidic", "Primal Order (Magician or Warden)"],
            "2": ["Wild Companion", "Wild Shape"],
            "3": ["Druid Circle Subclass"],
            "4": ["Ability Score Improvement"],
            "5": ["Wild Resurgence"],
            "6": ["Subclass Feature"],
            "7": ["Elemental Fury"],
            "8": ["Ability Score Improvement"],
            "9": ["Level 5 Spells"],
            "10": ["Subclass Feature"],
            "11": ["Level 6 Spells"],
            "12": ["Ability Score Improvement"],
            "13": ["Level 7 Spells"],
            "14": ["Subclass Feature"],
            "15": ["Improved Elemental Fury"],
            "16": ["Ability Score Improvement"],
            "17": ["Level 9 Spells"],
            "18": ["Beast Spells"],
            "19": ["Epic Boon"],
            "20": ["Archdruid"]
        }
    },
    "fighter": {
        "name": "Fighter",
        "hit_die": "d10",
        "primary_ability": ["strength", "constitution", "dexterity"],
        "saving_throws": ["strength", "constitution"],
        "armor_training": ["light", "medium", "heavy", "shields"],
        "weapon_training": ["simple", "martial"],
        "weapon_mastery_slots": 3,
        "spellcaster": False,
        "features_by_level": {
            "1": ["Fighting Style", "Second Wind", "Weapon Mastery (3)"],
            "2": ["Action Surge", "Tactical Mind"],
            "3": ["Fighter Archetype Subclass"],
            "4": ["Ability Score Improvement"],
            "5": ["Extra Attack", "Tactical Shift"],
            "6": ["Ability Score Improvement"],
            "7": ["Subclass Feature"],
            "8": ["Ability Score Improvement"],
            "9": ["Indomitable", "Tactical Master"],
            "10": ["Subclass Feature"],
            "11": ["Two Extra Attacks"],
            "12": ["Ability Score Improvement"],
            "13": ["Improved Indomitable"],
            "14": ["Ability Score Improvement"],
            "15": ["Subclass Feature"],
            "16": ["Ability Score Improvement"],
            "17": ["Action Surge (2 uses)", "Indomitable (3 uses)"],
            "18": ["Subclass Feature"],
            "19": ["Epic Boon"],
            "20": ["Three Extra Attacks"]
        }
    },
    "monk": {
        "name": "Monk",
        "hit_die": "d8",
        "primary_ability": ["dexterity", "wisdom"],
        "saving_throws": ["strength", "dexterity"],
        "armor_training": [],
        "weapon_training": ["simple", "martial_light"],
        "weapon_mastery_slots": 0,
        "spellcaster": False,
        "features_by_level": {
            "1": ["Martial Arts (d6)", "Unarmored Defense"],
            "2": ["Monk's Focus (Flurry of Blows, Patient Defense, Step of the Wind)", "Unarmored Movement", "Uncanny Metabolism"],
            "3": ["Deflect Attacks", "Monk Subclass"],
            "4": ["Ability Score Improvement", "Slow Fall"],
            "5": ["Extra Attack", "Martial Arts (d8)", "Stunning Strike"],
            "6": ["Empowered Strikes", "Subclass Feature"],
            "7": ["Evasion"],
            "8": ["Ability Score Improvement"],
            "9": ["Acrobatic Movement"],
            "10": ["Heightened Focus", "Self-Restoration"],
            "11": ["Martial Arts (d10)", "Subclass Feature"],
            "12": ["Ability Score Improvement"],
            "13": ["Deflect Energy"],
            "14": ["Disciplined Survivor"],
            "15": ["Perfect Focus"],
            "16": ["Ability Score Improvement"],
            "17": ["Martial Arts (d12)", "Subclass Feature"],
            "18": ["Superior Defense"],
            "19": ["Epic Boon"],
            "20": ["Body and Mind"]
        }
    },
    "paladin": {
        "name": "Paladin",
        "hit_die": "d10",
        "primary_ability": ["strength", "charisma"],
        "saving_throws": ["wisdom", "charisma"],
        "armor_training": ["light", "medium", "heavy", "shields"],
        "weapon_training": ["simple", "martial"],
        "weapon_mastery_slots": 2,
        "spellcaster": True,
        "spellcasting_ability": "charisma",
        "features_by_level": {
            "1": ["Lay on Hands", "Spellcasting", "Weapon Mastery (2)"],
            "2": ["Fighting Style", "Paladin's Smite"],
            "3": ["Channel Divinity", "Paladin Sacred Oath Subclass"],
            "4": ["Ability Score Improvement"],
            "5": ["Extra Attack", "Faithful Steed (Find Steed)"],
            "6": ["Aura of Protection"],
            "7": ["Subclass Feature"],
            "8": ["Ability Score Improvement"],
            "9": ["Abjure Foes"],
            "10": ["Aura of Courage"],
            "11": ["Radiant Strikes"],
            "12": ["Ability Score Improvement"],
            "13": ["Level 4 Spells"],
            "14": ["Restoring Touch"],
            "15": ["Subclass Feature"],
            "16": ["Ability Score Improvement"],
            "17": ["Level 5 Spells"],
            "18": ["Aura Expansion"],
            "19": ["Epic Boon"],
            "20": ["Subclass Capstone"]
        }
    },
    "ranger": {
        "name": "Ranger",
        "hit_die": "d10",
        "primary_ability": ["dexterity", "wisdom"],
        "saving_throws": ["strength", "dexterity"],
        "armor_training": ["light", "medium", "shields"],
        "weapon_training": ["simple", "martial"],
        "weapon_mastery_slots": 2,
        "spellcaster": True,
        "spellcasting_ability": "wisdom",
        "features_by_level": {
            "1": ["Favored Enemy (Hunter's Mark)", "Spellcasting", "Weapon Mastery (2)"],
            "2": ["Deft Explorer (Expertise)", "Fighting Style"],
            "3": ["Ranger Subclass"],
            "4": ["Ability Score Improvement"],
            "5": ["Extra Attack"],
            "6": ["Roving", "Subclass Feature"],
            "7": ["Subclass Feature"],
            "8": ["Ability Score Improvement"],
            "9": ["Level 3 Spells"],
            "10": ["Tireless"],
            "11": ["Subclass Feature"],
            "12": ["Ability Score Improvement"],
            "13": ["Level 4 Spells"],
            "14": ["Nature's Veil"],
            "15": ["Subclass Feature"],
            "16": ["Ability Score Improvement"],
            "17": ["Level 5 Spells"],
            "18": ["Feral Senses"],
            "19": ["Epic Boon"],
            "20": ["Foe Slayer"]
        }
    },
    "rogue": {
        "name": "Rogue",
        "hit_die": "d8",
        "primary_ability": ["dexterity"],
        "saving_throws": ["dexterity", "intelligence"],
        "armor_training": ["light"],
        "weapon_training": ["simple", "martial_finesse_light"],
        "weapon_mastery_slots": 2,
        "spellcaster": False,
        "features_by_level": {
            "1": ["Expertise", "Sneak Attack (1d6)", "Thieves' Cant", "Weapon Mastery (2)"],
            "2": ["Cunning Action"],
            "3": ["Roguish Archetype Subclass", "Sneak Attack (2d6)"],
            "4": ["Ability Score Improvement"],
            "5": ["Cunning Strike", "Sneak Attack (3d6)", "Uncanny Dodge"],
            "6": ["Expertise (2 skills)"],
            "7": ["Evasion", "Reliable Talent", "Sneak Attack (4d6)"],
            "8": ["Ability Score Improvement"],
            "9": ["Sneak Attack (5d6)", "Subclass Feature"],
            "10": ["Ability Score Improvement"],
            "11": ["Improved Cunning Strike", "Sneak Attack (6d6)"],
            "12": ["Ability Score Improvement"],
            "13": ["Sneak Attack (7d6)", "Subclass Feature"],
            "14": ["Devious Strikes"],
            "15": ["Sneak Attack (8d6)", "Slippery Mind"],
            "16": ["Ability Score Improvement"],
            "17": ["Sneak Attack (9d6)", "Subclass Feature"],
            "18": ["Elusive"],
            "19": ["Epic Boon"],
            "20": ["Sneak Attack (10d6)", "Stroke of Luck"]
        }
    },
    "sorcerer": {
        "name": "Sorcerer",
        "hit_die": "d6",
        "primary_ability": ["charisma"],
        "saving_throws": ["constitution", "charisma"],
        "armor_training": [],
        "weapon_training": ["simple"],
        "weapon_mastery_slots": 0,
        "spellcaster": True,
        "spellcasting_ability": "charisma",
        "features_by_level": {
            "1": ["Innate Sorcery", "Spellcasting"],
            "2": ["Font of Magic (Sorcery Points)", "Metamagic"],
            "3": ["Sorcerous Origin Subclass"],
            "4": ["Ability Score Improvement"],
            "5": ["Sorcerous Restoration"],
            "6": ["Subclass Feature"],
            "7": ["Sorcery Incarnate"],
            "8": ["Ability Score Improvement"],
            "9": ["Level 5 Spells"],
            "10": ["Metamagic (1 additional)"],
            "11": ["Level 6 Spells"],
            "12": ["Ability Score Improvement"],
            "13": ["Level 7 Spells"],
            "14": ["Subclass Feature"],
            "15": ["Level 8 Spells"],
            "16": ["Ability Score Improvement"],
            "17": ["Metamagic (1 additional)", "Level 9 Spells"],
            "18": ["Subclass Feature"],
            "19": ["Epic Boon"],
            "20": ["Arcane Apotheosis"]
        }
    },
    "warlock": {
        "name": "Warlock",
        "hit_die": "d8",
        "primary_ability": ["charisma"],
        "saving_throws": ["wisdom", "charisma"],
        "armor_training": ["light"],
        "weapon_training": ["simple"],
        "weapon_mastery_slots": 0,
        "spellcaster": True,
        "spellcasting_ability": "charisma",
        "features_by_level": {
            "1": ["Eldritch Invocations (1)", "Pact Magic"],
            "2": ["Eldritch Invocations (3)", "Magical Cunning"],
            "3": ["Otherworldly Patron Subclass"],
            "4": ["Ability Score Improvement"],
            "5": ["Eldritch Invocations (5)"],
            "6": ["Subclass Feature"],
            "7": ["Eldritch Invocations (6)"],
            "8": ["Ability Score Improvement"],
            "9": ["Contact Patron", "Eldritch Invocations (7)"],
            "10": ["Subclass Feature"],
            "11": ["Mystic Arcanum (Level 6)"],
            "12": ["Ability Score Improvement", "Eldritch Invocations (8)"],
            "13": ["Mystic Arcanum (Level 7)"],
            "14": ["Subclass Feature"],
            "15": ["Mystic Arcanum (Level 8)", "Eldritch Invocations (9)"],
            "16": ["Ability Score Improvement"],
            "17": ["Mystic Arcanum (Level 9)"],
            "18": ["Eldritch Invocations (10)"],
            "19": ["Epic Boon"],
            "20": ["Eldritch Master"]
        }
    },
    "wizard": {
        "name": "Wizard",
        "hit_die": "d6",
        "primary_ability": ["intelligence"],
        "saving_throws": ["intelligence", "wisdom"],
        "armor_training": [],
        "weapon_training": ["dagger", "dart", "sling", "quarterstaff", "light_crossbow"],
        "weapon_mastery_slots": 0,
        "spellcaster": True,
        "spellcasting_ability": "intelligence",
        "features_by_level": {
            "1": ["Arcane Recovery", "Ritual Adept", "Spellcasting", "Spellbook"],
            "2": ["Scholar (Expertise in academic skill)"],
            "3": ["Arcane Tradition Subclass"],
            "4": ["Ability Score Improvement"],
            "5": ["Memorize Spell"],
            "6": ["Subclass Feature"],
            "7": ["Level 4 Spells"],
            "8": ["Ability Score Improvement"],
            "9": ["Level 5 Spells"],
            "10": ["Subclass Feature"],
            "11": ["Level 6 Spells"],
            "12": ["Ability Score Improvement"],
            "13": ["Level 7 Spells"],
            "14": ["Subclass Feature"],
            "15": ["Level 8 Spells"],
            "16": ["Ability Score Improvement"],
            "17": ["Level 9 Spells"],
            "18": ["Spell Mastery"],
            "19": ["Epic Boon"],
            "20": ["Signature Spells"]
        }
    }
}

SUBCLASSES_2024 = {
    # Barbarian
    "path_of_the_berserker": {"class": "barbarian", "name": "Path of the Berserker", "features": ["Frenzy", "Mindless Rage", "Retaliation", "Intimidating Presence"]},
    "path_of_the_wild_heart": {"class": "barbarian", "name": "Path of the Wild Heart", "features": ["Rage of the Wilds", "Aspect of the Wilds", "Nature Speaker", "Power of the Wilds"]},
    "path_of_the_world_tree": {"class": "barbarian", "name": "Path of the World Tree", "features": ["Vitality of the Tree", "Branches of the Tree", "Battering Roots", "Travel Along the Tree"]},
    "path_of_the_zealot": {"class": "barbarian", "name": "Path of the Zealot", "features": ["Divine Fury", "Warrior of the Gods", "Fanatical Focus", "Zealous Presence", "Rage of the Gods"]},
    # Bard
    "college_of_dance": {"class": "bard", "name": "College of Dance", "features": ["Dazzling Footwork", "Inspiring Movement", "Tandem Footwork", "Leading Edge"]},
    "college_of_glamour": {"class": "bard", "name": "College of Glamour", "features": ["Beguiling Magic", "Mantle of Inspiration", "Mantle of Majesty", "Unbreakable Majesty"]},
    "college_of_lore": {"class": "bard", "name": "College of Lore", "features": ["Bonus Proficiencies (3 skills)", "Cutting Words", "Additional Magical Secrets", "Peerless Skill"]},
    "college_of_valor": {"class": "bard", "name": "College of Valor", "features": ["Combat Inspiration", "Martial Training (Medium Armor, Shields, Martial Weapons)", "Extra Attack", "Battle Magic"]},
    # Cleric
    "life_domain": {"class": "cleric", "name": "Life Domain", "features": ["Disciple of Life", "Domain Spells", "Preserve Life", "Blessed Healer", "Supreme Healing"]},
    "light_domain": {"class": "cleric", "name": "Light Domain", "features": ["Domain Spells", "Radiance of the Dawn", "Warding Flare", "Improved Warding Flare", "Corona of Light"]},
    "trickery_domain": {"class": "cleric", "name": "Trickery Domain", "features": ["Blessing of the Trickster", "Domain Spells", "Invoke Duplicity", "Trickster's Magic", "Improved Duplicity"]},
    "war_domain": {"class": "cleric", "name": "War Domain", "features": ["Domain Spells", "War Priest", "Guided Strike", "War God's Blessing", "Avatar of Battle"]},
    # Fighter
    "battle_master": {"class": "fighter", "name": "Battle Master", "features": ["Combat Superiority (Maneuvers: Trip, Push, Riposte, Menacing, Precision)", "Student of War", "Know Your Enemy", "Relentless"]},
    "champion": {"class": "fighter", "name": "Champion", "features": ["Improved Critical (19-20)", "Remarkable Athlete", "Heroic Warrior (Heroic Inspiration every turn)", "Superior Critical (18-20)", "Survivor"]},
    "eldritch_knight": {"class": "fighter", "name": "Eldritch Knight", "features": ["Weapon Bond", "Wizard Spellcasting", "War Magic", "Arcane Charge", "Improved War Magic"]},
    "psi_warrior": {"class": "fighter", "name": "Psi Warrior", "features": ["Psionic Power (Protective Field, Psionic Strike, Telekinetic Movement)", "Psi-Powered Leap", "Telekinetic Thrust", "Guarded Mind", "Bulwark of Force", "Telekinetic Master"]},
    # Rogue
    "arcane_trickster": {"class": "rogue", "name": "Arcane Trickster", "features": ["Mage Hand Legerdemain", "Wizard Spellcasting", "Magical Ambush", "Versatile Trickster", "Spell Thief"]},
    "assassin": {"class": "rogue", "name": "Assassin", "features": ["Assassinate (Advantage & bonus damage on round 1)", "Assassin's Tools", "Infiltration Expertise", "Envenom Weapons", "Death Strike"]},
    "soulknife": {"class": "rogue", "name": "Soulknife", "features": ["Psionic Power", "Psychic Blades", "Soul Blades (Homing Strikes, Telepathic Teleport)", "Psychic Veil", "Rend Mind"]},
    "thief": {"class": "rogue", "name": "Thief", "features": ["Fast Hands (Utilize/Magic Item as Bonus Action)", "Second-Story Work", "Supreme Sneak", "Use Magic Device", "Thief's Reflexes (2 turns in round 1)"]},
    # Wizard
    "abjurer": {"class": "wizard", "name": "School of Abjuration", "features": ["Abjuration Savant", "Arcane Ward", "Projected Ward", "Spell Breaker", "Spell Resistance"]},
    "diviner": {"class": "wizard", "name": "School of Divination", "features": ["Divination Savant", "Portent", "Expert Divination", "The Third Eye", "Greater Portent"]},
    "evoker": {"class": "wizard", "name": "School of Evocation", "features": ["Evocation Savant", "Sculpt Spells", "Potent Cantrip", "Empowered Evocation", "Overchannel"]},
    "illusionist": {"class": "wizard", "name": "School of Illusion", "features": ["Illusion Savant", "Improved Minor Illusion", "Malleable Illusions", "Phantasmal Creatures", "Illusory Self"]}
}

PROGRESSION_2024 = {
    "xp_by_level": {
        "1": 0, "2": 300, "3": 900, "4": 2700, "5": 6500, "6": 14000,
        "7": 23000, "8": 34000, "9": 48000, "10": 64000, "11": 85000,
        "12": 100000, "13": 120000, "14": 140000, "15": 165000,
        "16": 195000, "17": 225000, "18": 265000, "19": 305000, "20": 355000
    },
    "proficiency_bonus_by_level": {
        "1": 2, "2": 2, "3": 2, "4": 2,
        "5": 3, "6": 3, "7": 3, "8": 3,
        "9": 4, "10": 4, "11": 4, "12": 4,
        "13": 5, "14": 5, "15": 5, "16": 5,
        "17": 6, "18": 6, "19": 6, "20": 6
    },
    "full_caster_spell_slots": {
        "1": {"1": 2},
        "2": {"1": 3},
        "3": {"1": 4, "2": 2},
        "4": {"1": 4, "2": 3},
        "5": {"1": 4, "2": 3, "3": 2},
        "6": {"1": 4, "2": 3, "3": 3},
        "7": {"1": 4, "2": 3, "3": 3, "4": 1},
        "8": {"1": 4, "2": 3, "3": 3, "4": 2},
        "9": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 1},
        "10": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2},
        "11": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2, "6": 1},
        "12": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2, "6": 1},
        "13": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2, "6": 1, "7": 1},
        "14": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2, "6": 1, "7": 1},
        "15": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2, "6": 1, "7": 1, "8": 1},
        "16": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2, "6": 1, "7": 1, "8": 1},
        "17": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 2, "6": 1, "7": 1, "8": 1, "9": 1},
        "18": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 3, "6": 1, "7": 1, "8": 1, "9": 1},
        "19": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 3, "6": 2, "7": 1, "8": 1, "9": 1},
        "20": {"1": 4, "2": 3, "3": 3, "4": 3, "5": 3, "6": 2, "7": 2, "8": 1, "9": 1}
    }
}


def run():
    rules_dir = ROOT / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    
    with open(rules_dir / "classes.json", "w", encoding="utf-8") as f:
        json.dump(CLASSES_2024, f, indent=2)
    print(f"Saved {len(CLASSES_2024)} classes to rules/classes.json")

    with open(rules_dir / "subclasses.json", "w", encoding="utf-8") as f:
        json.dump(SUBCLASSES_2024, f, indent=2)
    print(f"Saved {len(SUBCLASSES_2024)} subclasses to rules/subclasses.json")

    with open(rules_dir / "progression.json", "w", encoding="utf-8") as f:
        json.dump(PROGRESSION_2024, f, indent=2)
    print(f"Saved level progression rules to rules/progression.json")


if __name__ == "__main__":
    run()
