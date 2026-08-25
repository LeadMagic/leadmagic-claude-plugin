---
name: market-search
description: Broad people, company, and jobs market search via LeadMagic MCP with unlimited-plan awareness and cursor pagination. Use when building full audiences, TAMs, account lists, or job-posting sweeps rather than single lookups.
---

# Market search (people · companies · jobs)

## Trigger
Use when the user wants a whole segment — an audience, a TAM, an account list, or a
job-posting sweep — not a single contact or company lookup.

## Unlimited on the right plan

Professional and Ultimate plans include **credit-free, volume-unlimited** access to the
three canonical search surfaces (People, Company, Jobs Search). The only limit is rate:
5 req/s sustained on Professional, 10 req/s on Ultimate. On these plans:

- Never ration, never narrow to save credits, never warn about credit cost for browse
  searches — go broad and page the whole segment.
- Contact-detail unlocks (raw emails/mobiles) are still credit-metered — size the
  audience first, unlock details last, on the final list only.
- Exports and lookalikes are metered on every plan.

On other plans, browse search costs ~1 credit per returned row — use `preview_cost` /
`check_credit_balance` (free) before large pulls and tell the user the cost.

## Workflow

1. Shape filters free first: `resolve_job_search_filters`, `get_job_search_catalogs`
   (jobs), or a small probe search (people/companies).
2. Run the broad search: `search_people`, `search_companies`, `search_jobs` / `find_jobs`.
3. Page with cursors (below) until the segment is complete.
4. Only then enrich: decision-maker emails and mobiles — per the `decision-makers` /
   `contact-lookup` skills. Finder emails come back pre-validated; validate only
   emails the user brought from elsewhere.

## Cursor pagination (all three surfaces)

- First page: filters + `limit` (≤50 per cursor page). No `cursor`; offset 0 or omitted.
- The response carries `next_cursor` (opaque) and `has_more`.
- Next page: **identical filters** + `cursor: <next_cursor>`. Changing filters
  mid-cursor invalidates it.
- Never combine `cursor` with a nonzero `offset` — the API rejects it, and a
  `next_cursor` is only minted on the offset-0 form. Paging by offset? Restart at
  offset 0 to switch to cursors.
- Stop when `next_cursor` is null / `has_more` is false. Dedupe on stable IDs.

## Output

- The full paged result set (or the file it was written to), row count, and pages fetched
- Which filters were used, and any segment the filters could not express
- Next enrichment step (emails, validation, mobile) with its credit cost
