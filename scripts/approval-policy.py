"""Local PreToolUse decisions from hook input and the explicit ask_all argument.

Run with /usr/bin/python3 -I -S. This module uses only the standard library;
it does not read configuration, credentials, or environment values, start other
processes, or make network requests. Approval receipts stay in the supplied input
and never appear in the emitted decision.
"""

import json
import re
import sys


ASK_BEFORE_TOOLS = {
    "cancel_sheet_run": "edit",
    "create_bulk_upload_session": "bulk",
    "delete_sheet_column": "delete",
    "delete_sheet_rows": "delete",
    "find_local_leads": "bulk",
    "import_cloud_crm": "import",
    "import_cloud_sequencer": "import",
    "import_sheet_recipe": "import",
    "process_attached_csv": "bulk",
    "publish_cloud_workflow": "run",
    "push_cloud_rows": "push",
    "remove_prospect_list_members": "delete",
    "restart_bulk_job": "bulk",
    "resume_bulk_job": "run",
    "resume_cloud_run": "run",
    "run_cloud_workflow": "run",
    "run_sheet_column": "run",
    "save_sheet_http_request": "push",
    "set_sheet_cells": "edit",
    "set_sheet_column_auto_run": "run",
    "submit_bulk_job": "bulk",
    "submit_detected_bulk_job": "bulk",
    "test_sheet_http_request": "push",
    "update_sheet_http_request": "push",
}

ACTING_PREFIXES = (
    (("import_",), "import"),
    (("push_",), "push"),
    (("publish_", "run_", "resume_", "rerun_"), "run"),
    (("submit_", "restart_"), "bulk"),
    (("delete_", "remove_"), "delete"),
    (("export_",), "export"),
    (("cancel_", "pause_", "update_", "add_", "restore_", "set_", "create_",
      "configure_", "reorder_", "extract_"), "edit"),
)

IMMEDIATE_TOOLS = {
    "create_bulk_upload_session", "process_attached_csv", "set_sheet_cells", "cancel_sheet_run",
}

REASONS = {
    "bulk": "queues a paid bulk job that bills every row. Check preview_cost and check_credit_balance, confirm the row count, then approve.",
    "run": "starts a paid run. Confirm the max credits shown by the preview call before approving.",
    "import": "imports records from a connected CRM or sequencer into a LeadMagic sheet. Check platform, object and maxRows before approving.",
    "push": "writes sheet rows out to a connected CRM or sequencer. Review the selected rows and destination before approving.",
    "delete": "deletes rows or list members in your LeadMagic workspace. Confirm the ids before approving.",
    "edit": "changes sheets, lists, or columns in your LeadMagic workspace, or pauses or stops an active run or import. Review the target before approving.",
    "export": "exports workspace data out of LeadMagic. Confirm the source and destination before approving.",
}


def output(reason):
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": reason,
        }
    }


def decide(payload):
    """Return a local permission decision, or None to retain normal permissions."""
    if not isinstance(payload, dict) or not isinstance(payload.get("tool_name"), str):
        return None
    if "permission_mode" in payload and not isinstance(payload["permission_mode"], str):
        return None
    if "tool_input" in payload and not isinstance(payload["tool_input"], dict):
        return None

    match = re.fullmatch(r"mcp__(?:plugin_leadmagic_)?leadmagic__([a-z0-9_]+)", payload["tool_name"])
    if match is None:
        return None
    name = match.group(1)
    permission_mode = payload.get("permission_mode") or "default"
    approval_present = isinstance(payload.get("tool_input", {}).get("confirmation_token"), str)

    group = ASK_BEFORE_TOOLS.get(name)
    known_preview = group is not None
    if group is None:
        for prefixes, candidate in ACTING_PREFIXES:
            if name.startswith(prefixes):
                group = candidate
                break

    if group is None:
        return None

    if known_preview and not approval_present and name not in IMMEDIATE_TOOLS:
        return None

    if permission_mode in ("bypassPermissions", "auto", "dontAsk"):
        return None
    return output(f"LeadMagic {name} {REASONS[group]}")


def reject_constant(value):
    raise ValueError("non-JSON constant")


def main():
    try:
        raw_input = sys.stdin.read()
        # Drain stdin even when opting out, then leave permission handling to Claude Code.
        if len(sys.argv) > 1 and sys.argv[1] in ("true", "1"):
            return
        payload = json.loads(raw_input, parse_constant=reject_constant)
    except (ValueError, UnicodeError, RecursionError):
        return
    result = decide(payload)
    if result is not None:
        print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    main()
