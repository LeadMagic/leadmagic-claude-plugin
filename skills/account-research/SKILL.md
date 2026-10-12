---
name: account-research
description: Research one company with LeadMagic MCP and summarize its GTM signals. Use when the user wants an account brief, ICP fit check, firmographics, funding, tech stack, hiring, or sales-call prep for a named company.
---

# Account research

## Trigger
Use when the user wants company research, ICP qualification, or a target-account brief for one company (or a handful). For a list of companies, use the `bulk-enrichment` or `sheets` skill instead.

## Workflow
1. Resolve the company with the cleanest identifier: `company_domain` (e.g. `acme.com`) first, else `company_name`. A company is the employer, never a person or a UI label.
2. Pick the narrowest tool that answers the question:
   - Full brief (firmographics, funding, tech, open jobs in one call) → `account_intel`. Call free `preview_cost` first, and switch off sections the user does not need (`include_jobs`, `include_technographics`, `include_research`).
   - Firmographics only (industry, size, HQ, founded year, description) → `enrich_company`.
   - Funding only (total raised, last round, investors) → `find_company_funding`.
3. Expand only when asked, and only for sections `account_intel` did not already return:
   - Tech stack → `get_company_technographics`
   - Open roles → `find_jobs`; hiring velocity → `get_company_hiring_signals`
   - Buyers → the `decision-makers` skill
4. More than 5 companies → do **not** loop single-account tools. Use `submit_detected_bulk_job` (`company_firmographics`, `company_funding`, …) or a sheet.
5. Do not repeat a lookup already made for the same inputs in this session.

## Output
Short GTM brief:
- What the company is
- Firmographics, funding, and signals the tools returned
- Tech stack if requested
- Unknowns (empty sections) and the recommended next LeadMagic step

Never fill gaps from memory — report only tool results.
