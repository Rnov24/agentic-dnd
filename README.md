# 🐉 Agentic D&D (5e 2024 Revision)

**An AI-native tabletop RPG operating environment driven by multi-agent autonomous orchestration, deterministic Python mechanics, and persistent Git-style versioning.**

[![CI Status](https://img.shields.io/badge/CI-Passing-34d399?style=flat-square&logo=githubactions&logoColor=white)](https://github.com/agentic-dnd/agentic-dnd/actions)
[![D&D 5e 2024](https://img.shields.io/badge/D%26D_5e-2024_Revision-6366f1?style=flat-square)](rules/)
[![Rules Compendium](https://img.shields.io/badge/Compendium-469_Entities-38bdf8?style=flat-square)](rules/)
[![Unit Tests](https://img.shields.io/badge/Tests-147_Passing-10b981?style=flat-square)](tests/)
[![Python Version](https://img.shields.io/badge/Python-3.9_--_3.13-f59e0b?style=flat-square&logo=python&logoColor=white)](pyproject.toml)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero_External-a855f7?style=flat-square)](requirements.txt)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

---

## 🌟 1. Overview

**Agentic D&D** transforms tabletop roleplaying into an **executable, inspectable, and persistent operating system** designed for AI coding assistants (Antigravity, Claude Code, Codex) and human players.

* **Deterministic Python Mechanics (Zero Hallucinations)**: LLMs and Agents generate sensory narration, NPC dialogue, and roleplay drama, while the deterministic Python runtime evaluates dice rolls, weapon masteries, saving throw DCs, spell slots, and condition math with 100% mathematical integrity.
* **Full D&D 2024 Player's Handbook (PHB) Alignment**: 469 verified entities across 14 compendium catalogs including Weapon Masteries (*Cleave, Graze, Nick, Push, Sap, Slow, Topple, Vex*), 2024 Origin Feats & Backgrounds (+2/+1 or +1/+1/+1), and reworked spells (*Cure Wounds 2d8, Healing Word 2d4, Counterspell CON save, Sleep WIS save*).
* **Autonomous Multi-Agent Turn Orchestration**: Turn processing is executed through a Directed Acyclic Graph (DAG) of specialized subagents (`Orchestrator`, `World`, `Rules`, `Combat`, `NPC`, `Character`, `Impact`, `DM`, and `Chronos`).
* **Git-Style Versioning & Rollback**: Every turn generates an immutable commit snapshot in `state/history.json`. Players and DMs can inspect visual diffs, explore multiverse branches, and rollback state to any past turn.
* **Tri-Layer State Isolation**:
  * **Layer 1 (Static Compendiums — `rules/`)**: Immutable rules schemas and SRD 2024 compendiums.
  * **Layer 2 (Narrative Memory — `campaign/`)**: Human-readable Markdown documents (`characters/`, `locations/`, `npcs/`, `quests/`).
  * **Layer 3 (Machine State — `state/`)**: Machine-readable JSON state and append-only commit logs.
* **Consequential Change Gate**: High-stakes permanent events (player death, major NPC death, quest failure) require explicit human approval before mutating persistent campaign state.
* **Zero External Runtime Dependencies**: Runs out-of-the-box on standard Python 3.9+ (`Windows`, `macOS`, and `Linux`).

---

## 🎮 2. Interactive Game Dashboard & Menu

When you launch a session or type `python dnd.py menu`, Agentic D&D displays the active scene, party vitals, and non-developer quick commands:

```text
======================================================================
           ⚔️  LOST MINE OF PHANDELVER — GAME DASHBOARD  ⚔️           
======================================================================
  Location: triboar_trail_ambush | Time: Late Afternoon | Weather: Overcast drizzle
  Lighting: Dim Light | Tension: Tense | State: 🌲 Exploration

--- [ CURRENT SCENE: Goblin Ambush on the Triboar Trail ] ---
  You spot two dead horses sprawled across the muddy path ahead, black-feathered
  goblin arrows protruding from their flanks.

  ⚠️ Active Threats:
   • 4 Cragmaw Goblins hiding in the thickets (Stealth +6 vs Passive Perception 10-15)

--- [ ACTIVE HERO: Thorin Ironbreaker (Lvl 1 Dwarf Fighter) ] ---
  Health:    [███████████████] 14/14 HP
  Armor Class: 16 | Hit Dice: 1/1 (1d10) | Conditions: None

--- [ 🎮 WHAT WOULD YOU LIKE TO DO? (ACTION MENU) ] ---
  💬 Natural Language (Just type what you want to do):
    • "I attack the goblin in front of me with my sword"
    • "I cast Fire Bolt at the nearest goblin archer"
    • "I quietly search the bushes for tracks or hidden enemies"
    • "We take a short rest and bandage our wounds"
    • "I talk to Sildar and ask what happened on the road"

  ⚡ Quick Slash Commands & Tool Shortcuts:
  [1] Play Action   : python dnd.py play "<intent>" (Full turn orchestration)
  [2] Attack Target : python dnd.py attack <target> [--cover half]
  [3] Cast Spell    : python dnd.py cast <spell> [--target <target>]
  [4] Skill Check   : python dnd.py check <stealth/perception/athletics> [dc]
  [5] Roll Tabletop : python dnd.py roll "1d20+5 --adv" / "2d6+3"
  [6] Inspect Sheet : python dnd.py inspect [character_name]
  [7] Switch Player : python dnd.py party switch <character_name>
  [8] Short/Long Rest: python dnd.py rest short / python dnd.py rest long
  [9] Lookup Rules  : python dnd.py explain <topic> / spell <name> / monster <name>
  [10] Status/Quests: python dnd.py status / python dnd.py menu
======================================================================
```

---

## ⚡ 3. Quickstart & Installation

### Requirements
* Python **3.9** or higher (Python 3.9, 3.10, 3.11, 3.12, 3.13 supported).
* No `pip install` required for gameplay! (100% Python standard library).

### Quickstart
```bash
# Clone repository
git clone https://github.com/agentic-dnd/agentic-dnd.git
cd agentic-dnd

# Boot the game dashboard
python dnd.py menu

# Take a turn using natural language
python dnd.py play "I draw my greatsword and strike the nearest goblin ambusher!"

# Run automated test suite
python dnd.py test
```

---

## 🛠️ 4. Comprehensive CLI Command Reference

| Command | Description |
|---|---|
| `python dnd.py menu` | Open full interactive session dashboard and action menu |
| `python dnd.py boot` | Fast-boot session initialization and state snapshot |
| `python dnd.py play "<action>"` | Process natural language action via autonomous multi-agent turn DAG |
| `python dnd.py status` | View party HP/AC, current scene, weather, threats, and active quests |
| `python dnd.py inspect [char]` | View visual character sheet with stats, saving throws, attacks, inventory |
| `python dnd.py party switch <char>` | Switch active player character in multiplayer roster |
| `python dnd.py create-character` | Create a new D&D 5e (2024) character with species, background, and stats |
| `python dnd.py level-up [char]` | Level up character (1-20) with HP scaling, spell slots, and new features |
| `python dnd.py check <skill> [dc]` | Perform a D&D 2024 ability or skill check with DC math |
| `python dnd.py attack <target>` | Perform weapon attack vs AC with cover adjustments (`--cover half/three_quarters`) |
| `python dnd.py cast <spell>` | Cast a spell from compendium with slot deduction, upcasting, or ritual |
| `python dnd.py rest [short/long]` | Take a Short Rest (spend Hit Dice) or Long Rest (full recovery) |
| `python dnd.py death-save` | Roll death saving throw at 0 HP (handles 3 successes, 3 failures, Nat 20/1) |
| `python dnd.py stabilize <char>` | Attempt DC 10 Medicine check to stabilize an unconscious ally |
| `python dnd.py initiative [roll/next]` | Roll and manage round-by-round combat initiative order |
| `python dnd.py loot [--cr <num>]` | Deterministic 5e individual or hoard treasure drop generator |
| `python dnd.py encounter -m "<monsters>"` | Evaluate combat encounter difficulty and adventuring day XP budget |
| `python dnd.py explain <topic>` | Explain D&D 2024 rules, weapon masteries, conditions, and actions |
| `python dnd.py compendium validate` | Validate all 14 compendium JSON schemas with 0 errors |
| `python dnd.py compendium stats` | Display compendium catalog entity counts |
| `python dnd.py history` | View Git-style commit timeline |
| `python dnd.py diff <commit_id>` | View unified state diff with visual before/after cards |
| `python dnd.py rollback <commit_id>` | Restore game state to a prior snapshot commit |
| `python dnd.py adventure [list/load]` | Discover, inspect, and load modular adventure packages |
| `python dnd.py test` | Run automated unit test suite (147 tests across 33 suites) |

---

## 🏗️ 5. Repository Architecture

```text
agentic-dnd/
├── .agents/skills/                 # Native Antigravity / Agentic Skills
│   ├── dnd-play/SKILL.md           # Turn Orchestration & Gameplay
│   ├── dnd-dm/SKILL.md             # Sensory Theater-of-the-Mind Narration
│   ├── dnd-rules/SKILL.md          # 5e 2024 Rules Engine & DCs
│   ├── dnd-versioning/SKILL.md     # Git Snapshots & Timeline Management
│   ├── dnd-dev/SKILL.md            # Developer Mode & Extensibility
│   └── dnd-multiverse/SKILL.md     # Alternate Reality Branching
│
├── campaign/                       # Persistent Human-Readable Markdown Memory
│   ├── characters/                 # Character Sheets (.md)
│   ├── locations/                  # Room & Wilderness Descriptions (.md)
│   ├── npcs/                       # NPC Lore & Profiles (.md)
│   └── quests/                     # Quests & Objectives (.md)
│
├── state/                          # Machine-Readable JSON Persistence
│   ├── world.json                  # Scene atmosphere, lighting, weather, flags
│   ├── party.json                  # Party stats, HP, spell slots, inventory
│   ├── npcs.json                   # NPC stats, memories, disposition
│   ├── combat.json                 # Combat tracker & initiative order
│   ├── quests.json                 # Active & completed quest tracker
│   └── history.json                # Immutable Git-style snapshot commit stream
│
├── rules/                          # Static D&D 2024 Rules Compendiums (469 Entities)
│   ├── glossary.json               # 140 Rules Glossary Terms (Appendix C)
│   ├── spells.json                 # 99 Spells (Chapter 7)
│   ├── weapons.json                # 37 Weapons with Weapon Masteries
│   ├── armor.json                  # 13 Armor & Shield types
│   ├── equipment.json              # 42 Artisan Tools, Gaming Sets, Gear
│   ├── backgrounds.json            # 17 Backgrounds with 2024 Ability Scores
│   ├── species.json                # 18 Species & Lineages
│   ├── feats.json                  # 20 Origin, General & Fighting Style Feats
│   ├── classes.json                # 12 Core Classes (Levels 1-20)
│   ├── subclasses.json             # 24 Subclasses
│   ├── conditions.json             # 15 Conditions (Exhaustion 1-6, etc.)
│   ├── actions.json                # 12 Actions (Attack, Hide, Study, Search, etc.)
│   ├── monsters.json               # Monster Bestiary Statblocks
│   ├── magic_items.json            # Magic Items & Attunement
│   └── progression.json            # Level 1-20 XP & Spell Slot Matrices
│
├── tools/                          # Deterministic Python Tool Modules
│   ├── compendium.py               # Compendium lookup & in-memory caching
│   ├── compendium_validator.py     # Schema validation & integrity checks
│   ├── character_creator.py        # D&D 2024 character creation engine
│   ├── character_inspector.py      # Terminal character sheet renderer
│   ├── level_up.py                 # Character level-up engine (1-20)
│   ├── multiplayer.py              # Multiplayer party management
│   ├── dice.py                     # Tabletop dice roller with advantage/crit
│   ├── mechanics.py                # Ability checks, saving throws, audit cards
│   ├── combat.py                   # Weapon attacks, AC hits, damage formulas
│   ├── spells.py                   # Spellcasting, slots, concentration, rituals
│   ├── resting.py                  # Short & Long rest recovery
│   ├── death_saves.py              # 0 HP death saves and stabilization
│   ├── encounters.py               # Encounter difficulty & XP budgeting
│   ├── loot.py                     # 5e individual & hoard treasure drops
│   ├── explainer.py                # Fuzzy 2024 mechanics search engine
│   ├── adventure_loader.py         # Modular adventure packager
│   ├── state_manager.py            # JSON/Markdown bi-directional sync
│   ├── git_versioning.py           # Snapshot commits, diffs, rollbacks
│   ├── impact_analyzer.py          # Consequential change gate
│   └── permissions.py              # Game Mode vs Developer Mode sandbox
│
├── agents/                         # Multi-Agent Subsystem
│   ├── orchestrator.py             # DAG Turn Orchestrator & Causal Tracing
│   ├── dm.py                       # Dungeon Master & Scene Atmosphere
│   ├── rules.py                    # 2024 Rules Engine & DCs
│   ├── combat.py                   # Combat Simulation
│   ├── npc.py                      # Persistent NPC Memory & Dialogue
│   ├── world.py                    # Environmental & Tactical Modifiers
│   ├── character.py                # AI Companion Commentary
│   ├── impact.py                   # Consequential Change Evaluator
│   └── developer.py                # Developer Mode Sandbox
│
├── tests/                          # 147 Automated Unit Tests (33 Test Suites)
├── dnd.py                          # Unified CLI Router & Bridge
├── pyproject.toml                  # Python Packaging Configuration
├── requirements.txt                # Zero Runtime Dependencies
├── requirements-dev.txt            # Contributor Dev Tooling
├── CONTRIBUTING.md                 # Contribution Guidelines
├── SECURITY.md                     # Security & Sandbox Model
├── CODE_OF_CONDUCT.md              # Contributor Covenant Code of Conduct
└── LICENSE                         # MIT License & SRD 5.1 / 2024 CC-BY-4.0 Notice
```

---

## 🧪 6. Testing & Continuous Integration

Run the full automated test suite anytime:
```bash
python dnd.py test
```

**Results**: **147 tests across 33 test suites passing with 100% OK (0 failures, 0 errors)**.

Run compendium schema validation:
```bash
python dnd.py compendium validate
```

**Results**: **469 entities validated with 0 errors**.

---

## 📜 7. License & Attribution

* Code is licensed under the [MIT License](LICENSE).
* D&D 5e rules compatibility is based on the **System Reference Document 5.1 (SRD 5.1 / 2024 revision)** released under the **Creative Commons Attribution 4.0 International License (CC-BY-4.0)**.
