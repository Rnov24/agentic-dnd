# 🐉 Agentic D&D (5e 2024 Revision)

**An AI-native tabletop RPG operating environment driven by multi-agent autonomous orchestration, deterministic Python mechanics, and persistent Git-style versioning.**

[![CI Status](https://img.shields.io/badge/CI-Passing-34d399?style=flat-square&logo=githubactions&logoColor=white)](https://github.com/agentic-dnd/agentic-dnd/actions)
[![D&D 5e 2024](https://img.shields.io/badge/D%26D_5e-2024_Revision-6366f1?style=flat-square)](rules/)
[![Rules Compendium](https://img.shields.io/badge/Compendium-469_Entities-38bdf8?style=flat-square)](rules/)
[![Unit Tests](https://img.shields.io/badge/Tests-158_Passing-10b981?style=flat-square)](tests/)
[![Python Version](https://img.shields.io/badge/Python-3.9_--_3.13-f59e0b?style=flat-square&logo=python&logoColor=white)](pyproject.toml)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero_External-a855f7?style=flat-square)](requirements.txt)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

---

## 🌟 1. Overview

**Agentic D&D** transforms tabletop roleplaying into an **executable, inspectable, and persistent operating system** designed for AI coding assistants (Antigravity, Claude Code, Codex) and human players.

* **Deterministic Python Mechanics (Zero Hallucinations)**: LLMs and Agents generate sensory narration, NPC dialogue, and roleplay drama, while the deterministic Python runtime evaluates dice rolls, weapon masteries, saving throw DCs, spell slots, and condition math with 100% mathematical integrity.
* **Full D&D 2024 Player's Handbook (PHB) Alignment**: 469 verified entities across 14 compendium catalogs including Weapon Masteries (*Cleave, Graze, Nick, Push, Sap, Slow, Topple, Vex*), 2024 Origin Feats & Backgrounds (+2/+1 or +1/+1/+1), and reworked spells (*Cure Wounds 2d8, Healing Word 2d4, Counterspell CON save, Sleep WIS save*).
* **Multi-Campaign Save Slots & Difficulty Modes**: Create and manage isolated campaign runs (`runs/`) with 4 distinct difficulty modes: 🟢 *Story*, 🔵 *Normal (Core 2024)*, 🟠 *Hardcore (Gritty Realism)*, and 🔴 *Deadly (Nightmare)*.
* **Global Character Vault**: Create and store persistent heroes in a global vault (`vault/`), freely recruiting or swapping party members across any campaign run.
* **Autonomous Multi-Agent Turn Orchestration**: Turn processing is executed through a Directed Acyclic Graph (DAG) of specialized subagents (`Orchestrator`, `World`, `Rules`, `Combat`, `NPC`, `Character`, `Impact`, `DM`, and `Chronos`).
* **Git-Style Versioning & Rollback**: Every turn generates an immutable commit snapshot in `state/history.json`. Players and DMs can inspect visual diffs, explore multiverse branches, and rollback state to any past turn.
* **Tri-Layer State Isolation**:
  * **Layer 1 (Static Compendiums — `rules/`)**: Immutable rules schemas and SRD 2024 compendiums.
  * **Layer 2 (Narrative Memory — `campaign/`)**: Human-readable Markdown documents (`characters/`, `locations/`, `npcs/`, `quests/`).
  * **Layer 3 (Machine State — `state/` & `runs/`)**: Machine-readable JSON state and append-only commit logs.
* **Consequential Change Gate**: High-stakes permanent events (player death, major NPC death, quest failure) require explicit human approval before mutating persistent campaign state.
* **Zero External Runtime Dependencies**: Runs out-of-the-box on standard Python 3.9+ (`Windows`, `macOS`, and `Linux`).

---

## 🎮 2. Interactive Game Dashboard & Pre-Run Setup Lobby

### Pre-Run Setup Lobby (`python dnd.py lobby`)
Before entering the field, configure difficulty, select an adventure, and recruit party members from your global vault:

```text
======================================================================
           🏰 AGENTIC D&D — CAMPAIGN LAUNCHER & RUN SETUP 🏰            
======================================================================
--- [ ACTIVE CAMPAIGN RUN: [Lost Mine Hardcore] ] ---
  Run ID: lost_mine_hardcore | Adventure: lost_mine_of_phandelver | Turns: 4
  Difficulty: 🟠 Hardcore — High-stakes tactical survival with strict death saves.

--- [ 🧙 GLOBAL CHARACTER VAULT (5 Heroes Available) ] ---
  [IN PARTY] Aria Nightwind (Lvl 1 Lightfoot Halfling Rogue) — 10/10 HP
  [IN PARTY] Eldrin of Silverymoon (Lvl 1 High Elf Wizard) — 7/7 HP
  [BENCH]    Eberk Ironfist (Lvl 1 Hill Dwarf Cleric) — 12/12 HP
  [BENCH]    Valeros of Neverwinter (Lvl 1 Human Fighter) — 12/12 HP
======================================================================
```

### Live Game Dashboard (`python dnd.py menu`)
During gameplay, view dynamic tactical and roleplay choices tailored to the active scene and actor abilities:

```text
======================================================================
             ⚔️  LOST MINE HARDCORE — GAME DASHBOARD  ⚔️              
======================================================================
  Location: wilderness | Time: Late Afternoon | Weather: Overcast
  Lighting: Dim Light | Tension: Tense | State: 🌲 Exploration

--- [ ACTIVE HERO: Aria Nightwind (Lvl 1 Lightfoot Halfling Rogue) ] ---
  Health:    [███████████████] 10/10 HP
  Armor Class: 13 | Hit Dice: 1/1 (1d8) | Conditions: None

--- [ 🎮 WHAT WOULD YOU LIKE TO DO? (TACTICAL & ROLEPLAY CHOICES) ] ---
  🔍 EXPLORATION & ENVIRONMENT:
    • Search Immediate Surroundings — Look for concealed paths, hidden loot, or traps
    • Stealth Reconnaissance — Slip through cover to scout ahead without alerting sentries

  🗣️ SOCIAL & INTERACTION:
    • Party Consultation — Discuss strategy and next steps with your companions

  ⛺ RECOVERY & PREPARATION:
    • Short Rest — Take a 1-hour rest to recharge short-rest class abilities
    • Long Rest / Make Camp — Establish a secure camp for 8 hours; full recovery

  Type your desired action in natural language or choose a tactical option above.
======================================================================
```

---

## ⚡ 3. Quickstart & Installation

### Requirements
* Python 3.9 or higher (Python 3.9, 3.10, 3.11, 3.12, 3.13)
* Standard Library only (zero third-party dependencies for gameplay)

### Installation
```bash
git clone https://github.com/Rnov24/agentic-dnd.git
cd agentic-dnd
```

### Launch Session
```bash
# Display Pre-Run Setup Lobby
python dnd.py lobby

# Enter the active campaign dashboard
python dnd.py menu

# Take an action
python dnd.py play "I search the area for goblin tracks"
```

---

## 📖 4. Comprehensive Command Reference

| Command | Action |
|---|---|
| `python dnd.py lobby` / `menu --lobby` | Display Campaign Launcher & Pre-Run Setup Lobby (runs, difficulty, party builder) |
| `python dnd.py run [list/new/switch/info/delete]` | Manage multi-campaign save slots and difficulty modes (Story, Normal, Hardcore, Deadly) |
| `python dnd.py vault [list/inspect/delete]` | Inspect and manage global Character Vault pool across all campaigns |
| `python dnd.py party [list/add/remove/roster/switch]` | Add/remove heroes from vault to active party and manage active player character |
| `python dnd.py menu` | Display full interactive game dashboard and dynamic contextual action menu |
| `python dnd.py boot` | Fast-boot session initialization and state snapshot |
| `python dnd.py play "<action>"` | Process player intent through multi-agent orchestration |
| `python dnd.py status` | View party HP/AC, current scene, threats, hit dice, spell slots, and quests |
| `python dnd.py inspect [char]` | View visual character sheet with stats, saving throws, attacks, inventory |
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
| `python dnd.py test` | Run automated unit test suite (158 tests across 37 suites) |

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
├── runs/                           # Isolated Multi-Campaign Save Slots & State
│   └── <run_id>/                   # Per-Run State, Campaign Logs & Manifest
│       ├── run_manifest.json       # Run metadata, difficulty mode & party IDs
│       ├── state/                  # Run-isolated JSON runtime state
│       └── campaign/               # Run-isolated narrative markdown logs
│
├── vault/                          # Global Reusable Character Vault
│   └── characters/                 # Persistent Hero JSON Profiles (.json)
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
│   ├── run_manager.py              # Multi-campaign runner & difficulty presets
│   ├── lobby.py                    # Pre-run setup lobby & party builder HUD
│   ├── vault.py                    # Global Character Vault manager
│   ├── action_suggester.py         # Dynamic contextual RPG action suggester
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
