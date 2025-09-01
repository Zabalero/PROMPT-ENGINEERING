AtlasRIPER — MCP and Tooling Integration

Objective
Provide a practical mapping between AtlasRIPER’s permissions/guards and tool execution via MCP servers or editor-integrated tools. Tools are represented as capabilities with enforced guards, previews, and logs.

Concepts
- Tool Adapter: An MCP server or editor-native integration that exposes commands (e.g., fs operations, git, test runners).
- Capability Binding: A mapping from a tool command to a permission object in docs/permissions.md.
- Guard Enforcer: Middleware that checks preview/test/branch requirements before allowing a tool call.
- Artifact Logger: Writes ActionLog entries, capturing previews, commands, outputs, and diffs.

Standard capability bindings
- fs.read → MCP fs.readFile / listDirectory
- fs.write.* → MCP fs.writeFile / applyDiff
- fs.refactor.large → MCP applyPatch (multi-file), move/delete
- cmd.run.safe → MCP process.exec for lint/test/build/format
- net.fetch.readonly → MCP http.get (allowlisted domains)
- net.post.external → MCP http.post/put (strict allowlist)

Guard enforcement flow
1) Request: Mode issues a capability request with intent metadata (why, scope, impact estimate)
2) Preview: Adapter generates a preview artifact
   - For fs.write: produce a diff; for cmd.run: a command plan with flags; for net.*: URL/method/body summary
3) Policy check: Compare against permission’s guards (risk tier, max_impact, allowlists, branch requirement)
4) Pre-checks: Run configured oracles (lint/unit as needed)
5) Apply: Execute the tool call; capture outputs/errors
6) Post-checks: Re-run oracles; verify acceptance deltas
7) Log: Write ActionLog entry; link artifacts; update memory-bank/progress.md timeline

ActionLog minimal schema
- timestamp
- mode
- capability (name, risk_tier)
- preview_ref (diff/plan)
- command_or_tool_call (serialized)
- result_summary (pass/fail, deltas)
- artifacts (paths, hashes)
- notes (rationale, next step)

Editor integration notes
- Cursor-like editors: Use native applyDiff, test/lint tasks, and branch management
- Provide dry-run via formatter/linter --check or test --dry-run flags when available
- Ensure all tool outputs are summarized; store large logs out-of-band

HTTP/network policies
- Maintain allowlists in a config file (e.g., docs/permissions.md appendix)
- Redact secrets; never echo tokens in logs
- Rate-limit with cooldown guard

Git/branch operations
- For risk ≥ M:
  - Create feature branch atlasriper/{ticket-or-task}
  - Commit after each logical step with concise message and artifact references
  - On failure: revert or cherry-pick rollback; keep failure notes

Extensibility
- New tool = new capability binding + guards
- Add adapter-specific notes in docs/tools/{adapter}.md

Quick example (pseudo)
- Request: fs.write.medium to modify src/utils.ts (impact est: 12 LOC)
- Preview: diff generated (ActionLog#123)
- Policy: preview_required=true, test_gate=unit → ok
- Pre-check: run unit tests (pass)
- Apply: write diff
- Post-check: unit + lint (pass)
- Log: ActionLog#124 with summary and artifact refs