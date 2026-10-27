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
6. Every paid sheet run requires a quote and explicit approval, including small samples and AI runs using the user's saved provider key. Only runs the server verifies are free can start immediately. Bulk jobs, paid sheet runs, imports, outbound pushes and deletes answer first with `needs_confirmation`, a summary and a `confirmation_token` — nothing has run. Show the scope and maximum credits; only after the user approves that quote, repeat the identical arguments with the token (the plugin hook prompts on that call in default permission modes). A token or an approval for different rows or columns is not consent; changed or expired quotes need fresh approval. Single-record paid tools do not use that gate — before any call you expect to exceed ~25 credits (`search_people` with limit > 25 on a metered plan, `find_company_employees`, `account_intel` with jobs), call `preview_cost` and ask.
7. Browse search (`search_people`, `search_companies`, `search_jobs`) is credit-free only on qualifying plans and within a fair-use cap; see the `market-search` skill and [pricing](https://leadmagic.io/pricing).

## Output
- Credits remaining / estimated cost when known
- Recommended cheapest path
- Clear stop if balance is insufficient (402)
