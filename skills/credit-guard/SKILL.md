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
5. Bulk/write tools require explicit user confirmation.

## Output
- Credits remaining / estimated cost when known
- Recommended cheapest path
- Clear stop if balance is insufficient (402)
