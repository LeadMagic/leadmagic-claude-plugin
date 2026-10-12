---
description: Build and run enrichment and AI columns in a LeadMagic sheet (credit-safe)
argument-hint: "[sheet name, or 'new'] [goal, e.g. 'find work emails']"
---

Work in a LeadMagic sheet: $ARGUMENTS

Follow the `sheets` skill:
1. **Open the sheet.** Find it with `list_sheets`, or `create_sheet` for "new". Read it with `get_sheet` for the column keys.
   - If the sheet tools are missing, tell the user Sheets must be enabled for the workspace they signed into, and stop.
2. **Size the work for free.** Call `check_credit_balance` and `get_sheet_stats` (how many rows still need the column).
3. **Add every column in one call.** Map the goal to columns and add them all with `add_sheet_columns`. This is free and fills nothing.
4. **Run once.** Make one `run_sheet_column` call for all the new columns (`also_column_keys`, `row_state: "notRun"`, `wait_seconds: 45`).
   - On a large fill, sample first with `sample_size: 3` and show the user the values.
   - A run quoted at 5 credits or less starts without a question.
   - On `needs_confirmation`, show the quote and resend with the `confirmation_token` only after the user says yes. Handle any `next_step` the same way.
5. **Read back and report.** Use `read_sheet_rows` (the filter root must be a group). Report rows filled, no result, and failed (`list_sheet_run_rows`), plus credits spent.
6. **Offer follow-ups:** a re-run on `row_state: "failed"` only, and `export_sheet_recipe` to save the build.
