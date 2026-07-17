---
name: account-research
description: Research a company with LeadMagic MCP and summarize GTM signals. Use for account briefs, ICP fit, and sales-call prep.
---

# Account research

## Trigger
Use when the user wants company research, ICP qualification, or a target account brief.

## Workflow
1. Resolve the company with the cleanest identifier (`company_domain` preferred, else name).
2. Prefer composite `account_intel` for a full briefing; otherwise `research_account`.
3. Expand only when asked:
   - Competitors → `list_company_competitors`
   - Tech stack → `get_company_technographics`
   - Open roles → `find_jobs` / hiring signals → `get_company_hiring_signals`
4. For CSV company lists, do **not** loop single-account tools — use the bulk enrichment path.
5. Free helpers first when budget-sensitive: `check_credit_balance`, `preview_cost`.

## Output
Short GTM brief:
- What the company is
- Firmographics / funding / signals available from tools
- Competitors or tech if requested
- Unknowns and recommended next LeadMagic lookup
