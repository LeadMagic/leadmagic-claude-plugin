# Changelog

## 0.3.6 — 2026-10-13

- Publish the plugin as LeadMagic Corporation (#24).

## 0.3.5 — 2026-10-13

- Validate approval-hook JSON fields and preserve normal permissions for invalid input or a missing `jq` installation.
- Cover both bundled and hand-added MCP tool names, and require approval for new acting tools until their preview contract is known.
- Keep default-mode approval for cell edits, sheet cancellation, and upload widgets; preserve the session's selected automatic permission mode.
- Check public files in CI and document the standalone public policy ownership.

## 0.3.4 — 2026-10-12

- Contact lookup reports the exact `valid`, `invalid`, or `unknown` email status; catch-all/unknown is never treated as deliverable, and the waterfall proceeds only until a valid result.
- Plugin and marketplace author support email is `support@leadmagic.io`.
- README distinguishes a remote marketplace installation from the exact local checkout loaded with `--plugin-dir`.

## 0.3.3 — 2026-10-12

- Guidance matches the current hosted MCP tools: bulk submits use `submit_detected_bulk_job`, and Sheets imports, runs, and saved lists use each tool's own named parameters.

## 0.3.2 — 2026-10-12

- Directory listing: icon, documentation, support, and terms of service links.

## 0.3.1 — 2026-10-12

- Command argument hints are valid YAML.
- Agents and the approval hook use the plugin-scoped MCP tool names.
- Asks before Sheet cell edits, stopping a sheet run, and connected-app imports.
- Adds the privacy policy URL to the manifest.

## 0.3.0 — 2026-10-12

- New `sheets` and `outbound-recipes` skills.
- New commands: `enrich-sheet`, `build-list`, `tam-map`, `lookalikes`, `job-change-sweep`, `waterfall-email`, `usage-report`, `find-buyers`, and `hiring-signals`.
- `bulk-enrichment`, `contact-lookup`, `account-research`, and `market-search` updated for the current tool set.
- Skill descriptions now say when to use each skill.
- README documents what the approval hook allows and asks for. Cell edits and cancelling sheet runs ask immediately in the default permission modes; automatic modes retain their selected behavior.
- Bulk examples use the public `submit_detected_bulk_job` tool.

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

