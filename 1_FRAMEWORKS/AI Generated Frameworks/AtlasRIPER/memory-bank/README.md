# AtlasRIPER — Memory Bank

Purpose
Durable, role-aware memory to preserve continuity across sessions and mode transitions. Keep artifacts compressed, structured, and inspectable.

Files
- projectbrief.md — stable, high-level goals and context
- activeContext.md — current ContextCard + IntentCard snapshot
- techContext.md — stack, dependencies, constraints, environment
- progress.md — timeline of PlanCard and ReviewCard entries
- protection.md — protected paths, policies, secrets handling
- systemPatterns.md — accumulated heuristics, playbooks, anti-patterns
- symbols.md — canonical symbols, abbreviations, and glossary

Principles
- Compression-first: Summaries ≤ 200 tokens per card unless justified
- Traceability: Link diffs, commits, ActionLog IDs, and artifacts
- Safety: No secrets; redact sensitive tokens; store pointers not raw logs
- Role-aware: Each update notes producing mode (architect/code/debug/ask/orchestrator)

Update cadence
- On Reflect/Intent: update activeContext.md
- On Plan: append PlanCard to progress.md
- On Execute/Review: append ReviewCard to progress.md
- On learning: update systemPatterns.md; on policy change: update protection.md

Templates
Use templates/ to author ContextCard, IntentCard, PlanCard, ReviewCard.