---
name: dnd-play
description: Process natural-language player actions, execute full turns through multi-agent orchestration, check campaign status, and advance the D&D 5e (2024 revision) game world. Use whenever the player describes an in-game action, attacks, explores, investigates, talks to an NPC, casts a spell, checks HP/inventory, takes a rest, or interacts with the environment, even if they don't explicitly say 'turn' or 'play'.
---

# Agentic D&D Gameplay Skill (5e 2024 Revision)

This skill enables the agent to autonomously orchestrate full player turns, manage multi-agent state mutations, and drive the living D&D world through the deterministic Python runtime.

---

## Why Deterministic Execution Matters
Never invent, estimate, or hallucinate dice rolls, modifiers, damage numbers, or AC values. When mechanics are calculated deterministically by Python tools, players experience true tabletop fairness, high stakes, and reproducible game history. The LLM's role is to interpret intent and deliver rich narrative prose based on exact tool outputs.

---

## Fast-Boot & Campaign Lobby Onboarding
Whenever a player starts a new session or simply says *"hi"*, *"hello"*, or *"what can I do?"*:
1. Run or retrieve `python dnd.py menu` (or `python dnd.py lobby`) in `< 20ms`.
2. Present the immersive Theater-of-the-Mind scene greeting, active hero vitals HUD, and dynamic contextual RPG action choices (Exploration, Combat, Social, Recovery).
3. Never output raw CLI command strings or awkward scripted first-person quotes in the greeting.

---

## Core Turn Workflow

### Step 1: Execute Player Intent via CLI
Run the deterministic orchestrator command:
```bash
python dnd.py play "<player intent>"
```
For structured machine JSON:
```bash
python dnd.py play "<player intent>" --json
```
For a specific character (e.g., companion or multi-character party):
```bash
python dnd.py play "<player intent>" --character aria_nightwind
```

### Step 2: Understand the Autonomous Execution Trace
When `dnd.py play` runs, it executes the multi-agent DAG:
1. `[Orchestrator]`: Analyzes player intent and sets mechanical objectives.
2. `[World Agent]`: Evaluates environmental factors (lighting, sound, weather, cover, hazards).
3. `[Rules Agent]`: Determines required D&D 2024 checks, DCs, and action economy costs.
4. `[Python Tool Runtime]`: Computes exact d20 rolls, modifiers, AC hits, and damage formulas.
5. `[NPC Agent]`: Simulates persistent NPC memory, reactions, and dialogue disposition.
6. `[Character Agent]`: Simulates companion reactions (e.g., Eldrin's spell assistance).
7. `[State Agent]`: Mutates JSON state in `state/` and synchronizes Markdown in `campaign/`.
8. `[Impact Agent]`: Evaluates whether changes require human approval.
9. `[Chronos Agent]`: Records an immutable Git-style commit snapshot in `state/history.json`.
10. `[DM Agent]`: Renders atmospheric Theater-of-the-Mind narration.

### Step 3: Check Campaign Status
When the player asks about party health, active threats, room layout, or inventory:
```bash
python dnd.py status
```
This displays active location, lighting, tension level, character HP/AC/spell slots, NPCs in area, and active quests.

### Step 4: Handle Consequential Change Gates
If an action results in an irreversible event (e.g. player death, major NPC slain, quest failure):
1. The execution trace flags `CONSEQUENTIAL CHANGE DETECTED — APPROVAL REQUIRED`.
2. Present the before/after state diff to the player.
3. Await their decision:
   - **Approve**: `python dnd.py approve --decision approve`
   - **Reject**: `python dnd.py approve --decision reject`

---

## Concrete Execution Examples

### Example 1: Infiltration & Lockpicking
- **Player Input**: `"I slip through the shadows behind Guard Karl, grab his keyring, and unlock Cell #3."`
- **Agent Action**:
  ```bash
  python dnd.py play "I sneak past Guard Karl, steal the key, and unlock Valen's cell"
  ```
- **Resulting Flow**: Orchestrator rolls Stealth check vs Passive Perception (11), Sleight of Hand check vs DC 14, updates Prisoner Valen's state to "Freed", and outputs DM narration.

### Example 2: Combat Engagement
- **Player Input**: `"I draw my Black Glass Dagger and strike at the sentry before he sounds the alarm!"`
- **Agent Action**:
  ```bash
  python dnd.py play "I attack Guard Karl with my Black Glass Dagger"
  ```
- **Resulting Flow**: Resolves Attack roll vs AC 13, rolls 1d4+3 + 2d6 Sneak Attack damage, applies HP reduction to `state/npcs.json`, and narrates the visceral impact.

---

## Bundled References
- Detailed turn DAG lifecycle: [`references/turn_lifecycle.md`](references/turn_lifecycle.md)
