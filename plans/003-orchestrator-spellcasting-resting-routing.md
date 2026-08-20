# Plan 003: Natural Language Spellcasting and Resting Routing in Orchestrator

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: Inspect `agents/orchestrator.py:140-205` and `agents/rules.py:20-80`.

## Status

- **Priority**: P1
- **Effort**: M (half to 1 day)
- **Risk**: MED
- **Depends on**: none
- **Category**: feature / architecture
- **Planned at**: 2026-08-20

## Why this matters

The multi-agent turn orchestrator (`python dnd.py play "<intent>"`) is the core natural language interface for players. Currently, `RulesAgent` and `OrchestratorAgent` only recognize `ability_check` and `combat_attack` actions. When a spellcaster says *"I cast Magic Missile at the goblin"* or a wounded party says *"We take a short rest and bandage our wounds"*, the orchestrator either treats the action as a physical weapon attack or falls back to an unhandled state, without deducting spell slots via `tools/spells.py` or spending Hit Dice via `tools/resting.py`.

## Current state

- `agents/rules.py:25-40`: Identifies attacks and checks, but lacks `spellcasting` and `resting` intent recognition.
- `agents/orchestrator.py:140-205`: Only handles `action_type == "ability_check"` and `action_type == "combat_attack"`.
- `tools/spells.py`: Fully functional `cast_spell(caster, spell_name, target, slot_level)` engine.
- `tools/resting.py`: Fully functional `execute_short_rest(party, hit_dice_spent)` and `execute_long_rest(party)` engines.

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Test Multi-Agent Turn Flow | `python -m unittest tests/test_multi_agent_flow.py` | OK, exit 0 |
| Test Spell Mechanics | `python -m unittest tests/test_spells.py` | OK, exit 0 |
| Test Resting Mechanics | `python -m unittest tests/test_resting.py` | OK, exit 0 |
| Run Full Test Suite | `python dnd.py test` | 97+ tests passed, exit 0 |

## Scope

**In scope**:
- `agents/rules.py` (Add intent recognition for `spellcasting` and `resting` action types)
- `agents/orchestrator.py` (Wire `action_type == "spellcasting"` to `tools/spells.py:cast_spell` and `action_type == "resting"` to `tools/resting.py`)
- `tests/test_multi_agent_flow.py` (Add test cases for natural language spellcasting turn and short rest turn)

**Out of scope**:
- Do not modify internal mechanics in `tools/spells.py` or `tools/resting.py`.

## Step-by-Step Implementation

### Step 1: Add spellcasting and resting intent analysis in `agents/rules.py`
In `RulesAgent.analyze_intent`:
1. Check for spellcasting intent:
```python
if any(w in lower_intent for w in ["cast", "magic missile", "fire bolt", "cure wounds", "shield", "thunderwave", "sleep", "cantrip"]):
    # Extract spell name and optional target
    return {
        "action_type": "spellcasting",
        "actor": actor.get("name"),
        "spell_name": extracted_spell,
        "target": target_name,
        "rationale": f"Player is casting {extracted_spell}."
    }
```
2. Check for resting intent:
```python
if any(w in lower_intent for w in ["short rest", "long rest", "take a rest", "bandage wounds", "sleep for the night", "camp"]):
    rest_type = "long" if "long" in lower_intent or "sleep" in lower_intent or "camp" in lower_intent else "short"
    return {
        "action_type": "resting",
        "rest_type": rest_type,
        "rationale": f"Party is taking a {rest_type} rest."
    }
```

### Step 2: Route spellcasting and resting in `agents/orchestrator.py`
In `OrchestratorAgent.process_player_intent`:
1. Handle `action_type == "spellcasting"`:
   - Call `cast_spell(caster=actor, spell_name=rules_analysis["spell_name"], target=target_npc)`.
   - Record tool call in `tool_calls_record`.
   - Append execution step with spell attack roll / save DC / damage / slot deduction.
   - Update caster in `state_manager`.
2. Handle `action_type == "resting"`:
   - If `short`: Call `execute_short_rest(party=party, hit_dice_spent={actor.get("id"): 1})`.
   - If `long`: Call `execute_long_rest(party=party)`.
   - Append execution step with HP recovered and Hit Dice restored.
   - Update party in `state_manager`.

### Step 3: Add automated tests in `tests/test_multi_agent_flow.py`
Add `test_spellcasting_intent_orchestration` and `test_resting_intent_orchestration`.

## Verification Gate
Run:
```bash
python -m unittest tests/test_multi_agent_flow.py
python dnd.py test
```

## STOP Conditions
- If slot deduction or rest recovery fails to mutate character state, check character ID matching against party roster.
