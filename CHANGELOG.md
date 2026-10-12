# Changelog

## 0.3.0 — 2026-10-12

Aligns the plugin with the tools the hosted MCP serves today, and adds Sheets, outbound recipes, and ten workflow commands.

- `research_account` is replaced by `account_intel` (and `enrich_company` for firmographics only) in `/leadmagic:research-company`, `account-research`, and `get-started`. References to job-search catalog and filter helpers are gone; `search_jobs` filters cover them.
- `market-search` is rewritten. Browse search (people, company, jobs) is credit-free only on qualifying plans, within the plan's rate limit and a fair-use cap of about 10M records a month (13,333 searches a day at 25-row pages, or the contract's limit if lower). Lookalikes, full search, exports, and contact unlocks stay metered. Page sizes now match the server: 25 rows on the credit-free lane. Plan details link to [pricing](https://leadmagic.io/pricing) instead of hardcoded numbers.
- New `sheets` skill: read the sheet card first, add columns in one call, one `run_sheet_column` per pipeline, the confirmation-token flow, the 10,000 row-id selection cap, and soft-delete undo. It covers enrichment and AI columns; custom HTTP columns are set up in the LeadMagic app.
- New `outbound-recipes` skill: MCP-only recipes with the fair-use cap stated and no plan prices.
- `bulk-enrichment` adds `watch_bulk_job_progress`, `export_bulk_job` (CSV up to 4 MB), pause / resume / restart, `get_bulk_job_errors`, and `find_local_leads` (200 credits per keyword × location, charged up front after confirmation).
- `contact-lookup` and `account-research` add `search_profile`, `email_to_b2b_profile`, `enrich_company`, and `find_company_funding`.
- New commands: `enrich-sheet`, `build-list`, `tam-map`, `lookalikes`, `job-change-sweep`, `competitor-ads`, `waterfall-email`, `usage-report`, `decision-makers`, and `hiring-signals`. List workflows hand more than 5 rows to a sheet or bulk job.
- Every skill description now says what it does and when to use it. Both agents carry the core spend rules inline; `leadmagic-gtm` gains a Sheets clause.
- The README approval table lists only tools this plugin exposes, adding `find_local_leads`, `import_sheet_recipe`, and `set_sheet_column_auto_run`. The README now states plainly what the hook auto-approves and what it asks for, that it honors `permission_mode`, the `LEADMAGIC_ASK_ALL=1` opt-out, and that the plugin connects only to `https://mcp.leadmagic.io/mcp` over OAuth. The hook's own list is unchanged; it mirrors the server's approval gate.
- The tool count reads 75+ instead of 130+. The redundant `hooks` field is removed from `plugin.json` (`hooks/hooks.json` loads automatically).

The bundled MCP server now points at `https://mcp.leadmagic.io/mcp`, the canonical URL for every client. The bare origin keeps working, so existing installs need no change.

When the session `permission_mode` is `bypassPermissions`, `auto`, or `dontAsk`, the approval hook allows paid and destructive LeadMagic tools instead of forcing an extra prompt. Default, accept-edits, and plan mode still ask. Plugin CI covers both cases.

Plugin CI smoke-tests the approval hook for both plugin-scoped (`mcp__plugin_leadmagic_leadmagic__*`) and hand-added (`mcp__leadmagic__*`) tool names, including preview-vs-token asks and the silent cases.

## 0.2.2 — 2026-10-01

The approval hook and both agents now apply to this plugin's own tools. Claude Code names a plugin-bundled server's tools `mcp__plugin_leadmagic_leadmagic__<tool>`, so the old `mcp__leadmagic__.*` matcher never fired: every LeadMagic call fell back to Claude Code's default permission prompt, and the agents had no LeadMagic tools. The hook and agents now match both the plugin-scoped names and a hand-added `leadmagic` server. Sheet runs of 5 credits or less no longer return a confirmation token, so filling a few new rows prompts nothing.

## 0.2.1 — 2026-09-23

One approval prompt per paid or destructive action. The hosted MCP now answers the first call to those tools with a preview and a `confirmation_token`, and acts only on a follow-up call carrying it, so the hook lets the preview through and asks on the follow-up. The CSV upload widget openers still ask every time.

## 0.2.0 — 2026-09-15

Approval policy hook. Read and single-record LeadMagic tools now run without a permission prompt; bulk jobs, paid runs, CRM/sequencer imports, outbound pushes and deletes still ask, with a reason naming the tool and what to check first. Replaces the bulk-only `credit-guard-bulk.sh` gate. Set `LEADMAGIC_ASK_ALL=1` to restore prompting for every tool.

## Public-content privacy review — 2026-09-06

Use synthetic contact examples, remove unnecessary identity and credential-like samples, and clarify publication, attribution, and claims requirements.


## Unreleased — 2026-09-06

Clarify OAuth, credit-aware use, and source-aware email validation; add public-file safety checks.

