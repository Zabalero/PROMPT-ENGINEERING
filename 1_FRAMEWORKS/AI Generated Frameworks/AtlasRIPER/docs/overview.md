# AtlasRIPER — Overview

## Purpose
AtlasRIPER is a permissioned, memoryful agentic framework for coding with LMs. It blends RIPER-5 cognition with a strict control plane (permissions, transitions, violation protocol) and durable memory. Goal: safe autonomy that can plan → act → verify → correct, repeatedly and reliably.

## Design Pillars
- Cognition backbone (RIPER-5): Reflect → Intent → Plan → Execute → Review, with compressed artifacts at each stage.
- Permissioned execution: default-deny capability grants with risk tiers, previews, and test gates.
- Modeful operation: Architect, Ask, Code, Debug, Orchestrator — each with rules, IO contracts, and allowed permissions.
- Persistent memory: project brief, active context, tech context, progress, protections, system patterns, and symbols.
- Verification-first: linters/tests as oracles, dry runs and two-phase commits for high-risk actions.
- Violation protocol: clear backoff, branch, and escalation rules on policy, test, or safety violations.

## What AtlasRIPER Is Not
- Not a monolithic runtime. It’s a framework and file-level operating model compatible with Cursor-like editors, MCP servers, and generic tool adapters.
- Not a thought dump. It enforces compressed, inspectable artifacts designed for reuse and low token budgets.

## Core Folders
- docs/: specifications (lifecycle, permissions, transitions, safeguards, MCP integration)
- rules-*/: mode-specific operational rules
- memory-bank/: structured persistent memory templates
- templates/: reusable prompt/artifact templates
- examples/: practical end-to-end flows
- res/: diagrams and symbols

## Minimal Loop (High Level)
1. Reflect + Intent: summarize context, goals, constraints → memory-bank/activeContext.md
2. Plan: produce a bounded, test-aware PlanCard → memory-bank/progress.md
3. Execute: apply gated actions via permissions; log diffs/commands → templates/action-log.md (or tool logs)
4. Review: verify vs. acceptance and tests; update learnings; if fail, correct and retry or escalate

## Compatibility
- Works with CursorRIPER.sigma-style permissions and transition controls
- Leverages roo-code-memory-bank-style role memory strategies
- Incorporates RIPER-5 cognition and compression practices

> NOTE: See docs/permissions.md and docs/transitions.md for guard and handoff details.