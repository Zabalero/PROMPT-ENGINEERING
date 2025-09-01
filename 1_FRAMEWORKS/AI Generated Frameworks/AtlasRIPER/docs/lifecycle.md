# AtlasRIPER — Lifecycle (RIPER-5 Mapped To Permissioned Execution)

## Goal
Operationalize Reflect → Intent → Plan → Execute → Review under explicit permissions, transitions, memory, and safeguards.

## Artifacts Per Phase (Compressed, Inspectable)
- ContextCard (Reflect): situation, constraints, risks
- IntentCard (Intent): goals, acceptance criteria, non-goals
- PlanCard (Plan): steps, tests, rollback, risk tier
- ActionLog (Execute): gated edits/commands/tools with diffs and previews
- ReviewCard (Review): outcomes vs acceptance, test results, fault isolation, next steps

Phase 1 — Reflect
Inputs
- memory-bank/projectbrief.md
- memory-bank/techContext.md
- current repo state (diffs, tests)
Outputs
- ContextCard (stored in memory-bank/activeContext.md)
- Risk summary, assumptions, constraints

Checklist
- Identify scope and constraints (time, tokens, permissions)
- Summarize relevant code areas, modules, dependencies
- Note risks (data loss, security, perf regressions)

Phase 2 — Intent
Outputs
- IntentCard (activeContext.md): goals, acceptance criteria, non-goals
- Success oracle definition (tests/linters/metrics)

Checklist
- Define measurable acceptance criteria
- Define non-goals and boundaries
- Map intended mode transitions (architect → code → debug)

Phase 3 — Plan
Outputs
- PlanCard in memory-bank/progress.md
  - Steps with owners (mode), expected artifacts, and required permissions
  - Test strategy and rollback/branch policy
  - Risk tier (L/M/H) with required safeguards

Checklist
- Order steps to minimize risk (read-only analysis → small diffs → wider changes)
- Add dry-run/preview for any high-impact action
- Ensure every step has a verification

Phase 4 — Execute
Mechanics
- Use permissions and transitions (docs/permissions.md, docs/transitions.md)
- Log every action in ActionLog (templates/action-log.md or tool logs)
- Enforce two-phase commit for risk tier ≥ Medium

Checklist
- For edits: preview diff, apply, re-run tests, capture results
- For commands: prefer dry-run, then execute if checks pass
- On failure: branch, isolate, retry with bounded attempts

Phase 5 — Review
Outputs
- ReviewCard appended to memory-bank/progress.md
  - Pass/fail vs acceptance
  - Test/metrics snapshot
  - Fault isolation notes
  - Learnings and updates to systemPatterns.md

Checklist
- If failing, update PlanCard and iterate; escalate at bounded retry limit
- Update protections and patterns to prevent recurrence

Bounded retries and escalation
- Default: 2 retries for Low risk, 1 for Medium, 0 for High without human review
- On violation/test regression: branch, roll back, request review per violation protocol

Compression guidance
- Keep each card ≤ 200 tokens unless justified
- Replace long logs with references and deltas
- Summarize rationales into bullet points; link artifacts

File map touched by lifecycle
- memory-bank/activeContext.md (ContextCard, IntentCard)
- memory-bank/progress.md (PlanCard, ReviewCard, timeline)
- memory-bank/systemPatterns.md (learnings)
- templates/action-log.md (or integrated tool logs)

Minimal lifecycle template references
- templates/context-card.md
- templates/intent-card.md
- templates/plan-card.md
- templates/review-card.md
- templates/action-log.md