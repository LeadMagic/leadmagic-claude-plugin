# Changelog

## 0.3.17 — 2026-11-02

- Keep policy unit tests in memory and move process, installation-path, and interpreter-startup checks into the CI workflow. The unit harness no longer launches processes or constructs process environments; CI still verifies the actual manifest command using synthetic values and an empty tool path.
- Keep the v0.3.16 input-only runtime, confirmation prompts, OAuth connector, skills, commands, agents, and repository source unchanged.

## 0.3.16 — 2026-11-02

- Replace the shell approval hook with an isolated Python standard-library implementation that reads only its supplied input and explicit preference argument. Remove the Bash and `jq` runtime dependencies; the hook requires Python 3.9 or newer at `/usr/bin/python3`.
- Remove automatic permission grants to address the directory's `HOOK_GRANTS_PERMISSION` finding. Reads, previews, and automatic session modes use Claude Code's own permission rules; guarded actions still request confirmation in normal modes.
- Preserve all 10 bundled skills, 12 commands, two agents, OAuth connection, and directory listing metadata. Verify the directory source and installation references point to `LeadMagic/leadmagic-claude-plugin` on `main`.

## 0.3.15 — 2026-11-02

- Run the approval hook with `/bin/bash -p` through its executable entrypoint, preventing inherited startup files, exported functions, and shell-option variables from affecting it. Approval decisions, the exec-form `ask_all` argument, and OAuth MCP configuration are unchanged.
- Reject prohibited `.env` files in the publication checker without reading their contents. Add regression coverage for both changes.
- Preserve the directory listing URLs. Local validation cannot establish remote directory policy clearance; Anthropic review and publication remain separate steps.

## 0.3.14 — 2026-11-02

- The approval hook now runs in exec form and receives the `ask_all` option as an argument (`${user_config.ask_all}`) instead of reading `CLAUDE_PLUGIN_OPTION_ASK_ALL` from its environment. The hook reads no environment values. Builds that ignore exec-form `args` run the hook with the policy on.

## 0.3.13 — 2026-11-02

- The approval-hook opt-out is now a plugin option, `ask_all`, which Claude Code passes to the hook as `CLAUDE_PLUGIN_OPTION_ASK_ALL`. It replaces the `LEADMAGIC_ASK_ALL` environment variable, so the plugin no longer reads values from the user's environment. The approval policy is otherwise unchanged.
- Drop the `icon` field and `assets/icon.png`. The directory listing icon is set in the directory itself, and Claude Code ignores the field.

## 0.3.12 — 2026-11-02

- Move the publisher and version consistency checks out of the public-file secret scanner into `scripts/check-publisher-metadata.py`. The secret scanner no longer reads plugin manifests, which the directory scan read as a credential forward. Both run in CI; the plugin's runtime behavior is unchanged.

## 0.3.11 — 2026-10-27

- Clarify the approval-hook opt-out wording in its comment and read-decision explanation; permission decisions and execution options are unchanged.

## 0.3.10 — 2026-10-27

- Launch the approval hook with the system Bash and enable its strict execution options by name, preserving all permission decisions and failure behavior.
- Exercise the executable hook entrypoint, including normal permission fallback without `jq`, and verify its execution options cannot be shadowed by a shell function.

## 0.3.9 — 2026-10-27

- Invoke Bash's strict-mode builtin explicitly, preserving the existing `errexit`, `nounset`, and `pipefail` flags and approval policy.

## 0.3.8 — 2026-10-27

- Rename the local approval-presence flag to make its boolean role explicit for directory review. The hook reads presence only and emits permission decisions, never confirmation receipt values.

## 0.3.7 — 2026-10-17

- Ask before workspace mutations and exports, including automation toggles, sheet configuration, row additions, pauses, cancellations, and restores.
- Keep known preview calls and reads automatic, and honor the session's selected automatic permission mode.
- Align the hook with the public LeadMagic skills policy and cover both bundled and hand-added MCP tool names.

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

