# AtlasRIPER — Debug Mode Rules

Purpose
Isolate faults quickly and safely, create or refine oracles, and apply minimal corrective changes with strong verification.

Inputs
- Failing test, error logs, or observed regression
- ContextCard + IntentCard (memory-bank/activeContext.md)
- Recent ActionLog entries and diffs

Outputs
- Reproduction steps recorded
- Minimal failing test (if none existed)
- Fault hypothesis and smallest viable fix plan
- ReviewCard appended to memory-bank/progress.md
- Transition decision: return to code or escalate

Rules
1) Reproduce deterministically
- Reduce the scenario to the smallest reproducer. Prefer an automated test.

2) Create/validate a failing test
- If absent, author a minimal failing test that captures the fault. This becomes the oracle.

3) Hypothesize before changing
- Write a concise fault hypothesis and proposed smallest fix; update PlanCard or create a debug sub-plan.

4) Minimize the change
- Prefer localized edits. Avoid broad refactors while debugging.

5) Verify thoroughly
- Run the failing test (now passing), plus targeted regression checks around the affected area.

6) Record and learn
- Capture root cause notes and prevention heuristics in systemPatterns.md.

Checklists
- Reproduction: clear, automated if possible
- Test: failing then passing after fix
- Diff: minimal and isolated
- Post-checks: pass on related areas
- ReviewCard: completed with outcomes and learnings

Anti-patterns
- Fixing without a failing test/oracle
- Large refactors during fault isolation
- Ignoring related edge cases uncovered by logs

Permissions
- fs.write.small for minimal code/test edits
- cmd.run.safe for test execution
- fs.write.medium only if test scaffolding needs moderate edits

Transition guards
- Enter: failing oracle or observed fault documented
- Exit: fault fixed or isolated with notes; or escalation with bounded retries exhausted
See docs/transitions.md for flow details.