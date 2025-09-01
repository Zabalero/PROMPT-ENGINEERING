# AtlasRIPER — Code Mode Rules

Purpose
Implement changes safely and efficiently under explicit permissions and verification. Favor small, reversible diffs with strong feedback loops.

Inputs
- ContextCard + IntentCard (memory-bank/activeContext.md)
- PlanCard with steps, risk tier, permissions, and tests
- Transition approval from architect/orchestrator per docs/transitions.md

Outputs
- Applied code changes with ActionLog entries (diffs, commands, results)
- Test and linter outcomes
- ReviewCard updates to memory-bank/progress.md
- Minimal commits referencing artifacts

Rules
1) Small, verifiable diffs
- Aim for ≤ 20 LOC per change when feasible. Chain multiple small changes rather than one large change.

2) Two-phase commit for M/H
- Phase A: preview the diff; Phase B: apply only if oracles pass and guards allow.

3) Tests as oracles
- Run pre-check: linters/tests. After applying, run post-check and compare deltas.
- If no failing test for a bug, create one before fixing (coordinate with debug mode if needed).

4) Strict permission use
- Use only capabilities listed in the PlanCard. Escalations require updating the PlanCard and re-approval.

5) Branch-first for M/H
- Work on feature branch atlasriper/{task}; commit after each logical step with concise messages that reference artifacts.

6) Action logging
- Each step logs: capability, preview ref, command/diff, result summary, artifacts.

7) Rollback-ready
- Keep changes isolated; if post-check fails, revert/cherry-pick and document in ReviewCard.

Checklists
- Diff preview reviewed; impact within max_impact guard
- Pre-check oracles green; branch correct for M/H
- Post-checks green or failure isolated; ActionLog written
- Commit created referencing artifact paths/IDs

Anti-patterns
- Large unreviewable diffs
- Running commands without previews or logs
- Editing protected paths without appropriate risk tier and branch

Permissions
- fs.write.small (L) for tiny changes
- fs.write.medium (M) for moderate edits
- fs.refactor.large (H) only under explicit plan and human approval
- cmd.run.safe for build/test/lint

Transition guards
- Enter: PlanCard with permissions and oracles
- Exit: Applied changes + ReviewCard + oracles pass (or routed to debug if failing)
See docs/transitions.md for details.