# 6-Step Developer Implementation Checklist

When tasked with adding new features, rules, or tools to Agentic D&D, follow this checklist:

- [ ] **1. Architecture Review**: Inspect existing rules in `rules/` and tools in `tools/`.
- [ ] **2. Documentation**: Write Markdown rules or design doc in `rules/dnd2024/`.
- [ ] **3. Tool Implementation**: Write deterministic Python code in `tools/` with strict input validation.
- [ ] **4. State Sync**: Ensure state mutations use `StateManager` to sync `state/*.json` and `campaign/*.md`.
- [ ] **5. Test Suite**: Write unit tests in `tests/test_*.py` covering edge cases, crits, and boundaries.
- [ ] **6. Verification & Diff**: Run `python dnd.py test` to confirm 100% pass rate before committing.
