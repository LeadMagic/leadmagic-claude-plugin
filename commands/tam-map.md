---
description: Size and segment a market with LeadMagic company search before pulling full lists
argument-hint: [market, e.g. "US fintechs, 11-500 employees"]
---

Map the TAM for: $ARGUMENTS

1. **Build the segment matrix.** Translate the market into `company_filters` permutations: `industries` × employee bands (`min_employees` / `max_employees`) × `country_codes`.
2. **Probe each segment.** Run `search_companies` with a small `limit` (5) per segment.
   - Report any total the response returns. If it only matches the rows returned, mark the segment "at least N".
   - Probes are credit-free only on qualifying plans; elsewhere they cost per result. Call `preview_cost` first and state it.
3. **Recommend.** Present the matrix and recommend which segments to work.
4. **Pull only the segments the user picks**, by cursor paging (`market-search` skill). Each snapshot returns at most 1,000 rows, so keep segments narrow.

No contact unlocks in this command. Hand the chosen accounts to `/leadmagic:find-buyers` or `/leadmagic:build-list`.
