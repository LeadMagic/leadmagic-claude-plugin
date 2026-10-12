---
name: hiring-intent
description: Surface open roles and hiring velocity for prioritization using LeadMagic MCP jobs and hiring-signal tools.
---

# Hiring intent

## Trigger
Use when the user asks who is hiring, what roles are open, or whether a company is ramping headcount.

## Workflow
1. Company-scoped open roles → `find_jobs`.
2. Broader Jobs Data search → `search_jobs`, using its own filters (`titles`, `company_domains` up to 25, `countries`, `seniority`, `posted_within`, `tags`, `has_remote`). One call with `company_domains` covers several accounts — do not loop one call per domain.
3. Aggregated velocity → `get_company_hiring_signals` (not a job list).
4. Prefer domain identifiers; keep results factual from tools only.

## Output
- Matching roles / locations / links when available
- Hiring-signal summary when requested
- Suggested GTM angle (e.g. teams growing in sales/eng)
