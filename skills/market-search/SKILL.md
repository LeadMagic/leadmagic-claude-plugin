---
name: market-search
description: Broad people, company, and jobs market search via LeadMagic MCP with plan-aware cost, fair-use limits, and cursor pagination. Use when building audiences, TAMs, account lists, or job-posting sweeps rather than single lookups.
---

# Market search (people · companies · jobs)

## Trigger
Use when the user wants a whole segment — an audience, a TAM, an account list, or a job-posting sweep — not a single contact or company lookup.

## What costs credits

**Browse search** means the three canonical searches: `search_people`, `search_companies`, and `search_jobs`.

- **On qualifying plans, browse search is credit-free**, within two limits:
  - **Rate limit**, set by the plan.
  - **Fair-use cap**: about 10M records a month — **13,333 searches a day** at 25-row pages, or your contract's limit if lower. People, company, and jobs searches share one cap per workspace.
- **On other plans**, browse search is metered by results returned.
- **Always metered, on every plan**: lookalikes (`find_lookalike_companies`), full search, exports, and contact unlocks (emails, phones).

Which plans qualify, and their rate limits, are on [leadmagic.io/pricing](https://leadmagic.io/pricing). Never promise that search has no limit. If you don't know the user's plan, call the free `check_credit_balance` and `preview_cost` before a large pull, and state the expected cost.

Even when search itself is free:
- Size the audience first.
- Unlock contact details last, and only on the final list.

## Workflow

1. **Shape filters with a small probe page** (`limit` 5–10) and adjust them before paging. Tool filters:
   - `search_people`: `company_domain`, or `company_filters` (`industries`, `min_employees` / `max_employees`, `country_codes`, `company_domains`), plus `titles` / `roles` and `people_filters`.
   - `search_companies`: `company_filters` or `query`.
   - `search_jobs`: `titles`, `company_domains` (up to 25), `countries`, `seniority`, `posted_within`, `tags`, `has_remote`.
2. **Run the broad search and page it with cursors** (see below).
3. **Respect the snapshot cap.** One browse snapshot returns at most 1,000 rows. For a bigger market, split it into filter segments (industry × size band × country) and page each one separately. Do not try to page past the cap.
4. **Only then enrich.** Get emails per the `decision-makers` / `contact-lookup` skills, or through the `bulk-enrichment` / `sheets` skills for more than 5 people.
   - Finder emails come back already validated.
   - Validate only emails the user brought from elsewhere.

## Page size

| Lane | Rows per page |
| --- | --- |
| Credit-free browse lane | Capped at **25**, whatever `limit` you send |
| Metered: `search_people` | `limit` up to 100; cursor pages up to 50 |
| Metered: `search_companies`, `search_jobs` | `limit` up to 50 |

Send the page size you want. Expect 25-row pages on the credit-free lane.

## Cursor pagination (all three searches)

- **First page:** filters plus `limit`. Omit `cursor`.
- **Each response** carries `next_cursor` (opaque) and `has_more`.
- **Next page:** the **same arguments** plus `cursor: <next_cursor>`, copied verbatim.
  - Only `limit` may change between pages.
  - Changing any other argument invalidates the cursor.
  - When the response spells out the exact next-page arguments, send exactly those.
- **Never combine `cursor` with a nonzero `offset`.** To switch from offset paging to cursors, restart at offset 0.
- **Stop** when `has_more` is false or `next_cursor` is null.
- **Dedupe** on stable IDs.

## Output

- The paged result set (or the file it was written to), the row count, and the pages fetched
- The filters used, and any part of the segment the filters could not express
- The next enrichment step and its credit cost (from `preview_cost`)
