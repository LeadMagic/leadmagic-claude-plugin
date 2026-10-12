---
description: Find contacts who changed jobs — champion tracking with LeadMagic job-change detection
argument-hint: "[contacts: profile URLs or work emails, or a CSV path]"
---

Run a job-change sweep over: $ARGUMENTS

1. **Preflight.** Call `check_credit_balance` and `preview_cost` (job-change checks are paid per contact). State the total and confirm.
2. **Pick the path by size:**
   - **5 contacts or fewer:** call `detect_job_change` per contact, with `profile_url` (the full URL; the path ends in `in/{slug}`) or `work_email`, plus `company_domain` / `company_name` for the expected employer.
   - **More than 5:** use `submit_detected_bulk_job` with `enrichment: "job_change"` (confirm with the token), or a `job_change_detector` column in a sheet. Never loop the single tool.
3. **Read the results.** Treat only a clear "yes" as a mover. Inconclusive results mean "recheck next sweep", not a move.
4. **Movers only:** find the new work email with `find_work_email` at the new domain (bulk or sheet for more than 5 people).
5. **Output.** A movers table: old company → new company, new title, fresh email. Report credits spent, and suggest re-running the sweep periodically.
