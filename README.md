# LeadMagic Claude Code Plugin: B2B Research and MCP Enrichment

Official LeadMagic plugin for [Claude Code](https://code.claude.com): skills, agents, commands, and the hosted MCP connector (available tools depend on your workspace; Sheets tools appear when your workspace has Sheets) at `https://mcp.leadmagic.io/mcp`.

Published by LeadMagic Corporation.

[LeadMagic B2B enrichment](https://leadmagic.io?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-intro) · [MCP setup guide](https://leadmagic.io/docs/mcp/setup?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-intro) · [Pricing and credits](https://leadmagic.io/pricing?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-intro)

> Search cost, rate limits, and fair-use caps depend on your plan. Check [current pricing](https://leadmagic.io/pricing?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-intro) before a large run; the `market-search` skill covers pagination and plan-dependent search cost.
>
> Prefer raw REST + API-level skills? See [LeadMagic/leadmagic-skills](https://github.com/LeadMagic/leadmagic-skills) (`npx skills add LeadMagic/leadmagic-skills`).

## What this plugin connects to

- **One network endpoint.** The plugin's only server is `https://mcp.leadmagic.io/mcp`, over HTTP with OAuth sign-in in your browser. The plugin stores no keys.
- **Nothing sent elsewhere.** The plugin's skills, agents, and commands send nothing to any other host. The plugin ships no hooks.
- **Custom HTTP sheet columns are configured in the LeadMagic app, not through this plugin.** If you set one up there, LeadMagic's servers call the host you chose, with that row's values.

Prefer the REST API? That lives in a separate project: [LeadMagic/leadmagic-skills](https://github.com/LeadMagic/leadmagic-skills). Finder tools return already-validated work emails. Use `validate_work_email` only for addresses that came from somewhere else. Costs depend on the tool and your plan — see the [credit rules](https://leadmagic.io/docs/v1/credits?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-connects-to), and call the free `preview_cost` before paid work.

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

The GitHub marketplace install uses the remote source revision held by Claude Code's marketplace cache; it does not mirror a local checkout. A local checkout may contain newer, uncommitted, or branch-only changes. To test the exact files in a checkout, use `claude --plugin-dir /path/to/leadmagic-claude-plugin` instead.

Directory availability depends on approval of the listing. Use the GitHub installation above until LeadMagic appears in the [Claude directory](https://claude.ai/directory).

## Connect

1. After install, Claude Code loads the `leadmagic` MCP server (HTTP → `https://mcp.leadmagic.io/mcp`).
2. Complete OAuth sign-in in the browser.
3. Try: *Check my LeadMagic credit balance.*

The bundled connection uses OAuth sign-in.

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

Claude Code's own permission rules control every MCP tool call. The plugin ships no hooks; set the MCP permissions you want in Claude Code (`permissions.allow`, `permissions.ask`, `permissions.deny`).

**Server-side two-step approval:** bulk jobs, paid sheet runs, CRM/sequencer imports, outbound pushes, and deletes act in two steps on the hosted server. The first call returns only a preview with the scope, the maximum credits, and a `confirmation_token`. Nothing runs until a second call carries that token. Every paid sheet run needs approval, including small samples and AI columns; only runs the server verifies are free can start immediately.

The `credit-guard` skill and both agents tell Claude to show you that quote and wait for your explicit approval before resending with the token, and to call the free `preview_cost` before any large single-record call.

To be prompted on every acting call as well, add an `ask` rule, for example `"mcp__plugin_leadmagic_leadmagic__run_sheet_column"`, or `"mcp__plugin_leadmagic_leadmagic"` for every LeadMagic tool.

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
