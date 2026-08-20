# Plan 020: Orchestrator Causal Execution Graph & CLI Explain Command

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.

## Status

- **Priority**: P2
- **Effort**: S–M (0.5 day)
- **Risk**: LOW
- **Depends on**: 018, 019
- **Category**: dx / tooling
- **Planned at**: commit `v1.0.0-phase4`, 2026-08-20

## Why this matters

When an autonomous multi-agent system runs a complex turn (involving Orchestrator, WorldAgent, RulesAgent, CombatAgent, NPCAgent, ImpactAgent, and DMAgent), developers and players need clear explainability of *why* specific agent subroutines were called and how data flowed between them. Furthermore, users often need interactive rules explanations (e.g. `python dnd.py explain topple`, `python dnd.py explain stealth`, `python dnd.py explain death_saves`). Adding causal metadata to `ExecutionTrace` and implementing `python dnd.py explain <topic>` provides transparency across both runtime execution and static rules.

## Current state

- `agents/orchestrator.py:ExecutionTrace`: Contains a flat list of `ExecutionStep` objects with no causal linking (`caused_by_step_id`, `subsystem_trigger`).
- `dnd.py`: Has no `explain` command for inspecting rules, weapon masteries, condition mechanics, or spell schools.

## Scope

**In scope**:
- `agents/orchestrator.py` (Add `step_id`, `caused_by`, `input_summary`, `output_summary` to `ExecutionStep`; add `render_causal_graph()` to `ExecutionTrace`)
- `tools/explainer.py` (Create dedicated rules & mechanics explainer module querying `Compendium`)
- `dnd.py` (Add `explain` subcommand: `python dnd.py explain <topic>`)
- `tests/test_explainer.py` (Unit tests for rules explanation queries and causal graph rendering)

**Out of scope**:
- Do not add external graph visualization dependencies (use ASCII / Unicode box art).

## Step-by-Step Implementation

### Step 1: Enhance `ExecutionStep` in `agents/orchestrator.py`
Add fields:
- `step_id: int`
- `caused_by: Optional[int]`
- `decision_rationale: str`
- `state_diff_preview: Optional[str]`

### Step 2: Create `tools/explainer.py`
Implement `explain_mechanic(query: str) -> Dict[str, Any]` supporting:
- Weapon Masteries (`topple`, `push`, `vex`, `sap`, `slow`, `graze`, `cleave`, `nick`)
- Conditions (`blinded`, `charmed`, `frightened`, `poisoned`, `prone`, `stunned`, `unconscious`)
- Rules (`death_saves`, `resting`, `cover`, `initiative`, `opportunity_attack`)
- Spellcasting rules (`ritual`, `concentration`, `upcasting`, `components`)

### Step 3: Add `cmd_explain` in `dnd.py`
Register `python dnd.py explain <topic>` subparser.

### Step 4: Write tests in `tests/test_explainer.py`
Verify explanation lookups for masteries, conditions, and core mechanics.

## Verification Gate
Run:
```bash
python -m unittest tests/test_explainer.py
python dnd.py explain topple
python dnd.py explain death_saves
python dnd.py test
```

## STOP Conditions
- Ensure `explain` command gracefully suggests close matches if a topic typo occurs.
