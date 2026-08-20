---
name: dnd-multiverse
description: Multiverse timeline exploration, alternate reality branching, timeline comparison, and what-if scenario arbitration for Agentic D&D. Use whenever exploring alternate campaign paths, creating parallel story timelines, comparing different choices across branches, or merging timeline outcomes, even if the user asks 'what if we took the other door?' or 'create an alternate timeline where we spared the captain'.
---

# Multiverse Timeline & Branching Skill

This skill enables players and DMs to fork the campaign reality into parallel multiverse timelines, test "what-if" narrative choices, and switch between diverging story paths without losing previous history.

---

## Why Multiverse Branching Matters
Tabletop RPGs are defined by high-consequence choices. With multiverse branching, players can explore both sides of a moral dilemma (e.g. *What if we spared Captain Aldric vs what if we assassinated him?*) or experiment with risky tactical options (e.g. *Stealth Infiltration vs Front-Gate Siege*).

---

## Core Multiverse Commands

### 1. Create a New Alternate Timeline Branch
```bash
# Fork current reality into a named timeline branch
python dnd.py branch "timeline-spared-aldric" --create
```

### 2. Switch Active Reality Timeline
```bash
# Switch to an existing branch
python dnd.py branch "main"

# Or switch to the alternate timeline
python dnd.py branch "timeline-spared-aldric"
```

### 3. Compare Diverging Realities
```bash
# Inspect history of a specific timeline branch
python dnd.py history --branch "timeline-spared-aldric"

# Diff state between two different timeline commits
python dnd.py diff <commit_on_timeline_b> <commit_on_timeline_a>
```

---

## Concrete Multiverse Scenarios

### Example 1: Creating a "What-If" Reality
- **Player Input**: *"I want to see what would happen if we bribed Guard Karl with 50 gold instead of knocking him out."*
- **Action**:
  ```bash
  python dnd.py branch "what-if-karl-bribed" --create
  python dnd.py play "I offer Guard Karl a pouch with 50 gold pieces to look the other way"
  ```
- **Result**: Creates a parallel timeline where Karl takes the bribe and aids the escape. The `main` timeline remains completely intact and untouched.

---

## Bundled References
- Common Multiverse Patterns: [`references/multiverse_patterns.md`](references/multiverse_patterns.md)
