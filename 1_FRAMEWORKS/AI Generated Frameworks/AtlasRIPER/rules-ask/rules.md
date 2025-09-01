# AtlasRIPER — Ask Mode Rules

Purpose
Efficiently acquire and distill external or internal knowledge to unblock planning or implementation, with strict sourcing and compression.

Inputs
- Specific questions or hypotheses from architect/code/debug
- Allowlisted sources and tools (docs, codebase, registries)
- Current ContextCard/IntentCard

Outputs
- Q&A summary appended to memory-bank/activeContext.md
- Updates to PlanCard or acceptance criteria if findings affect scope
- Citations/links and notes to support traceability

Rules
1) Question-first
- Define crisp questions before searching; avoid broad, unfocused queries.
- Tie each question to a decision it will unblock.

2) Source hygiene
- Use allowlisted domains/tools; capture citations (URL, title, date, version).
- Prefer primary sources (official docs, source code) over posts.

3) Compression discipline
- Summarize findings ≤ 150 tokens per topic.
- Extract key constraints, APIs, version specifics, and edge cases.
- Capture deltas vs prior assumptions.

4) Actionable outcomes
- For each answer, state the decision impact: plan change, test addition, permission adjustment, or no change.

5) Verification when applicable
- Where feasible, run small, safe experiments (read-only or sandbox).
- Document experiment inputs/outputs succinctly.

6) Handoff integrity
- Update Intent/Plan acceptance criteria if findings introduce new requirements or risks.
- Link citations in memory-bank/activeContext.md.

Checklists
- Questions are concrete and mapped to decisions
- Sources are cited and allowlisted
- Summaries are compressed and actionable
- Plan/Intent updated when needed
- No permissions beyond read/network allowlist were used

Anti-patterns
- Copying long text without compression
- Relying on a single secondary source
- Research without tying back to Plan/Intent

Permissions
- net.fetch.readonly (allowlist)
- fs.read (repo/**)
- No writes beyond updating memory-bank with findings

Transition guards
- Enter: concrete questions defined by source mode
- Exit: Q&A summary with citations; deltas reflected in Context/Plan
- See docs/transitions.md for ask entry/exit conditions