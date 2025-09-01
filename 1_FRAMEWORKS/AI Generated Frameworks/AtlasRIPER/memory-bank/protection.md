# Protection Policy (AtlasRIPER)

## Purpose
Define protected paths and policies for safe autonomous operation.

## Protected Paths (Examples; Adjust Per Repo)
- / (repo root): High risk for delete/move
- **/docs/**: Medium for edits, High for deletions
- **/.github/**, **/ci/**, **/.vscode/**: High
- Secrets/config: never store secrets in repo; redact in logs
- Binary assets: treat as High; no automated rewrites

## Rules
- Default deny: only explicitly allowed actions are permitted
- Branch-first for M/H: perform changes on feature branches
- Two-phase commit: preview then apply for M/H
- Test-gated: run configured oracles pre/post
- Logging: all changes must be recorded in ActionLog with artifacts

## Approvals
- H-tier changes require human approval unless explicitly waived
- Policy exceptions must be documented with rationale and expiry

## Incident Response
- On violation: stop, record, branch if needed, revert when possible
- Open a task entry in memory-bank/progress.md with a FaultNote
- Replan with reduced scope or additional safeguards

## References
- docs/permissions.md for risk tiers and guards
- docs/safeguards.md for detailed safety mechanisms

> WARNING: Never commit secrets or sensitive data; ensure redaction in all logs and artifacts.