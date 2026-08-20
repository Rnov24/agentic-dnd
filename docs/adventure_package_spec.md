# Generalized Adventure Module Specification & Storage Standard

This specification defines the universal architecture, directory layout, and storage principles for importing, packaging, and running any D&D adventure book (e.g. *Lost Mine of Phandelver*, *Curse of Strahd*, *Tomb of Annihilation*, *Waterdeep: Dragon Heist*, or custom homebrew modules) in **Agentic D&D**.

---

## 1. The Core Storage Standard: When to Use Markdown vs. JSON

To ensure maximum **information retrieval efficiency**, **zero-hallucination deterministic mechanics**, and **rich Theater-of-the-Mind storytelling**, the architecture enforces strict separation criteria between Markdown and JSON:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           INFORMATION STORAGE TAXONOMY                      │
├──────────────────────────────────────┬──────────────────────────────────────┤
│          MARKDOWN (.md)              │             JSON (.json)             │
│   (Narrative, Sensory & Semantic)    │    (Deterministic & Machine-Indexed) │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • Read-Aloud Boxed Descriptions      │ • Room Graph & Exit Connectivity     │
│ • Sensory Details (Light, Scent, Tone│ • DC Values, Trap Damage Formulas    │
│ • NPC Voice, Backstory, Personality  │ • Entity Stats (HP, AC, Speed, CR)   │
│ • Roleplaying Tactics & Dialogue Tips│ • Quest Objectives & Boolean State   │
│ • Historical Lore & Campaign Plots   │ • Magic Item Bonuses, Charges, Stats │
│ • Atmospheric Scene Framing          │ • Pre-calculated Encounter XP/Diff   │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

### Detailed Decision Matrix

| Data Type | Primary Storage | Secondary Storage | Retrieval & Use Rationale |
|---|---|---|---|
| **Room Narrative & Atmosphere** | `.md` (Location Sheet) | `.json` (summary in node) | The DM Agent needs rich descriptive prose to convey spatial relations without grid coordinates. |
| **Room Connections & Exits** | `.json` (`locations.json`) | `.md` (links section) | The World Agent must deterministically validate travel between nodes without guessing paths. |
| **Traps & Hazards** | `.json` (DC, Save, Damage) | `.md` (Visual Description) | Mechanical trigger resolution is calculated in Python (`tools/combat.py`), visual effect rendered by DM. |
| **NPC Personality & Roleplaying** | `.md` (NPC Profile) | — | LLM reasoning benefits from nuanced personality traits, ideals, bonds, flaws, and dialogue samples. |
| **NPC Combat Stats & Disposition** | `.json` (`npcs.json`) | `.md` (Stat block header) | Mechanical HP, AC, disposition scores (-100 to +100), and memory streams require atomic JSON mutation. |
| **Quest Objectives & Progress** | `.json` (`quests.json`) | `.md` (Quest Document) | State tracking requires discrete boolean objective completion and automated state snapshots. |
| **Monster Statblocks** | `.json` (`monsters.json`) | — | Combat engine needs exact arithmetic (damage dice, attack modifiers, saving throw bonuses). |
| **Magic Items** | `.json` (`magic_items.json`) | `.md` (Lore Document) | Mechanics engine checks attunement slots, stat overrides (e.g. STR 19), and daily charge counts. |
| **Factions & Renown** | `.json` (`factions.json`) | `.md` (Faction Overview) | Tracks discrete character renown points, standing, and local faction representatives. |

---

## 2. Generalized Directory Tree for Adventure Modules

Every adventure module is packaged under `adventures/<adventure_slug>/` using this standardized layout:

```text
adventures/<adventure_slug>/
├── adventure.json                  # Module manifest (title, level range, starting scene, author)
├── README.md                       # Adventure synopsis, DM background, and campaign hooks
├── chapters/                       # Narrative story acts and pacing guidelines (.md)
│   ├── chapter_1_<name>.md
│   ├── chapter_2_<name>.md
│   └── chapter_N_<name>.md
├── locations/                      # All keyed adventure locations
│   ├── locations.json              # Complete machine-queriable room graph
│   └── <dungeon_or_region>/        # Regional subdirectories with .md sheets
│       ├── 01_<room_name>.md
│       └── 02_<room_name>.md
├── npcs/                           # All adventure NPCs
│   ├── npcs.json                   # Machine-readable entity state & disposition database
│   ├── <major_npc>.md              # Deep roleplaying profiles for key figures
│   └── minor_npcs/                 # Brief profile sheets
├── quests/                         # Adventure quests & sidequests
│   ├── quests.json                 # Machine-trackable quest objectives, prerequisites, & rewards
│   └── <quest_name>.md             # Human-readable quest overview & narrative triggers
├── encounters/                     # Combat scenarios
│   └── encounters.json             # Encounter monster rosters, XP budgets, and difficulty ratings
├── items/                          # Module-specific magic items & relics
│   ├── magic_items.json            # Machine-readable item stats & charge rules
│   └── <item_name>.md              # Item lore, history, and appearance
├── monsters/                       # Custom monster statblocks
│   └── monsters.json               # Full D&D 5e JSON statblocks
└── factions/                       # Adventure factions & local contacts
    └── factions.json               # Faction goals, representatives, and renown tiers
```

---

## 3. Universal Manifest Schema (`adventure.json`)

```json
{
  "id": "lost_mine_of_phandelver",
  "title": "Lost Mine of Phandelver",
  "version": "1.0.0",
  "author": "Wizards of the Coast (Imported for Agentic D&D)",
  "recommended_levels": { "start": 1, "end": 5 },
  "starting_location": "triboar_trail_ambush",
  "starting_scene": {
    "title": "Goblin Ambush on the Triboar Trail",
    "description": "You have been on the High Road from Neverwinter for several days, escorting a wagon of mining provisions to the frontier town of Phandalin...",
    "weather": "Overcast with intermittent cool drizzle",
    "time_of_day": "Late Afternoon",
    "lighting": "Dim Light",
    "tension_level": "Tense"
  },
  "chapters": [
    { "id": "part_1", "title": "Part 1: Goblin Arrows", "file": "chapters/chapter_1_goblin_arrows.md", "level_range": "1" },
    { "id": "part_2", "title": "Part 2: Phandalin", "file": "chapters/chapter_2_phandalin.md", "level_range": "2-3" },
    { "id": "part_3", "title": "Part 3: The Spider's Web", "file": "chapters/chapter_3_the_spiders_web.md", "level_range": "3-4" },
    { "id": "part_4", "title": "Part 4: Wave Echo Cave", "file": "chapters/chapter_4_wave_echo_cave.md", "level_range": "4-5" }
  ]
}
```
