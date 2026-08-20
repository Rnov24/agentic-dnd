# Contributing to Agentic D&D

Thank you for your interest in contributing to **Agentic D&D**!

Agentic D&D is an AI-native tabletop RPG operating environment driven by multi-agent autonomous orchestration, deterministic Python mechanics, and persistent Git-style versioning.

---

## 🏛️ Core Architectural Principles

When contributing code or campaign content, you must uphold our core engineering principles:

1. **Deterministic Mechanics (Zero Hallucination)**:
   - All dice math, DCs, weapon masteries, saving throws, AC hits, and spell slots must be evaluated deterministically in Python (`tools/` or `rules/`).
   - LLMs and Agents generate sensory narrative and roleplay dialogue based on exact tool outputs.

2. **Tri-Layer State Isolation**:
   - **Layer 1: Static Compendiums (`rules/`)**: Immutable rules schemas and SRD 2024 catalogs. Never write runtime turn mutations here.
   - **Layer 2: Narrative Memory (`campaign/`)**: Human-readable Markdown files (`campaign/characters/`, `campaign/locations/`, `campaign/npcs/`, `campaign/quests/`). Synchronized via `StateManager`.
   - **Layer 3: Machine State (`state/`)**: Machine-readable JSON files (`party.json`, `npcs.json`, `world.json`, `quests.json`) and append-only commit history (`history.json`).

3. **Zero Mandatory Runtime Dependencies**:
   - The core runtime must remain 100% executable on Python 3.9+ using only the Python standard library.

4. **100% Unit Test Pass Rate**:
   - All pull requests must pass the automated test suite (`python dnd.py test`).

---

## 🚀 Contributor Quickstart

### 1. Fork & Clone Repository
```bash
git clone https://github.com/<your-username>/agentic-dnd.git
cd agentic-dnd
```

### 2. Set Up Virtual Environment (Optional)
```bash
python -m venv .venv
# On Linux/macOS:
source .venv/bin/activate
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
```

### 3. Install Dev Dependencies (Optional)
```bash
pip install -r requirements-dev.txt
```

### 4. Run the Test Suite
```bash
python dnd.py test
```
All 147+ unit tests should pass with 0 failures and 0 errors.

---

## 🛠️ How to Add a New Tabletop Mechanic

Follow this 6-step engineering pipeline:

1. **Rule Definition**: Add Markdown reference docs to `rules/dnd2024/<mechanic>.md`.
2. **Deterministic Python Tool**: Implement calculation logic in `tools/<mechanic>.py` using the `@dnd_tool` decorator from `tools.permissions`.
3. **State Schema & Synchronization**: Add required attributes to `state/*.json` and update `tools/state_manager.py` if Markdown syncing is required.
4. **Agent Integration**: Wire the mechanic into `agents/rules.py`, `agents/orchestrator.py`, or `agents/dm.py`.
5. **Unit Tests**: Write comprehensive test cases in `tests/test_<mechanic>.py`.
6. **Compendium & CI Verification**: Run `python dnd.py compendium validate` and `python dnd.py test`.

---

## 🧪 Pull Request Checklist

Before submitting a Pull Request, verify:

- [ ] `python dnd.py test` passes 100% (all 147+ tests OK).
- [ ] `python dnd.py compendium validate` passes with 0 schema errors.
- [ ] New features include corresponding unit tests in `tests/`.
- [ ] No hardcoded absolute file paths or machine-specific environment flags are introduced.
- [ ] Code follows PEP 8 conventions with standard type hints and docstrings.
- [ ] Markdown documents in `campaign/` remain synchronized with `state/` schemas.

---

## 📜 Licensing & Code of Conduct

By contributing to Agentic D&D, you agree that your contributions will be licensed under the project's [MIT License](LICENSE) and that you will abide by our [Code of Conduct](CODE_OF_CONDUCT.md).
