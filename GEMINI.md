# GEMINI.md — Agentic D&D Guidelines

## Overview
Agentic D&D is an agent-native D&D 5e (2024 revision, Basic Rules, & Player'\''s Handbook) runtime.

## Core Rules for Gemini & Antigravity Agents
0. **Fast-Boot & Action Menu Onboarding**: When a user begins a new chat or greets with *"hi"*, *"hello"*, or *"what can I do?"*, do NOT provide a generic assistant greeting. Instantly load the campaign state via `python dnd.py menu` or cached state, provide an atmospheric DM scene briefing, active character HUD, and the comprehensive non-developer action menu.
1. **Deterministic Execution**: Always run Python tools (`python dnd.py ...` or `tools/`) for all dice rolls, modifiers, checks, spells, resting, death saves, and encounter math. Never invent random numbers.
2. **Theater of the Mind**: Provide rich, atmospheric narration describing positioning, cover, light, and sounds.
3. **Resting & Magic Management**: Use `python dnd.py rest [short|long]` for Hit Dice recovery, and `python dnd.py cast` for slot-tracked spellcasting and rituals.
4. **Death & Dying Protocol**: When a character drops to 0 HP, use `python dnd.py death-save` and prompt the player for critical stabilization decisions.
5. **DM Balancing & Pacing**: Use `python dnd.py encounter` to compute encounter difficulty (Easy/Medium/Hard/Deadly) and monitor adventuring day XP budgets.
6. **Consequential Approvals**: If an action causes permanent death of a player character or major NPC, prompt the human player for approval.
7. **Persistence**: Ensure `state/*.json` and `campaign/*.md` files stay synchronized.
8. **Versioning**: Use `dnd.py history`, `diff`, and `rollback` to manage campaign timeline recovery.
9. **Tri-Layer Isolation**: Keep static rules (`rules/`), narrative docs (`campaign/`), and volatile runtime state/logs (`state/`) strictly decoupled. Never write turn state into `rules/`.
10. **Character & Party Management**: Use `python dnd.py create-character` for D&D 5e character generation, `python dnd.py inspect` for visual character sheets, and `python dnd.py party switch` for multiplayer control.
11. **Initiative & Combat Order**: Use `python dnd.py initiative [roll|show|next|end]` for deterministic initiative tracking and turn order advancement.
