---
description: Expand a target-account list from seed customers with LeadMagic lookalike search
argument-hint: "[seed company domains]"
---

Find lookalike companies for: $ARGUMENTS

1. **State the cost first.** Lookalike search is metered on every plan. Call `preview_cost` for `find_lookalike_companies`, state the estimate, and confirm.
2. **Search per seed.** Call `find_lookalike_companies` once per seed domain (`company_domain`, `limit` up to 100; page with `offset`). Merge the results and dedupe on domain.
3. **Optional fit filter.** Use `search_companies` with `company_filters` to enforce size, country, or industry.
4. **Deliver.** Output a companies table or CSV noting which seed each match came from. Suggest `/leadmagic:hiring-signals` to rank the set before spending on people.
