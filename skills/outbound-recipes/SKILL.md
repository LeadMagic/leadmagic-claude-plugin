---
name: outbound-recipes
description: Composable, credit-aware LeadMagic MCP recipes for outbound — ICP list builds, account briefs, contact waterfalls, bulk hygiene, hiring-intent sweeps, job-change tracking, competitor ads, lookalike expansion, TAM mapping, and local-business lists. Use when designing or running a multi-step prospecting or GTM data workflow.
---

# Outbound recipes

Each recipe below is a short chain of hosted MCP tools. Pick the one that matches the goal, and state its projected cost before spending.

## Operating rules (every recipe)

1. **Preflight for free.** Call `check_credit_balance` first. Call `preview_cost` before any composite or paid run, and state the projected spend.
2. **Plan-aware search.**
   - On qualifying plans, browse search (`search_people`, `search_companies`, `search_jobs`) is credit-free, within the plan's rate limit and a fair-use cap of about 10M records a month (13,333 searches a day at 25-row pages, or the contract's limit if lower).
   - Elsewhere, browse search is metered.
   - Lookalikes, exports, and contact unlocks are always metered.
   - Details are on [leadmagic.io/pricing](https://leadmagic.io/pricing). Never promise that search has no limit.
3. **Composites over chains.** `account_intel`, `enrich_contact`, and `find_decision_makers` replace long chains of single tools.
4. **More than 5 rows goes to a sheet or a bulk job.** Never loop single-record tools per row. See the `sheets` and `bulk-enrichment` skills.
5. **Confirmation tokens.** Paid batch tools answer first with `needs_confirmation` and a `confirmation_token`. Show the summary, and resend with the token only after the user agrees.
6. **Cheapest first, stop at the first hit.** Misses are usually free; retry only rows whose inputs changed.
7. **Close the loop.** After a run, compare the actual spend from `get_account_analytics` (free) with the estimate.
8. **Report only tool results.** Never invent emails, phones, funding, ads, or job data.

## Recipes

| # | Recipe | Tools, in order |
| --- | --- | --- |
| 1 | ICP list build | small probe `search_people` / `search_companies` → refine filters → cursor-page the segment (`market-search` skill) |
| 2 | Account brief | `preview_cost` → `account_intel` (switch off unneeded sections) |
| 3 | Contact waterfall (one person) | `validate_work_email` → `find_work_email` → `b2b_profile_to_work_email` → `find_personal_email`, stopping at the first hit; `find_mobile_number` only if the user asks for a phone |
| 4 | Bulk list enrichment | `preview_cost` → `submit_detected_bulk_job` (token) → `watch_bulk_job_progress` → `get_bulk_job_rows` / `export_bulk_job` |
| 5 | List hygiene before a send | bulk `email_validation` via `submit_detected_bulk_job`, or an `email_validation` sheet column; segment into valid / risky / invalid |
| 6 | Hiring-intent sweep | one `search_jobs` call with `company_domains` (up to 25) + `titles` + `posted_within`, then `get_company_hiring_signals` for the shortlist |
| 7 | Decision-maker mapping | `find_decision_makers` with 1–5 `titles`; set `include_email_discovery` only when emails are wanted |
| 8 | Job-change champion loop | ≤5 contacts: `detect_job_change`; more: bulk `job_change` or a `job_change_detector` sheet column → `find_work_email` at the new domain for confirmed movers |
| 9 | Competitor ads monitor | `search_google_ads` / `search_meta_ads` / `search_b2b_ads` with `limit` → `get_b2b_ad_details` for creatives worth dissecting |
| 10 | Lookalike expansion | `find_lookalike_companies` per seed → dedupe → optional `search_companies` fit filter → recipe 6 to rank |
| 11 | TAM map | filter permutations (industry × size × country) with small probe pages → segment matrix → full pages only for the segments the user picks |
| 12 | Local-business list | `find_local_leads` (200 credits per keyword × location, charged up front, after the token) → bulk-job results |
| 13 | Sheet pipeline | `get_sheet` → `add_sheet_columns` → one `run_sheet_column` (`sample_size` 3 first on big fills) → `read_sheet_rows` → `export_sheet_recipe` |

## Output
- The recipe used and the tools called
- Credits: projected vs actual
- The result set (or a file / sheet / job reference)
- The next recipe in the chain, if any
