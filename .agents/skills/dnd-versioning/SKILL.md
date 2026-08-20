---
name: dnd-versioning
description: Git-style campaign history, timeline inspection, unified state diffing, rollback, and multiverse branching for Agentic D&D. Use whenever the user asks to view past turns, check what changed, undo an action, restore a prior snapshot, explore 'what-if' alternate choices, or manage campaign branches, even if they simply say 'go back one turn' or 'show me the diff'.
---

# Git-Style Campaign Versioning Skill

This skill governs immutable snapshot commits, state diffing, timeline exploration, and non-destructive rollbacks in Agentic D&D.

---

## Why Git Versioning Matters in D&D
Tabletop campaigns often involve catastrophic mistakes, tactical blunders, or desires to explore "what-if" narrative branches. By versioning the entire world (`campaign/` Markdown + `state/` JSON) into content-addressable SHA commits, the campaign functions as an inspectable Git repository where no story is ever accidentally lost.

---

## Quick CLI Versioning Commands

### 1. View History Timeline
```bash
# View recent commits on the active branch
python dnd.py history

# View history with limit
python dnd.py history --limit 10

# Output as structured JSON
python dnd.py history --json
```

### 2. View Unified State Diffs
```bash
# View unified diff between a commit snapshot and its parent
python dnd.py diff <commit_id>

# Output diff as JSON payload
python dnd.py diff <commit_id> --json
```

### 3. Non-Destructive State Rollback
Restores both JSON state in `state/` and human-readable Markdown docs in `campaign/` to the exact snapshot at `<commit_id>`:
```bash
python dnd.py rollback <commit_id>
```
*Note: Rollback is non-destructive. Before rewinding, a safety snapshot of the current state is automatically recorded, allowing players to jump back and forth across timelines.*

### 4. Multiverse Timeline Branching
```bash
# Create an alternate timeline branch (e.g. stealth route vs assault route)
python dnd.py branch "assault-timeline" --create

# Switch active timeline branch
python dnd.py branch "main"
```

---

## Concrete Versioning Scenarios

### Example 1: Inspecting Turn History
- **User Prompt**: *"What happened over our last few turns?"*
- **Action**:
  ```bash
  python dnd.py history --limit 5
  ```
- **Output**: Shows commit hashes, timestamps, player intents, and affected files (e.g. `captain_aldric.md`, `state/npcs.json`).

### Example 2: Inspecting State Diff After Combat
- **User Prompt**: *"Show me exactly what changed when we attacked Guard Karl."*
- **Action**:
  ```bash
  python dnd.py diff 5bf77379
  ```
- **Output**: Displays unified diff showing Karl's HP dropping from 12 to 0 and condition updated to `unconscious`.

### Example 3: Undoing a Catastrophic Turn
- **User Prompt**: *"Wait, opening that sarcophagus triggered a fatal poison trap! Can we roll back to before I touched it?"*
- **Action**:
  ```bash
  python dnd.py rollback d7992972
  ```
- **Output**: Restores HP, party status, and room state to the pre-trap commit.

---

## Bundled References
- Commit Record Schema: [`references/commit_schema.md`](references/commit_schema.md)
- Interpreting State Diffs: [`references/diff_guide.md`](references/diff_guide.md)
