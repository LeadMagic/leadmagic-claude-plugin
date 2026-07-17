---
name: get-started
description: Onboard with LeadMagic MCP — check credits, run one company or one contact outcome, and confirm cost before spend. Use when a user is new to LeadMagic in Claude Code.
---

# Get started with LeadMagic

## Trigger
Use when the user is connecting LeadMagic for the first time, asks how to begin, or wants a safe first enrichment.

## Workflow
1. Call free `check_credit_balance` and summarize remaining credits.
2. Pick **one** outcome the user cares about:
   - Company → prefer `account_intel` (fallback `research_account`) with `company_domain` when possible.
   - Contact → `validate_work_email` if they have an email; otherwise `find_work_email` or `enrich_contact`.
3. Before any multi-row or bulk work, call free `preview_cost` and confirm.
4. Never invent emails, funding, or firmographics — only report tool results.

## Output
- Credits remaining
- One concrete result (account brief or contact outcome)
- Exact tools used
- Suggested next step (decision-makers, hiring, ads, or bulk CSV)
