# AtlasRIPER — Quick Start

Goal
Run a minimal AtlasRIPER lifecycle on a coding task with safe guardrails.

Scenario
Task: Add a utility function and unit test with small, verifiable changes.

1) Reflect + Intent (architect)
- Fill templates/context-card.md and templates/intent-card.md
- Update memory-bank/activeContext.md with ContextCard + IntentCard
Example (compressed)
- Objective: Add sum(a,b) with tests and export
- Acceptance: test passes, linter clean, ≤ 10 LOC modified, no public API break

2) Plan (architect → plan)
- Create a PlanCard using templates/plan-card.md; append summary to memory-bank/progress.md
- Risk: Low; Oracles: unit tests + linter
- Permissions: fs.write.small, cmd.run.safe

3) Execute (code)
- Preview changes
  - Implement sum in src/utils.ts (≤ 10 LOC)
  - Export from index
  - Add unit test
- Run pre-check
  - npm run lint
  - npm test (baseline)
- Apply edits (fs.write.small); commit on feature branch atlasrIPER/demo-sum
- Post-check
  - npm run lint
  - npm test
- Log ActionLog with diff and results (location of logs dependent on editor/tool)

4) Review (review)
- Fill templates/review-card.md and append to memory-bank/progress.md
- If pass: mark outcome=pass; update systemPatterns.md if a new heuristic discovered
- If fail: route to debug with reproduction steps

Example artifacts (summaries)
- PlanCard: risk L, steps: implement, test, export; oracles: lint+unit
- ReviewCard: tests pass; 8 LOC changed; no regressions

Command snippet (see docs/command_cheatsheet.md)
- git checkout -b atlasriper/demo-sum
- npm run lint -- --max-warnings=0
- npm test
- git add -A && git commit -m "AtlasRIPER: add sum util [artifacts: progress.md#entry]"
- npm test

Notes
- Keep cards ≤ 200 tokens; link to diffs/commits instead of pasting them.
- For Medium/High work, require previews and branch-first policy; expand tests to include e2e as needed.