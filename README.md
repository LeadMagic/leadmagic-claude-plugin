# LeadMagic Claude Code Plugin: B2B Research and MCP Enrichment

<img src="https://raw.githubusercontent.com/LeadMagic/leadmagic-claude-plugin/main/assets/logo.svg" width="64" height="64" alt="LeadMagic logo">

Official LeadMagic plugin for [Claude Code](https://code.claude.com): skills, agents, an approval-policy hook, and the hosted MCP connector (70+ tools; Sheets tools appear only when your workspace has Sheets) at `https://mcp.leadmagic.io/mcp`.

[LeadMagic B2B enrichment](https://leadmagic.io?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-intro) · [MCP setup guide](https://leadmagic.io/docs/mcp/setup?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-intro) · [Pricing and credits](https://leadmagic.io/pricing?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-intro)

> Search cost, rate limits, and fair-use caps depend on your plan. Check [current pricing](https://leadmagic.io/pricing?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-intro) before a large run; the `market-search` skill covers pagination and plan-dependent search cost.
>
> Prefer raw REST + API-level skills? See [LeadMagic/leadmagic-skills](https://github.com/LeadMagic/leadmagic-skills) (`npx skills add LeadMagic/leadmagic-skills`).

## What this plugin connects to

- **One network endpoint.** The plugin's only server is `https://mcp.leadmagic.io/mcp`, over HTTP with OAuth sign-in in your browser. No API key goes into any config file.
- **Nothing sent elsewhere.** The plugin's skills, agents, commands, and hook send nothing to any other host. The hook is a local shell script that makes no network calls.
- **Custom HTTP sheet columns are configured in the LeadMagic app, not through this plugin.** If you set one up there, LeadMagic's servers call the host you chose, with that row's values.

Prefer raw REST with an API key? That lives in a separate project: [LeadMagic/leadmagic-skills](https://github.com/LeadMagic/leadmagic-skills). Finder tools return already-validated work emails. Use `validate_work_email` only for addresses that came from somewhere else. Costs depend on the tool and your plan — see the [credit rules](https://leadmagic.io/docs/v1/credits?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-connects-to), and call the free `preview_cost` before paid work.

## Install

### From a local checkout (dev)

```bash
claude --plugin-dir /path/to/leadmagic-claude-plugin
```

### From GitHub

```text
/plugin marketplace add LeadMagic/leadmagic-claude-plugin
/plugin install leadmagic@leadmagic-plugins
```

Or submit/install via the [Claude plugin directory](https://claude.com/docs/plugins/submit).

## Connect

1. After install, Claude Code loads the `leadmagic` MCP server (HTTP → `https://mcp.leadmagic.io/mcp`).
2. Complete OAuth sign-in in the browser.
3. Try: *Check my LeadMagic credit balance.*

The bundled connection uses OAuth; no REST API key is required.

## Skills

| Skill | Purpose |
|-------|---------|
| `get-started` | Credits + first safe outcome |
| `account-research` | Company / GTM briefing |
| `contact-lookup` | Find or validate work email |
| `decision-makers` | Buyers / roles at a company |
| `hiring-intent` | Jobs + hiring signals |
| `market-search` | Broad people/company/jobs search — plan-aware cost, fair-use cap, cursor pagination |
| `bulk-enrichment` | CSV / list jobs, local-business lists, watch, export, restart |
| `credit-guard` | Spend discipline |
| `sheets` | Build, run, and read LeadMagic Sheets (enrichment + AI columns) |
| `outbound-recipes` | Composable multi-step outbound recipes |

## Commands

| Command | What it does |
|---------|--------------|
| `/leadmagic:check-credits` | Credit balance (free) |
| `/leadmagic:research-company` | Account brief via `account_intel` |
| `/leadmagic:validate-email` | Validate one work email |
| `/leadmagic:waterfall-email` | Cheapest-first email for one contact |
| `/leadmagic:find-buyers` | Buyers at a target account |
| `/leadmagic:build-list` | ICP prospect list via search |
| `/leadmagic:tam-map` | Segment and size a market |
| `/leadmagic:lookalikes` | Expand from seed companies |
| `/leadmagic:hiring-signals` | Rank accounts by hiring activity |
| `/leadmagic:job-change-sweep` | Find contacts who changed jobs |
| `/leadmagic:enrich-sheet` | Build and run columns in a sheet |
| `/leadmagic:usage-report` | Credit and usage report (free) |

## Agents

- `leadmagic-gtm` — general research & enrichment
- `leadmagic-bulk` — file / multi-row jobs

## Credit safety and approval prompts

Claude Code normally asks before every MCP tool call. Left alone, a long LeadMagic task would stall on a prompt at every step. So the plugin ships a `PreToolUse` hook (`scripts/approval-policy.sh`) that answers some of those prompts for you.

**What the hook auto-approves (no prompt):**

- **Read and single-record tools**: lookups, searches, validation, composites like `account_intel`, sheet reads, and cell edits.
- Some of these spend a credit or two per call. The `credit-guard` skill has the model call the free `preview_cost` before anything larger.

**What still asks, with a reason naming the tool and what to check:**

| Group | Tools |
| --- | --- |
| Bulk jobs | `submit_bulk_job`, `submit_detected_bulk_job`, `create_bulk_upload_session`, `process_attached_csv`, `restart_bulk_job`, `find_local_leads` |
| Paid runs | `run_sheet_column`, `resume_bulk_job`, `set_sheet_column_auto_run` |
| Recipe import | `import_sheet_recipe` |
| Deletes | `delete_sheet_rows`, `delete_sheet_column` |

The hook's internal list also names a few other server-gated tool names. It mirrors the server's own approval gate, and this plugin does not currently expose those tools.

**How the two-step approval works:**

- These tools act in two steps on the server. The first call only returns a preview and a `confirmation_token`.
- Nothing runs until a second call carries that token.
- The hook lets the preview through and asks you once, on the call that would act.
- The two upload-widget openers (`create_bulk_upload_session`, `process_attached_csv`) always ask in the default permission mode.

**Permission modes:**

- If your session already skips approval prompts (`permission_mode` of `bypassPermissions`, `auto`, or `dontAsk`), the hook allows those tools instead of returning `ask`. A hook `ask` would otherwise force a prompt even in auto mode.
- `default`, `acceptEdits`, and `plan` modes still ask.

**Always allowed:** `cancel_*` and `pause_*` run without asking, because they stop spend rather than start it.

**Your own rules win:** your `permissions.deny` and `permissions.ask` rules still take precedence over the hook.

**Opt out:** set `LEADMAGIC_ASK_ALL=1` in the environment Claude Code runs in. That restores stock Claude Code prompting for every LeadMagic tool.

**Connected LeadMagic without the plugin** (`claude mcp add …`)? Hooks only ship with the plugin. Paste the equivalent policy into `~/.claude/settings.json` instead. The snippet is in the LeadMagic app under Settings → API → AI tooling → Claude Code.

## Validate

```bash
claude plugin validate .
claude plugin validate --strict .
```

## Related

- Hosted MCP / Connectors Directory: `https://mcp.leadmagic.io/mcp` for every client (the bare origin still works for existing installs)
- Docs: [leadmagic.io/docs/mcp/introduction](https://leadmagic.io/docs/mcp/introduction?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-related)
- Privacy: [leadmagic.io/privacy](https://leadmagic.io/privacy?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-related)
- Support: [leadmagic.io/docs/support](https://leadmagic.io/docs/support?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-related)

## License

MIT — see [LICENSE](./LICENSE).

## Public examples and publication

Examples are fictional unless an explicit public source is cited. See [PUBLICATION.md](PUBLICATION.md) for data, claims, attribution, and disclosure requirements.

## Related LeadMagic projects

- [Cursor integration](https://github.com/LeadMagic/leadmagic-cursor-plugin)
- [LeadMagic API skills](https://github.com/LeadMagic/leadmagic-skills)

## License and contributions

[MIT license](LICENSE) · [Third-party materials and contribution policy](LICENSE-NOTES.md). Reuse is allowed under the license; changes to this repository require maintainer review.
