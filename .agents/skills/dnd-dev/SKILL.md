---
name: dnd-dev
description: Elevated Developer Mode for Agentic D&D. Use when creating new Python tools, adding homebrew game mechanics, refactoring character schemas, modifying rules, creating campaign content, importing sourcebooks, or running automated unit test suites, even if the user asks to 'add a new rule' or 'run tests'.
---

# Developer Mode & Extensibility Skill

This skill grants elevated developer authority to inspect the codebase, create deterministic Python tools, refactor state schemas, extend D&D 2024 mechanics, and maintain 100% test suite pass rates.

---

## Developer vs Game Mode Security Boundary
- **Game Mode**: Sandboxed. Agents can only call allowlisted tools and mutate permitted campaign state.
- **Developer Mode**: Elevated authority. The developer agent can write Python code, create tools, modify rules, update JSON schemas, import sourcebooks, and execute unit test suites.

---

## Core Developer Workflows

### 1. Running the Automated Unit Test Suite
Always verify code changes by executing the test suite:
```bash
# Run all automated tests via the CLI router
python dnd.py test

# Or run standard unittest discovery
python -m unittest discover -s tests -p "test_*.py" -v
```

### 2. End-to-End Workflow: Adding a New Mechanic (e.g. Sanity/Horror System)
Follow this 6-step engineering pipeline:
1. **Rule Specification**: Write Markdown documentation in `rules/dnd2024/<mechanic>.md`.
2. **Deterministic Python Tool**: Implement calculation logic in `tools/<mechanic>.py` (using `@developer_only` decorator from `tools.permissions`).
3. **State Schema & Data**: Add required attributes to `state/party.json` or `state/world.json`.
4. **Agent Integration**: Hook the mechanic into `agents/rules.py` and `agents/dm.py`.
5. **Unit Tests**: Create test cases in `tests/test_<mechanic>.py`.
6. **Verification**: Run `python dnd.py test` to ensure 0 failures and 100% test pass rate.

### 3. Importing Sourcebooks & Campaign Content
To import a magic item, monster, or location from a campaign book:
1. Create the narrative Markdown sheet in `campaign/items/<item>.md` or `campaign/locations/<loc>.md`.
2. Register the mechanical statblock or damage formula in `rules/rules_engine.py` (e.g. `WEAPONS_TABLE`).
3. Synchronize structured state using `tools/state_manager.py`.

---

## Concrete Developer Scenarios

### Example 1: Creating a Custom Python Mechanics Tool
```python
from tools.permissions import developer_only, dnd_tool
from tools.mechanics import roll_saving_throw
from tools.state_manager import StateManager

@dnd_tool(name="sanity.check", description="Evaluates a character Wisdom save against horror DC")
@developer_only
def roll_sanity_check(character_id: str, horror_dc: int = 15, seed: int = None) -> dict:
    sm = StateManager()
    char = sm.get_character(character_id)
    save_result = roll_saving_throw(char, ability="wisdom", dc=horror_dc, seed=seed)
    
    if not save_result["success"]:
        sanity = char.get("sanity", {"current": 100, "max": 100})
        sanity["current"] = max(0, sanity["current"] - 10)
        char["sanity"] = sanity
        sm.update_character(char)
        
    return {
        "character": char["name"],
        "save_result": save_result,
        "current_sanity": char.get("sanity", {}).get("current", 100)
    }
```

### Example 2: Writing a Unit Test for Mechanics Verification
```python
import unittest
from tools.dice import roll_dice
from tools.combat import apply_damage

class TestCustomMechanic(unittest.TestCase):
    def test_damage_absorption(self):
        target = {"name": "Test Dummy", "hp": {"current": 20, "max": 20, "temp": 5}}
        res = apply_damage(target, 10, "slashing")
        self.assertEqual(res["temp_hp_after"], 0)
        self.assertEqual(res["hp_after"], 15)
```

---

## Bundled References
- 6-Step Developer Checklist: [`references/dev_workflow.md`](references/dev_workflow.md)
- Structured Schema Registry Guidelines: [`references/schema_registry.md`](references/schema_registry.md)
