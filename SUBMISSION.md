# Claude plugin directory — submission copy

Use with https://claude.ai/admin-settings/directory/submissions/plugins/new  
(or https://platform.claude.com/plugins/submit)

## Basics

| Field | Value |
|-------|--------|
| Plugin name | LeadMagic |
| Display name | LeadMagic |
| Version | 0.1.0 |
| Public GitHub | `https://github.com/LeadMagic/leadmagic-claude-plugin` (publish this package) |
| Homepage | https://leadmagic.io/docs/mcp/introduction |
| Support | https://leadmagic.io/docs/support |
| Privacy | https://leadmagic.io/privacy |
| License | MIT |

## One-liner

B2B enrichment for Claude Code — research accounts, validate work emails, hiring & ads signals, and credit-safe bulk CSV jobs.

## Description

LeadMagic connects Claude Code to hosted MCP (`https://mcp.leadmagic.io/mcp`) for account research, work email discovery/validation, decision-maker search, hiring intent, ads research, analytics, and queued bulk enrichment. Includes skills, GTM/bulk agents, and a PreToolUse confirmation gate before credit-consuming bulk tools. OAuth only — no API keys in the client.

## Categories / keywords

productivity, sales, data, gtm, enrichment, mcp

## Pre-submit

```bash
claude plugin validate --strict .
```

- [x] Public GitHub repo created and pushed
- [x] `claude plugin validate --strict` passes
- [ ] OAuth smoke: `check_credit_balance` after install
- [x] Skills invoke without LinkedIn/mobile marketing copy
- [x] Bulk hook prompts on `submit_*`
- [x] Directory Terms / Policy acknowledged in form
- [x] Submitted to Claude plugin directory (2026-07-16) — in review

## Notes for reviewers

- MCP URL: `https://mcp.leadmagic.io/mcp` (bare origin also accepted)
- Same production OAuth as the Connectors Directory listing
- Free helpers do not consume LeadMagic credits
- Bulk tools enqueue jobs; poll status ≥45s between calls
