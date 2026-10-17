#!/usr/bin/env bash
# PreToolUse approval policy for LeadMagic MCP tools (mcp__plugin_leadmagic_leadmagic__*
# from this plugin, mcp__leadmagic__* when the server was added by hand).
#
# Auto-approves reads, free previews, and paid single-record lookups. Every tool
# that changes workspace state prompts: ASK_BEFORE_TOOLS (known preview /
# confirmation_token contract) and any name with a mutating prefix (see the
# prefix case below). Emits no decision at all (Claude Code's normal permission
# flow) when stdin cannot be parsed, the tool is not a LeadMagic tool, or
# LEADMAGIC_ASK_ALL=1 is set.
#
# Contract: tests/test_approval_policy.py verifies this hook. Coordinate policy
# updates between LeadMagic/leadmagic-claude-plugin and LeadMagic/leadmagic-skills.
# The policy is also mirrored by the Claude Code permissions
# snippet on app.leadmagic.io (Settings -> API -> AI tooling). One
# "tool:group" entry per line, double-quoted, sorted. Groups: bulk | run | import |
# push | delete | edit | export.
#
# Bash 3.2 compatible (macOS /bin/bash): no associative arrays, no lowercasing.
set -euo pipefail

ASK_BEFORE_TOOLS=(
  "cancel_sheet_run:edit"
  "create_bulk_upload_session:bulk"
  "delete_sheet_column:delete"
  "delete_sheet_rows:delete"
  "find_local_leads:bulk"
  "import_cloud_crm:import"
  "import_cloud_sequencer:import"
  "import_sheet_recipe:import"
  "process_attached_csv:bulk"
  "publish_cloud_workflow:run"
  "push_cloud_rows:push"
  "remove_prospect_list_members:delete"
  "restart_bulk_job:bulk"
  "resume_bulk_job:run"
  "resume_cloud_run:run"
  "run_cloud_workflow:run"
  "run_sheet_column:run"
  "save_sheet_http_request:push"
  "set_sheet_cells:edit"
  "set_sheet_column_auto_run:run"
  "submit_bulk_job:bulk"
  "submit_detected_bulk_job:bulk"
  "test_sheet_http_request:push"
  "update_sheet_http_request:push"
)

# Always drain stdin first, even when we decide to say nothing.
input="$(cat || true)"

# Escape hatch: fall back to Claude Code's own permission rules for every tool.
if [[ "${LEADMAGIC_ASK_ALL:-}" == "1" ]]; then
  exit 0
fi

# Parse only top-level hook fields. Raw-text matching could treat values inside
# tool_input as permission metadata or decide on malformed JSON. Without jq,
# retain Claude Code's normal permission flow instead of guessing.
if ! command -v jq >/dev/null 2>&1; then
  exit 0
fi
parsed="$(printf '%s' "$input" | jq -ers '
  if length != 1 then error("expected one hook input") else .[0] end |
  if type != "object" or (.tool_name | type) != "string"
     or (has("permission_mode") and (.permission_mode | type) != "string")
     or (has("tool_input") and (.tool_input | type) != "object")
  then error("invalid hook input")
  else [.tool_name, (.permission_mode // "default" | if . == "" then "default" else . end),
        ((.tool_input.confirmation_token? | type) == "string")] | @tsv
  end
' 2>/dev/null)" || exit 0
IFS=$'\t' read -r tool permission_mode has_token <<< "$parsed"

# Only decide for well-formed LeadMagic tool names; anything else gets no output.
# The strict charset also makes $name safe to interpolate into JSON below.
# Plugin tools use mcp__plugin_<plugin>_<server>__<tool>; hand-added tools use
# mcp__<server>__<tool>.
if [[ ! "$tool" =~ ^mcp__(plugin_leadmagic_)?leadmagic__([a-z0-9_]+)$ ]]; then
  exit 0
fi
name="${BASH_REMATCH[2]}"

# A hook ask forces a prompt even in automatic permission modes. Honor the
# session's selected mode, read from the parsed top-level field above.
session_skips_ask() {
  case "$permission_mode" in
    bypassPermissions|auto|dontAsk) return 0 ;;
    *) return 1 ;;
  esac
}

group=""
known_preview="false"
for entry in "${ASK_BEFORE_TOOLS[@]}"; do
  if [[ "${entry%%:*}" == "$name" ]]; then
    group="${entry##*:}"
    known_preview="true"
    break
  fi
done

# Every other state-changing tool asks on each call: these have no known preview
# contract, and new tools with these prefixes stay protected by default. Reads
# (get_, list_, search_, read_, watch_), check_credit_balance, preview_cost,
# draft_sheet_ai_prompt, and single-record lookups match none of these.
if [[ -z "$group" ]]; then
  case "$name" in
    import_*) group="import" ;;
    push_*) group="push" ;;
    publish_*|run_*|resume_*|rerun_*) group="run" ;;
    submit_*|restart_*) group="bulk" ;;
    delete_*|remove_*) group="delete" ;;
    export_*) group="export" ;;
    cancel_*|pause_*|update_*|add_*|restore_*|set_*|create_*|configure_*|reorder_*|extract_*) group="edit" ;;
  esac
fi

emit() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"%s","permissionDecisionReason":"%s"}}\n' "$1" "$2"
}

if [[ -z "$group" ]]; then
  emit allow "LeadMagic ${name}: read, preview, or single-record lookup, auto-approved by the LeadMagic plugin. Set LEADMAGIC_ASK_ALL=1 to prompt for every tool."
  exit 0
fi

# The hosted server runs these tools only when the call carries the
# confirmation_token its first, preview-only call returned. So the preview runs
# unprompted and the person is asked once, on the call that would act. The two
# widget openers, cell edits, and sheet cancellations ask before the first call
# in the default permission modes.
case "$name" in
  create_bulk_upload_session|process_attached_csv|set_sheet_cells|cancel_sheet_run) ;;
  *)
    if [[ "$known_preview" == "true" && "$has_token" != "true" ]]; then
      emit allow "LeadMagic ${name}: initial call allowed by the plugin. If the server returns a confirmation_token, approve the follow-up before sending it."
      exit 0
    fi ;;
esac

case "$group" in
  bulk)
    reason="LeadMagic ${name} queues a paid bulk job that bills every row. Check preview_cost and check_credit_balance, confirm the row count, then approve." ;;
  run)
    reason="LeadMagic ${name} starts a paid run. Confirm the max credits shown by the preview call before approving." ;;
  import)
    reason="LeadMagic ${name} imports records from a connected CRM or sequencer into a LeadMagic sheet. Check platform, object and maxRows before approving." ;;
  push)
    reason="LeadMagic ${name} writes sheet rows out to a connected CRM or sequencer. Review the selected rows and destination before approving." ;;
  delete)
    reason="LeadMagic ${name} deletes rows or list members in your LeadMagic workspace. Confirm the ids before approving." ;;
  edit)
    reason="LeadMagic ${name} changes sheets, lists, or columns in your LeadMagic workspace, or pauses or stops an active run or import. Review the target before approving." ;;
  export)
    reason="LeadMagic ${name} exports workspace data out of LeadMagic. Confirm the source and destination before approving." ;;
  *)
    reason="LeadMagic ${name} needs explicit approval under the LeadMagic plugin policy." ;;
esac
if session_skips_ask; then
  emit allow "LeadMagic ${name}: session permission_mode is ${permission_mode}, so the LeadMagic plugin does not add an approval prompt."
  exit 0
fi
emit ask "$reason"
