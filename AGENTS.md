# AGENTS.md — Agentic D&D Operational Guidelines

Welcome to **Agentic D&D** — an AI-native tabletop RPG operating environment driven by multi-agent autonomous orchestration, deterministic Python mechanics, and persistent inspectable state.

## Core Rules for Agents

### 0. Fast-Boot Session Readiness & Non-Developer Greeting Protocol
- **Zero-Friction Cold Start**: When a new conversation begins or the user greets with *"hi"*, *"hello"*, or *"let's play"*, **never** output a generic assistant greeting.
- Automatically execute the fast-boot sequence (via `python dnd.py menu` or reading cached state) and present:
  1. An atmospheric Dungeon Master greeting describing the current scene, lighting, weather, and immediate surroundings.
  2. The **Active Hero Status HUD** (Name, Class, Level, HP bar, AC, Spell Slots, Conditions).
  3. The **Comprehensive Action Menu** tailored for non-developer players with 5 natural language action examples and categorized quick commands.

### 1. Deterministic Mechanics (Zero Hallucinations)
- **NEVER fabricate dice results, modifiers, or DC math.**
- Always execute mechanics through the deterministic Python CLI or tool modules:
  - `python dnd.py menu` (Interactive dashboard & non-developer action menu)
  - `python dnd.py play "<intent>"` (Full multi-agent turn)
  - `python dnd.py check <skill> <dc>` (Ability check)
  - `python dnd.py attack <target> [--cover half|three_quarters]` (Attack roll)
  - `python dnd.py cast <spell> [--target <target>] [--level <lvl>] [--ritual]` (Spellcasting)
  - `python dnd.py rest [short|long] [--hit-dice <num>]` (Resting and recovery)
  - `python dnd.py death-save` (0 HP death saving throws)
  - `python dnd.py encounter -m "<monsters>"` (Encounter difficulty evaluation)
  - `python dnd.py roll "<expr>"` (Dice roll)

### 2. Theater of the Mind & DM Adjudication
- The primary presentation is narrative Theater of the Mind.
- Convey tactical position, distance, lighting, cover, and environmental threats through rich sensory description rather than asking the player for grid coordinates.
- Balance encounters and pace the adventuring day using official D&D Basic Rules & PHB XP thresholds and multipliers.

### 3. Dual Mode Security Sandbox
- **Game Mode**: Agents interact strictly with game state (`campaign/`, `state/`) and approved game mechanics tools.
- **Developer Mode**: Elevated authority to create tools, modify schemas, refactor rules, and run test suites.

### 4. Consequential Change Gate
- When a major permanent event occurs (Player/Major NPC death, faction destruction, quest failure), require human approval before finalizing the commit.

### 5. Persistent State & Git Versioning
- All turns record snapshots in `state/history.json`.
- State can be rolled back at any time via `python dnd.py rollback <commit_id>`.
- Markdown documents in `campaign/` must remain in sync with JSON in `state/`.

### 6. Tri-Layer Persistence Boundaries
- **Layer 1 (Static Rules & Compendiums — `rules/`)**: Immutable during gameplay. Never write runtime turn mutations here.
- **Layer 2 (Narrative Docs — `campaign/`)**: Human-readable Markdown documents. Synchronized via `StateManager`.
- **Layer 3 (Runtime State & Gamelogs — `state/`)**: Machine-readable JSON state (`party.json`, `npcs.json`) and append-only commit history (`history.json`).

---

## Quick Slash Commands & CLI Reference

| Command | Action |
|---|---|
| `python dnd.py menu` | Display full interactive game dashboard and non-developer action menu |
| `python dnd.py boot` | Fast-boot session initialization and state snapshot |
| `python dnd.py play "<action>"` | Process player intent through multi-agent orchestration |
| `python dnd.py status` | View party HP/AC, current scene, threats, hit dice, spell slots, and quests |
| `python dnd.py rest [short/long]` | Execute Short Rest (spend Hit Dice) or Long Rest (full recovery) |
| `python dnd.py cast <spell>` | Cast a spell from PHB compendium with slot deduction, upcasting, or ritual |
| `python dnd.py spell <name>` | Display spell card, casting time, range, components, duration |
| `python dnd.py death-save` | Roll death saving throw at 0 HP (handles 3 successes, 3 failures, Nat 20/1) |
| `python dnd.py stabilize <char>` | Attempt DC 10 Medicine check to stabilize an unconscious ally |
| `python dnd.py roll "<expr>"` | Roll tabletop dice (e.g. `1d20+5 --adv`, `2d6+3 --crit`) |
| `python dnd.py check <skill> [dc]` | Perform a D&D 2024 ability or skill check |
| `python dnd.py attack <target>` | Perform weapon attack vs AC with cover adjustments (`--cover half/three_quarters`) |
| `python dnd.py encounter -m "<monsters>"` | Evaluate combat difficulty and XP budget (D&D Basic Rules) |
| `python dnd.py monster <name>` | Display monster statblock, traits, and actions |
| `python dnd.py item <name>` | Display magic item properties, rarity, and attunement |
| `python dnd.py adventure [list/info/load/new]` | Discover, inspect, scaffold, and load modular adventure packages |
| `python dnd.py compendium [validate/stats]` | Validate rules JSON schemas and display compendium catalog statistics |
| `python dnd.py history` | View Git-style commit timeline |
| `python dnd.py diff <commit_id>` | View unified state diff with visual before/after cards |
| `python dnd.py rollback <commit_id>` | Restore game state to a snapshot commit |
| `python dnd.py create-character` | Create a new D&D 5e character with species, background, and stats |
| `python dnd.py level-up [char]` | Level up character (1-20) with HP scaling, spell slots, and new features |
| `python dnd.py inspect [char]` | View comprehensive visual character sheet, skills, attacks, and inventory |
| `python dnd.py party [list/switch]` | Manage multiplayer party roster and active player character |
| `python dnd.py initiative [roll/next]` | Roll and manage round-by-round combat initiative order |
| `python dnd.py loot [--cr <num>] [--hoard]` | Generate deterministic 5e individual or hoard treasure |
| `python dnd.py explain <topic>` | Explain D&D 2024 rules, weapon masteries, conditions, and spell systems |
| `python dnd.py test` | Run automated unit test suite (138 tests) |
| `python dnd.py dev "<prompt>"` | Execute Developer Agent task |
