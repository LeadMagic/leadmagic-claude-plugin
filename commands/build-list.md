---
description: Build an ICP prospect list with LeadMagic people or company search
argument-hint: [ICP, e.g. "VP Sales at 51-200 employee US software companies"]
---

Build a prospect list for: $ARGUMENTS

Follow the `market-search` skill:
1. **Translate the ICP into filters.** Use `search_people` with `company_filters` (`industries`, `min_employees` / `max_employees`, `country_codes`) plus `titles`. For account lists, use `search_companies`.
2. **Probe and state the cost.** Run one small page (`limit` 5–10) to check the filters. Call `preview_cost` and state the expected cost for the full pull. Browse search is credit-free only on qualifying plans and within the fair-use cap ([pricing](https://leadmagic.io/pricing)).
3. **Page the list.** On the user's go-ahead, page with `cursor` and the same arguments. Stop at `has_more: false`, dedupe on stable IDs, and write a CSV.
   - Each snapshot returns at most 1,000 rows. Split bigger ICPs into segments.
4. **Search never returns emails or phones.** Offer the next step: work emails through `submit_detected_bulk_job` or a sheet (`/leadmagic:enrich-sheet`). Never loop single lookups.
