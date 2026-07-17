---
name: bulk-enrichment
description: Credit-safe CSV/list enrichment with LeadMagic MCP — balance, preview, submit, poll. Use for uploaded files or multi-row enrichment jobs.
---

# Bulk enrichment

## Trigger
Use when the user has a CSV/JSON/JSONL file, many rows, or asks to queue bulk enrichment.

## Workflow
1. Free `check_credit_balance` then `preview_cost` when product/volume is known.
2. Confirm with the user before write tools (hook will also ask).
3. Prefer `process_attached_csv` / `create_bulk_upload_session` for the upload widget, or `submit_detected_bulk_job` when mapping is ready.
4. After submit: `get_bulk_job_status` once, then wait **≥45 seconds** between polls.
5. On completion: `get_bulk_job_rows` / `get_bulk_job_errors` as needed.
6. Never loop single-contact tools across a whole file.

## Output
- Job id / status
- Credits context
- Row success/error summary
- Next action (retry failures, export)
