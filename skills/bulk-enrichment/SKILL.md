---
name: bulk-enrichment
description: Credit-safe CSV and list enrichment with LeadMagic bulk jobs — balance, preview, confirm, submit, watch, export, and recover failed rows. Use when the user has a CSV/JSON/JSONL file, more than 5 rows to enrich, or wants a local-business list built.
---

# Bulk enrichment

## Trigger
Use this skill when the user:
- has a CSV/JSON/JSONL file,
- has more than 5 rows to enrich,
- asks to queue bulk enrichment, or
- wants a list of local businesses.

If they want to see and iterate on the results in a grid, use the `sheets` skill instead.

## Spend rules
1. **Free first.** Call `check_credit_balance`, then `preview_cost` once the product and row count are known. State the projected spend.
2. **Use bulk, never per-row loops.** Never loop single-contact tools (`find_work_email`, `enrich_contact`, …) across a file.
3. **Confirm with the token.** Bulk submits, restarts, and resumes answer first with `needs_confirmation`, a summary, and a `confirmation_token`. Nothing has run yet. Show the summary, and repeat the identical call with the token only after the user agrees. Never invent a token.
4. **Report actuals.** Don't re-run unchanged rows. Misses are usually free.

## Submit
- **A file attached in Claude** → `process_attached_csv` only. The widget uploads and submits on its own, so do not call `resolve_bulk_upload_mapping` or `submit_*` after it.
- **Inline CSV, rows, or an HTTPS `file_url`** → `submit_detected_bulk_job`.
  - Common enrichments: `work_email_finder`, `email_validation`, `mobile_finder` (only when the user asks for phones), `job_change`, `company_firmographics`.
  - For profile URL → work email, pick the profile-to-email option from the tool's `enrichment` list.
  - For larger files, prefer `file_url` with `format: "auto"` over pasting CSV text into the call.

## Local businesses (`find_local_leads`)
`find_local_leads` builds a list of local businesses for business types across cities or US ZIP codes. Example: `keywords: ["dentist"]`, `locations: ["Austin, TX", "78704"]`.

**Cost:**
- Each keyword × location pair is one search at **200 credits, charged up front**.
- A run can have at most 100 searches.

**Steps:**
1. The first call charges nothing. It resolves the locations and returns the search grid, the cost, and a `confirmation_token`. Show the user the grid and the cost.
2. Call again with the same arguments plus the token, only after the user approves.
3. Results arrive as a bulk job. Watch and read it the same way as any other bulk job (below).

## Watch progress
After submitting:
1. Call `get_bulk_job_status` once.
2. Then use `watch_bulk_job_progress` (`timeout_seconds` up to 30) instead of blind polling. It returns the latest status and whether the watch timed out; repeat it to keep watching.
3. If you poll `get_bulk_job_status` directly instead, wait at least 45 seconds between calls.

For history and diagnostics, use `list_bulk_jobs`, `get_bulk_job_events`, and `get_bulk_job_logs`.

## Results
- **Read rows** with `get_bulk_job_rows`: up to 500 rows per page, paged with `offset` / `cursor`. Add `status: "failed"` to see only failures.
- **Error reasons** come from `get_bulk_job_errors`.
- **Export** with `export_bulk_job`, which returns CSV up to **4 MB**. For bigger jobs, page `get_bulk_job_rows`.

## Control
- `pause_bulk_job` stops processing. It needs no approval.
- `resume_bulk_job` processes the remaining rows and charges them, so it needs confirmation. If a job paused because credits ran out, top up ([billing](https://app.leadmagic.io/settings/billing)), then resume.
- `restart_bulk_job` re-queues rows and charges them again, so it needs confirmation.
  - It defaults to `mode: "failed_only"`; completed results are kept.
  - Restart only after the failed rows' inputs have been fixed.

## Output
- Job id, status, and rows processed / failed
- Credits: estimate vs actual
- A summary of row successes and errors, with the top error reasons
- The next action (fix and restart failures, export, or move the results into a sheet)
