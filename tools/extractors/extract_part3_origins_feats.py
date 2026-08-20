"""
Extractor for Part 3: Character Origins (Backgrounds, Species, and Feats).
Creates rules/backgrounds.json, rules/species.json, and rules/feats.json based on PHB 2024.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

BACKGROUNDS_2024 = {
    "acolyte": {
        "name": "Acolyte",
        "feature": "Shelter of the Faithful",
        "ability_scores": ["intelligence", "wisdom", "charisma"],
        "feat": "Magic Initiate (Cleric)",
        "skill_proficiencies": ["insight", "religion"],
        "tool_proficiency": "Calligrapher's Supplies",
        "equipment": ["Calligrapher's Supplies", "Book (prayers)", "Holy Symbol", "Parchment (10 sheets)", "Robe", "8 GP"],
        "description": "You devoted yourself to service in a temple, shrine, or monastery, learning sacred rites and theological wisdom."
    },
    "artisan": {
        "name": "Artisan",
        "feature": "Guild Membership",
        "ability_scores": ["strength", "dexterity", "intelligence"],
        "feat": "Crafter",
        "skill_proficiencies": ["investigation", "persuasion"],
        "tool_proficiency": "Artisan's Tools (one of choice)",
        "equipment": ["Artisan's Tools", "Abacus", "Pouch", "Traveler's Clothes", "25 GP"],
        "description": "You began apprenticing at a young age, mastering a craft and learning how business and guild politics work."
    },
    "charlatan": {
        "name": "Charlatan",
        "feature": "False Identity",
        "ability_scores": ["dexterity", "constitution", "charisma"],
        "feat": "Skilled",
        "skill_proficiencies": ["deception", "sleight_of_hand"],
        "tool_proficiency": "Forgery Kit",
        "equipment": ["Forgery Kit", "Costume", "Pouch", "Fine Clothes", "15 GP"],
        "description": "You mastered deception, adopting false identities, sleight of hand, and confidence games to get ahead."
    },
    "criminal": {
        "name": "Criminal",
        "feature": "Criminal Contact",
        "ability_scores": ["dexterity", "constitution", "intelligence"],
        "feat": "Alert",
        "skill_proficiencies": ["sleight_of_hand", "stealth"],
        "tool_proficiency": "Thieves' Tools",
        "equipment": ["2 Daggers", "Thieves' Tools", "Crowbar", "Pouch", "Traveler's Clothes", "16 GP"],
        "description": "You learned to survive on the wrong side of the law, navigating shadows, locks, and underworld contacts."
    },
    "cultist": {
        "name": "Cultist",
        "feature": "Cult Secrets",
        "ability_scores": ["intelligence", "wisdom", "charisma"],
        "feat": "Magic Initiate (Warlock)",
        "skill_proficiencies": ["arcana", "religion"],
        "tool_proficiency": "Disguise Kit",
        "equipment": ["Dagger", "Disguise Kit", "Robes", "Occult Symbol", "19 GP"],
        "description": "You were initiated into a secretive cult dedicated to an otherworldly entity or dark power."
    },
    "entertainer": {
        "name": "Entertainer",
        "feature": "By Popular Demand",
        "ability_scores": ["strength", "dexterity", "charisma"],
        "feat": "Musician",
        "skill_proficiencies": ["acrobatics", "performance"],
        "tool_proficiency": "Musical Instrument (one of choice)",
        "equipment": ["Musical Instrument", "Costume", "Mirror (steel)", "Perfume", "8 GP"],
        "description": "You thrive in front of an audience, captivating crowds with song, dance, storytelling, or acrobatics."
    },
    "farmer": {
        "name": "Farmer",
        "feature": "Rustic Hospitality",
        "ability_scores": ["strength", "constitution", "wisdom"],
        "feat": "Tough",
        "skill_proficiencies": ["animal_handling", "nature"],
        "tool_proficiency": "Carpenter's Tools",
        "equipment": ["Sickle", "Carpenter's Tools", "Healer's Kit", "Iron Pot", "Shovel", "Traveler's Clothes", "23 GP"],
        "description": "You grew up working the soil and caring for livestock, developing rugged endurance and practical skills."
    },
    "guard": {
        "name": "Guard",
        "feature": "Watcher's Eye",
        "ability_scores": ["strength", "intelligence", "wisdom"],
        "feat": "Alert",
        "skill_proficiencies": ["athletics", "perception"],
        "tool_proficiency": "Gaming Set (one of choice)",
        "equipment": ["Spear", "Light Crossbow", "20 Crossbow Bolts", "Gaming Set", "Manacles", "Traveler's Clothes", "12 GP"],
        "description": "You served as a sentry, city watch officer, or bodyguard, keeping keen eyes on doors, crowds, and perimeter walls."
    },
    "guide": {
        "name": "Guide",
        "feature": "Wanderer",
        "ability_scores": ["dexterity", "constitution", "wisdom"],
        "feat": "Magic Initiate (Druid)",
        "skill_proficiencies": ["stealth", "survival"],
        "tool_proficiency": "Cartographer's Tools",
        "equipment": ["Shortbow", "20 Arrows", "Cartographer's Tools", "Bedroll", "Tent", "Traveler's Clothes", "3 GP"],
        "description": "You learned the secrets of the untamed wilderness, navigating dangerous terrain, tracking game, and reading weather."
    },
    "hermit": {
        "name": "Hermit",
        "feature": "Discovery",
        "ability_scores": ["constitution", "wisdom", "charisma"],
        "feat": "Healer",
        "skill_proficiencies": ["medicine", "religion"],
        "tool_proficiency": "Herbalism Kit",
        "equipment": ["Quarterstaff", "Herbalism Kit", "Bedroll", "Book (philosophy)", "Traveler's Clothes", "15 GP"],
        "description": "You lived in secluded contemplation in nature or a monastery, seeking spiritual enlightenment and holistic cures."
    },
    "merchant": {
        "name": "Merchant",
        "feature": "Trade Routes",
        "ability_scores": ["constitution", "intelligence", "charisma"],
        "feat": "Lucky",
        "skill_proficiencies": ["animal_handling", "persuasion"],
        "tool_proficiency": "Navigator's Tools",
        "equipment": ["Navigator's Tools", "Pouch", "Traveler's Clothes", "Fine Clothes", "Letter of Introduction", "22 GP"],
        "description": "You bought and sold goods across trading hubs and caravan routes, learning negotiation and trade logistics."
    },
    "noble": {
        "name": "Noble",
        "feature": "Position of Privilege",
        "ability_scores": ["strength", "intelligence", "charisma"],
        "feat": "Skilled",
        "skill_proficiencies": ["history", "persuasion"],
        "tool_proficiency": "Gaming Set (one of choice)",
        "equipment": ["Gaming Set", "Fine Clothes", "Signet Ring", "Perfume", "Scroll of Pedigree", "29 GP"],
        "description": "You were born into privilege and political intrigue, trained in heraldry, etiquette, and high-society rhetoric."
    },
    "sage": {
        "name": "Sage",
        "feature": "Researcher",
        "ability_scores": ["constitution", "intelligence", "wisdom"],
        "feat": "Magic Initiate (Wizard)",
        "skill_proficiencies": ["arcana", "history"],
        "tool_proficiency": "Calligrapher's Supplies",
        "equipment": ["Quarterstaff", "Calligrapher's Supplies", "Book (history)", "Ink & Pen", "Parchment (8 sheets)", "8 GP"],
        "description": "You spent years studying dusty tomes, esoteric libraries, and academic theories in search of ancient knowledge."
    },
    "sailor": {
        "name": "Sailor",
        "feature": "Ship's Passage",
        "ability_scores": ["strength", "dexterity", "wisdom"],
        "feat": "Tavern Brawler",
        "skill_proficiencies": ["acrobatics", "perception"],
        "tool_proficiency": "Navigator's Tools",
        "equipment": ["Dagger", "Navigator's Tools", "Silk Rope (50ft)", "Lucky Charm", "Traveler's Clothes", "10 GP"],
        "description": "You grew up on the decks of merchant galleys, warships, or fishing smacks, weathering gales and sea monsters."
    },
    "scribe": {
        "name": "Scribe",
        "feature": "Archival Access",
        "ability_scores": ["dexterity", "intelligence", "wisdom"],
        "feat": "Skilled",
        "skill_proficiencies": ["investigation", "perception"],
        "tool_proficiency": "Calligrapher's Supplies",
        "equipment": ["Calligrapher's Supplies", "Fine Clothes", "Lamp", "Oil (flask)", "Parchment (10 sheets)", "23 GP"],
        "description": "You earned your living drafting official charters, translating scrolls, and maintaining civic records."
    },
    "soldier": {
        "name": "Soldier",
        "feature": "Military Rank",
        "ability_scores": ["strength", "dexterity", "constitution"],
        "feat": "Savage Attacker",
        "skill_proficiencies": ["athletics", "intimidation"],
        "tool_proficiency": "Gaming Set (one of choice)",
        "equipment": ["Spear", "Shortbow", "20 Arrows", "Gaming Set", "Healer's Kit", "Traveler's Clothes", "14 GP"],
        "description": "You were trained in military discipline and formation combat as part of an army, militia, or mercenary company."
    },
    "wayfarer": {
        "name": "Wayfarer",
        "feature": "City Secrets",
        "ability_scores": ["dexterity", "wisdom", "charisma"],
        "feat": "Lucky",
        "skill_proficiencies": ["insight", "stealth"],
        "tool_proficiency": "Thieves' Tools",
        "equipment": ["2 Daggers", "Thieves' Tools", "Gaming Set", "Bedroll", "Traveler's Clothes", "16 GP"],
        "description": "You grew up as an urchin or drifter on city streets, relying on quick wits, alleys, and luck to survive."
    }
}

SPECIES_2024 = {
    "aasimar": {
        "name": "Aasimar",
        "size": "Medium or Small",
        "speed": 30,
        "bonuses": {"charisma": 2, "wisdom": 1},
        "traits": [
            "Celestial Resistance: Resistance to Necrotic and Radiant damage.",
            "Darkvision: 60 feet.",
            "Healing Hands: As an Action, touch a creature and restore HP equal to a roll of d4s equal to your Proficiency Bonus (1/Long Rest).",
            "Light Bearer: You know the Light cantrip (Charisma).",
            "Celestial Revelation: At Level 3, transform as a Bonus Action for 1 minute (Heavenly Wings, Inner Radiance, or Necrotic Shroud, 1/Long Rest)."
        ]
    },
    "dragonborn": {
        "name": "Dragonborn",
        "size": "Medium",
        "speed": 30,
        "bonuses": {"strength": 2, "charisma": 1},
        "traits": [
            "Draconic Ancestry: Choose Black, Blue, Brass, Bronze, Copper, Gold, Green, Red, Silver, or White dragon ancestor.",
            "Breath Weapon: When you take the Attack action, replace one attack with a 15ft cone or 30ft line breath (Damage: 1d10 at lvl 1, 2d10 at lvl 5, 3d10 at lvl 11, 4d10 at lvl 17; uses = PB/Long Rest).",
            "Damage Resistance: Resistance to the damage type associated with your Draconic Ancestry.",
            "Darkvision: 60 feet.",
            "Draconic Flight: At Level 5, gain flying speed equal to your Speed for 10 minutes as a Bonus Action (1/Long Rest)."
        ]
    },
    "dwarf": {
        "name": "Dwarf",
        "size": "Medium",
        "speed": 30,
        "bonuses": {"constitution": 2},
        "traits": [
            "Darkvision: 120 feet.",
            "Dwarven Resilience: Resistance to Poison damage and Advantage on saving throws against the Poisoned condition.",
            "Dwarven Toughness: Your Hit Point maximum increases by 1 for each level you possess.",
            "Stonecunning: As a Bonus Action, gain Tremorsense with a range of 60 feet for 10 minutes while on stone surfaces (uses = PB/Long Rest)."
        ]
    },
    "hill_dwarf": {
        "name": "Hill Dwarf",
        "size": "Medium",
        "speed": 30,
        "bonuses": {"constitution": 2, "wisdom": 1},
        "traits": [
            "Darkvision: 120 feet.",
            "Dwarven Resilience: Resistance to Poison damage.",
            "Dwarven Toughness: Hit Point maximum increases by 1 per level."
        ]
    },
    "mountain_dwarf": {
        "name": "Mountain Dwarf",
        "size": "Medium",
        "speed": 30,
        "bonuses": {"strength": 2, "constitution": 2},
        "traits": [
            "Darkvision: 120 feet.",
            "Dwarven Resilience: Resistance to Poison damage.",
            "Dwarven Armor Training: Proficiency with light and medium armor."
        ]
    },
    "elf": {
        "name": "Elf",
        "size": "Medium",
        "speed": 30,
        "bonuses": {"dexterity": 2},
        "traits": [
            "Darkvision: 60 feet (120 feet for Drow).",
            "Elven Lineage: Choose Drow (Darkvision 120ft, Dancing Lights, Faerie Fire, Darkness), High Elf (Prestidigitation, Detect Magic, Misty Step), or Wood Elf (Speed 35ft, Druidcraft, Longstrider, Pass without Trace).",
            "Fey Ancestry: Advantage on saving throws against being Charmed.",
            "Keen Senses: Proficiency in the Perception skill.",
            "Trance: You don't need sleep. Finishing a Long Rest requires only 4 hours of restful meditation."
        ]
    },
    "high_elf": {
        "name": "High Elf",
        "size": "Medium",
        "speed": 30,
        "bonuses": {"dexterity": 2, "intelligence": 1},
        "traits": [
            "Darkvision: 60 feet.",
            "Fey Ancestry: Advantage on saving throws against being Charmed.",
            "Keen Senses: Perception proficiency.",
            "Cantrip: You know one cantrip from the wizard spell list (Prestidigitation)."
        ]
    },
    "wood_elf": {
        "name": "Wood Elf",
        "size": "Medium",
        "speed": 35,
        "bonuses": {"dexterity": 2, "wisdom": 1},
        "traits": [
            "Fleet of Foot: Base walking speed 35 feet.",
            "Mask of the Wild: Attempt to hide even when only lightly obscured.",
            "Keen Senses: Perception proficiency."
        ]
    },
    "drow": {
        "name": "Drow",
        "size": "Medium",
        "speed": 30,
        "bonuses": {"dexterity": 2, "charisma": 1},
        "traits": [
            "Superior Darkvision: 120 feet.",
            "Drow Magic: Dancing Lights cantrip; Faerie Fire and Darkness as you level up."
        ]
    },
    "gnome": {
        "name": "Gnome",
        "size": "Small",
        "speed": 30,
        "bonuses": {"intelligence": 2},
        "traits": [
            "Darkvision: 60 feet.",
            "Gnomish Cunning: Advantage on all Intelligence, Wisdom, and Charisma saving throws.",
            "Gnomish Lineage: Choose Forest Gnome (Minor Illusion, Speak with Animals) or Rock Gnome (Mending, Prestidigitation, Clockwork device creation)."
        ]
    },
    "forest_gnome": {
        "name": "Forest Gnome",
        "size": "Small",
        "speed": 30,
        "bonuses": {"intelligence": 2, "dexterity": 1},
        "traits": [
            "Natural Illusionist: Minor Illusion cantrip.",
            "Speak with Small Beasts: Communicate simple ideas with small beasts."
        ]
    },
    "rock_gnome": {
        "name": "Rock Gnome",
        "size": "Small",
        "speed": 30,
        "bonuses": {"intelligence": 2, "constitution": 1},
        "traits": [
            "Artificer's Lore: Add twice your PB to History checks related to magic items/devices.",
            "Tinker: Craft clockwork devices using tinker's tools."
        ]
    },
    "goliath": {
        "name": "Goliath",
        "size": "Medium",
        "speed": 35,
        "bonuses": {"strength": 2, "constitution": 1},
        "traits": [
            "Giant Ancestry: Choose Cloud (Misty Step PB/day), Fire (+1d10 fire dmg), Frost (+1d6 cold dmg & slow), Hill (knock prone on hit), Stone (reduce damage by 1d12+CON), or Storm (reaction 1d8 thunder dmg).",
            "Large Form: At Level 5, as a Bonus Action, you can transform to Large size for 10 minutes (Advantage on Strength checks, Speed +10ft, 1/Long Rest).",
            "Powerful Build: You count as one size larger when determining carrying capacity and weight you can push, drag, or lift."
        ]
    },
    "halfling": {
        "name": "Halfling",
        "size": "Small",
        "speed": 30,
        "bonuses": {"dexterity": 2},
        "traits": [
            "Brave: Advantage on saving throws against the Frightened condition.",
            "Halfling Nimbleness: You can move through the space of any creature that is of a size larger than yours.",
            "Lucky: When you roll a 1 on the d20 for a D20 Test, you can reroll the die and must use the new roll.",
            "Naturally Stealthy: You can take the Hide action even when obscured only by a creature at least one size larger than you."
        ]
    },
    "lightfoot_halfling": {
        "name": "Lightfoot Halfling",
        "size": "Small",
        "speed": 30,
        "bonuses": {"dexterity": 2, "charisma": 1},
        "traits": [
            "Naturally Stealthy: Hide when obscured by creature at least one size larger."
        ]
    },
    "human": {
        "name": "Human",
        "size": "Medium or Small",
        "speed": 30,
        "bonuses": {"strength": 1, "dexterity": 1, "constitution": 1, "intelligence": 1, "wisdom": 1, "charisma": 1},
        "traits": [
            "Resourceful: You gain Heroic Inspiration whenever you finish a Long Rest.",
            "Skillful: You gain proficiency in one skill of your choice.",
            "Versatile: You gain one Origin feat of your choice."
        ]
    },
    "orc": {
        "name": "Orc",
        "size": "Medium",
        "speed": 30,
        "bonuses": {"strength": 2, "constitution": 1},
        "traits": [
            "Adrenaline Rush: As a Bonus Action, take the Dash action and gain Temporary Hit Points equal to your Proficiency Bonus (uses = PB/Short or Long Rest).",
            "Darkvision: 120 feet.",
            "Relentless Endurance: When dropped to 0 HP but not killed outright, drop to 1 HP instead (1/Long Rest)."
        ]
    },
    "tiefling": {
        "name": "Tiefling",
        "size": "Medium or Small",
        "speed": 30,
        "bonuses": {"charisma": 2, "intelligence": 1},
        "traits": [
            "Darkvision: 60 feet.",
            "Fiendish Legacy: Choose Abyssal (Poison resistance, Poison Spray, Ray of Sickness, Hold Person), Chthonic (Necrotic resistance, Chill Touch, False Life, Ray of Enfeeblement), or Infernal (Fire resistance, Fire Bolt, Hellish Rebuke, Darkness).",
            "Otherworldly Presence: You know the Thaumaturgy cantrip (Charisma)."
        ]
    }
}

FEATS_2024 = {
    # Origin Feats (Level 1)
    "alert": {
        "name": "Alert",
        "category": "origin",
        "level_prereq": 1,
        "prerequisite": "None",
        "benefits": [
            "Initiative Proficiency: Add your Proficiency Bonus to your Initiative rolls.",
            "Initiative Swap: Immediately after you roll Initiative, you can swap your Initiative roll with the Initiative roll of one willing ally in the same combat."
        ]
    },
    "crafter": {
        "name": "Crafter",
        "category": "origin",
        "level_prereq": 1,
        "prerequisite": "None",
        "benefits": [
            "Tool Proficiency: Proficiency with 3 different Artisan's Tools of your choice.",
            "Discount: 20% discount on nonmagical items you purchase.",
            "Fast Crafting: Craft nonmagical items in 20% less time."
        ]
    },
    "healer": {
        "name": "Healer",
        "category": "origin",
        "level_prereq": 1,
        "prerequisite": "None",
        "benefits": [
            "Battle Medic: When you use a Healer's Kit to stabilize a creature, that creature also regains 1 HP.",
            "Healing Rerolls: When you roll dice to determine HP restored by a spell or ability, you can reroll any roll of a 1."
        ]
    },
    "lucky": {
        "name": "Lucky",
        "category": "origin",
        "level_prereq": 1,
        "prerequisite": "None",
        "benefits": [
            "Luck Points: Gain Luck Points equal to your Proficiency Bonus (regained on Long Rest).",
            "Advantage: Spend 1 Luck Point to gain Advantage on a D20 Test.",
            "Disadvantage: When an attack roll is made against you, spend 1 Luck Point to impose Disadvantage on the attack roll."
        ]
    },
    "magic_initiate": {
        "name": "Magic Initiate",
        "category": "origin",
        "level_prereq": 1,
        "prerequisite": "None",
        "benefits": [
            "Two Cantrips: Choose 2 cantrips from the Cleric, Druid, or Wizard spell list.",
            "Level 1 Spell: Choose one 1st-level spell from that same list (cast 1/Long Rest without slot, and can also cast using spell slots).",
            "Spellcasting Ability: Intelligence, Wisdom, or Charisma (chosen when taking feat)."
        ]
    },
    "musician": {
        "name": "Musician",
        "category": "origin",
        "level_prereq": 1,
        "prerequisite": "None",
        "benefits": [
            "Instrument Training: Gain proficiency with 3 Musical Instruments of your choice.",
            "Inspiring Song: As part of a Short or Long Rest, play music to grant Heroic Inspiration to allies equal to your Proficiency Bonus."
        ]
    },
    "savage_attacker": {
        "name": "Savage Attacker",
        "category": "origin",
        "level_prereq": 1,
        "prerequisite": "None",
        "benefits": [
            "Damage Advantage: Once per turn when you hit a target with a weapon attack, roll the weapon's damage dice twice and use either total."
        ]
    },
    "skilled": {
        "name": "Skilled",
        "category": "origin",
        "level_prereq": 1,
        "prerequisite": "None",
        "benefits": [
            "Versatile Expertise: Gain proficiency in any combination of 3 skills or tools of your choice (Repeatable)."
        ]
    },
    "tavern_brawler": {
        "name": "Tavern Brawler",
        "category": "origin",
        "level_prereq": 1,
        "prerequisite": "None",
        "benefits": [
            "Enhanced Unarmed Strike: Unarmed Strike damage becomes 1d4 + Strength modifier.",
            "Damage Rerolls: Reroll any damage die of a 1 on Unarmed Strikes.",
            "Push: When you hit with an Unarmed Strike, push the target 5 feet straight away."
        ]
    },
    "tough": {
        "name": "Tough",
        "category": "origin",
        "level_prereq": 1,
        "prerequisite": "None",
        "benefits": [
            "Hit Point Surge: Max HP increases by 2 per level (including retroactive past levels)."
        ]
    },
    # General Feats (Level 4+)
    "ability_score_improvement": {
        "name": "Ability Score Improvement",
        "category": "general",
        "level_prereq": 4,
        "prerequisite": "None",
        "benefits": [
            "Increase one ability score by 2, or two ability scores by 1 each (max 20). Repeatable."
        ]
    },
    "great_weapon_master": {
        "name": "Great Weapon Master",
        "category": "general",
        "level_prereq": 4,
        "prerequisite": "Strength 13+",
        "benefits": [
            "Ability Score: Increase Strength by 1.",
            "Heavy Weapon Mastery: On your turn with a Heavy weapon, deal extra damage equal to your Proficiency Bonus on hit.",
            "Hew: On critical hit or dropping enemy to 0 HP, make one bonus melee attack."
        ]
    },
    "polearm_master": {
        "name": "Polearm Master",
        "category": "general",
        "level_prereq": 4,
        "prerequisite": "Strength or Dexterity 13+",
        "benefits": [
            "Ability Score: Increase Strength or Dexterity by 1.",
            "Polearm Butt Strike: Bonus Action attack with opposite end dealing 1d4 bludgeoning damage.",
            "Reactive Strike: Opportunity Attack when a creature enters your reach."
        ]
    },
    "sentinel": {
        "name": "Sentinel",
        "category": "general",
        "level_prereq": 4,
        "prerequisite": "Strength or Dexterity 13+",
        "benefits": [
            "Ability Score: Increase Strength or Dexterity by 1.",
            "Guardian: Hit with Opportunity Attack reduces target's Speed to 0 for rest of turn.",
            "Vengeance: Make melee reaction attack against enemy attacking an ally within 5ft."
        ]
    },
    "war_caster": {
        "name": "War Caster",
        "category": "general",
        "level_prereq": 4,
        "prerequisite": "Spellcaster",
        "benefits": [
            "Ability Score: Increase INT, WIS, or CHA by 1.",
            "Advantage on Concentration saves to maintain spells when taking damage.",
            "Somatic Casting: Perform somatic components while holding weapons/shields.",
            "Opportunity Spell: Cast a 1-action spell as a Reaction when enemy provokes Opportunity Attack."
        ]
    },
    # Fighting Style Feats
    "fighting_style_archery": {
        "name": "Fighting Style: Archery",
        "category": "fighting_style",
        "level_prereq": 1,
        "prerequisite": "Fighting Style Feature",
        "benefits": ["Gain a +2 bonus to attack rolls made with ranged weapons."]
    },
    "fighting_style_defense": {
        "name": "Fighting Style: Defense",
        "category": "fighting_style",
        "level_prereq": 1,
        "prerequisite": "Fighting Style Feature",
        "benefits": ["Gain a +1 bonus to Armor Class while wearing Light, Medium, or Heavy armor."]
    },
    "fighting_style_dueling": {
        "name": "Fighting Style: Dueling",
        "category": "fighting_style",
        "level_prereq": 1,
        "prerequisite": "Fighting Style Feature",
        "benefits": ["Gain a +2 bonus to damage rolls when wielding a melee weapon in one hand and no other weapons."]
    },
    "fighting_style_great_weapon": {
        "name": "Fighting Style: Great Weapon Fighting",
        "category": "fighting_style",
        "level_prereq": 1,
        "prerequisite": "Fighting Style Feature",
        "benefits": ["When rolling damage for a Two-Handed or Versatile melee weapon, treat any roll of a 1 or 2 as a 3."]
    },
    "fighting_style_two_weapon": {
        "name": "Fighting Style: Two-Weapon Fighting",
        "category": "fighting_style",
        "level_prereq": 1,
        "prerequisite": "Fighting Style Feature",
        "benefits": ["When making an extra attack from Two-Weapon Fighting / Light property, add your ability modifier to the damage."]
    }
}


def run():
    rules_dir = ROOT / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    
    with open(rules_dir / "backgrounds.json", "w", encoding="utf-8") as f:
        json.dump(BACKGROUNDS_2024, f, indent=2)
    print(f"Saved {len(BACKGROUNDS_2024)} backgrounds to rules/backgrounds.json")

    with open(rules_dir / "species.json", "w", encoding="utf-8") as f:
        json.dump(SPECIES_2024, f, indent=2)
    print(f"Saved {len(SPECIES_2024)} species to rules/species.json")

    with open(rules_dir / "feats.json", "w", encoding="utf-8") as f:
        json.dump(FEATS_2024, f, indent=2)
    print(f"Saved {len(FEATS_2024)} feats to rules/feats.json")


if __name__ == "__main__":
    run()
