# AtlasRIPER: A Permissioned, Memoryful Agentic Framework For Coding With LMs
Created by Horizon Beta

## Why AtlasRIPER
- Agentic control plane: explicit permissions, transitions, and violation handling to safely grant autonomy.
- RIPER-5 cognition: Reflect → Intent → Plan → Execute → Review as the thinking backbone.
- Persistent memory: role-aware memory bank for continuity across sessions and modes.
- Practical integration: command cheatsheets, MCP/tool/tool-use guidance, and templates ready for real work.

## Core Concepts
- Modes: architect, ask, code, debug, orchestrator. Each mode has rules, inputs, outputs, and allowed permissions.
- Transitions: a guarded directed graph of mode moves, with preconditions and postconditions.
- Permissions: fine-grained capability grants (file edits, command execution, network calls) with risk tiers and review gates.
- Memory bank: durable, structured project memory — brief, active context, tech context, progress, protections, system patterns.

## Lifecycle (RIPER-5 Mapped)
- Reflect: situation, constraints, assumptions, risks → summarized context object.
- Intent: goals, acceptance criteria, non-goals → saved in active context.
- Plan: steps, artifacts, tests, rollback plan → PlanCard in progress.md.
- Execute: gated actions using permissions; every edit/command leaves an artifact (diff/command log).
- Review: verify against acceptance; if fail, isolate fault, update learnings, retry or escalate.

## Quick Start
1. Read docs/overview.md and docs/lifecycle.md
2. Configure permissions in docs/permissions.md
3. Use templates in templates/ to run a RIPER-5 cycle
4. Persist context in memory-bank/ as you go
5. Follow examples/ to see end-to-end flows

## Folder Map
- docs/: core documentation (overview, lifecycle, permissions, transitions, safeguards, MCP integration)
- rules-*/: mode-specific operational rules
- memory-bank/: structured persistent memory templates
- templates/: reusable prompt and artifact templates
- examples/: practical usage examples
- res/: diagrams and images

## Safety Principles
- Default deny: start with minimal permissions and escalate only as needed.
- Two-phase commit: preview changes (plan/diff), then apply with confirmation gates for higher-risk actions.
- Dry runs first: for commands and tool calls, prefer dry-run or no-op simulation when supported.
- Test-gated execution: run tests/linters before and after making changes; require passing checks to proceed for protected areas.
- Violation protocol: on any violation or repeated failure, back off, branch, and request human review.

## Compatibility
- Works with Cursor-like environments, MCP servers, or generic tool adapters.
- Language-agnostic; examples focus on coding agents.

> NOTE: See docs/ for full specifications and templates.