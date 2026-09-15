#!/usr/bin/env bash
# PreToolUse approval policy for LeadMagic MCP tools (mcp__leadmagic__*).
#
# Auto-approves every LeadMagic tool except ASK_BEFORE_TOOLS, which still prompt
# because they queue paid jobs, start paid runs, move data in or out of connected
# systems, or delete. Emits no decision at all (Claude Code's normal permission
# flow) when stdin cannot be parsed, the tool is not a LeadMagic tool, or
# LEADMAGIC_ASK_ALL=1 is set.
#
# Contract: the ASK_BEFORE_TOOLS array is parsed by
# lm-tui/tests/unit/plugin-approval-policy.test.ts and mirrored by the Claude Code
# permissions snippet on app.leadmagic.io (Settings -> API -> AI tooling). One
# "tool:group" entry per line, double-quoted, sorted. Groups: bulk | run | import |
# push | delete.
#
# Bash 3.2 compatible (macOS /bin/bash): no associative arrays, no lowercasing.
set -euo pipefail

ASK_BEFORE_TOOLS=(
  "create_bulk_upload_session:bulk"
  "delete_sheet_rows:delete"
  "import_cloud_crm:import"
  "import_cloud_sequencer:import"
  "process_attached_csv:bulk"
  "publish_cloud_workflow:run"
  "push_cloud_rows:push"
  "remove_prospect_list_members:delete"
  "restart_bulk_job:bulk"
  "resume_bulk_job:run"
  "resume_cloud_run:run"
  "run_cloud_workflow:run"
  "run_sheet_column:run"
  "submit_bulk_job:bulk"
  "submit_detected_bulk_job:bulk"
)

# Always drain stdin first, even when we decide to say nothing.
input="$(cat || true)"

# Escape hatch: fall back to Claude Code's own permission rules for every tool.
if [[ "${LEADMAGIC_ASK_ALL:-}" == "1" ]]; then
  exit 0
fi

# Leftmost match wins. Claude Code emits tool_name before tool_input, so a
# "tool_name" string inside tool_input cannot shadow the real key.
tool_name_pattern='"tool_name"[[:space:]]*:[[:space:]]*"([^"]*)"'
tool=""
if [[ "$input" =~ $tool_name_pattern ]]; then
  tool="${BASH_REMATCH[1]}"
fi

# Only decide for well-formed LeadMagic tool names; anything else gets no output.
# The strict charset is also what makes $name safe to interpolate into JSON below.
if [[ ! "$tool" =~ ^mcp__leadmagic__([a-z0-9_]+)$ ]]; then
  exit 0
fi
name="${BASH_REMATCH[1]}"

group=""
for entry in "${ASK_BEFORE_TOOLS[@]}"; do
  if [[ "${entry%%:*}" == "$name" ]]; then
    group="${entry##*:}"
    break
  fi
done

emit() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"%s","permissionDecisionReason":"%s"}}\n' "$1" "$2"
}

if [[ -z "$group" ]]; then
  emit allow "LeadMagic ${name}: read or single-record tool, auto-approved by the LeadMagic plugin. Set LEADMAGIC_ASK_ALL=1 to prompt for every tool."
  exit 0
fi

case "$group" in
  bulk)
    reason="LeadMagic ${name} queues a paid bulk job that bills every row. Check preview_cost and check_credit_balance, confirm the row count, then approve." ;;
  run)
    reason="LeadMagic ${name} starts a paid run. Confirm the previewed max credits (run_sheet_column preview or quote_cloud_workflow) before approving." ;;
  import)
    reason="LeadMagic ${name} imports records from a connected CRM or sequencer into a LeadMagic sheet. Check platform, object and maxRows before approving." ;;
  push)
    reason="LeadMagic ${name} writes sheet rows out to a connected CRM or sequencer. Review the selected rows and destination before approving." ;;
  delete)
    reason="LeadMagic ${name} deletes rows or list members in your LeadMagic workspace. Confirm the ids before approving." ;;
  *)
    reason="LeadMagic ${name} needs explicit approval under the LeadMagic plugin policy." ;;
esac
emit ask "$reason"
