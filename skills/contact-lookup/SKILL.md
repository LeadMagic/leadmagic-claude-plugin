---
name: contact-lookup
description: Find or validate a work email for a B2B contact using LeadMagic MCP. Use when the user has a person plus company or an existing email.
---

# Contact lookup

## Trigger
Use when the user needs a validated work email or wants LeadMagic to find the likely work email for a specific person.

## Workflow
1. Start from the strongest identifier:
   - Existing work email → `validate_work_email`
   - Full name + company/domain → `find_work_email` or composite `enrich_contact`
   - Needs full dossier → `enrich_contact`
   - Job-change signal → `detect_job_change`
2. Prefer the cheapest path that answers the question. Do not re-find an email that already validates.
3. Prefer composites over chaining many primitives.
4. For lists/CSVs → bulk enrichment skill (do not loop per row).
5. Only report fields returned by tools — never invent contacts.

## Output
- Best contact field found
- Validation / status when available
- Inputs used
- Concise next action
