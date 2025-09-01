# AtlasRIPER — Command Cheatsheet (agent/operator quick reference)

Purpose
Standardize common operations with preview-first, test-gated commands. Adapt flags to your environment.

Conventions
- Use preview (dry-run/--check) when available before apply.
- For Medium/High risk: operate on feature branch atlasriper/{task}.
- Log artifacts: store diff previews and outcomes referenced in ActionLog.

Git and branching
- Create feature branch (M/H):
  git checkout -b atlasriper/{task}
- Stage and commit:
  git add -A && git commit -m "AtlasRIPER: {step} [artifacts: paths/ids]"
- Show staged diff (preview):
  git diff --staged
- Revert last commit:
  git revert HEAD
- Discard local changes (use carefully):
  git reset --hard && git clean -fd

Linters/formatters (examples)
- ESLint preview:
  npm run lint -- --max-warnings=0
- Prettier check:
  npx prettier . --check
- Prettier write (apply):
  npx prettier . --write

Testing
- Run unit tests (pre/post):
  npm test
- Run a specific test:
  npm test -- -t "pattern"
- Jest dry-run (list tests):
  npm test -- --listTests
- Vitest:
  npx vitest run

Build
- Local build:
  npm run build
- TypeScript check (no emit):
  npx tsc --noEmit

Diff and patch (editor/tool adapters can replace)
- Preview diff for a file:
  git diff -- path/to/file
- Apply a patch (generated preview to apply):
  git apply path/to/patch.diff

Safety utilities
- Search protected areas:
  git ls-files "docs/**" ".github/**" ".vscode/**"
- Count LOC in diff (impact estimate):
  git diff --shortstat

HTTP (read-only research)
- Curl preview (headers only):
  curl -I https://example.com/docs
- Curl GET (store to temp file):
  curl -sS https://example.com/docs -o tmp/doc.html

Notes
- Always capture previews and outcomes in ActionLog with timestamps and references.
- Use allowlists for network access; redact secrets.