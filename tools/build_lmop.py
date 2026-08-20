import json
from pathlib import Path

OUT = Path('adventures/lost_mine_of_phandelver')
OUT.mkdir(parents=True, exist_ok=True)
for sub in ['chapters', 'locations', 'npcs', 'quests', 'encounters', 'items', 'monsters', 'factions']:
    (OUT / sub).mkdir(parents=True, exist_ok=True)

# 1. Manifest
manifest = {
    'id': 'lost_mine_of_phandelver',
    'title': 'Lost Mine of Phandelver',
    'version': '1.0.0',
    'author': 'Wizards of the Coast (Imported for Agentic D&D)',
    'setting': 'Forgotten Realms (Sword Coast)',
    'recommended_levels': {'start': 1, 'end': 5},
    'starting_location': 'triboar_trail_ambush',
    'starting_scene': {
        'title': 'Goblin Ambush on the Triboar Trail',
        'description': 'You have been on the High Road from Neverwinter for several days, escorting a wagon laden with mining provisions and supplies to the frontier settlement of Phandalin. As you round a bend in the Triboar Trail flanked by dense briars, you spot two dead horses sprawled across the muddy path ahead, black-feathered goblin arrows protruding from their flanks.',
        'weather': 'Overcast with intermittent cool drizzle',
        'time_of_day': 'Late Afternoon',
        'lighting': 'Dim Light',
        'tension_level': 'Tense',
        'threats': ['4 Cragmaw Goblins hiding in the thickets (Stealth +6 vs Passive Perception 10-15)'],
        'exits': ['Follow the goblin trail northwest toward the Cragmaw Hideout', 'Continue along the Triboar Trail toward Phandalin']
    },
    'chapters': [
        {'id': 'part_1', 'title': 'Part 1: Goblin Arrows', 'file': 'chapters/chapter_1_goblin_arrows.md', 'level_range': '1'},
        {'id': 'part_2', 'title': 'Part 2: Phandalin', 'file': 'chapters/chapter_2_phandalin.md', 'level_range': '2-3'},
        {'id': 'part_3', 'title': 'Part 3: The Spider's Web', 'file': 'chapters/chapter_3_the_spiders_web.md', 'level_range': '3-4'},
        {'id': 'part_4', 'title': 'Part 4: Wave Echo Cave', 'file': 'chapters/chapter_4_wave_echo_cave.md', 'level_range': '4-5'}
    ]
}
with open(OUT / 'adventure.json', 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)

# 2. NPCs
npcs = {
    'sildar_hallwinter': {
        'id': 'sildar_hallwinter',
        'name': 'Sildar Hallwinter',
        'race': 'Human',
        'role': 'Lords Alliance Agent / Escort',
        'faction': 'Lords Alliance',
        'status': 'Alive',
        'ac': 16,
        'hp': {'current': 11, 'max': 11},
        'stats': {'strength': 13, 'dexterity': 10, 'constitution': 12, 'intelligence': 10, 'wisdom': 11, 'charisma': 10},
        'disposition': 50,
        'description': 'A kind-hearted human warrior in his fifties with silver hair and an honorable bearing. Agent of the Lords Alliance seeking his lost companion Iarno Albrek.'
    },
    'gundren_rockseeker': {
        'id': 'gundren_rockseeker',
        'name': 'Gundren Rockseeker',
        'race': 'Dwarf',
        'role': 'Prospector & Explorer',
        'status': 'Alive',
        'ac': 10,
        'hp': {'current': 10, 'max': 10},
        'stats': {'strength': 14, 'dexterity': 10, 'constitution': 14, 'intelligence': 12, 'wisdom': 12, 'charisma': 11},
        'disposition': 60,
        'description': 'An ambitious, enthusiastic dwarf prospector who discovered the entrance to Wave Echo Cave with his brothers Tharden and Nundro.'
    },
    'iarno_albrek': {
        'id': 'iarno_albrek',
        'name': 'Iarno Glasstaff Albrek',
        'race': 'Human',
        'role': 'Former Lords Alliance Wizard / Leader of the Redbrands',
        'status': 'Alive',
        'ac': 13,
        'hp': {'current': 22, 'max': 22},
        'stats': {'strength': 9, 'dexterity': 14, 'constitution': 11, 'intelligence': 17, 'wisdom': 12, 'charisma': 14},
        'disposition': -80,
        'description': 'A treacherous wizard with a glass staff who betrayed the Lords Alliance to establish his own criminal syndicate in Phandalin under the patronage of the Black Spider.'
    },
    'nezznar_the_black_spider': {
        'id': 'nezznar_the_black_spider',
        'name': 'Nezznar the Black Spider',
        'race': 'Drow',
        'role': 'Mastermind & Drow Mage',
        'status': 'Alive',
        'ac': 11,
        'hp': {'current': 27, 'max': 27},
        'stats': {'strength': 9, 'dexterity': 13, 'constitution': 10, 'intelligence': 16, 'wisdom': 14, 'charisma': 13},
        'disposition': -100,
        'description': 'A sinister, patient drow wizard who orchestrates the Cragmaw goblins and Redbrands from the depths of Wave Echo Cave, seeking to unlock the secrets of the Forge of Spells.'
    },
    'klarg': {
        'id': 'klarg',
        'name': 'Klarg',
        'race': 'Bugbear',
        'role': 'Cragmaw Hideout Chieftain',
        'status': 'Alive',
        'ac': 16,
        'hp': {'current': 27, 'max': 27},
        'stats': {'strength': 15, 'dexterity': 14, 'constitution': 13, 'intelligence': 8, 'wisdom': 11, 'charisma': 9},
        'disposition': -90,
        'description': 'A vainglorious, brutal bugbear who believes he is destined to conquer the Sword Coast. Pet wolf named Ripper.'
    },
    'reidoth': {
        'id': 'reidoth',
        'name': 'Reidoth',
        'race': 'Human',
        'role': 'Druid of the Emerald Enclave',
        'faction': 'Emerald Enclave',
        'status': 'Alive',
        'ac': 13,
        'hp': {'current': 27, 'max': 27},
        'stats': {'strength': 10, 'dexterity': 12, 'constitution': 13, 'intelligence': 12, 'wisdom': 15, 'charisma': 11},
        'disposition': 40,
        'description': 'A gaunt, white-bearded hermit druid who knows every path and secret in the wilderness. Warns travelers away from Venomfang the green dragon.'
    },
    'agatha': {
        'id': 'agatha',
        'name': 'Agatha',
        'race': 'Elf (Banshee)',
        'role': 'Undead Oracle of Conyberry',
        'status': 'Undead',
        'ac': 12,
        'hp': {'current': 58, 'max': 58},
        'disposition': 0,
        'description': 'A vain, melancholy elven spirit who dwells in a dome of woven branches. Knows ancient regional lore and answers questions if flattered with beautiful gifts.'
    },
    'halia_thornton': {
        'id': 'halia_thornton',
        'name': 'Halia Thornton',
        'race': 'Human',
        'role': 'Guildmistress of Phandalin Miners Exchange',
        'faction': 'Zhentarim',
        'status': 'Alive',
        'ac': 12,
        'hp': {'current': 11, 'max': 11},
        'disposition': 20,
        'description': 'An ambitious and calculating woman who quietly maneuvers to make the Miners Exchange the supreme authority in Phandalin.'
    },
    'sister_garaele': {
        'id': 'sister_garaele',
        'name': 'Sister Garaele',
        'race': 'Elf',
        'role': 'Priestess of Tymora / Harpers Agent',
        'faction': 'Harpers',
        'status': 'Alive',
        'ac': 11,
        'hp': {'current': 9, 'max': 9},
        'disposition': 50,
        'description': 'A zealous, kind young elf who oversees the Shrine of Luck while gathering intelligence for the Harpers.'
    }
}
with open(OUT / 'npcs' / 'npcs.json', 'w', encoding='utf-8') as f:
    json.dump(npcs, f, indent=2)

# 3. Quests
quests = [
    {
        'id': 'goblin_arrows_deliver_supplies',
        'title': 'Escort Provisions to Barthens',
        'type': 'main',
        'giver': 'Gundren Rockseeker',
        'status': 'active',
        'priority': 'High',
        'objectives': [
            {'id': 'deliver_wagon', 'description': 'Escort the ox wagon safely to Barthens Provisions in Phandalin', 'completed': False},
            {'id': 'claim_payment', 'description': 'Receive 10 gp per adventurer from Elmar Barthen', 'completed': False}
        ],
        'rewards': {'xp': 100, 'gp': 50}
    },
    {
        'id': 'rescue_sildar',
        'title': 'Rescue Sildar Hallwinter',
        'type': 'main',
        'giver': 'Auto (Goblin Ambush Clue)',
        'status': 'active',
        'priority': 'Critical',
        'objectives': [
            {'id': 'infiltrate_hideout', 'description': 'Follow goblin trail to Cragmaw Hideout', 'completed': False},
            {'id': 'free_sildar', 'description': 'Rescue Sildar Hallwinter from Yeemiks clutches', 'completed': False}
        ],
        'rewards': {'xp': 150, 'gp': 50}
    },
    {
        'id': 'redbrand_menace',
        'title': 'The Redbrand Menace',
        'type': 'main',
        'giver': 'Sildar Hallwinter / Townspeople',
        'status': 'active',
        'priority': 'High',
        'objectives': [
            {'id': 'infiltrate_tresendar', 'description': 'Infiltrate the Redbrand Hideout beneath Tresendar Manor', 'completed': False},
            {'id': 'defeat_glasstaff', 'description': 'Defeat or capture Iarno Glasstaff Albrek', 'completed': False},
            {'id': 'rescue_dendrars', 'description': 'Free Mirna Dendrar and her children from the slave pens', 'completed': False}
        ],
        'rewards': {'xp': 400, 'gp': 200}
    },
    {
        'id': 'find_cragmaw_castle',
        'title': 'Find Cragmaw Castle & Rescue Gundren',
        'type': 'main',
        'giver': 'Sildar Hallwinter',
        'status': 'active',
        'priority': 'Critical',
        'objectives': [
            {'id': 'locate_castle', 'description': 'Discover castle location from Reidoth, Agatha, or captured goblin', 'completed': False},
            {'id': 'defeat_grol', 'description': 'Defeat King Grol and recover Gundrens map', 'completed': False},
            {'id': 'rescue_gundren', 'description': 'Save Gundren Rockseeker from execution', 'completed': False}
        ],
        'rewards': {'xp': 600, 'gp': 500}
    },
    {
        'id': 'wave_echo_cave_forge',
        'title': 'Reclaim Wave Echo Cave & The Forge of Spells',
        'type': 'main',
        'giver': 'Gundren Rockseeker',
        'status': 'active',
        'priority': 'Epic',
        'objectives': [
            {'id': 'enter_cave', 'description': 'Travel to the secret entrance of Wave Echo Cave', 'completed': False},
            {'id': 'defeat_black_spider', 'description': 'Defeat Nezznar the Black Spider in the Temple of Dumathoin', 'completed': False},
            {'id': 'reclaim_forge', 'description': 'Secure the Forge of Spells and restore prosperity to Phandalin', 'completed': False}
        ],
        'rewards': {'xp': 1200, 'gp': 1000, 'items': ['Spider Staff', 'Lightbringer', 'Dragonguard']}
    },
    {
        'id': 'agatha_comb',
        'title': 'Sister Garaeles Bargain (Agathas Comb)',
        'type': 'sidequest',
        'giver': 'Sister Garaele',
        'status': 'active',
        'priority': 'Medium',
        'objectives': [
            {'id': 'visit_agatha', 'description': 'Present the jeweled silver comb to Agatha in Conyberry', 'completed': False},
            {'id': 'ask_spellbook', 'description': 'Inquire about the location of the legendary spellbook of Bowgentle', 'completed': False}
        ],
        'rewards': {'xp': 100, 'gp': 0, 'items': ['3x Potion of Healing']}
    }
]
with open(OUT / 'quests' / 'quests.json', 'w', encoding='utf-8') as f:
    json.dump(quests, f, indent=2)

# 4. Encounters
encounters = [
    {
        'id': 'goblin_ambush',
        'name': 'Goblin Ambush on Triboar Trail',
        'monsters': ['goblin', 'goblin', 'goblin', 'goblin'],
        'base_xp': 200,
        'adjusted_xp': 400,
        'difficulty': 'Deadly for 1st level',
        'tactics': '2 melee goblins rush with scimitars while 2 archers fire from +2 half-cover thickets.'
    },
    {
        'id': 'cragmaw_kennel',
        'name': 'Cragmaw Kennel Wolves',
        'monsters': ['wolf', 'wolf', 'wolf'],
        'base_xp': 150,
        'adjusted_xp': 300,
        'difficulty': 'Hard for 1st level'
    },
    {
        'id': 'klargs_den',
        'name': 'Chieftain Klarg & Ripper',
        'monsters': ['bugbear', 'wolf', 'goblin', 'goblin'],
        'base_xp': 350,
        'adjusted_xp': 700,
        'difficulty': 'Deadly for 1st level',
        'tactics': 'Klarg attempts a surprise strike dealing +2d6 damage from hiding.'
    },
    {
        'id': 'redbrand_street_confrontation',
        'name': 'Sleeping Giant Redbrands',
        'monsters': ['bandit', 'bandit', 'bandit', 'bandit'],
        'base_xp': 100,
        'adjusted_xp': 200,
        'difficulty': 'Medium for 2nd level'
    },
    {
        'id': 'nothic_crevasse',
        'name': 'The Nothic of Tresendar Manor',
        'monsters': ['nothic'],
        'base_xp': 450,
        'adjusted_xp': 450,
        'difficulty': 'Medium for 2nd level',
        'tactics': 'Uses telepathy and Weird Insight to bargain for meat and magical secrets before attacking.'
    },
    {
        'id': 'cragmaw_castle_throne',
        'name': 'King Grol & Doppelganger',
        'monsters': ['bugbear', 'wolf', 'doppelganger'],
        'base_xp': 900,
        'adjusted_xp': 1800,
        'difficulty': 'Hard for 3rd level'
    },
    {
        'id': 'venomfang_tower',
        'name': 'Venomfang the Young Green Dragon',
        'monsters': ['young_green_dragon'],
        'base_xp': 3900,
        'adjusted_xp': 3900,
        'difficulty': 'Deadly for 3rd level',
        'tactics': 'Opens with Poison Breath (DC 14 CON save, 12d6 poison), flies out of reach if reduced below half HP.'
    },
    {
        'id': 'black_spider_climax',
        'name': 'Nezznar the Black Spider & Spiders',
        'monsters': ['nezznar_black_spider', 'giant_spider', 'giant_spider', 'giant_spider', 'giant_spider'],
        'base_xp': 1100,
        'adjusted_xp': 2200,
        'difficulty': 'Hard for 4th level'
    }
]
with open(OUT / 'encounters' / 'encounters.json', 'w', encoding='utf-8') as f:
    json.dump(encounters, f, indent=2)

# 5. Magic Items
items = {
    'spider_staff': {
        'id': 'spider_staff',
        'name': 'Spider Staff',
        'type': 'Staff',
        'rarity': 'rare',
        'attunement': True,
        'description': 'The top of this black, polished wooden staff is carved in the likeness of a spider. The staff has 10 charges and regains 1d6 + 4 expended charges daily at dusk. While holding it, you deal an extra 1d6 poison damage on melee weapon hits, and can cast spider climb (1 charge) or web (2 charges, spell save DC 15).',
        'bonuses': {'melee_poison_damage': '1d6'},
        'charges': {'max': 10, 'recharge': '1d6+4 daily at dusk'}
    },
    'staff_of_defense': {
        'id': 'staff_of_defense',
        'name': 'Staff of Defense',
        'type': 'Staff',
        'rarity': 'rare',
        'attunement': True,
        'description': 'This slender, hollow staff is made of hardened glass. While holding it, you gain a +2 bonus to Armor Class. The staff has 4 charges and regains 1d4 expended charges daily at dawn. While holding it, you can cast mage armor (1 charge) or shield (2 charges) as an action or reaction.',
        'bonuses': {'ac': 2},
        'charges': {'max': 4, 'recharge': '1d4 daily at dawn'}
    },
    'lightbringer': {
        'id': 'lightbringer',
        'name': 'Lightbringer',
        'type': 'Weapon (warhammer)',
        'rarity': 'uncommon',
        'attunement': False,
        'description': 'This +1 warhammer was forged for a cleric of Lathander. The head is shaped like a sunburst. On command, it sheds bright light in a 15-foot radius. When hitting an undead creature, it deals an extra 1d6 radiant damage.',
        'bonuses': {'attack': 1, 'damage': 1, 'undead_radiant_damage': '1d6'}
    },
    'dragonguard': {
        'id': 'dragonguard',
        'name': 'Dragonguard',
        'type': 'Armor (breastplate)',
        'rarity': 'rare',
        'attunement': False,
        'description': 'This +1 breastplate has a gold dragon design worked into the chest. While wearing it, you have advantage on saving throws against the breath weapons of creatures of the dragon type.',
        'bonuses': {'ac': 1, 'dragon_breath_advantage': True}
    },
    'talon': {
        'id': 'talon',
        'name': 'Talon',
        'type': 'Weapon (longsword)',
        'rarity': 'uncommon',
        'attunement': False,
        'description': 'This +1 longsword has a hilt carved in the shape of a bird of prey. It belonged to the knight Aldith Tresendar, known as the Black Hawk.',
        'bonuses': {'attack': 1, 'damage': 1}
    },
    'hew': {
        'id': 'hew',
        'name': 'Hew',
        'type': 'Weapon (battleaxe)',
        'rarity': 'uncommon',
        'attunement': False,
        'description': 'This +1 battleaxe was forged for a dwarf prospector. It deals maximum damage against wooden objects and plants.',
        'bonuses': {'attack': 1, 'damage': 1}
    }
}
with open(OUT / 'items' / 'magic_items.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, indent=2)

# 6. Custom Monsters
monsters = {
    'nezznar_black_spider': {
        'id': 'nezznar_black_spider',
        'name': 'Nezznar the Black Spider',
        'size': 'Medium',
        'type': 'humanoid (elf, drow)',
        'alignment': 'neutral evil',
        'ac': 11,
        'hp': {'current': 27, 'max': 27, 'formula': '6d8'},
        'speed': 30,
        'stats': {'strength': 9, 'dexterity': 13, 'constitution': 10, 'intelligence': 16, 'wisdom': 14, 'charisma': 13},
        'saving_throws': {'intelligence': 5, 'wisdom': 4},
        'skills': {'perception': 4, 'stealth': 3, 'arcana': 5},
        'senses': 'darkvision 120 ft., passive Perception 14',
        'languages': 'Elvish, Undercommon',
        'cr': '2',
        'xp': 450,
        'traits': {
            'fey_ancestry': 'Advantage on saves against being charmed, magic cannot put to sleep.',
            'sunlight_sensitivity': 'Disadvantage on attacks and sight perception in direct sunlight.'
        },
        'actions': [
            {'name': 'Spider Staff', 'type': 'melee', 'bonus': 1, 'damage': '1d6-1', 'extra_damage': '1d6 poison', 'damage_type': 'bludgeoning'}
        ]
    },
    'evil_mage': {
        'id': 'evil_mage',
        'name': 'Evil Mage (Glasstaff)',
        'size': 'Medium',
        'type': 'humanoid (human)',
        'alignment': 'lawful evil',
        'ac': 13,
        'hp': {'current': 22, 'max': 22, 'formula': '5d8'},
        'speed': 30,
        'stats': {'strength': 9, 'dexterity': 14, 'constitution': 11, 'intelligence': 17, 'wisdom': 12, 'charisma': 14},
        'saving_throws': {'intelligence': 5, 'wisdom': 3},
        'skills': {'arcana': 5, 'history': 5},
        'senses': 'passive Perception 11',
        'languages': 'Common, Draconic, Elvish',
        'cr': '1',
        'xp': 200,
        'actions': [
            {'name': 'Quarterstaff', 'type': 'melee', 'bonus': 1, 'damage': '1d6-1', 'damage_type': 'bludgeoning'}
        ]
    },
    'nothic': {
        'id': 'nothic',
        'name': 'Nothic',
        'size': 'Medium',
        'type': 'aberration',
        'alignment': 'neutral evil',
        'ac': 15,
        'hp': {'current': 45, 'max': 45, 'formula': '6d8+18'},
        'speed': 30,
        'stats': {'strength': 14, 'dexterity': 16, 'constitution': 16, 'intelligence': 13, 'wisdom': 10, 'charisma': 8},
        'skills': {'arcana': 3, 'insight': 4, 'perception': 2, 'stealth': 5},
        'senses': 'truesight 120 ft., passive Perception 12',
        'languages': 'Undercommon, Telepathy 120 ft.',
        'cr': '2',
        'xp': 450,
        'traits': {
            'weird_insight': 'Target contested Insight vs Deception to learn one piece of target secret knowledge.'
        },
        'actions': [
            {'name': 'Claws (Multiattack x2)', 'type': 'melee', 'bonus': 4, 'damage': '1d6+3', 'damage_type': 'slashing'},
            {'name': 'Rotting Gaze', 'type': 'ranged', 'save': 'DC 12 CON', 'damage': '3d6', 'damage_type': 'necrotic'}
        ]
    },
    'flameskull': {
        'id': 'flameskull',
        'name': 'Flameskull',
        'size': 'Tiny',
        'type': 'undead',
        'alignment': 'neutral evil',
        'ac': 13,
        'hp': {'current': 40, 'max': 40, 'formula': '9d4+18'},
        'speed': 0,
        'fly_speed': 40,
        'stats': {'strength': 1, 'dexterity': 17, 'constitution': 14, 'intelligence': 16, 'wisdom': 10, 'charisma': 11},
        'damage_resistances': ['lightning', 'necrotic', 'piercing'],
        'damage_immunities': ['cold', 'fire', 'poison'],
        'senses': 'darkvision 60 ft., passive Perception 12',
        'languages': 'Common',
        'cr': '4',
        'xp': 1100,
        'traits': {
            'rejuvenation': 'Regains all HP in 1 hour unless holy water or dispel magic is used on its remains.',
            'magic_resistance': 'Advantage on saving throws against spells.'
        },
        'actions': [
            {'name': 'Fire Ray', 'type': 'ranged', 'bonus': 5, 'damage': '3d6', 'damage_type': 'fire'}
        ]
    },
    'redbrand_ruffian': {
        'id': 'redbrand_ruffian',
        'name': 'Redbrand Ruffian',
        'size': 'Medium',
        'type': 'humanoid (human)',
        'alignment': 'neutral evil',
        'ac': 14,
        'hp': {'current': 16, 'max': 16, 'formula': '3d8+3'},
        'speed': 30,
        'stats': {'strength': 11, 'dexterity': 14, 'constitution': 12, 'intelligence': 9, 'wisdom': 9, 'charisma': 11},
        'skills': {'intimidation': 2},
        'senses': 'passive Perception 9',
        'languages': 'Common',
        'cr': '1/2',
        'xp': 100,
        'actions': [
            {'name': 'Multiattack (x2 Shortswords)', 'type': 'melee', 'bonus': 4, 'damage': '1d6+2', 'damage_type': 'piercing'}
        ]
    }
}
with open(OUT / 'monsters' / 'monsters.json', 'w', encoding='utf-8') as f:
    json.dump(monsters, f, indent=2)

# 7. Factions
factions = {
    'harpers': {
        'name': 'The Harpers',
        'motto': 'Knowledge is power; balance in all things.',
        'representative_in_phandalin': 'Sister Garaele',
        'location': 'Shrine of Luck',
        'goals': 'Eliminate tyranny, promote equality, preserve ancient historical lore.',
        'membership_reward': 'Title of Watcher (1 renown point)'
    },
    'order_of_the_gauntlet': {
        'name': 'Order of the Gauntlet',
        'motto': 'Faith, vigilance, and righteousness.',
        'representative_in_phandalin': 'Daran Edermath',
        'location': 'Edermath Orchard',
        'goals': 'Smite evil and undead threats wherever they arise.',
        'membership_reward': 'Title of Chevall (1 renown point)'
    },
    'emerald_enclave': {
        'name': 'Emerald Enclave',
        'motto': 'Preserve the natural order.',
        'representative_in_phandalin': 'Reidoth the Druid',
        'location': 'Ruins of Thundertree',
        'goals': 'Protect the balance of nature against encroaching abominations and corruption.',
        'membership_reward': 'Title of Springwarden (1 renown point)'
    },
    'lords_alliance': {
        'name': 'The Lords Alliance',
        'motto': 'Security and order through united rule.',
        'representative_in_phandalin': 'Sildar Hallwinter',
        'location': 'Townmasters Hall',
        'goals': 'Restore civilization and security to frontier settlements.',
        'membership_reward': 'Title of Cloak (1 renown point)'
    },
    'zhentarim': {
        'name': 'The Zhentarim (The Black Network)',
        'motto': 'Wealth and power for those bold enough to seize it.',
        'representative_in_phandalin': 'Halia Thornton',
        'location': 'Phandalin Miners Exchange',
        'goals': 'Expand commercial and political dominance across the Sword Coast.',
        'membership_reward': 'Title of Fang (1 renown point)'
    }
}
with open(OUT / 'factions' / 'factions.json', 'w', encoding='utf-8') as f:
    json.dump(factions, f, indent=2)

print('Full Lost Mine of Phandelver package successfully generated!')
