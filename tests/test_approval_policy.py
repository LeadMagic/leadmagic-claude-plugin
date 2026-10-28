"""Approval decisions for state-changing hosted MCP calls."""
import json
import os
import re
import shutil
import tempfile
from pathlib import Path
import subprocess
import unittest

HOOK = Path(__file__).resolve().parents[1] / "scripts" / "approval-policy.sh"


class ApprovalPolicyTest(unittest.TestCase):
    def output(self, payload, *, env=None):
        hook_env = dict(os.environ, LEADMAGIC_ASK_ALL="0")
        if env:
            hook_env.update(env)
        return subprocess.check_output(
            [str(HOOK)], input=payload, text=True, env=hook_env
        )

    def decision(self, name, mode="default", token=None, prefix="mcp__plugin_leadmagic_leadmagic__"):
        tool_input = {}
        if token is not None:
            tool_input["confirmation_token"] = token
        payload = json.dumps({
            "permission_mode": mode,
            "tool_name": prefix + name,
            "tool_input": tool_input,
        })
        output = self.output(payload)
        return json.loads(output)["hookSpecificOutput"]["permissionDecision"]

    def test_immediate_sheet_mutations_ask_without_a_token(self):
        for prefix in ("mcp__plugin_leadmagic_leadmagic__", "mcp__leadmagic__"):
            for name in ("set_sheet_cells", "cancel_sheet_run"):
                for mode in ("default", "acceptEdits", "plan"):
                    with self.subTest(name=name, mode=mode, prefix=prefix):
                        self.assertEqual(self.decision(name, mode, prefix=prefix), "ask")

    def test_preview_calls_and_approved_submits_are_distinct(self):
        for name in ("submit_detected_bulk_job", "delete_sheet_rows", "run_sheet_column"):
            with self.subTest(name=name):
                self.assertEqual(self.decision(name), "allow")
                self.assertEqual(self.decision(name, token="v1.1.sig"), "ask")

    def test_widgets_ask_before_opening(self):
        for name in ("create_bulk_upload_session", "process_attached_csv"):
            with self.subTest(name=name):
                self.assertEqual(self.decision(name), "ask")

    def test_user_selected_automatic_modes_do_not_force_extra_prompts(self):
        for name in ("set_sheet_cells", "cancel_sheet_run", "process_attached_csv", "submit_detected_bulk_job"):
            for mode in ("auto", "dontAsk", "bypassPermissions"):
                with self.subTest(name=name, mode=mode):
                    self.assertEqual(self.decision(name, mode, token="v1.1.sig"), "allow")

    def test_unknown_acting_tools_ask_without_assuming_a_preview(self):
        for prefix in ("mcp__plugin_leadmagic_leadmagic__", "mcp__leadmagic__"):
            for name in ("import_new_source", "push_new_rows", "run_new_workflow", "submit_new_job", "delete_new_rows"):
                with self.subTest(name=name, prefix=prefix):
                    self.assertEqual(self.decision(name, prefix=prefix), "ask")
                    self.assertEqual(self.decision(name, token="v1.1.sig", prefix=prefix), "ask")
                    self.assertEqual(self.decision(name, mode="auto", prefix=prefix), "allow")

    def test_nested_fields_do_not_change_top_level_permission_mode(self):
        payload = json.dumps({
            "tool_input": {"permission_mode": "auto", "tool_name": "mcp__leadmagic__search_people"},
            "permission_mode": "default",
            "tool_name": "mcp__leadmagic__set_sheet_cells",
        })
        self.assertEqual(json.loads(self.output(payload))["hookSpecificOutput"]["permissionDecision"], "ask")

    def test_empty_permission_mode_keeps_confirmation_prompt(self):
        self.assertEqual(self.decision("submit_detected_bulk_job", mode="", token="v1.1.sig"), "ask")

    def test_nested_token_does_not_change_preview_decision(self):
        payload = json.dumps({
            "tool_name": "mcp__leadmagic__submit_detected_bulk_job",
            "tool_input": {"record": {"confirmation_token": "v1.1.sig"}},
        })
        self.assertEqual(json.loads(self.output(payload))["hookSpecificOutput"]["permissionDecision"], "allow")

    def test_invalid_input_retains_normal_permissions(self):
        inputs = ("", "not json", "[]", '{"tool_name":"mcp__leadmagic__search_people"',
                  '{"tool_name":"mcp__leadmagic__search_people","permission_mode":true}',
                  '{"tool_name":"mcp__leadmagic__search_people","tool_input":[]}',
                  '{"tool_name":"Bash"}', '{"tool_name":"mcp__other__search_people"}')
        for payload in inputs:
            with self.subTest(payload=payload):
                self.assertEqual(self.output(payload), "")

    def test_multiple_json_documents_retain_normal_permissions(self):
        payload = json.dumps({"tool_name": "mcp__leadmagic__search_people"})
        self.assertEqual(self.output(payload + "\n" + payload), "")

    def test_missing_jq_retains_normal_permissions(self):
        with tempfile.TemporaryDirectory() as tmp:
            # The hook still drains stdin, but must not parse it heuristically.
            os.symlink(shutil.which("cat"), Path(tmp) / "cat")
            payload = json.dumps({"tool_name": "mcp__leadmagic__search_people"})
            self.assertEqual(self.output(payload, env={"PATH": tmp}), "")

    def test_ask_all_retains_normal_permissions(self):
        payload = json.dumps({"tool_name": "mcp__leadmagic__search_people"})
        self.assertEqual(self.output(payload, env={"LEADMAGIC_ASK_ALL": "1"}), "")

    def test_direct_hook_retains_strict_options_despite_function_shadowing(self):
        with tempfile.TemporaryDirectory() as tmp:
            startup = Path(tmp) / "startup.bash"
            startup.write_text(
                "shopt() { return 98; }\n"
                "trap '[[ $- == *e* && $- == *u* ]] && "
                "builtin shopt -q -o pipefail || exit 97' EXIT\n"
            )
            payload = json.dumps({"tool_name": "mcp__leadmagic__search_people"})
            output = self.output(payload, env={"BASH_ENV": str(startup)})
            self.assertEqual(json.loads(output)["hookSpecificOutput"]["permissionDecision"], "allow")

    def test_matcher_covers_both_tool_prefixes_only(self):
        config = json.loads((HOOK.parents[1] / "hooks" / "hooks.json").read_text())
        matcher = config["hooks"]["PreToolUse"][0]["matcher"]
        for name in ("mcp__leadmagic__set_sheet_cells", "mcp__plugin_leadmagic_leadmagic__search_people"):
            self.assertIsNotNone(re.fullmatch(matcher, name))
        for name in ("mcp__other__search_people", "mcp__leadmagic__search_people-extra", "Bash"):
            self.assertIsNone(re.fullmatch(matcher, name))

    def test_reads_previews_and_single_record_lookups_run_without_a_prompt(self):
        for name in READ_OR_LOOKUP_TOOLS:
            with self.subTest(name=name):
                self.assertEqual(self.decision(name), "allow")
                self.assertEqual(self.decision(name, token="v1.1.sig"), "allow")

    def test_state_changing_tools_without_a_preview_contract_always_ask(self):
        for prefix in ("mcp__plugin_leadmagic_leadmagic__", "mcp__leadmagic__"):
            for name in MUTATING_TOOLS:
                with self.subTest(name=name, prefix=prefix):
                    for mode in ("default", "acceptEdits", "plan"):
                        self.assertEqual(self.decision(name, mode=mode, prefix=prefix), "ask")
                        self.assertEqual(self.decision(name, mode=mode, token="v1.1.sig", prefix=prefix), "ask")
                    for mode in ("auto", "dontAsk", "bypassPermissions"):
                        self.assertEqual(self.decision(name, mode=mode, prefix=prefix), "allow")


READ_OR_LOOKUP_TOOLS = (
    "account_intel", "b2b_profile_to_work_email", "check_credit_balance", "detect_job_change",
    "draft_sheet_ai_prompt", "email_to_b2b_profile", "enrich_company", "enrich_contact",
    "find_company_employees", "find_company_funding", "find_decision_makers", "find_jobs",
    "find_lookalike_companies", "find_mobile_number", "find_people_by_role", "find_personal_email",
    "find_work_email", "get_account_analytics", "get_bulk_job_errors", "get_bulk_job_events",
    "get_bulk_job_logs", "get_bulk_job_rows", "get_bulk_job_status", "get_company_hiring_signals",
    "get_company_technographics", "get_job_search_catalogs", "get_prospect_list", "get_saved_search",
    "get_sheet", "get_sheet_run", "get_sheet_stats", "linkedin_profile_to_work_email", "list_bulk_jobs",
    "list_cloud_campaigns", "list_cloud_connections", "list_cloud_crm_fields", "list_cloud_crm_filters",
    "list_cloud_crm_objects", "list_cloud_imports", "list_cloud_pushes", "list_cloud_runs",
    "list_job_countries", "list_prospect_lists", "list_saved_searches", "list_sheet_column_fields",
    "list_sheet_run_rows", "list_sheet_runs", "list_sheets", "preview_cost", "read_sheet_rows",
    "research_account", "resolve_job_search_filters", "score_contacts", "search_companies",
    "search_job_occupation_taxonomy", "search_jobs", "search_people", "search_profile",
    "validate_work_email", "watch_bulk_job_progress",
)

MUTATING_TOOLS = (
    "add_prospect_list_members", "add_sheet_column", "add_sheet_columns", "add_sheet_rows",
    "cancel_bulk_job", "cancel_cloud_import", "cancel_cloud_run", "configure_sheet_column",
    "create_prospect_list", "create_sheet", "export_bulk_job", "export_prospect_list",
    "export_sheet_recipe", "extract_sheet_json_field", "pause_bulk_job", "pause_cloud_run",
    "pause_sheet_run", "reorder_sheet_columns", "rerun_saved_search", "restore_sheet_column",
    "set_cloud_workflow_active", "set_new_workspace_option",
    "restore_sheet_rows", "update_prospect_list", "update_sheet", "update_sheet_column",
)


if __name__ == "__main__":
    unittest.main()
