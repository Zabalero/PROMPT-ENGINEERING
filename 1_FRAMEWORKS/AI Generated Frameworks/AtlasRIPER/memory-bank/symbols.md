# Symbols And Glossary (AtlasRIPER)

## Modes
- architect: Problem framing, scope, constraints, design
- ask: Research, clarification, documentation lookup
- code: Implementation, refactors, file edits
- debug: Fault isolation, testing, regression analysis
- orchestrator: Multi-step coordination across modes

## Artifacts
- ContextCard: compressed situational summary (Reflect)
- IntentCard: goals, acceptance, non-goals, oracles (Intent)
- PlanCard: steps, permissions, tests, rollback plan (Plan)
- ActionLog: diffs/commands, previews, results (Execute)
- ReviewCard: outcomes vs acceptance, tests, learnings (Review)

## Permissions And Risk
- risk_tier: L | M | H — Low/Medium/High risk classification
- guards: preview, tests, dry-run, max_impact, retry_limit, cooldown
- two-phase commit: preview then apply for M/H actions

## Memory Files
- projectbrief.md: stable high-level context/goals
- activeContext.md: current ContextCard + IntentCard
- techContext.md: stack/deps/constraints
- progress.md: timeline of Plan/Review entries
- protection.md: protected paths and policies
- systemPatterns.md: heuristics and anti-patterns

## Other Symbols
- oracle: an automated verifier (tests, linters, metrics)
- allowlist: approved resources/domains/tools
- preview: proposed diff/command plan before execution
- rollback: revert to safe state after failure
- branch-first: create feature branch for M/H actions

## Abbreviations
- MTTR: mean time to rollback/recover
- LOC: lines of code
- SLO: service level objective

## Conventions
- Keep artifacts ≤ 200 tokens where possible; link long logs/diffs
- Always reference artifacts by path and commit hash when available

> NOTE: Prefer lower-case for non-proper nouns in lists for readability consistency.