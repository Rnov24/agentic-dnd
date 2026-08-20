# Plan 018: Dynamic Entity Context & Rules Agent Decoupling

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.

## Status

- **Priority**: P1
- **Effort**: S (1–2 hours)
- **Risk**: LOW
- **Depends on**: 017
- **Category**: tech-debt / architecture
- **Planned at**: commit `v1.0.0-phase4`, 2026-08-20

## Why this matters

Currently, `RulesAgent` (`agents/rules.py:19-30`) and `DMAgent` (`agents/dm.py:42-55`) contain residual hardcoded string constants from a single tutorial prologue (`"guard_karl"`, `"captain_aldric"`, `"valen"`, `"under the rumbling cover of distant thunder"`). When running any modular adventure package (such as *Lost Mine of Phandelver* or homebrew modules), this creates ambiguity in target extraction and narrative generation. Decoupling target extraction and DC rules so they resolve dynamically from active NPCs, threats, and environment state eliminates narrative bleed across campaigns.

## Current state

- `agents/rules.py:19-30`: `_extract_target` has hardcoded list `["goblin", "bugbear", "karl", "aldric", "valen"]` and defaults to `"guard_karl"` or `"captain_aldric"`.
- `agents/rules.py:45`: `_extract_weapon` defaults to `"Black Glass Dagger"`.
- `agents/rules.py:131-155`: `analyze_intent` hardcodes DC 13 for "Guard Karl's belt" and DC 14 for "free Valen".
- `agents/dm.py:43-55`: Hardcoded narration text references wet flagstones and distant thunder for all stealth checks.

## Scope

**In scope**:
- `agents/rules.py` (Dynamically extract targets from `context.get("threats", [])` + active NPCs in `state/npcs.json`; dynamically derive weapon from actor's equipped inventory; dynamically derive DC from room difficulty / rule tables instead of hardcoded strings)
- `agents/dm.py` (Generate contextual Theater-of-the-Mind descriptions using the actual location name, lighting, weather, and actor features)
- `tests/test_rules_decoupling.py` (Unit tests verifying generic target extraction across arbitrary NPC names)

**Out of scope**:
- Do not alter the underlying deterministic D&D 2024 mechanics math.

## Step-by-Step Implementation

### Step 1: Update `RulesAgent._extract_target()` in `agents/rules.py`
Inspect:
1. `context.get("threats", [])`
2. `context.get("npcs", [])` and `state/npcs.json`
3. Active monsters in the room
Match target using fuzzy word boundary tokenization without hardcoded names.

### Step 2: Update `RulesAgent._extract_weapon()` in `agents/rules.py`
Inspect `actor.get("equipment")` and `actor.get("attacks")`. Default to the first equipped weapon, or "Unarmed Strike" if no weapon is carried.

### Step 3: Update `DMAgent.narrate_turn()` in `agents/dm.py`
Use dynamic sensory templates parameterized by `world_context.get("lighting")`, `world_context.get("weather")`, and `world_context.get("location_name")`.

### Step 4: Write tests in `tests/test_rules_decoupling.py`
Verify target extraction on Phandalin NPCs (*Toblen*, *Halia*, *Gundren*) and generic enemies.

## Verification Gate
Run:
```bash
python -m unittest tests/test_rules_decoupling.py
python dnd.py play "I sneak past the goblins"
python dnd.py test
```

## STOP Conditions
- Ensure all existing multi-agent flow tests (`tests/test_multi_agent_flow.py`) continue to pass.
