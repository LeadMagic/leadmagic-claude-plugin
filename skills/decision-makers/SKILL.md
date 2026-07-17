---
name: decision-makers
description: Find executives and buyers at a company and attach work emails when possible via LeadMagic MCP.
---

# Decision-makers

## Trigger
Use when the user asks for VP/Director/C-level contacts, buyers, or people by role at a company.

## Workflow
1. Resolve company domain when possible.
2. Prefer `find_decision_makers` (composite with emails) when the ask is broad.
3. For a specific title → `find_people_by_role` or `search_people`.
4. Validate or enrich emails only when the user needs higher confidence (`validate_work_email` / `enrich_contact`).
5. Check credits with free helpers before large people searches.

## Output
- Ranked people with title + company
- Work emails when tools returned them
- Gaps (not found) and next enrichment step
