# Plan 012: In-Turn Mini-HUD and Tactical Condition Badges

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.

## Status

- **Priority**: P2
- **Effort**: S (1 hour)
- **Risk**: LOW
- **Depends on**: none
- **Category**: ux / immersion
- **Planned at**: 2026-08-20

## Why this matters

When playing turns through `python dnd.py play "<intent>"`, the terminal displays the DM narration panel and execution trace, but does not display an immediate summary HUD of the active hero's post-turn vitals (current HP, spent spell slots, tactical zone, active conditions like Concentrating or Poisoned). Players currently have to issue a second command (`python dnd.py status`) just to see how much HP they have left after combat.

## Current state

- `agents/orchestrator.py`: Generates `ExecutionTrace` with `steps` and `narration`, but no compact post-turn HUD summary.
- `dnd.py:cmd_play`: Prints DM narration and execution steps.

## Scope

**In scope**:
- `tools/formatting.py` (Add `render_turn_mini_hud(actor, world_state, combat_state) -> str`)
- `dnd.py:cmd_play` (Append mini-HUD after DM narration in terminal output)
- `tests/test_formatting.py` (Add unit test for mini-HUD formatting)

**Out of scope**:
- Do not alter `ExecutionTrace` dictionary format for `--json` consumers.

## Step-by-Step Implementation

### Step 1: Implement `render_turn_mini_hud` in `tools/formatting.py`
Render a 1–2 line status footer:
```
  [ Rodolfo Edinburgh (Wizard 1) | HP: 7/7 | Slots Lvl 1: [●●] 2/2 | Zone: Engaged | Status: Normal ]
```

### Step 2: Integrate into `dnd.py:cmd_play`
After printing `trace.narration`, print the mini-HUD footer when not in `--json` mode.

### Step 3: Write unit tests in `tests/test_formatting.py`
Verify output format and resilience when character fields are partially populated.

## Verification Gate
Run:
```bash
python -m unittest tests/test_formatting.py
python dnd.py test
```

## STOP Conditions
- Ensure the footer is compact (<= 2 lines) so it does not clutter terminal output.
