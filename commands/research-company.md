---
description: Research a company with LeadMagic account intel
argument-hint: "[company domain, e.g. acme.com]"
---

Research this company with LeadMagic MCP: $ARGUMENTS (prefer the domain).

1. Call the free `preview_cost` for `account_intel` with the same inputs and state the estimate.
2. Call `account_intel` with `company_domain` (add `company_name` when known; technographics needs it). Turn off sections the user does not need (`include_jobs`, `include_technographics`) to save credits.
3. Return a short GTM brief: what the company does, firmographics, funding and hiring signals if present, and one next step (for example `/leadmagic:find-buyers`).

Report only fields the tool returned.
