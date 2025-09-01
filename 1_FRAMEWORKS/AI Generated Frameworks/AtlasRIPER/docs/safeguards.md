AtlasRIPER — Safeguards and Violation Handling

Objective
Minimize risk while enabling efficient autonomous operation. Safeguards apply during planning, execution, and verification, with clear recovery steps.

Safeguard layers
1) Policy layer (preconditions)
- Default deny permissions; explicit allowlists only
- Protected areas list with elevated risk tiers
- Mode entry/exit checklists must be satisfied

2) Preview layer (two-phase commit)
- Phase A: Produce preview (diff/command plan) with estimated impact and guard checks
- Phase B: Apply only if preview passes automatic gates (and human approval when configured)

3) Test/Oracle layer
- Define oracles per task: unit tests, linters, e2e, metrics thresholds, acceptance criteria
- Run pre-check and post-check; block on regressions

4) Runtime caps
- Max impact per action (LOC/file count)
- Time and token budgets per mode
- Retry limits per risk tier

5) Isolation & rollback
- For M/H work: branch-first policy
- For failures: selective revert or full rollback; keep artifacts for inspection

Risk classification
- L: Read-only, trivial writes; no-branch required, minimal previews
- M: Moderate writes or local commands; requires previews, tests, and branch if touching protected areas
- H: Large or sensitive operations; branch-only, mandatory previews + tests, human approval recommended

Violation protocol (standard)
Trigger examples
- Missing preview, failing tests, scope breach, exceeding max impact, unauthorized transition
Response steps
1) Stop and record violation in ActionLog with context
2) If on default branch and risk ≥ M, create a branch and revert last change if applicable
3) Update memory-bank/progress.md with a FaultNote (what failed, root hypothesis)
4) Replan in orchestrator; reduce scope or split into smaller steps
5) Require human review if retry_limit reached or any H-tier guard breached

Fault isolation checklist
- Reproduce failure deterministically
- Minimize changeset to locate culprit
- Add a failing test if none exists
- Apply smallest corrective change; rerun tests; record deltas

Backoff strategy
- Progressive backoff on repeated failures: reduce step size, increase verification strictness, request review
- Escalation after budget exhaustion (tokens/time/retries)

Observation and metrics
- Track: change failure rate, MTTR (rollback), violation rate, token usage efficiency, test coverage changes
- Periodically update memory-bank/systemPatterns.md to encode new preventative patterns

Secure logging
- Never log secrets/tokens; redact automatically
- Replace long logs with references and hashes
- Store diffs and command outputs as summarized artifacts with links

Configuration knobs
- Guard strictness per repository area
- Human approval gates for H-tier operations
- Budget ceilings by mode (time/tokens/impact)

References
- docs/permissions.md for risk tiers and guards
- docs/transitions.md for mode entry/exit conditions
- docs/lifecycle.md for artifact expectations