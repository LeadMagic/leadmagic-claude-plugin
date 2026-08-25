# LeadMagic for Claude Code

Official LeadMagic plugin for [Claude Code](https://code.claude.com): skills, agents, credit-safe hooks, and the hosted MCP connector at `https://mcp.leadmagic.io/mcp`.

> **Unlimited search on Professional & Ultimate plans:** People, Company, and Jobs Search are credit-free with no volume cap — rate-limited only (5 req/s Professional, 10 req/s Ultimate). The `market-search` skill teaches Claude to use that properly, including cursor pagination.
>
> Prefer raw REST + API-level skills? See [LeadMagic/leadmagic-skills](https://github.com/LeadMagic/leadmagic-skills) (`npx skills add LeadMagic/leadmagic-skills`).

## Install

### From a local checkout (dev)

```bash
claude --plugin-dir /path/to/mcp-claude-plugin
```

### From GitHub (after the public repo is published)

```text
/plugin marketplace add LeadMagic/leadmagic-claude-plugin
/plugin install leadmagic@leadmagic-plugins
```

Or submit/install via the [Claude plugin directory](https://claude.com/docs/plugins/submit).

## Connect

1. After install, Claude Code loads the `leadmagic` MCP server (HTTP → `https://mcp.leadmagic.io/mcp`).
2. Complete OAuth (Clerk + PKCE) in the browser.
3. Try: *Check my LeadMagic credit balance.*

No API keys in the client — tokens are resolved server-side.

## Skills

| Skill | Purpose |
|-------|---------|
| `get-started` | Credits + first safe outcome |
| `account-research` | Company / GTM briefing |
| `contact-lookup` | Find or validate work email |
| `decision-makers` | Buyers / roles at a company |
| `hiring-intent` | Jobs + hiring signals |
| `market-search` | Broad people/company/jobs search — unlimited-plan aware, cursor pagination |
| `ads-research` | Google / Meta / B2B creatives |
| `bulk-enrichment` | CSV queue + poll |
| `credit-guard` | Spend discipline |

## Agents

- `leadmagic-gtm` — general research & enrichment
- `leadmagic-bulk` — file / multi-row jobs

## Credit safety

A PreToolUse hook asks before bulk write tools (`submit_*`, CSV upload session helpers). Free helpers: `check_credit_balance`, `preview_cost`, `get_account_analytics`, `get_job_search_catalogs`, `resolve_job_search_filters`.

## Validate

```bash
claude plugin validate .
claude plugin validate --strict .
```

## Related

- Hosted MCP / Connectors Directory: `https://mcp.leadmagic.io/mcp`
- Docs: [leadmagic.io/docs/mcp/introduction](https://leadmagic.io/docs/mcp/introduction?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin)
- Privacy: [leadmagic.io/privacy](https://leadmagic.io/privacy?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin)
- Support: [leadmagic.io/docs/support](https://leadmagic.io/docs/support?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin)

## License

MIT — see [LICENSE](./LICENSE).
