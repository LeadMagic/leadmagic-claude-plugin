# Changelog

## 0.3.22 — 2026-11-13

- `plugin.json` holds metadata only. Skills, commands, agents, and the hosted MCP server load from their standard locations (`skills/`, `commands/`, `agents/`, `.mcp.json`).
- Agents no longer pin a Claude Code-only tool name, so they load the same way in Claude Code, claude.ai, and Cowork.

## 0.3.21 — 2026-11-09

- Remove outdated setup wording from the docs. The plugin's only connection is the hosted MCP server, signed in with OAuth.
- Condense the changelog. The full history is in the [commit log](https://github.com/LeadMagic/leadmagic-claude-plugin/commits/main).

## 0.3.18 – 0.3.20 — 2026-11-09

- Meet Claude plugin directory policy: no hooks, no scripts or binary assets, and no CI step that scans files for secrets (GitHub secret scanning covers that).
- Paid and destructive actions stay gated by the hosted server's preview and `confirmation_token`, the `credit-guard` skill, and Claude Code's own permission rules.

## 0.3.0 – 0.3.17 — 2026-10-12 to 2026-11-02

- Added the Sheets, outbound-recipes, and market-search skills and nine slash commands (`/build-list`, `/enrich-sheet`, `/find-buyers`, `/hiring-signals`, `/job-change-sweep`, `/lookalikes`, `/tam-map`, `/usage-report`, `/waterfall-email`).
- Publisher metadata names LeadMagic Corporation; directory listing links added to `plugin.json`.

## 0.1.0 – 0.2.2 — 2026-09-06 to 2026-10-01

- Initial release: hosted MCP connector at `https://mcp.leadmagic.io/mcp` (OAuth), research and enrichment skills, the `leadmagic-gtm` and `leadmagic-bulk` agents, and credit-safe bulk workflows.
