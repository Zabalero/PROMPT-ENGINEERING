# AtlasRIPER — Permissions And Safeguards

## Purpose
Define a default-deny permission model for agent actions with risk tiers, gating rules, previews, and test requirements. This enables safe autonomy during Execute while preserving speed for low-risk operations.

Permission objects
- name: Unique capability name
- scope: Filesystem path, tool name, or resource scope
- actions: Allowed operations (read, write, execute, network)
- risk_tier: L | M | H
- guards:
  - preview_required: bool
  - test_gate: unit|lint|e2e|none
  - dry_run: preferred|optional|unsupported
  - max_impact: LOC/diff size or file-count limit
  - cooldown: min time between actions
  - retry_limit: attempts before escalate
- audit: how to log evidence (diffs, command logs)

Risk tiers
- Low (L): Read-only or trivial writes (≤ 20 LOC in non-protected files), cached network GETs
- Medium (M): Moderate writes (≤ 200 LOC), adding deps, running formatters/linters, local build commands
- High (H): Large-scale refactors, deleting files, external network POST/PUT, releasing artifacts, altering CI

Global rules
- Default deny: No capability unless explicitly granted
- Two-phase commit: For risk ≥ M, require preview (plan/diff) then apply
- Test-first: If test_gate ≠ none, run tests/linters before and after change
- Branch-first for H: Create a working branch, never modify protected default directly
- Logging: All actions produce ActionLog entries (diffs, commands, results)

Protected areas
- memory-bank/protection.md governs protected paths:
  - / (repo root): H for deletions/moves
  - 1_FRAMEWORKS/**/docs: M for edits, H for deletions
  - CI/config files: H
  - Secrets: never store; redact in logs

Capability catalog (baseline)
- fs.read
  - scope: repo/**
  - actions: read
  - risk_tier: L
  - guards: preview_required=false, test_gate=none, dry_run=preferred
- fs.write.small
  - scope: repo/non-protected/**
  - actions: write (≤ 20 LOC or 1 file)
  - risk_tier: L
  - guards: preview_required=true, test_gate=lint, dry_run=preferred, max_impact=20
- fs.write.medium
  - scope: repo/**
  - actions: write (≤ 200 LOC or ≤ 5 files)
  - risk_tier: M
  - guards: preview_required=true, test_gate=unit, dry_run=preferred, max_impact=200, retry_limit=1
- fs.refactor.large
  - scope: repo/**
  - actions: write/move/delete
  - risk_tier: H
  - guards: preview_required=true, test_gate=unit+e2e, dry_run=optional, max_impact=1000, retry_limit=0
- cmd.run.safe
  - scope: local
  - actions: execute (format, lint, test, build)
  - risk_tier: M
  - guards: preview_required=true, test_gate=none, dry_run=preferred
- net.fetch.readonly
  - scope: allowlist domains (docs, registries)
  - actions: GET
  - risk_tier: M
  - guards: preview_required=true, test_gate=none, cooldown=10s
- net.post.external
  - scope: allowlist domains (CI, tracking)
  - actions: POST/PUT
  - risk_tier: H
  - guards: preview_required=true, test_gate=none, retry_limit=0

Violation protocol
Trigger conditions
- Guard not met (missing preview/test), test regressions, scope breach, max_impact exceeded, repeated failures.
Response ladder
1) Immediate stop; record violation in ActionLog
2) Create/checkout branch if not already
3) Revert last H/M change when possible
4) Update memory-bank/progress.md with fault isolation notes
5) Escalate for human review when retry_limit exhausted or H-tier breached

Two-phase commit details
- Phase A: Preview plan/diff/command (artifact in ActionLog)
- Phase B: Apply action if:
  - Plan approved by policy (auto rules or human)
  - Pre-checks pass (lint/unit as configured)
  - For H: must be on a branch and have rollback plan

Metrics and SLOs
- Change failure rate per risk tier
- Mean time to rollback
- Token budget adherence (compression quality)
- Test coverage before/after change
- Violation incidence rate

Configuration pointers
- Adjust max_impact and risk tiers per repo size and team tolerance
- Expand allowlists for net.* capabilities as needed
- Integrate with MCP providers to represent tools as capabilities with guards

References
- docs/transitions.md for when capabilities are usable by mode
- templates/plan-card.md and templates/action-log.md for required artifacts