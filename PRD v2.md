# Product Requirements Document: Agentic D&D 2.0

**Status:** Approved Master Architecture & Ecosystem Specification  
**Version:** 2.0.0 (Production Release)  
**Product:** Agentic D&D (Next-Gen Tabletop Operating Environment)  
**Ruleset:** D&D 5e (2024 Revision) + Modular Tabletop Rules Engine  
**Target Environments:** Antigravity IDE, Claude Code, Codex, Cursor, CLI & Autonomous Agent Runtime  
**UX Paradigm:** Narrative Theater-of-the-Mind + Inspectable Agentic Workspace + Multimodal Sensory Engine  
**AI Role:** Autonomous Dungeon Master, World Simulation, NPC Cognitive Minds, Co-Pilot  
**Human Roles:** Player (Solo / Co-Op Party), Worldbuilder, Privileged Developer  
**Mechanics Engine:** Deterministic Python Runtime (Zero-Hallucination Mathematics)  
**Persistence Layer:** Hybrid Tri-Layer (Human Markdown + Structured JSON + Vector Semantic Memory)  
**Versioning Engine:** Git-Native Multiverse Snapshots, Timeline Branching, State Diffing & Rollback  
**Security Governance:** Dual-Mode Sandboxing (Game Mode Sandbox vs Developer Elevated Mode) + Consequential Change Gates  

---

## Table of Contents

1. [Executive Summary & System Philosophy](#1-executive-summary--system-philosophy)
2. [Product Vision & Next-Gen Paradigm](#2-product-vision--next-gen-paradigm)
3. [Target Personas, Game Modes & User Journeys](#3-target-personas-game-modes--user-journeys)
4. [The 7 Inviolable Core Principles](#4-the-7-inviolable-core-principles)
5. [Dual-Mode Security Sandbox & Governance](#5-dual-mode-security-sandbox--governance)
6. [Multi-Agent System Architecture (MAS 2.0)](#6-multi-agent-system-architecture-mas-20)
7. [Agent Execution Lifecycle, Resilience & Circuit Breakers](#7-agent-execution-lifecycle-resilience--circuit-breakers)
8. [D&D 5e (2024 Revision) Rules & Mechanics Specification](#8-dd-5e-2024-revision-rules--mechanics-specification)
9. [Combat Subsystem & Tactical Theater of the Mind](#9-combat-subsystem--tactical-theater-of-the-mind)
10. [NPC Cognitive Model & Dynamic Social Simulation](#10-npc-cognitive-model--dynamic-social-simulation)
11. [Persistent Tri-Layer State Architecture](#11-persistent-tri-layer-state-architecture)
12. [Git-Style Multiverse Versioning & Timeline Branching](#12-git-style-multiverse-versioning--timeline-branching)
13. [Consequential Change & Impact Gate](#13-consequential-change--impact-gate)
14. [Antigravity Skills & CLI Interface Specification](#14-antigravity-skills--cli-interface-specification)
15. [Multiplayer & Collaborative Session Protocol](#15-multiplayer--collaborative-session-protocol)
16. [Sensory, Audio & Multi-Modal Presentation Layer](#16-sensory-audio--multi-modal-presentation-layer)
17. [Developer Platform, Modding SDK & Rule Extensions](#17-developer-platform-modding-sdk--rule-extensions)
18. [Complete Structured Data Schemas (JSON Schema v7)](#18-complete-structured-data-schemas-json-schema-v7)
19. [Comprehensive Testing & Verification Strategy](#19-comprehensive-testing--verification-strategy)
20. [Performance, Latency & Context Optimization](#20-performance-latency--context-optimization)
21. [Risk Analysis, Guardrails & Mitigations](#21-risk-analysis-guardrails--mitigations)
22. [Implementation Roadmap & Milestones (v2.0 -> v2.5)](#22-implementation-roadmap--milestones-v20---v25)
23. [Appendix & Command Cheat Sheet](#23-appendix--command-cheat-sheet)

---

# 1. Executive Summary & System Philosophy

**Agentic D&D 2.0** is an AI-native Tabletop Role-Playing Game (TTRPG) operating environment. It abandons traditional chat-wrapper paradigms to treat a tabletop campaign as an **executable, persistent, inspectable, version-controlled software project operated by specialized AI agents and deterministic toolchains**.

In Agentic D&D 2.0:
- The **Campaign** is the repository (`campaign/`, `state/`, `rules/`).
- The **AI Multi-Agent System** is the runtime operating system.
- **Python** is the deterministic mathematics and rule-validation engine.
- **Markdown & Structured JSON** form the persistent cognitive world memory.
- **Git-Style Snapshots** enable timeline branching, multiverse exploration, and instant rollback.
- **Theater of the Mind** delivers rich literary narration without requiring grid-based micromanagement.

### The v1 to v2 Evolution

| Dimension | Agentic D&D v1.0 (MVP) | Agentic D&D v2.0 (Production Platform) |
|---|---|---|
| **Agent Coordination** | Linear Pipeline (Orchestrator -> Agents) | Asynchronous DAG Multi-Agent Swarm with Parallel Tooling |
| **Rules Engine** | Core Checks, Basic Attacks, Conditions | Full D&D 2024 Rules (8 Weapon Masteries, 9 Spell Levels, Rituals, Exhaustion) |
| **State Persistence** | Markdown + Flat JSON State | Tri-Layer Hybrid (Markdown + Structured JSON + Vector Semantic Memory) |
| **Timeline Management** | Linear Commit History & Basic Rollback | Multiverse Branching, Timeline Merging, Causal Diff Trees & Replays |
| **Social Simulation** | Static NPC State (Role, Disposition) | Deep NPC Cognitive Vector (Big 5, Dynamic Disposition -100 to +100, Memory Stream) |
| **Multiplayer Support** | Single Player Intent Loop | Asynchronous Intent Queuing, Party Turn Arbitration, Role-Based Access |
| **Sensory System** | Text Narration Only | Multi-Modal Sensory Director (Lighting, Acoustics, Scents, Weather, Voice TTS) |
| **Developer Tools** | Basic File & Test Execution | Full Modding SDK (`@dnd_tool`), Schema Migration Engine, Auto-Scaffolders |
| **Test Verification** | 35 Unit Tests | 100+ Tests (Deterministic Checks, Concurrency, Invariant & Penetration Tests) |

---

# 2. Product Vision & Next-Gen Paradigm

> **"Transform Dungeons & Dragons from a static conversation into an autonomous, deterministic, persistent simulation where AI agents direct the living world, mathematical tools guarantee absolute rule integrity, and humans interact through pure intent."**

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AGENTIC D&D 2.0 RUNTIME                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   HUMAN INTENT:                                                             │
│   > "I slip out of the shadows, plunge my dagger into the cultist leader,   │
│      kick the altar over to break the ritual, and yell for Eldrin to run."  │
│                                                                             │
│   ORCHESTRATOR DAG EXECUTION:                                               │
│   ├─► [World Agent]      Evaluate darkness (Dim Light -> Advantage on Sneak)│
│   ├─► [Rules Agent]      Resolve Stealth Check (DC 14), Attack vs AC 13     │
│   ├─► [Python Tool]      d20=18+4=22 (Sneak Success), d20=19+5=24 (Hit)     │
│   ├─► [Combat Agent]     Damage: 1d4+3 + 2d6 Sneak Attack = 14 Piercing     │
│   ├─► [NPC Agent]        Cultist HP: 12 -> 0 (Incapacitated / Dying)        │
│   ├─► [Character Agent]  AI Companion Eldrin readies Dash action            │
│   ├─► [State Agent]      Mutate cultist, altar state, active quest flags    │
│   ├─► [Impact Agent]     Impact: High (Major Ritual Disrupted) -> Auto-Log  │
│   ├─► [Chronos Agent]    Record Snapshot Commit [a7f3c91e]                  │
│   └─► [DM Agent]         Renders atmospheric Theater-of-the-Mind Narration  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

The game operates as an agentic software repository. Every location, NPC, monster, item, and quest is an inspectable file. Game actions are deterministic functions executed by Python. Timeline changes are Git-style commits. Narrations are rendered in rich literary prose with spatial awareness.

---

# 3. Target Personas, Game Modes & User Journeys

## 3.1 Personas

### 1. Solo Adventurer
- **Profile:** Player desiring rich, uninterrupted, solo tabletop campaigns.
- **Experience:** Zero DM overhead. AI orchestrates the entire world, encounters, companions, and story twists with zero mechanical friction.

### 2. Multi-Human Co-Op Party
- **Profile:** 2 to 6 human players participating in a shared campaign.
- **Experience:** Each human commands their own character via agent chat or CLI. The AI DM arbitrates party turns, initiative, synchronized state, and inter-character dialogue.

### 3. AI Companion Enthusiast
- **Profile:** Solo or duo human players seeking fully fleshed out AI party companions.
- **Experience:** AI companions have distinct psychological traits, memories, tactical combat instincts, and organic conversational banter.

### 4. Human DM Co-Pilot / Worldbuilder
- **Profile:** A human Dungeon Master running a live game who uses Agentic D&D as a mechanical co-pilot.
- **Experience:** Instant rule lookups, automated monster turns, dynamic sensory generation, and persistent lore tracking without breaking narrative flow.

### 5. Tabletop Engine Developer / Modder
- **Profile:** Developer creating custom campaigns, importing homebrew rules (e.g. Sanity, Cyberpunk, Gritty Realism), creating new tools, and running automated test suites.

## 3.2 User Journeys

```text
Player Turn Execution Journey in Agentic D&D 2.0:
1. Input: Player enters natural language intent -> Orchestrator parses goals
2. Mechanics: World & Rules agents inspect context -> Deterministic Python math computes outcomes
3. Dynamic Simulation: Combat Agent computes damage/conditions -> NPC Agent evaluates memory/reactions
4. State & Safety: Impact Agent tests approval gate -> State Agent persists Markdown & JSON -> Chronos snapshots commit
5. Delivery: DM Agent crafts sensory Theater-of-the-Mind prose -> Sensory Director outputs audio cues
```

---
# 4. The 7 Inviolable Core Principles

1. **Zero-Hallucination Determinism:** All dice rolls, DC checks, AC hits, saving throws, damage formulas, spell slot deductions, and condition applications are executed strictly in Python. The LLM *never* invents numbers or calculates dice math.
2. **Theater of the Mind with Spatial Math:** The narrative presentation is pure literary prose (describing distances, lighting, cover, and line of sight). The underlying engine computes coordinate ranges and zone distances deterministically without requiring a 2D/3D visual grid.
3. **Dual-Mode Security Sandboxing:** A strict wall separates Game Mode (sandboxed state mutations, allowlisted mechanics) from Developer Mode (elevated authority to edit engine code, agents, tools, and run arbitrary scripts).
4. **Consequential Change & Irreversibility Gating:** Irreversible catastrophic events (Player death, major faction leader demise, permanent relic destruction, quest failure) trigger a human approval gate before state commits.
5. **Inspectable Tri-Layer Persistence:** All game state is transparent and synchronized across human-readable Markdown (`campaign/`), structured machine JSON (`state/`), and vector memory (`state/embeddings/`).
6. **Git-Style Multiverse Versioning:** Every game action produces an immutable content-addressable commit snapshot. Players can explore alternate timelines, view diffs, branch realities, and rollback to any turn.
7. **Autonomous Loop Safety & Circuit Breakers:** Multi-agent execution is bounded by maximum step limits, token budgets, loop cycle detectors, and deterministic fallbacks.

---

# 5. Dual-Mode Security Sandbox & Governance

```text
                             SYSTEM GOVERNANCE
                                     │
                 ┌───────────────────┴───────────────────┐
                 │                                       │
                 ▼                                       ▼
        [DEVELOPER MODE]                            [GAME MODE]
     Elevated Authority Sandbox                  Strict Gameplay Sandbox
                 │                                       │
   ├─► Read/Write All Files (Code/Rules/Agents)   ├─► Read Campaign & Rules Docs
   ├─► Create & Refactor Python Tools            ├─► Call Approved Mechanics Tools
   ├─► Modify JSON Schemas                       ├─► Mutate Permitted Game State
   ├─► Run Test Suites & Shell Execution         ├─► Append Commit History
   └─► Rebase & Merge Multiverse Branches        └─► Trigger Approval Gates
                                                         │
                                                 [FORBIDDEN IN GAME MODE]
                                                 ✖ No Shell Execution
                                                 ✖ No Engine Code Mutation
                                                 ✖ No Tool Creation
                                                 ✖ No Sandbox Escalation
```

### Game Mode Tool Allowlist Matrix

```json
{
  "allowlisted_tools": [
    "dice.roll",
    "mechanics.check",
    "mechanics.saving_throw",
    "mechanics.contest",
    "combat.attack",
    "combat.damage",
    "combat.apply_condition",
    "combat.remove_condition",
    "combat.heal",
    "spells.cast",
    "spells.consume_slot",
    "inventory.transfer",
    "state.read",
    "state.update_character",
    "state.update_npc",
    "state.update_world",
    "state.update_quest",
    "git.commit",
    "git.history",
    "impact.evaluate"
  ],
  "forbidden_tools": [
    "os.system",
    "subprocess.Popen",
    "eval",
    "exec",
    "fs.delete_file",
    "tools.create_tool",
    "permissions.elevate"
  ]
}
```

---

# 6. Multi-Agent System Architecture (MAS 2.0)

Agentic D&D 2.0 replaces linear chaining with an asynchronous **Directed Acyclic Graph (DAG)** orchestration system.

```text
                      ┌──────────────────────┐
                      │ User Intent / Action │
                      └──────────┬───────────┘
                                 │
                                 ▼
                      ┌──────────────────────┐
                      │  Orchestrator Agent  │
                      └──────────┬───────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
   [World Agent]           [Rules Agent]          [Character Agent]
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                                 ▼
                      ┌──────────────────────┐
                      │ Deterministic Python │
                      │     Tool Runtime     │
                      └──────────┬───────────┘
                                 │
         ┌───────────────────────┴───────────────────────┐
         ▼                                               ▼
   [Combat Agent]                                [NPC Cognitive Agent]
         │                                               │
         └───────────────────────┬───────────────────────┘
                                 │
                                 ▼
                      ┌──────────────────────┐
                      │ State Manager Agent  │
                      └──────────┬───────────┘
                                 │
                                 ▼
                      ┌──────────────────────┐
                      │ Impact Analyzer Gate │
                      └──────────┬───────────┘
                                 │
                                 ▼
                      ┌──────────────────────┐
                      │ Chronos Versioning   │
                      └──────────┬───────────┘
                                 │
         ┌───────────────────────┴───────────────────────┐
         ▼                                               ▼
     [DM Agent]                              [Sensory Director Agent]
         │                                               │
         └───────────────────────┬───────────────────────┘
                                 │
                                 ▼
                      ┌──────────────────────┐
                      │  Narrative Delivery  │
                      │  + Diffs + Audio     │
                      └──────────────────────┘
```

### Specialized Agent Specifications

| Agent Name | Core Responsibilities | Model Tier Recommendation | Primary Tools Utilized |
|---|---|---|---|
| **Orchestrator** | Intent decomposition, DAG dispatch, execution budgeting, loop termination | `pro` / `inherit` | `permissions.py`, `state_manager.py` |
| **DM Agent** | Theater-of-the-Mind prose, sensory narration, scene pacing, dramatic tension | `pro` / `inherit` | `state_manager.py`, `world.py` |
| **Rules Agent** | D&D 2024 mechanics resolution, DC determination, Action economy validation | `flash` / `inherit` | `rules_engine.py`, `mechanics.py` |
| **Combat Agent** | Initiative tracking, enemy tactical AI, range & cover arbitration, damage calculation | `flash` / `inherit` | `combat.py`, `dice.py` |
| **NPC Cognitive Agent**| Psychological traits, Big-5 vectors, episodic memory recall, dialogue styling | `pro` / `flash` | `state_manager.py`, vector recall |
| **World Agent** | Weather, lighting, factions, spatial zones, environmental hazards, passage of time | `flash` / `inherit` | `state_manager.py` |
| **Character Agent** | AI party companion simulation, tactical advice, organic party banter | `pro` / `flash` | `combat.py`, `state_manager.py` |
| **State Manager Agent**| Tri-layer persistence synchronization, schema validation, checksum verification | `flash_lite` / `inherit` | `state_manager.py` |
| **Impact Analyzer** | 4-tier consequential change classification, approval modal generation | `flash_lite` / `inherit` | `impact_analyzer.py` |
| **Chronos Agent** | Content-addressable SHA commits, unified diffs, multiverse branch management | `flash_lite` / `inherit` | `git_versioning.py` |
| **Sensory Director** | Environmental acoustics, lighting levels, olfactory cues, voice TTS dispatch | `flash_lite` / `inherit` | Sensory API, Audio sidecar |
| **Developer Agent** | Privileged code creation, schema migrations, tool scaffolding, test execution | `pro` / `inherit` | Full Python runtime, test runners |

---
# 7. Agent Execution Lifecycle, Resilience & Circuit Breakers

To guarantee rock-solid runtime stability and eliminate agent stalls or infinite loops, every turn adheres to strict execution budgets:

```text
Turn Start
  │
  ├─► [Budget Allocated: Max 12 Agent Steps | 30s Timeout | 8000 Token Ceiling]
  │
  ├─► Step 1: Orchestrator Intent Decomposition
  ├─► Step 2: Parallel Context Query (World + Rules + Character)
  ├─► Step 3: Tool Execution (Deterministic Python Engine)
  ├─► Step 4: State Mutation & Schema Validation
  ├─► Step 5: Impact Analysis
  │     ├── High Impact? -> Suspend loop, render Approval Modal, await input.
  │     └── Low/Medium Impact? -> Auto-commit.
  ├─► Step 6: Chronos Commit Snapshot
  ├─► Step 7: DM Theater-of-the-Mind Narration
  │
Turn Complete
```

### Circuit Breaker Specifications
1. **Max Steps Circuit Breaker:** If an orchestrator loop exceeds 12 discrete sub-agent steps, execution halts, commits the intermediate safe state, and falls back to DM narration with a status advisory.
2. **Loop Cycle Detector:** If the identical tool signature is called >= 3 times with identical parameters in a single turn, the loop aborts the repeated call and forces a resolution step.
3. **State Invariant Validator:** Before committing, the State Manager verifies JSON schema validity and invariant constraints (e.g. 0 <= HP <= Max HP + Temp HP, Spell Slots >= 0).

---

# 8. D&D 5e (2024 Revision) Rules & Mechanics Specification

Agentic D&D 2.0 implements the complete mechanical framework of the 2024 revision of D&D 5e.

## 8.1 The Core D20 Test
All resolution uses the standard formula:
Total = d20 Roll + Ability Modifier + Proficiency Bonus (if applicable) + Circumstantial Modifiers

- **Natural 20 (Critical Success):** Automatic hit in combat (damage dice doubled). Grants Heroic Inspiration in 2024 rules.
- **Natural 1 (Critical Fumble):** Automatic miss in combat regardless of modifiers.

### Standard Difficulty Classes (DC)
| Difficulty | Target DC | Typical Feat |
|---|---|---|
| Very Easy | 5 | Spotting a torch in darkness; climbing an untied ladder |
| Easy | 10 | Picking a rusted lock; recalling common local lore |
| Medium | 15 | Slipping past an alert guard; deciphering an archaic glyph |
| Hard | 20 | Picking a masterwork vault; convincing a hostile captain to retreat |
| Very Hard | 25 | Swimming across a raging whirlpool; identifying a lost ancient relic |
| Nearly Impossible | 30 | Tracking an invisible assassin through a torrential rainstorm |

## 8.2 2024 Weapon Mastery System
Every weapon in the 2024 rules possesses a Weapon Mastery property that triggers deterministically on qualifying attacks:

```json
{
  "weapon_masteries": {
    "cleave": {
      "trigger": "On melee hit",
      "effect": "Make a second attack against an adjacent target within 5ft using weapon damage die without ability modifier."
    },
    "graze": {
      "trigger": "On weapon miss",
      "effect": "Target still takes damage equal to the ability modifier used for the attack roll (minimum 1)."
    },
    "nick": {
      "trigger": "On Light weapon Extra Attack",
      "effect": "Make the additional off-hand attack as part of the Attack action rather than consuming a Bonus Action."
    },
    "push": {
      "trigger": "On hit",
      "effect": "Push target up to 10 feet straight away if it is Large or smaller."
    },
    "sap": {
      "trigger": "On hit",
      "effect": "Target has Disadvantage on its next attack roll before the start of your next turn."
    },
    "slow": {
      "trigger": "On damage",
      "effect": "Target speed is reduced by 10 feet until the start of your next turn."
    },
    "topple": {
      "trigger": "On hit",
      "effect": "Target must succeed on a Constitution saving throw (DC = 8 + Str Mod + Prof) or fall Prone."
    },
    "vex": {
      "trigger": "On hit and damage",
      "effect": "Gain Advantage on your next attack roll against that target before the end of your next turn."
    }
  }
}
```

## 8.3 Full Magic & Spellcasting Subsystem
1. **Spell Slot Progression:** Tracks 1st through 9th level spell slots, pact magic, and cantrip scaling (levels 1, 5, 11, 17).
2. **Ritual Casting:** 2024 rules permit any character with ritual spells prepared to cast them as rituals (adds 10 minutes, costs 0 spell slots).
3. **Concentration Arbitration:**
   - Only 1 concentration spell active at a time per caster.
   - Taking damage triggers a Constitution saving throw: Concentration DC = max(10, floor(Damage Taken / 2)).
   - Failing the save instantly removes the active spell effect and clears concentration state.
4. **Upcasting Math:** Spells automatically scale damage formulas, target counts, or duration when cast with higher-level slots.
5. **Counterspell Resolution (2024 Rule):** Counterspell triggers a Constitution saving throw by the original caster against the counterspeller Spell Save DC. On a failed save, the spell fails and the slot is wasted.

## 8.4 Exhaustion (2024 Revised Rule)
Exhaustion has 6 progressive levels:
- Each level inflicts a -2 penalty to all d20 tests (attack rolls, ability checks, saving throws).
- Each level reduces Speed by 5 feet.
- Level 6 results in immediate death.
- Long rest removes 1 level of Exhaustion provided the character has sufficient food and water.

## 8.5 Complete 14-Condition State Matrix
`rules/dnd2024/conditions.md` and `rules_engine.py` manage the full condition lifecycle:
`blinded`, `charmed`, `deafened`, `exhaustion`, `frightened`, `grappled`, `incapacitated`, `invisible`, `paralyzed`, `petrified`, `poisoned`, `prone`, `restrained`, `stunned`, `unconscious`.

---

# 9. Combat Subsystem & Tactical Theater of the Mind

Combat in Agentic D&D 2.0 is fast, visceral, and strictly calculated.

```text
                                COMBAT ROUND FLOW
                                        │
        ┌───────────────────────────────┴───────────────────────────────┐
        │                                                               │
        ▼                                                               ▼
   [SURPRISE & INITIATIVE]                                      [ROUND PROGRESSION]
   - Stealth vs Passive Perception                              - Ordered by Initiative
   - Initiative: d20 + DEX Mod                                  - Active Turn Economy:
                                                                  • Action (1)
                                                                  • Bonus Action (1)
                                                                  • Reaction (1)
                                                                  • Movement (ft)
                                                                  • Free Interaction (1)
                                                                        │
        ┌───────────────────────────────────────────────────────────────┘
        │
        ▼
   [ATTACK & DAMAGE RESOLUTION]
   1. Check Range & Tactical Zone (Melee / Close / Medium / Long)
   2. Apply Cover (+2 Half Cover / +5 3/4 Cover / Total Cover)
   3. Check Advantage / Disadvantage (Conditions, Lighting, Help)
   4. Roll d20 vs Target AC
   5. If Hit -> Roll Damage Formula + Modifiers + Weapon Mastery Triggers
   6. Apply Damage vs Resistances, Vulnerabilities & Temp HP
   7. Target HP == 0? -> Unconscious / Dying / Death Saves / Impact Gate
```

### Spatial Zones in Theater of the Mind
To eliminate the need for grid maps while preserving exact tactical math, the combat engine maintains distance zones:

| Zone Name | Distance from Party Center | Valid Attacks / Actions |
|---|---|---|
| **Engaged (Melee)** | 0 – 5 ft | Melee attacks, Shove, Grapple, Cleave, Topple |
| **Close Range** | 6 – 30 ft | Standard movement, short-range spells, Thrown weapons |
| **Medium Range** | 31 – 60 ft | Dash required for melee; standard bows, cantrips |
| **Long Range** | 61 – 120 ft | Longbow (normal), heavy crossbow, Fireball |
| **Extreme Range** | 121 – 300+ ft | Longbow (disadvantage), sniper spells, scouting |

---
# 10. NPC Cognitive Model & Dynamic Social Simulation

NPCs in Agentic D&D 2.0 are persistent psychological agents rather than static statblocks.

```json
{
  "npc_schema_v2": {
    "id": "captain_aldric",
    "name": "Captain Aldric",
    "role": "Garrison Commander",
    "disposition_score": -35,
    "disposition_tier": "Unfriendly",
    "psychological_profile": {
      "openness": 20,
      "conscientiousness": 90,
      "extraversion": 65,
      "agreeableness": 30,
      "neuroticism": 45
    },
    "core_instincts": [
      "Maintain garrison order at all costs",
      "Distrust cloaked or rogue-like strangers",
      "Protect royal secrets"
    ],
    "memory_stream": [
      {
        "turn": 3,
        "event": "Caught Aria tampering with dungeon cell lock",
        "emotional_impact": "Heightened suspicion",
        "disposition_delta": -20
      }
    ],
    "dialogue_style": {
      "tone": "Commanding, gruff, impatient",
      "syntax": "Short declarative sentences, military jargon"
    }
  }
}
```

### Disposition Scale
- **-100 to -60 (Hostile):** Attacks on sight or commands arrest.
- **-59 to -10 (Unfriendly):** Refuses assistance; high Charisma check DCs (+5 DC).
- **-9 to +20 (Neutral):** Transactional; standard DCs.
- **+21 to +69 (Friendly):** Helpful, shares rumors, grants discounts (-5 DC).
- **+70 to +100 (Devoted):** Will risk safety to defend or aid the party.

---

# 11. Persistent Tri-Layer State Architecture

Agentic D&D 2.0 implements a **Tri-Layer Hybrid Storage Model**:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TRI-LAYER HYBRID STORAGE ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  TIER 1: HUMAN-READABLE MARKDOWN (`campaign/`)                             │
│  ├── characters/*.md    (Character identity, lore, equipment, background)   │
│  ├── npcs/*.md          (NPC profiles, relationships, dialogue notes)       │
│  ├── locations/*.md     (Atmospheric descriptions, sensory notes, exits)    │
│  ├── quests/*.md        (Narrative objectives, clues, rewards)              │
│  └── sessions/*.md      (Chronological session logs & chapter summaries)    │
│                                                                             │
│  TIER 2: STRUCTURED RUNTIME JSON (`state/`)                                 │
│  ├── world.json         (Scene state, lighting, weather, tension, time)     │
│  ├── party.json         (Stats, HP, spell slots, inventory, conditions)     │
│  ├── npcs.json          (Numerical stats, disposition scores, memories)     │
│  ├── combat.json        (Initiative tracker, active rounds, turn index)     │
│  ├── quests.json        (Objective booleans, progression stages, flags)     │
│  ├── relationships.json (Faction standing, inter-character graph)           │
│  └── history.json       (Git commit stream, branch pointers, head SHA)      │
│                                                                             │
│  TIER 3: SEMANTIC VECTOR RETRIEVAL (`state/embeddings/` / SQLite-Vec)       │
│  ├── Episodic NPC memory retrieval (cosine similarity query on past turns)  │
│  ├── Campaign lore & world history semantic cross-referencing              │
│  └── Rulebook semantic lookup for edge-case rulings                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Bi-Directional Synchronization Protocol
Whenever a state mutation occurs:
1. Structured JSON in `state/` is updated and validated against schemas.
2. The corresponding Markdown file in `campaign/` is updated via structured template injection.
3. SHA-256 state checksums are verified to guarantee zero drift between Markdown and JSON representations.

---

# 12. Git-Style Multiverse Versioning & Timeline Branching

Every turn in Agentic D&D produces an immutable, content-addressable commit snapshot:

```text
   [main] (Commit: c1b9e02a) - "Aria infiltrates dungeon cells"
     │
     ├──► [timeline-fork-aldric-killed] (Commit: f82d910b) - "Captain Aldric slain"
     │      │
     │      └──► (Commit: e41a027c) - "Garrison goes on high alert, gates barred"
     │
     └──► [timeline-fork-aldric-bribed] (Commit: 730d6e1a) - "Captain Aldric accepts 100gp bribe"
            │
            └──► (Commit: b59c814f) - "Aria escorted safely to outer courtyard"
```

### Multiverse Versioning Commands & API
- **`dnd.py history [--branch <name>]`**: Displays chronological commit DAG.
- **`dnd.py diff <commit_id>`**: Generates unified diff of state and campaign files.
- **`dnd.py branch <branch_name>`**: Forks the active reality into an alternate timeline.
- **`dnd.py rollback <commit_id>`**: Restores full game state and Markdown files to any prior snapshot without destructive history deletion.

---

# 13. Consequential Change & Impact Gate

To protect story continuity and give players agency over irreversible world events, the **Impact Analyzer Agent** classifies all mutations:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CONSEQUENTIAL CHANGE CLASSIFICATION                      │
├──────────────┬───────────────────────────────┬──────────────────────────────┤
│ Impact Tier  │ Examples                      │ Execution Policy             │
├──────────────┼───────────────────────────────┼──────────────────────────────┤
│ Tier 1: Low  │ HP loss, torch lit, minor item│ Auto-apply & commit silently │
│ Tier 2: Med  │ Spell slot spent, NPC annoyed │ Auto-apply & record in trace │
│ Tier 3: High │ Ritual halted, ally wounded   │ Auto-apply & highlight diff  │
│ Tier 4: CRIT │ Character death, major NPC    │ HARD GATE: Requires explicit │
│              │ slain, artifact destroyed,    │ human approval via modal or  │
│              │ faction citadel collapsed     │ `python dnd.py approve`      │
└──────────────┴───────────────────────────────┴──────────────────────────────┘
```

### Approval Modal Payload Example
```json
{
  "consequential_event": {
    "action": "Execute NPC: Captain Aldric",
    "cause": "Critical hit from Black Glass Dagger (24 damage vs 18 current HP)",
    "impact_tier": "CRITICAL",
    "affected_documents": [
      "campaign/npcs/captain_aldric.md",
      "campaign/factions/royal_garrison.md",
      "campaign/quests/escape_the_fort.md",
      "state/npcs.json",
      "state/world.json"
    ],
    "before_state": { "captain_aldric_status": "Alive", "garrison_alert": "Normal" },
    "after_state": { "captain_aldric_status": "Dead", "garrison_alert": "High Alert - Lockdown" },
    "approval_options": [
      { "decision": "approve", "command": "python dnd.py approve --decision approve" },
      { "decision": "reject", "command": "python dnd.py approve --decision reject" }
    ]
  }
}
```

---
# 14. Antigravity Skills & CLI Interface Specification

Agentic D&D 2.0 provides 7 native skills registered under `.agents/skills/`:

| Skill | Directory | Primary Trigger & Purpose |
|---|---|---|
| `dnd-play` | `.agents/skills/dnd-play/` | Natural-language player turns, status checks, gameplay loop |
| `dnd-dm` | `.agents/skills/dnd-dm/` | Theater-of-the-Mind narration, sensory descriptions, scene pacing |
| `dnd-rules` | `.agents/skills/dnd-rules/` | D&D 2024 rules checks, ability checks, weapon masteries, conditions |
| `dnd-versioning`| `.agents/skills/dnd-versioning/`| Git snapshots, timeline branching, diffs, rollback |
| `dnd-dev` | `.agents/skills/dnd-dev/` | Developer Mode: tool creation, schema edits, test runner |
| `dnd-spells` | `.agents/skills/dnd-spells/` | Spellcasting, slot management, concentration, rituals |
| `dnd-multiverse`| `.agents/skills/dnd-multiverse/`| Alternate timeline exploration and timeline merge arbitration |

### Full CLI Command Matrix (`dnd.py`)

```bash
# Gameplay & Intent Execution
python dnd.py play "<intent>" [--character <id>] [--seed <int>] [--no-commit] [--json]
python dnd.py status [--json]
python dnd.py approve --decision <approve|reject>

# Deterministic Mechanics Tools
python dnd.py roll "<expression>" [--adv] [--disadv] [--crit] [--bonus <int>] [--seed <int>] [--json]
python dnd.py check <skill> [dc] [--character <id>] [--adv] [--disadv] [--guidance] [--bonus <int>] [--json]
python dnd.py attack <target> [--attacker <id>] [--weapon <name>] [--adv] [--disadv] [--bonus <int>] [--json]
python dnd.py cast <spell> <target> [--caster <id>] [--level <int>] [--json]
python dnd.py rest <short|long> [--character <id>] [--json]

# Git Versioning & Multiverse
python dnd.py history [--branch <name>] [--limit <int>] [--json]
python dnd.py diff <commit_id> [--json]
python dnd.py rollback <commit_id>
python dnd.py branch <branch_name>

# Developer & Test Suite
python dnd.py test [--verbose]
python dnd.py dev "<developer_task_prompt>"
```

---

# 15. Multiplayer & Collaborative Session Protocol

Agentic D&D 2.0 supports multi-human collaborative campaigns with role-based access:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MULTIPLAYER SESSION ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Human Player 1: Aria (Rogue)]    ──► [Intent: "I pick the lock"]         │
│  [Human Player 2: Eldrin (Wizard)] ──► [Intent: "I cast Minor Illusion"]   │
│                                                   │                         │
│                                                   ▼                         │
│                                     ┌───────────────────────────┐           │
│                                     │ Multi-Party Turn Manager  │           │
│                                     │ - Shared Initiative Queue │           │
│                                     │ - Turn Conflict Arbitrator│           │
│                                     │ - Synchronized State Lock │           │
│                                     └─────────────┬─────────────┘           │
│                                                   ▼                         │
│                                     [Multi-Agent Orchestrator]              │
│                                                   │                         │
│                                                   ▼                         │
│                                     [Unified DM Narration & Diff]           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

1. **Party Intent Queue:** In non-combat exploration, players can submit intents simultaneously. The Orchestrator orders them by logical causality or Dexterity.
2. **Turn Arbitration:** In combat, turns strictly follow the deterministic initiative order tracked in `state/combat.json`.
3. **Character Authority Sandbox:** Player 1 cannot mutate Player 2's character sheet without explicit permission.

---

# 16. Sensory, Audio & Multi-Modal Presentation Layer

Theater of the Mind is enhanced with dynamic sensory and multi-modal integration:

```json
{
  "sensory_state": {
    "lighting": "Dim, flickering torchlight with deep shadows",
    "acoustics": "Distant water droplets echoing against wet cobblestone; muffled guard footsteps above",
    "olfactory": "Damp moss, ozone from arcane residue, rusted iron",
    "temperature": "Chilling 48°F draft blowing from dungeon grating",
    "atmospheric_tension": "High (Guards actively searching)",
    "audio_cues": {
      "ambient_track": "dungeon_ambience_loop_03.mp3",
      "sound_effects": ["iron_lock_click.wav", "torch_sputter.wav"]
    }
  }
}
```

- **Voice DM Integration:** Hooks for low-latency streaming Text-to-Speech (TTS) delivering expressive, dramatic voice acting for narration and distinct NPC voices.
- **Generative Artifact Visualizer:** Hooks to render visual inspectable documents (e.g. ancient maps, ciphered letters, bounty posters) directly into the agent workspace.

---

# 17. Developer Platform, Modding SDK & Rule Extensions

Developer Mode allows developers to extend the engine safely:

### Creating a Custom Tool via the SDK
```python
from tools.permissions import developer_only, dnd_tool

@dnd_tool(name="fear.check", description="Evaluates a character fear check against horror DC")
@developer_only
def roll_fear_check(character_id: str, horror_dc: int = 15, seed: int = None) -> dict:
    from tools.mechanics import roll_saving_throw
    from tools.state_manager import StateManager
    
    sm = StateManager()
    char = sm.get_character(character_id)
    save_result = roll_saving_throw(char, ability="wisdom", dc=horror_dc, seed=seed)
    
    if not save_result["success"]:
        char["conditions"] = list(set(char.get("conditions", []) + ["frightened"]))
        sm.update_character(char)
        
    return {
        "character": char["name"],
        "save_result": save_result,
        "frightened_applied": not save_result["success"]
    }
```

---
# 18. Complete Structured Data Schemas (JSON Schema v7)

### 18.1 Party Character Schema (`state/party.json`)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PartyCharacter",
  "type": "object",
  "required": ["id", "name", "class", "level", "ac", "hp", "stats", "is_player"],
  "properties": {
    "id": { "type": "string" },
    "name": { "type": "string" },
    "class": { "type": "string" },
    "subclass": { "type": "string" },
    "level": { "type": "integer", "minimum": 1, "maximum": 20 },
    "is_player": { "type": "boolean" },
    "ac": { "type": "integer", "minimum": 1 },
    "speed": { "type": "integer", "default": 30 },
    "hp": {
      "type": "object",
      "required": ["current", "max", "temp"],
      "properties": {
        "current": { "type": "integer", "minimum": 0 },
        "max": { "type": "integer", "minimum": 1 },
        "temp": { "type": "integer", "minimum": 0 }
      }
    },
    "stats": {
      "type": "object",
      "required": ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"],
      "properties": {
        "strength": { "type": "integer", "minimum": 1, "maximum": 30 },
        "dexterity": { "type": "integer", "minimum": 1, "maximum": 30 },
        "constitution": { "type": "integer", "minimum": 1, "maximum": 30 },
        "intelligence": { "type": "integer", "minimum": 1, "maximum": 30 },
        "wisdom": { "type": "integer", "minimum": 1, "maximum": 30 },
        "charisma": { "type": "integer", "minimum": 1, "maximum": 30 }
      }
    },
    "proficiencies": {
      "type": "object",
      "properties": {
        "skills": { "type": "array", "items": { "type": "string" } },
        "expertise": { "type": "array", "items": { "type": "string" } },
        "saving_throws": { "type": "array", "items": { "type": "string" } }
      }
    },
    "spell_slots": {
      "type": "object",
      "patternProperties": {
        "^[1-9]$": {
          "type": "object",
          "properties": {
            "current": { "type": "integer", "minimum": 0 },
            "max": { "type": "integer", "minimum": 0 }
          }
        }
      }
    },
    "conditions": { "type": "array", "items": { "type": "string" } },
    "inventory": { "type": "array", "items": { "type": "string" } }
  }
}
```

### 18.2 Combat State Schema (`state/combat.json`)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CombatState",
  "type": "object",
  "required": ["is_active", "round", "turn_index", "combatants"],
  "properties": {
    "is_active": { "type": "boolean" },
    "round": { "type": "integer", "minimum": 0 },
    "turn_index": { "type": "integer", "minimum": 0 },
    "combatants": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "name", "initiative", "is_player", "hp"],
        "properties": {
          "id": { "type": "string" },
          "name": { "type": "string" },
          "initiative": { "type": "integer" },
          "is_player": { "type": "boolean" },
          "zone": { "type": "string", "enum": ["engaged", "close", "medium", "long", "extreme"] },
          "conditions": { "type": "array", "items": { "type": "string" } }
        }
      }
    }
  }
}
```

---

# 19. Comprehensive Testing & Verification Strategy

Agentic D&D 2.0 maintains a rigorous 100+ automated test suite across 5 critical testing pillars:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       AUTOMATED TEST SUITE TOPOLOGY                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [1. Deterministic Mechanics Tests] (tests/test_dice.py, test_mechanics.py) │
│  - Exact formula verification (crits, fumbles, advantage, disadvantage)     │
│  - 2024 DC evaluations & skill checks with proficiency & expertise          │
│  - Damage resistance, vulnerability, and temp HP absorption calculations    │
│                                                                             │
│  [2. Combat & Action Economy Tests] (tests/test_combat.py)                  │
│  - Weapon mastery trigger executions (Nick, Vex, Topple, Cleave, Graze)    │
│  - Death saving throws & instant perma-death massive damage threshold       │
│  - Tactical zone distances and cover modifier applications                  │
│                                                                             │
│  [3. Multi-Agent & Orchestration Tests] (tests/test_multi_agent_flow.py)    │
│  - Multi-step DAG intent resolution & step trace generation                 │
│  - NPC cognitive disposition updates & memory stream persistence           │
│  - AI companion assist behaviors                                            │
│                                                                             │
│  [4. Persistence & Git Versioning Tests] (tests/test_git_versioning.py)     │
│  - Content-addressable SHA commit integrity & rollback accuracy             │
│  - Bi-directional Markdown and JSON synchronization invariants              │
│  - Multiverse timeline branch creation and timeline diff verification       │
│                                                                             │
│  [5. Security & Sandbox Governance Tests] (tests/test_permissions.py)       │
│  - Game Mode isolation & privilege escalation attack containment            │
│  - Consequential change detection & approval gate modal payload validation  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Running Tests:**
```bash
python dnd.py test
```
*Acceptance Criterion: 100% Pass Rate across all unit, integration, and security tests.*

---

# 20. Performance, Latency & Context Optimization

1. **Tiered Model Routing:**
   - Complex Narration / DM / Developer Tasks -> High-reasoning Models (`pro` / `inherit`).
   - Fast Deterministic Evaluation / State Queries / Checks -> High-speed Models (`flash` / `flash_lite`).
2. **Context Window Compaction:**
   - Active Working Context retains current scene, party sheet, threats, and last 3 turns of dialogue.
   - Older session history is compressed into episodic Markdown summaries in `campaign/sessions/`.
3. **Sub-Second Tool Execution:**
   - Python deterministic tools execute in < 5ms. Full multi-agent turns complete in < 1.5s.

---

# 21. Risk Analysis, Guardrails & Mitigations

| Identified Risk | Severity | Failure Mode | Mitigation in 2.0 |
|---|---|---|---|
| **Agent Math Hallucination** | CRITICAL | LLM invents dice roll or miscalculates hit AC | Pure Python toolchain. All numbers originate in Python; LLM merely narrates output. |
| **State File Drift** | HIGH | Markdown text says HP 10 but JSON says HP 20 | Synchronized State Manager with SHA-256 checksum validation upon every commit. |
| **Agent Infinite Loops** | HIGH | Orchestrator endlessly re-queries sub-agents | 12-Step Hard Circuit Breaker & 3-Call Cycle Detector. |
| **Accidental Character Perma-Death** | HIGH | Bad roll kills player character instantly | Impact Analyzer Gate halts state commit and demands explicit human approval. |
| **Sandbox Privilege Escalation** | CRITICAL | Game Mode agent attempts to execute shell commands | Strict RuntimeMode enum gate + tool allowlist validation before execution. |

---

# 22. Implementation Roadmap & Milestones (v2.0 -> v2.5)

```text
Phase 1 (v2.0 Base): Complete
├── Deterministic Python Engine & 35 Unit Tests
├── Git Snapshots, Diffs & Rollback Engine
└── Antigravity Native Skills & CLI Router

Phase 2 (v2.1 Spells & Masteries):
├── Full 2024 Weapon Mastery System Integration
└── Complete Spellcasting & Ritual Engine

Phase 3 (v2.2 Multiverse & Memory):
├── Multiverse Timeline Branching & Visual Diff GUI
└── Vector Semantic Memory for NPC Cognitive Recall

Phase 4 (v2.3 Multiplayer & Voice):
├── Multi-Player Party Intent Queue & Turn Sync
└── Voice DM Streaming TTS Sidecar

Phase 5 (v2.5 Modding & Marketplace):
└── Developer Modding SDK & Community Rulesets
```

---

# 23. Appendix & Command Cheat Sheet

### Core Gameplay Slash Commands

| Command | Action | Example |
|---|---|---|
| `python dnd.py play "<intent>"` | Process player natural language intent through multi-agent DAG | `python dnd.py play "I sneak past Guard Karl and unlock the cell"` |
| `python dnd.py status` | View party HP, active location, sensory conditions & quests | `python dnd.py status` |
| `python dnd.py roll "<expr>"` | Roll tabletop dice deterministically with advantage/crits | `python dnd.py roll "2d6+3" --adv` |
| `python dnd.py check <skill> [dc]` | Perform D&D 2024 ability or skill check | `python dnd.py check stealth 14` |
| `python dnd.py attack <target>` | Perform weapon attack against target AC with damage | `python dnd.py attack guard_karl --weapon "Shortsword"` |
| `python dnd.py cast <spell> <target>` | Cast spell with slot deduction, saves, and damage | `python dnd.py cast fire_bolt goblin_1` |
| `python dnd.py history` | View chronological Git snapshot commit timeline | `python dnd.py history --limit 10` |
| `python dnd.py diff <commit_id>` | View unified state and Markdown diffs for a snapshot | `python dnd.py diff a7f3c91e` |
| `python dnd.py rollback <commit_id>`| Restore full world state and campaign files to a snapshot | `python dnd.py rollback a7f3c91e` |
| `python dnd.py branch <name>` | Fork active reality into an alternate multiverse timeline | `python dnd.py branch timeline-aldric-spared` |
| `python dnd.py test` | Run complete automated unit and regression test suite | `python dnd.py test` |
| `python dnd.py dev "<prompt>"` | Execute privileged developer task (tools, schemas, code) | `python dnd.py dev "Add a fear and sanity mechanic"` |

---
*Agentic D&D 2.0 Architecture Specification — Designed for Antigravity, Claude Code, Codex, and Autonomous AI Agent Runtimes.*
