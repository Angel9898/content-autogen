# Zero-Cost Auto-Posting System — Expanded Final Implementation

This repository contains a full implementation scaffold for automated content generation and publishing.
All publish scripts are expanded with complete flows (where possible) and include clear instructions for obtaining and configuring credentials.

**Important:** Never commit secrets into the repo. Add them into GitHub Secrets in your repository settings.

Files:
- scripts/: generation + expanded publish scripts
- helpers/: model clients + validators + utilities
- .github/workflows/: daily and per-platform dry-test/publish workflows
- docs/flowchart.mmd and .png: pictorial representation

Use `SELF_TEST=true` and `DRY_RUN=true` to avoid real publishing during tests.

