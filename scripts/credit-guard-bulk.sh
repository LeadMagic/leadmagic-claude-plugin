#!/usr/bin/env bash
# PreToolUse gate for LeadMagic bulk / write MCP tools.
# Always asks the user before enqueueing credit-consuming bulk jobs.
set -euo pipefail

# Read tool-use JSON from stdin (ignored; we always ask for bulk writes).
cat >/dev/null || true

cat <<'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "ask",
    "permissionDecisionReason": "Bulk enrichment queues a paid LeadMagic job. Confirm credit balance / preview_cost first, then approve to continue."
  }
}
EOF
exit 0
