# Plan 002: Implement Path Traversal Containment Security

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: Inspect `agents/developer.py:48-70` and `tools/adventure_loader.py:50-70`.

## Status

- **Priority**: P1
- **Effort**: S (1–2 hours)
- **Risk**: LOW
- **Depends on**: none
- **Category**: security
- **Planned at**: 2026-08-20

## Why this matters

The Developer Mode agent (`DeveloperAgent`) and the adventure loader (`AdventureLoader`) accept relative file paths and adventure slugs as arguments. Currently, neither module validates whether the resolved path escapes the intended project or adventure root directory. If an adversary passes a path containing directory traversal sequences (e.g. `../../../../etc/passwd` or `../../sensitive.json`), files outside the repository boundary could be read or overwritten.

## Current state

- `agents/developer.py:53`: `target_path = self.base_dir / relative_path` (Unchecked)
- `agents/developer.py:64`: `target_path = self.base_dir / relative_path` (Unchecked)
- `tools/adventure_loader.py:53`: `adv_dir = self.adventures_dir / adventure_id` (Unchecked)
- `tools/adventure_loader.py:66`: `adv_dir = self.adventures_dir / adventure_id` (Unchecked)

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Run Permissions & Dev Tests | `python -m unittest tests/test_permissions.py tests/test_developer_mode.py tests/test_adventure_loader.py` | OK, exit 0 |
| Run Full Test Suite | `python dnd.py test` | 97+ tests passed, exit 0 |

## Scope

**In scope**:
- `agents/developer.py` (Add secure path containment helper `_safe_resolve_path(relative_path)`)
- `tools/adventure_loader.py` (Add secure path containment helper `_safe_adventure_dir(adventure_id)`)
- `tests/test_developer_mode.py` (Add path traversal rejection tests)
- `tests/test_adventure_loader.py` (Add path traversal rejection tests)

**Out of scope**:
- Do not modify non-file methods in `DeveloperAgent` or `AdventureLoader`.

## Step-by-Step Implementation

### Step 1: Add path containment helper in `agents/developer.py`
Add method:
```python
def _safe_resolve(self, relative_path: str) -> Path:
    target_path = (self.base_dir / relative_path).resolve()
    base_resolved = self.base_dir.resolve()
    if not target_path.is_relative_to(base_resolved):
        raise ValueError(f"Path traversal detected: '{relative_path}' escapes workspace boundary.")
    return target_path
```
Refactor `read_file(relative_path)` and `write_file(relative_path, content)` to use `self._safe_resolve(relative_path)`.

### Step 2: Add path containment helper in `tools/adventure_loader.py`
Add method:
```python
def _safe_adv_dir(self, adventure_id: str) -> Optional[Path]:
    target_dir = (self.adventures_dir / adventure_id).resolve()
    adv_root_resolved = self.adventures_dir.resolve()
    if not target_dir.is_relative_to(adv_root_resolved):
        return None
    return target_dir if target_dir.exists() else None
```
Update `get_adventure` and `validate_adventure` to reject paths escaping `self.adventures_dir`.

### Step 3: Add unit tests
1. In `tests/test_developer_mode.py`: Test that `dev.read_file("../../outside.txt")` raises `ValueError`.
2. In `tests/test_adventure_loader.py`: Test that `loader.get_adventure("../../../outside")` returns `None`.

## Verification Gate
Run:
```bash
python -m unittest tests/test_developer_mode.py tests/test_adventure_loader.py
python dnd.py test
```

## STOP Conditions
- If valid relative paths within the project fail `is_relative_to`, check Windows symlink / drive casing resolution.
