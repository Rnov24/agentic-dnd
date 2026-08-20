# Product Requirements Document: Agentic D&D

**Status:** Draft v1  
**Product:** Agentic D&D  
**Ruleset:** D&D 5e (2024 revision)  
**Primary UX:** Claude Code / Codex / Antigravity-style agentic terminal + graphical workspace  
**Gameplay:** Theater of the Mind  
**AI Role:** Full Dungeon Master  
**Human Roles:** Player + Developer  
**Mechanics:** Deterministic Python tools  
**Persistence:** Markdown + structured data  
**Versioning:** Git-style campaign history  

---

# 1. Executive Summary

Agentic D&D is an AI-native Dungeons & Dragons platform designed around an **agentic coding/runtime experience** rather than a conventional RPG interface.

The AI is the full Dungeon Master. Human users are players who control playable characters, while developers have a privileged Developer Mode for building and extending the game.

Multiple human players may participate in the same campaign. AI agents control NPCs, enemies, creatures, factions, companions, and world simulation.

The system combines:

- Multi-agent autonomous orchestration
- Claude Code/Codex/Antigravity-style interaction
- Natural-language intent-driven gameplay
- Theater-of-the-mind narration
- Python tools for deterministic dice and rules mechanics
- Markdown + structured persistent campaign state
- Git-style versioning, diffs, rollback, and branching
- Strict Game Mode / Developer Mode separation
- Human approval for consequential world-state changes

The goal is to make a D&D campaign feel like a **living software project operated by agents**.

---

# 2. Product Vision

> **Make D&D an executable, inspectable, persistent world where AI agents act as the Dungeon Master, deterministic tools enforce mechanics, and humans interact through intent rather than menus.**

The product should feel closer to using an advanced coding agent than playing a conventional digital RPG.

Example:

```text
Player:
> I sneak into the fortress, find the prisoner, free them, and escape.

Orchestrator:
→ Analyze player intent

DM Agent:
→ Determine scene and possible resolution

World Agent:
→ Inspect fortress state

Rules Agent:
→ Determine required checks

Python:
→ Execute deterministic dice rolls

NPC Agent:
→ Determine guard reactions

State Agent:
→ Update prisoner, guards, quest, and location state

Impact Agent:
→ Determine whether changes require approval

DM Agent:
→ Narrate the result
````

---

# 3. Target Users

## 3.1 Solo Player

A player who wants a complete AI-DM campaign without a human Dungeon Master.

## 3.2 Multiplayer Players

Multiple human players share one campaign.

Each human controls one or more playable characters.

The AI remains the Dungeon Master.

## 3.3 AI Party Player

A human may play one character while AI agents control companion/player-party characters.

## 3.4 Developer / Power User

A technically capable user who wants to customize:

* Campaigns
* Rules
* Agents
* Tools
* Character systems
* World systems
* Schemas
* Game mechanics

through an agentic development environment.

---

# 4. Product Principles

## 4.1 AI Is the Dungeon Master

There is no required human DM role.

The AI DM controls:

* Narration
* NPC behavior
* World simulation
* Encounters
* Quests
* Story progression
* Consequences
* Environmental interpretation
* Agent coordination

---

## 4.2 Human Players Own Their Characters

Players communicate using natural-language intent.

Example:

```text
Player:
> I distract the guard, steal the key, and free the prisoner.
```

The system should interpret this as a high-level goal and autonomously resolve appropriate sub-actions.

The player should not need to micromanage every dice roll or mechanical operation.

---

## 4.3 Human Developer Has Elevated Authority

Developer Mode provides full agentic development capabilities.

Game Mode does not.

---

## 4.4 Deterministic Mechanics

LLMs should not be trusted as the final authority for numerical game mechanics.

Python tools handle:

* Dice
* Modifiers
* Attack rolls
* Damage
* Saving throws
* Ability checks
* Initiative
* Conditions
* Resource calculations
* Rule validation
* Combat calculations

The AI decides **what should happen mechanically**.

Python determines **what the actual mechanical result is**.

---

## 4.5 State Must Be Inspectable

Important campaign information must be stored in human-readable and machine-readable forms.

The developer must be able to inspect the world directly.

---

## 4.6 Agentic, Not Chatbot-Centric

The system should actively:

* Plan
* Delegate
* Inspect
* Execute
* Validate
* Modify state
* Test
* Recover from errors
* Explain actions

rather than simply generate conversational responses.

---

# 5. Game Mode

Game Mode is the protected gameplay runtime.

Agents may:

* Read campaign state
* Read rules
* Call approved tools
* Perform deterministic calculations
* Modify permitted game state
* Update characters
* Update NPCs
* Update items
* Update locations
* Update quests
* Advance world state
* Create routine state records

Agents may NOT:

* Modify core engine code
* Modify agent definitions
* Create arbitrary new tools
* Modify system permissions
* Modify the rules engine
* Modify developer configuration
* Alter runtime infrastructure

---

# 6. Consequential Change Approval

Routine changes happen automatically.

Important or irreversible changes require human approval.

Examples:

* Character death
* Major NPC death
* Permanent item destruction
* Faction destruction
* Major location destruction
* Permanent quest failure
* Major world-state changes

Approval should display:

```text
CONSEQUENTIAL CHANGE

Action:
Kill NPC: Captain Aldric

Cause:
Player attacked and defeated Captain Aldric.

Affected:
- npcs/captain_aldric.md
- factions/royal_guard.md
- quests/escape_the_fort.md

Before:
Captain Aldric = Alive

After:
Captain Aldric = Dead

[Approve] [Reject] [Inspect Diff]
```

---

# 7. Developer Mode

Developer Mode provides **Claude Code / Codex-level repository manipulation**.

The Developer Agent may:

* Inspect repository
* Search files
* Read architecture
* Create files
* Modify files
* Delete files with approval
* Create Python tools
* Modify tools
* Modify agents
* Modify schemas
* Modify campaign configuration
* Modify rules implementation
* Write tests
* Run tests
* Execute Python
* Diagnose errors
* Fix errors
* Refactor code
* Create campaign content
* Create reusable systems
* Show diffs
* Commit changes

---

# 8. Example Developer Task

User:

```text
Add a sanity system.

Requirements:
- Characters have sanity.
- Horror events can reduce sanity.
- Add sanity saving throws.
- Add temporary and permanent madness.
- Integrate with exploration and combat.
- Store state in Markdown and structured data.
- Implement calculations in Python.
- Write tests.
- Update the DM agent behavior.
```

Developer Agent:

```text
1. Inspect repository
2. Inspect existing character schema
3. Inspect rules architecture
4. Inspect Python tools
5. Plan implementation
6. Create sanity schema
7. Modify character state
8. Create Python sanity tools
9. Modify DM agent
10. Add tests
11. Run tests
12. Fix failures
13. Validate state
14. Show diff
15. Commit changes
```

This is the intended developer experience.

---

# 9. Agent Architecture

The platform should use a multi-agent architecture.

```text
                    ┌──────────────────┐
                    │      USER        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Agentic Interface│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Orchestrator    │
                    └────────┬─────────┘
                             │
        ┌────────────────────┼─────────────────────┐
        │                    │                     │
        ▼                    ▼                     ▼
   DM Agent            Rules Agent           World Agent
        │                    │                     │
        ├────────────────────┼─────────────────────┤
        │                    │                     │
        ▼                    ▼                     ▼
 Combat Agent           NPC Agent          Character Agent
        │                    │                     │
        └────────────────────┼─────────────────────┘
                             ▼
                    ┌──────────────────┐
                    │   Tool Runtime   │
                    │ Python + Tools   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ State Management │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Git / Versioning │
                    └──────────────────┘
```

---

# 10. Orchestrator Agent

The Orchestrator is responsible for:

* Understanding user intent
* Selecting agents
* Delegating tasks
* Managing execution loops
* Maintaining task context
* Handling failures
* Validating completion
* Controlling permissions

Agents should be able to call other agents.

---

# 11. DM Agent

The DM Agent is the primary game intelligence.

Responsibilities:

* Narration
* Scene management
* Player intent interpretation
* Story pacing
* World decisions
* Encounter direction
* Consequence generation
* Agent coordination

Example:

```text
Player:
> I open the ancient door.

DM Agent:
→ Inspect location
→ Determine door state
→ Ask World Agent for environmental context
→ Ask Rules Agent whether a check is necessary
→ Execute mechanics if necessary
→ Update state
→ Narrate
```

---

# 12. Rules Agent

The Rules Agent interprets D&D 5e 2024 rules.

Responsibilities:

* Determine applicable rules
* Determine required checks
* Determine DCs
* Determine actions
* Determine conditions
* Validate player intent
* Explain rules decisions

The Rules Agent must use Python for deterministic outcomes.

---

# 13. Combat Agent

Responsibilities:

* Encounter lifecycle
* Initiative
* Combat state
* Action interpretation
* Movement interpretation
* Enemy behavior
* Conditions
* Turn progression
* Combat resolution

Combat should be fully agentic.

---

# 14. NPC Agent

NPC agents maintain:

* Goals
* Motivations
* Knowledge
* Personality
* Relationships
* Memories
* Fears
* Loyalties
* Behavioral state

NPCs should react according to their persistent state rather than being regenerated from scratch every interaction.

---

# 15. World Agent

The World Agent maintains:

* Locations
* Factions
* World events
* Timelines
* Environmental state
* Travel
* Global consequences
* World relationships

---

# 16. Character Agent

Character Agents control AI party members.

They should have:

* Goals
* Personality
* Memories
* Relationships
* Preferences
* Combat behavior
* Party relationships

AI companions should behave as characters rather than generic assistants.

---

# 17. State Agent

The State Agent manages persistent game state.

Responsibilities:

* Read state
* Determine state mutations
* Apply validated changes
* Update Markdown
* Update structured state
* Validate consistency
* Record provenance

---

# 18. Developer Agent

The Developer Agent is available only in Developer Mode.

Responsibilities:

* Repository inspection
* Code generation
* Tool creation
* Testing
* Debugging
* Refactoring
* Architecture changes
* Agent modifications

---

# 19. Agent Execution Loop

Agents support autonomous multi-step loops.

```text
USER INTENT
    ↓
ORCHESTRATOR
    ↓
PLAN
    ↓
DELEGATE
    ↓
AGENT
    ↓
TOOL
    ↓
RESULT
    ↓
VALIDATE
    ↓
STATE UPDATE
    ↓
IMPACT CHECK
    ↓
APPROVAL?
    ├── YES → Human approval
    └── NO
    ↓
CONTINUE
    ↓
NARRATE
```

Agents should be capable of:

* Inspecting before acting
* Calling multiple tools
* Calling other agents
* Revising plans
* Retrying failures
* Validating results
* Stopping when the objective is complete

---

# 20. Player Interaction

## 20.1 Intent-Driven

Natural language is the primary gameplay interface.

Examples:

```text
I investigate the altar.

I try to convince the captain we're royal messengers.

I sneak through the camp and steal the map.

I attack the ogre with my greatsword.

I search the dead wizard for anything useful.
```

The player should not need to translate these into formal game commands.

---

# 21. Theater of the Mind

The primary gameplay presentation is **pure narrative theater of the mind**.

The system does not require:

* Tactical grids
* Battle maps
* Persistent graphical maps
* Character tokens

The AI DM communicates:

* Position
* Distance
* Cover
* Threats
* Objects
* NPC behavior
* Environment
* Combat conditions

through narration.

The underlying engine may still maintain exact spatial information for mechanical consistency.

Example:

```text
The ogre is roughly twenty feet away, blocking the narrow passage.

Behind it, you can see a heavy iron gate.

The floor between you is scattered with broken shields and loose stones.
```

---

# 22. Combat Philosophy

Combat is:

* Fully agentic
* Intent-driven
* Theater-of-the-mind
* Deterministic underneath

Example:

```text
Player:
> I rush the ogre, swing my greatsword, and use Action Surge if I miss.
```

The system handles:

```text
Determine current state
        ↓
Validate intent
        ↓
Resolve movement
        ↓
Determine attack
        ↓
Python dice roll
        ↓
Calculate damage
        ↓
Apply conditions/resources
        ↓
Process enemy reaction
        ↓
Process enemy turn
        ↓
Update state
        ↓
Narrate
```

---

# 23. Ruleset

Initial ruleset:

> **D&D 5e — 2024 revision**

Architecture should support future rulesets.

Recommended abstraction:

```text
Game Runtime
      ↓
Rules Interface
      ↓
D&D 2024 Implementation
```

Future implementations could include:

```text
D&D 2024
Pathfinder
Custom RPG
Other tabletop systems
```

---

# 24. State Architecture

The system uses:

> **Markdown + structured data**

Markdown is primarily human-readable campaign knowledge.

Structured data is optimized for runtime processing.

---

# 25. Markdown State

Suggested structure:

```text
campaign/
├── characters/
├── npcs/
├── items/
├── locations/
├── factions/
├── quests/
├── lore/
├── events/
├── sessions/
└── rules/
```

Example:

```text
characters/
└── aria_nightwind.md
```

Possible content:

```markdown
# Aria Nightwind

## Identity

Name: Aria Nightwind
Class: Rogue
Level: 3

## Personality

Quiet, observant, distrustful of nobles.

## Goals

- Discover who murdered her mentor.
- Protect the party.

## Relationships

- Captain Aldric: Hostile
- Mira: Trusted ally

## Important Memories

- Escaped the royal prison.
- Found a mysterious black dagger.

## Current Status

HP: 21/24
Location: Blackstone Fortress
```

---

# 26. Structured State

Structured state stores machine-oriented information:

* IDs
* Numeric attributes
* HP
* Resources
* Conditions
* Relationships
* References
* Quest status
* Locations
* Initiative
* Combat state
* Timestamps
* Provenance

Possible technologies:

* JSON
* YAML
* SQLite
* Embedded database

The exact choice remains an implementation decision.

---

# 27. Python Tool Layer

Python is the deterministic execution layer.

Initial tools:

```python
roll_dice()
roll_check()
roll_attack()
roll_damage()

calculate_modifier()
calculate_dc()

apply_damage()
apply_healing()

apply_condition()
remove_condition()

calculate_initiative()

validate_action()
validate_character()
validate_state()
```

Tools should return structured results.

Example:

```json
{
  "roll": 17,
  "modifier": 5,
  "total": 22,
  "critical": false,
  "success": true
}
```

The LLM should never fabricate the result.

---

# 28. Agentic Coding Interface

The main interface should feel like:

* Claude Code
* Codex
* Antigravity

rather than a traditional RPG UI.

Primary interface:

```text
┌────────────────────────────────────────────────────┐
│ Agentic D&D                                       │
├───────────────────────┬────────────────────────────┤
│ Campaign Files        │ Agent Terminal             │
│                       │                            │
│ campaign/             │ > I enter the crypt.       │
│  characters/          │                            │
│  npcs/                │ DM Agent                   │
│  items/               │ The stone stairs descend...│
│  locations/           │                            │
│                       │ → World Agent              │
│ state/                │ → Rules Agent              │
│ agents/               │ → Python                   │
│ tools/                │                            │
│                       │                            │
├───────────────────────┴────────────────────────────┤
│ Execution Trace / Diff / State                     │
└────────────────────────────────────────────────────┘
```

The terminal/conversation remains the primary interface.

---

# 29. Project Explorer

Users should be able to inspect:

```text
campaign/
state/
agents/
tools/
rules/
tests/
sessions/
config/
```

Files can be opened and edited directly in Developer Mode.

---

# 30. Execution Trace

Developer/debug view should expose:

```text
DM Agent
→ Inspect current scene

World Agent
→ Query fortress

Rules Agent
→ Stealth check required

Python
→ d20 = 14
→ modifier = +5
→ total = 19

State Agent
→ No permanent state change

DM Agent
→ Narrate success
```

Normal players may see a simplified version.

---

# 31. Git-Style Campaign Versioning

Each campaign behaves like a Git repository.

Features:

* Automatic commits
* Diffs
* Rollback
* Restore
* Branches
* Timeline exploration
* Change attribution

Example:

```text
commit 81f2c1a

The Goblin King was defeated

Changed:
- npcs/goblin_king.md
- factions/goblin_clan.md
- quests/goblin_threat.md
- locations/goblin_fort.md
- state/world.json
```

Every change should record:

* Agent
* User action
* Reason
* Files changed
* Tool calls
* Validation
* Approval

---

# 32. Permissions

Critical security boundary:

```text
                    SYSTEM
                       │
             ┌─────────┴─────────┐
             │                   │
      Developer Mode        Game Mode
             │                   │
       Full authority      Sandbox authority
             │                   │
       Code/tools/etc.     Game state only
```

Game Mode must not be able to escalate into Developer Mode.

---

# 33. Game Mode Tool Policy

Game Mode tools should be explicitly allowlisted.

Allowed examples:

```text
dice.roll
rules.check
rules.attack
rules.damage
state.read
state.update
npc.evaluate
world.query
combat.resolve
quest.update
```

Forbidden examples:

```text
shell.execute
package.install
engine.modify
agent.modify
permission.modify
secret.read
tool.create
```

---

# 34. Observability

Every important action should be traceable.

Capture:

* User intent
* Agent
* Agent task
* Tool invocation
* Tool result
* State change
* Validation
* Approval
* Final narration

This enables debugging and campaign auditing.

---

# 35. Example Gameplay Session

```text
PLAYER
> I sneak into the old fort and find whoever is being held prisoner.

ORCHESTRATOR
→ Inspect character
→ Inspect current location
→ Query World Agent

RULES AGENT
→ Stealth check required

PYTHON
→ d20 = 14
→ modifier = +5
→ total = 19

WORLD AGENT
→ Guards remain unaware.

DM AGENT
→ Continue scene.

PLAYER
> I search for the prisoner.

WORLD AGENT
→ Inspect fort state.

DM AGENT
→ Prisoner discovered.

STATE AGENT
→ Update prisoner discovery.

PLAYER
> I break them out.

NPC AGENT
→ Evaluate guard response.

RULES AGENT
→ Determine required mechanics.

PYTHON
→ Resolve checks.

STATE AGENT
→ Update prisoner
→ Update guards
→ Update quest

IMPACT CHECK
→ No consequential approval required.

DM AGENT
→ Narrate outcome.
```

---

# 36. Consequential Change System

Changes should be classified.

## Low Impact

Automatically apply:

* HP changes
* Temporary conditions
* Inventory consumption
* Routine NPC reactions
* Quest progress
* Discovered information
* Position changes
* Ordinary dialogue

## High Impact

Require approval:

* Permanent character death
* Major NPC death
* Important item destruction
* Faction collapse
* Major location destruction
* Permanent quest failure
* Major irreversible world changes

---

# 37. MVP

## Agent Runtime

* Orchestrator
* DM Agent
* Rules Agent
* State Agent
* Combat Agent
* NPC capabilities
* World capabilities
* Tool calling
* Multi-step loops

## Gameplay

* D&D 2024 core rules
* Character state
* NPCs
* Locations
* Items
* Quests
* Exploration
* Dialogue
* Skill checks
* Combat
* Conditions
* Inventory
* Character progression

## Deterministic Engine

* Python dice
* Core calculations
* Rule validation
* Combat calculations

## Persistence

* Markdown
* Structured state
* Validation
* Session history

## Interface

* Agentic terminal
* Project explorer
* Game conversation
* Execution trace
* State viewer
* Diff viewer

## Security

* Game Mode sandbox
* Developer Mode
* Consequential-change approval

## Versioning

* Git integration
* Automatic commits
* Diff
* Rollback

---

# 38. Suggested Repository

```text
agentic-dnd/
│
├── campaign/
│   ├── characters/
│   ├── npcs/
│   ├── items/
│   ├── locations/
│   ├── factions/
│   ├── quests/
│   ├── lore/
│   └── events/
│
├── state/
│   ├── world.json
│   ├── combat.json
│   ├── party.json
│   └── relationships.json
│
├── rules/
│   └── dnd2024/
│
├── agents/
│   ├── orchestrator/
│   ├── dm/
│   ├── rules/
│   ├── combat/
│   ├── npc/
│   ├── world/
│   ├── character/
│   ├── state/
│   └── developer/
│
├── tools/
│   ├── dice/
│   ├── combat/
│   ├── character/
│   └── state/
│
├── tests/
│
├── sessions/
│
├── config/
│
└── README.md
```

---

# 39. Key User Stories

## Player

* I can describe my character's intent naturally.
* The AI DM resolves routine sub-actions.
* Dice results are deterministic.
* I can play entirely through theater of the mind.
* My character persists between sessions.
* Important irreversible events can require approval.

## Multiplayer Player

* Multiple humans can join a campaign.
* Each player controls playable characters.
* AI controls the Dungeon Master.
* AI controls NPCs and enemies.

## Developer

* I can ask an agent to inspect the repository.
* I can ask an agent to modify game code.
* I can ask an agent to create Python tools.
* I can ask an agent to write tests.
* I can run tests through the agent.
* I can inspect diffs.
* I can customize rules.
* I can customize agents.
* I can customize schemas.
* Developer capabilities are unavailable during Game Mode.

---

# 40. Example Developer Workflow

```text
Developer:
> Add a fear mechanic.

Developer Agent:
→ Inspect rules
→ Inspect character schema
→ Inspect Python tools
→ Inspect DM Agent
→ Create implementation plan

→ Modify:
  rules/dnd2024/fear.md
  tools/rules/fear.py
  state/character_schema.json
  agents/dm/instructions.md

→ Add:
  tests/test_fear.py

→ Run tests

→ Fix failing test

→ Validate state

→ Show diff

→ Commit:
  feat: add fear mechanic
```

---

# 41. Success Criteria

## Gameplay Success

A player can say:

> "I sneak into the fortress, find the prisoner, free them, and escape."

The system should autonomously:

* Understand intent
* Inspect state
* Plan
* Delegate
* Execute tools
* Roll dice
* Resolve rules
* Simulate NPCs
* Update world state
* Detect consequential changes
* Ask for approval if necessary
* Continue the simulation
* Narrate the outcome

without requiring manual mechanical orchestration.

---

# 42. Developer Success

A developer can say:

> "Add a sanity system with stress points, saving throws, Markdown state, Python mechanics, tests, and DM integration."

The Developer Agent should:

1. Inspect the repository.
2. Plan the implementation.
3. Modify/create files.
4. Implement Python mechanics.
5. Update schemas.
6. Update agents.
7. Write tests.
8. Run tests.
9. Fix failures.
10. Validate.
11. Present a diff.
12. Commit the change.

---

# 43. High-Level Architecture

```text
                     HUMAN
                       │
                       ▼
              ┌─────────────────┐
              │ Agentic UI      │
              │ Terminal + GUI  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Orchestrator   │
              └────────┬────────┘
                       │
       ┌───────────────┼────────────────┐
       │               │                │
       ▼               ▼                ▼
   DM Agent       Rules Agent       World Agent
       │               │                │
       ▼               ▼                ▼
 Combat Agent      NPC Agent      Character Agent
       │               │                │
       └───────────────┼────────────────┘
                       ▼
              ┌─────────────────┐
              │ Tool Runtime    │
              │ Python          │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ State Layer     │
              │ Markdown + Data │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Git Versioning  │
              └─────────────────┘

Developer Mode
      │
      ▼
Repository / Code / Agents / Tools
```

---

# 44. Major Risks

## Agent Hallucination

Mitigation:

* Deterministic tools
* Validation
* Structured state
* Execution traces

## State Corruption

Mitigation:

* Schemas
* Transactions
* Validation
* Git snapshots
* Rollback

## Permission Escalation

Mitigation:

* Game Mode sandbox
* Tool allowlists
* Separate Developer Mode

## Rules Errors

Mitigation:

* Dedicated Rules Agent
* Deterministic Python mechanics
* Automated tests

## Long-Term Memory

Mitigation:

* Markdown
* Structured state
* Retrieval
* Indexes
* Summaries
* Scoped context

## Agent Infinite Loops

Mitigation:

* Step limits
* Execution budgets
* Cancellation
* Cycle detection

## NPC Inconsistency

Mitigation:

* Persistent goals
* Memories
* Relationships
* Knowledge state
* Provenance

## Latency / Cost

Mitigation:

* Specialized agents
* Model routing
* Caching
* Lightweight agents
* Parallel execution where safe

---

# 45. Future Extensions

Possible future features:

* Additional tabletop rulesets
* Campaign marketplace
* Shared online campaigns
* Voice input
* Voice DM
* AI-generated sound
* Optional character portraits
* Optional maps
* Campaign replay
* Alternate timelines
* Agent-generated campaign modules
* Community plugins
* Local LLM support
* Automated campaign testing
* AI encounter balancing
* Modding ecosystem

---

# 46. Open Decisions

The following decisions remain open:

1. Exact LLM/provider architecture.
2. Character creation UX.
3. Multiplayer networking architecture.
4. Exact structured-state technology.
5. Full D&D 2024 rules implementation scope.
6. Plugin/tool security architecture.
7. UI framework.
8. Campaign synchronization strategy.
9. Cost/latency optimization.
10. How much agent execution detail normal players should see.

---

# 47. Product Definition

Agentic D&D should not be understood simply as:

> "An AI chatbot that plays D&D."

It should be understood as:

> **An agentic operating environment for persistent tabletop RPG worlds.**

The campaign is the project.

The agents are the runtime.

Python is the deterministic mechanics layer.

Markdown and structured data are persistent world memory.

Git is the history and recovery system.

The AI is the Dungeon Master.

Humans are the players and developers.

Natural-language intent is the primary command interface.

Theater of the mind is the primary gameplay presentation.

The defining product advantage is the combination of:

**Deep agentic autonomy

* deterministic mechanics
* persistent inspectable state
* developer-grade extensibility
* safe permission boundaries**

