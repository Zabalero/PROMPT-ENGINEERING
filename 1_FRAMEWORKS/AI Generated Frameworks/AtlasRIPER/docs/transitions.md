AtlasRIPER — Mode Transitions and Guards

Modes
- architect: problem framing, scope, constraints, high-level design
- ask: research, clarification, documentation lookup
- code: implementation, refactors, file edits
- debug: fault isolation, testing, regression analysis
- orchestrator: multi-step coordination, planning across modes

Transition graph (directed)
architect → ask
architect → code
architect → orchestrator
ask → architect
ask → code
code → debug
debug → code
orchestrator → architect
orchestrator → ask
orchestrator → code
orchestrator → debug
(debug → orchestrator) when broader coordination is required

General transition rule
- A transition is allowed only if the source mode’s exit conditions AND the destination mode’s entry conditions are satisfied.

Entry/Exit conditions
architect
- entry: ContextCard exists; objective and constraints identified
- exit: IntentCard (goals, acceptance), initial PlanCard skeleton
ask
- entry: Specific questions/hypotheses defined; sources/allowlists ready
- exit: Answers distilled into updates to Context/Plan; citations captured
code
- entry: PlanCard steps with required permissions; tests or acceptance defined
- exit: Changes applied with ActionLog, tests run, diffs captured
debug
- entry: Failing tests or suspected faults; reproduction steps documented
- exit: Fault isolated/resolved; tests pass; learnings added
orchestrator
- entry: Multi-step plan needed; cross-mode coordination required
- exit: Delegations executed; sub-results integrated; lifecycle advanced

Guards by transition
architect → code
- require: IntentCard + PlanCard with risk tier and test strategy
- enforce: permissions for fs.write.*; two-phase commit for M/H
ask → code
- require: documented findings + updated acceptance criteria
- enforce: link citations; re-validate PlanCard before edits
code → debug
- require: test failures, runtime errors, or uncertainty flagged
- enforce: create failing test if none; capture reproduction steps
debug → code
- require: fault hypothesis + minimal fix plan
- enforce: small diffs (prefer L/M); rerun tests; append ReviewCard
orchestrator → any
- require: subplan and responsibility (mode) assigned
- enforce: sub-mode entry conditions; aggregate artifacts

Risk-aware branching
- For H-tier work, transitions into code must occur on a dedicated branch with rollback plan documented in PlanCard.

Timeouts and backoff
- If a mode exceeds predefined step/time/token budgets, transition to orchestrator to replan or request human review.

Artifacts required to transition
- architect → code: ContextCard, IntentCard, PlanCard
- code → debug: ActionLog excerpt + failing test/log
- debug → code: Fault note + fix plan card
- ask → architect/code: Q&A summary + updates to Context/Plan
- orchestrator → any: subplan ticket with entry checklist satisfied

Violations
- Attempting disallowed transition logs a violation, triggers backoff, and returns to orchestrator for replanning.

## References
- docs/lifecycle.md for artifact definitions
- docs/permissions.md for capability gates
- memory-bank/* for persistent storage of cards

> NOTE: Use orchestrator when budgets are at risk or transitions are disputed.