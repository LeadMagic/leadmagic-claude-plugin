---
name: sheets
description: Build, fill, and read LeadMagic Sheets (Sheet Enrichment) over the hosted MCP — add enrichment, AI, formula and JSON columns, run them with credit confirmation, read results, undo, and save recipes. Use when the user mentions a LeadMagic sheet, Sheet Enrichment, enriching rows or columns in a grid, an AI column, or a sheet recipe or template.
---

# LeadMagic Sheets

A LeadMagic sheet is a live grid in the app (**Sheet Enrichment** in the sidebar). The MCP tools drive the **same** sheet the user has open: every write shows up in their browser.

Each column is one of two things:
- **typed data**, or
- **something that fills itself per row**: a LeadMagic enrichment product, an AI prompt, a formula, or a field pulled out of another column's response.

Sheet tools appear only when the signed-in workspace has Sheets. If they are missing:
1. Check the user is on a plan with Sheets ([billing](https://app.leadmagic.io/settings/billing)).
2. Check they picked the workspace that owns the sheet during OAuth.
3. Reconnect.

A 403 "Sheets are not enabled" response means the same thing. Never invent data instead.

## Operating loop

Always in this order. Use column **keys** (`col_…`) from `get_sheet`, never display names.

1. **Find the sheet.** Use `list_sheets` (the user names a sheet) or `create_sheet` (a new one; free, and it returns the column keys).
2. **Read the card first.** Call `get_sheet` before any write. It returns the columns, their keys, what fills each one, and how to write this sheet.
3. **Size the work.** `get_sheet_stats` answers "how many rows are missing an email" without paging. Use `read_sheet_rows` only when you need actual values.
4. **Add rows if needed.**
   - `add_sheet_rows`: up to 100 rows per call, values keyed by column key. It runs nothing and spends nothing.
   - `set_sheet_cells`: corrections, batched up to 500 edits per call. Never make one call per cell.
   - For thousands of rows, ask the user to drop the file into Sheet Enrichment instead of streaming rows through chat.
5. **Build all the columns in one call.** `add_sheet_columns` adds and configures several columns at once, left to right. Configuring is free and fills nothing.
6. **Run once.** Make **one** `run_sheet_column` call for the whole pipeline:
   - `column_key` plus `also_column_keys` (up to 10 columns in total)
   - `row_state: "notRun"`
   - `wait_seconds: 45`
   - Columns that read another requested column start after it finishes.

   On a big fill, first add `sample_size: 3` and follow the approval step below before running the sample. Show the user the sampled values (`read_sheet_rows` on those rows), then request a new quote and approval for the full run without `sample_size`.
7. **Confirm when the server asks.**
   - Every paid run, including a small sample or an AI run using the user's saved provider key, first returns `needs_confirmation`, a summary, and a `confirmation_token`. Nothing has run yet. Only runs the server verifies are free can start immediately.
   - Show the exact sheet, columns, row scope, and maximum credits from the quote. Only after the user explicitly approves that quote, send the **identical** arguments plus the token.
   - A token, available credits, or approval for another scope is not consent. Never invent a token or reuse one for a changed scope. If the scope changes or the quote expires, obtain a new quote and approval.
8. **Follow `next_step`.** When a run returns `next_step` plus `next_arguments`, that is the next paid stage of the pipeline. Show its summary, and on approval send `next_arguments` with its token. Don't make separate quote or status calls in between.
9. **Read results back.** Use `read_sheet_rows` with `columns` (to save tokens) and `filter`.
   - The filter's **root must be a group**: `{"type":"group","join":"and","children":[{"type":"cond","columnKey":"col_…","op":"empty"}]}`
   - Wrap a single condition in a group too.
10. **Explain gaps.** `list_sheet_run_rows` shows how each row ended: `completed`, `failed`, `insufficient_credits`, or no result.
    - Re-run only the failures, with `row_state: "failed"`.
    - Re-run filled cells only with `force: true` and the user's explicit consent.
11. **Save the build.** `export_sheet_recipe` turns a working sheet into a template. `import_sheet_recipe` builds a new sheet from one; it may answer with `needs_confirmation` first.

## Column kinds

| Kind | Fills from | Cost | Set with |
| --- | --- | --- | --- |
| `manual` | typed by the user or `set_sheet_cells` | free | `add_sheet_column(s)` |
| `enrichment` | a LeadMagic product + `input_mapping` {product input → column key} | the product's per-row credits; misses are usually free | `add_sheet_columns` / `configure_sheet_column` |
| `ai` | a per-row `prompt` naming columns as `{Column Name}` | LeadMagic AI by default, charged in credits by usage; or the user's own provider key saved in the app | `add_sheet_columns` / `configure_sheet_column` |
| `formula` | an expression, e.g. `{First Name} & " " & {Last Name}` | free | `configure_sheet_column` |
| `json` | one field of another column's response (`source_column_key` + `path`) | free | `extract_sheet_json_field` |

### Enrichment products and inputs

| Product | Inputs (map every one the sheet has a column for) |
| --- | --- |
| `email_finder` | `first_name`, `last_name`, `domain`, `company_name`, `profile_url` |
| `email_validation` | `email` |
| `personal_email_finder` | `profile_url` |
| `profile_search` | `profile_url` |
| `mobile_finder` | `profile_url` |
| `role_finder` | `domain`, `company_name`, `job_title` |
| `job_change_detector` | `profile_url`, `domain`, `company_name` |
| `email_to_b2b_profile` | `email` |
| `b2b_profile_to_email` | `profile_url` |
| `company_search` | `domain`, `company_name` |
| `company_funding` | `domain`, `company_name` |
| `technographics` | `domain` |

Notes on enrichment columns:
- `email_finder` with first name + last name + domain finds far more than a profile URL alone.
- If the sheet only has a full name, split it with a formula, or with a `json` column on `role_finder`'s `first_name` / `last_name`.
- `profile_url` columns hold full profile URLs (the path ends in `in/{slug}`).
- Sheets has **no job-postings product**. Use the `hiring-intent` skill for that.
- After an enrichment column runs, `list_sheet_column_fields` shows its response fields. Then `extract_sheet_json_field` adds columns such as `company.industry` for free.

### AI columns

- **Output types** (`output_type`): `text`, `category` (with 2 or more `categories`), `number`, `boolean`, or `json`.
- **Drafting:** `draft_sheet_ai_prompt` turns a plain-language goal into a prompt and output shape for this sheet. It writes nothing.
- **Research agents:** `web_search: true` and `leadmagic_tools` turn the column into a per-row research agent. Bound it with `max_steps`, `max_credits_per_row`, and `max_wall_seconds`.
- **Auto-run:** `set_sheet_column_auto_run` (workspace admins only) makes an AI column run on `rowAdded` or `inputsChanged`. Turning it on needs a confirmation.
  - Enrichment columns never run by themselves.
  - Fill them with `run_sheet_column` after `add_sheet_rows`.

### Custom HTTP columns

Custom HTTP (API request) columns are not available through this plugin. Users set them up in the LeadMagic app at [app.leadmagic.io](https://app.leadmagic.io). Don't try to build one over MCP.

## Run controls

**Choosing rows:**
- `scope`: `column` (the default: the whole column), `selection` (with `row_ids`), or `sheet`.
- Narrow further with `filter`, `q`, `row_state` (`notRun`, `failed`, `insufficientCredits`, `noResult`), or `start_row` / `end_row`.

**Row-id selection cap: 10,000 per call.** This applies to `row_ids` in `run_sheet_column`, `delete_sheet_rows`, and `restore_sheet_rows`.
- On a bigger sheet, don't build a giant selection. Run with `scope: "column"` plus `row_state` or `filter`.
- In the app, select-all only ticks loaded rows. Clear the selection and run the column instead.

**Spend and retries:**
- `confirm_max_credits` is the user's ceiling. The run is refused if the quote is higher.
- Reuse the same `idempotency_key` when retrying the same submission.
- After an ambiguous or failed paid call, inspect existing runs, saved results, and credits before retrying. Do not automatically replay work whose outcome is unknown.

**Waiting:** pass `wait_seconds: 45` once (to `run_sheet_column`, `get_sheet_run`, or `list_sheet_runs` with `active: true`) instead of polling.

**Stopping:**
- `pause_sheet_run` keeps finished cells and stops charging. To continue later, run the column again with `row_state: "notRun"`.
- `cancel_sheet_run` stops for good. Unstarted rows are not charged.

## Imports, workspace runs, and saved lists

These tools take only their own named parameters. Pass ids from the list tool shown.

| Task | Tools and parameters |
| --- | --- |
| Connected apps | `list_cloud_connections` (no parameters) |
| CRM import | `list_cloud_crm_objects` (`crm_platform`) → `list_cloud_crm_fields` / `list_cloud_crm_filters` (`crm_platform`, `object`) → `import_cloud_crm` (`crm_platform`, `object`, `fields` as `[{field, label?}]`, `idempotency_key`; optional `list_view_id`, `lifecycle_stage`, `name`, `max_rows`) |
| Outbound import | `list_cloud_campaigns` (`platform`, optional `search`, `limit`) → `import_cloud_sequencer` (`platform`, `campaigns`, `fields`, `idempotency_key`; optional `name`, `max_rows`) |
| Import status | `list_cloud_imports` (`sheet_id`) → `cancel_cloud_import` (`sheet_id`, `import_id`) |
| Runs and deliveries | `list_cloud_runs` (`sheet_id`, optional `status`, `column_key`, `active_only`) → `pause_cloud_run` / `cancel_cloud_run` (`sheet_id`, `run_id`); `list_cloud_pushes` (`sheet_id`) |
| Saved prospect lists | `list_prospect_lists` (`list_type`: `people` or `company`) → `get_prospect_list` / `export_prospect_list` (`list_type`, `list_id`); `create_prospect_list` (`list_type`, `name`, optional `description`, `rows`); `add_prospect_list_members` (`list_type`, `list_id`, `rows`); `update_prospect_list` (`list_type`, `list_id`, `name` and/or `description`); `remove_prospect_list_members` (`list_type`, `list_id`, `member_ids`) |
| Saved searches | `list_saved_searches` (`search_type`: `people` or `company`) → `get_saved_search` / `rerun_saved_search` (`search_type`, `search_id`) |

- Generate one `idempotency_key` (a UUID) per import and resend it unchanged on a retry.
- Imports ask for confirmation first. Connect a CRM or outbound platform in the app (Integrations), not over MCP.

## Undo

Deletes are soft and restorable:
- `delete_sheet_rows` → `restore_sheet_rows`
- `delete_sheet_column` → `restore_sheet_column`

Both deletes ask for confirmation first.

## Spend rules

1. **Free first:** `check_credit_balance` and `get_sheet_stats` before paid runs. Sample before a full run.
2. **Composites over chains:** put every column in one `run_sheet_column` call; don't make one call per column.
3. **More than 5 rows means a sheet run or bulk job.** Never loop single-record tools (`find_work_email`, `enrich_contact`, …) row by row.
4. **Ask only when the server asks.** Use the `needs_confirmation` + `confirmation_token` flow above.
5. **402 / `insufficient_credits`:** send the user to [billing](https://app.leadmagic.io/settings/billing) or [auto top-up](https://app.leadmagic.io/settings/auto-top-up). Then re-run with `row_state: "insufficientCredits"`. On a 401, reconnect OAuth.

Report only values the sheet returned. Empty or no-result cells stay empty: never fill them from memory. Never put API keys, AI keys, or personal data into prompts, recipes, or chat.

## Sheets vs bulk jobs

| Use | When the user wants to |
| --- | --- |
| **Sheets** | see and iterate on the list, chain several columns (find → validate → classify), or reuse the build |
| **`bulk-enrichment`** | run a one-shot file in / file out with no grid |

Both bill the same per-product credits.
