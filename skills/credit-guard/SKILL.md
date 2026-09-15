---
name: credit-guard
description: Always-on spend discipline for LeadMagic MCP — free helpers first, composites over chains, no duplicate lookups.
---

# Credit guard

## Trigger
Use whenever enrichment may spend credits, before bulk jobs, or when the user asks about cost/usage.

## Rules
1. Free first: `check_credit_balance`, `preview_cost`, `get_account_analytics`, `get_job_search_catalogs`, `resolve_job_search_filters`.
2. Prefer composites (`account_intel`, `enrich_contact`, `find_decision_makers`) over long primitive chains.
3. Do not repeat the same lookup for identical inputs in one session.
4. Empty/not-found results are usually free — say so when reporting.
5. Bulk jobs, paid runs, imports, outbound pushes and deletes prompt the user through the plugin hook. Single-record paid tools do not — before any call you expect to exceed ~25 credits (`search_people` with limit > 25, `find_company_employees`, `account_intel` with jobs), call `preview_cost` and ask.

## Output
- Credits remaining / estimated cost when known
- Recommended cheapest path
- Clear stop if balance is insufficient (402)
