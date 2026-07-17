# Security policy

## Scope

This repository packages a Claude Code plugin that connects to LeadMagic’s hosted MCP server (`https://mcp.leadmagic.io`). Most MCP tools are read-only enrichment/discovery helpers. A small set of bulk tools enqueue asynchronous enrichment jobs (`readOnlyHint: false`); they do not delete or overwrite customer data.

## Reporting vulnerabilities

1. Email `security@leadmagic.io` with description, reproduction steps, and impact.
2. Do **not** open a public GitHub issue for security vulnerabilities.

## Hardening

- Never commit tokens, assertions, or credentials.
- Plugin ships **no API keys** — OAuth is completed in the client; LeadMagic resolves Bearer tokens server-side.
- Bulk write tools are gated by a PreToolUse confirmation hook.
- Keep dependencies minimal; this plugin is primarily Markdown + shell hooks.
