---
name: decision-makers
description: Find executives and buyers at a company via LeadMagic MCP, with work emails when requested. Use when the user asks for VP, Director, or C-level contacts, buyers, or people by role at a named company.
---

# Decision-makers

## Trigger
Use when the user asks for VP/Director/C-level contacts, buyers, or people by role at a company.

## Workflow
1. Resolve company domain when possible.
2. Prefer composite `find_decision_makers` (1–5 `titles`) when the ask is broad. Call free `preview_cost` with the same titles first. Email discovery is opt-in: set `include_email_discovery: true` only when the user wants emails.
3. For a specific title → `find_people_by_role` or `search_people`.
4. Emails returned by LeadMagic tools are already validated — never re-validate them. Use `validate_work_email` only for emails the user brought from elsewhere (CRM, lists, sign-ups).
5. Check credits with free helpers before large people searches. For many accounts, use a sheet (`role_finder` column) or bulk job rather than one call per company.

## Output
- Ranked people with title + company
- Work emails when tools returned them
- Gaps (not found) and next enrichment step
