# System Patterns (AtlasRIPER)

## Purpose
Codify proven heuristics, playbooks, and anti-patterns discovered during work. Keep entries concise and reference artifacts.

## Heuristics
- Small-first edits
  - Prefer ≤ 20 LOC diffs before larger refactors; validate with tests/linters.
  - References:
- Test-oracle before change
  - Ensure a failing test or measurable oracle before attempting a fix.
  - References:
- Two-phase commit discipline
  - Always preview diffs/commands; apply only after checks.
  - References:
- Branch for medium/high risk
  - Never modify default branch directly for M/H-tier work.
  - References:

## Playbooks
- Add a feature with safety
  1) Architect: ContextCard + IntentCard + PlanCard (risk tier, tests)
  2) Code: implement in small diffs on feature branch
  3) Debug: fix failing tests; update ReviewCard
  4) Review: merge after oracles pass
- Hotfix regression
  1) Debug: reproduce, create failing test
  2) Code: minimal diff fix
  3) Review: verify oracles; backport as needed

## Anti-Patterns
- Big-bang refactor without tests
  - Symptom: large diffs, no oracles
  - Remedy: split, add tests, enforce two-phase
- Silent tool runs
  - Symptom: commands without previews or logs
  - Remedy: ActionLog mandate; dry-run first
- Memory drift
  - Symptom: outdated activeContext/progress
  - Remedy: update on each lifecycle phase

## Records
- Date:
- Pattern name:
- Summary (≤ 120 tokens):
- Artifacts/links:

> NOTE: Keep each heuristic/playbook atomic and link to concrete examples.