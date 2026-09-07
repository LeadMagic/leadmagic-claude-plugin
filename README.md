# LeadMagic Claude Code Plugin: B2B Research and MCP Enrichment

Official LeadMagic plugin for [Claude Code](https://code.claude.com): skills, agents, credit-safe hooks, and the hosted MCP connector at `https://mcp.leadmagic.io/mcp`.

[LeadMagic B2B enrichment](https://leadmagic.io?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-intro) · [MCP setup guide](https://leadmagic.io/docs/mcp/setup?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-intro) · [Pricing and credits](https://leadmagic.io/pricing?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-intro)

> Search access and rate limits depend on your plan. Check [current pricing](https://leadmagic.io/pricing?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-intro) before a large run; the `market-search` skill covers pagination and account entitlements.
>
> Prefer raw REST + API-level skills? See [LeadMagic/leadmagic-skills](https://github.com/LeadMagic/leadmagic-skills) (`npx skills add LeadMagic/leadmagic-skills`).

## Current integration contract

Reviewed against [LeadMagic's public documentation](https://leadmagic.io/docs?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-current-integration-contract) on 2026-09-06. REST uses `https://api.leadmagic.io` and `X-API-Key`; hosted MCP uses `https://mcp.leadmagic.io/mcp` with OAuth; lm-tui uses `lm login`. Keep credentials and customer data out of committed examples.

Email Finder returns validated work emails. Use Email Validation for externally sourced addresses. Check the [current pricing and credit rules](https://leadmagic.io/docs/v1/credits?utm_source=github&utm_medium=readme&utm_campaign=leadmagic-claude-plugin&utm_content=readme-current-integration-contract) before paid work; costs are endpoint- and plan-dependent. API-only integrations must not send app-only `preview` options.


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
