# Plan 010: Action Error Recovery and Fuzzy Suggestions

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.

## Status

- **Priority**: P2
- **Effort**: S (1–2 hours)
- **Risk**: LOW
- **Depends on**: none
- **Category**: ux / error-handling
- **Planned at**: 2026-08-20

## Why this matters

When players enter slight typos or invalid options (e.g. `python dnd.py check flying` or `python dnd.py cast fireblt`), the CLI currently fails with an abrupt error or generic fallback. Adding fuzzy matching and contextual suggestions (e.g. *"Unknown skill 'flying'. Did you mean: Athletics, Acrobatics? Available skills: athletics, acrobatics, stealth, perception..."*) guides non-technical players gracefully back onto the right track.

## Current state

- `dnd.py:cmd_check`: Directly calls `roll_check` which defaults or fails if the skill is not in standard list.
- `tools/spells.py:cast_spell`: Returns `{"success": False, "error": f"Spell '{spell_name}' not found"}` without suggestions.

## Scope

**In scope**:
- `tools/suggestions.py` (Create fuzzy matcher helper using `difflib.get_close_matches`)
- `tools/spells.py` (Add suggestions when spell is not found)
- `dnd.py` (Enhance `cmd_check` and `cmd_spell` with suggestions on typo)
- `tests/test_suggestions.py` (Unit tests for suggestion engine)

**Out of scope**:
- Do not alter standard dice roll math.

## Step-by-Step Implementation

### Step 1: Implement `tools/suggestions.py`
```python
import difflib
from typing import List

def suggest_closest(query: str, possibilities: List[str], n: int = 3, cutoff: float = 0.5) -> List[str]:
    return difflib.get_close_matches(query.lower(), [p.lower() for p in possibilities], n=n, cutoff=cutoff)
```

### Step 2: Integrate suggestions in `tools/spells.py` and `dnd.py`
- In `tools/spells.py`: When spell is not found, suggest matching known spells or compendium spells.
- In `dnd.py:cmd_check`: When skill is unrecognized, suggest closest D&D 5e skills.

### Step 3: Write tests in `tests/test_suggestions.py`
Verify typos like `"stealt"`, `"percepton"`, `"fireblt"` return appropriate suggestions.

## Verification Gate
Run:
```bash
python -m unittest tests/test_suggestions.py
python dnd.py test
```

## STOP Conditions
- If no close match exists, provide the top 4 most common skills/spells instead of an empty list.
