---
name: credit-guard
description: Spend discipline for LeadMagic MCP — free helpers first, composites over chains, confirmation tokens, no duplicate lookups or per-row loops. Use when any LeadMagic call may spend credits, before bulk jobs or sheet runs, or when the user asks about cost or usage.
---

# Credit guard

## Trigger
Use whenever enrichment may spend credits, before bulk jobs, or when the user asks about cost/usage.

## Rules
1. Free first: `check_credit_balance`, `preview_cost`, `get_account_analytics`. Narrow job searches with `search_jobs` filters and a small `limit` rather than broad pulls.
2. Prefer composites (`account_intel`, `enrich_contact`, `find_decision_makers`) over long primitive chains.
3. Do not repeat the same lookup for identical inputs in one session.
4. More than 5 rows → a sheet run (`sheets` skill) or a bulk job (`bulk-enrichment` skill). Never loop single-record tools per row.
5. Empty/not-found results are usually free — say so when reporting.
6. Don't ask before single-record lookups or a sheet run of 5 credits or less (e.g. filling a few new rows) — they run directly. Bulk jobs, bigger sheet runs, imports, outbound pushes and deletes answer first with `needs_confirmation`, a summary and a `confirmation_token` — nothing has run. Show the summary; only after the user agrees, repeat the call with the token (the plugin hook prompts on that call). Single-record paid tools do not — before any call you expect to exceed ~25 credits (`search_people` with limit > 25 on a metered plan, `find_company_employees`, `account_intel` with jobs), call `preview_cost` and ask.
7. Browse search (`search_people`, `search_companies`, `search_jobs`) is credit-free only on qualifying plans and within a fair-use cap; see the `market-search` skill and [pricing](https://leadmagic.io/pricing).

## Output
- Credits remaining / estimated cost when known
- Recommended cheapest path
- Clear stop if balance is insufficient (402)
