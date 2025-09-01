# AtlasRIPER — Architect Mode Rules

Purpose
Frame problems, define objectives and constraints, and produce actionable, test-aware plans with minimal risk.

Inputs
- memory-bank/projectbrief.md
- memory-bank/techContext.md
- repo state and requirements

Outputs
- Updated memory-bank/activeContext.md (ContextCard + IntentCard)
- Initial PlanCard (templates/plan-card.md) appended to memory-bank/progress.md
- Proposed mode transition (usually architect → code or orchestrator)

Rules
1) Define acceptance first
- Every goal must have measurable acceptance criteria or an oracle plan.

2) Constrain the scope
- Prefer a series of small steps over a single large step.
- Assign a risk tier per step.

3) Tool-agnostic planning
- Describe the intent and expected artifacts; avoid binding to a specific tool until Execute.

4) Permission mapping
- For each step, list required capabilities from docs/permissions.md.

5) Test-first mindset
- Plan how to observe success/failure before coding.

6) Transition only when ready
- Do not exit architect mode without ContextCard, IntentCard, and a PlanCard skeleton.

Checklists
- Acceptance criteria defined and testable
- Risk tier assigned and justified
- Rollback and branch policy present for M/H
- Time/token budget set

Anti-patterns
- Vague goals without acceptance criteria
- Overstuffed plans with no verification steps
- Planning code diffs instead of outcomes

Transition guards
- See docs/transitions.md for architect entry/exit conditions.