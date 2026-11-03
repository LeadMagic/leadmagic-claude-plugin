"""Approval decisions for state-changing hosted MCP calls."""
import json
import re
import shutil
import tempfile
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "scripts" / "approval-policy.py"


def configured_command(ask_all="false", root=ROOT):
    config = json.loads((ROOT / "hooks" / "hooks.json").read_text())
    hook = config["hooks"]["PreToolUse"][0]["hooks"][0]
    return [arg.replace("${CLAUDE_PLUGIN_ROOT}", str(root))
            .replace("${user_config.ask_all}", ask_all)
            for arg in [hook["command"], *hook["args"]]]


# Fixed tool path for the hook; the tests pass no other environment values.
TOOL_PATH = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"


class ApprovalPolicyTest(unittest.TestCase):
    def output(self, payload, *, env=None, args=("false",)):
        hook_env = {"PATH": TOOL_PATH}
        if env:
            hook_env.update(env)
        return subprocess.check_output(
            [*configured_command()[:-1], *args], input=payload, text=True, env=hook_env
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
        return json.loads(output)["hookSpecificOutput"]["permissionDecision"] if output else None

    def test_immediate_sheet_mutations_ask_without_a_token(self):
        for prefix in ("mcp__plugin_leadmagic_leadmagic__", "mcp__leadmagic__"):
            for name in ("set_sheet_cells", "cancel_sheet_run"):
                for mode in ("default", "acceptEdits", "plan"):
                    with self.subTest(name=name, mode=mode, prefix=prefix):
                        self.assertEqual(self.decision(name, mode, prefix=prefix), "ask")

    def test_preview_calls_and_approved_submits_are_distinct(self):
        for name in ("submit_detected_bulk_job", "delete_sheet_rows", "run_sheet_column"):
            with self.subTest(name=name):
                self.assertEqual(self.decision(name), None)
                self.assertEqual(self.decision(name, token="v1.1.sig"), "ask")

    def test_widgets_ask_before_opening(self):
        for name in ("create_bulk_upload_session", "process_attached_csv"):
            with self.subTest(name=name):
                self.assertEqual(self.decision(name), "ask")

    def test_user_selected_automatic_modes_use_host_permissions(self):
        for name in ("set_sheet_cells", "cancel_sheet_run", "process_attached_csv", "submit_detected_bulk_job"):
            for mode in ("auto", "dontAsk", "bypassPermissions"):
                with self.subTest(name=name, mode=mode):
                    self.assertEqual(self.decision(name, mode, token="v1.1.sig"), None)

    def test_unknown_acting_tools_ask_without_assuming_a_preview(self):
        for prefix in ("mcp__plugin_leadmagic_leadmagic__", "mcp__leadmagic__"):
            for name in ("import_new_source", "push_new_rows", "run_new_workflow", "submit_new_job", "delete_new_rows"):
                with self.subTest(name=name, prefix=prefix):
                    self.assertEqual(self.decision(name, prefix=prefix), "ask")
                    self.assertEqual(self.decision(name, token="v1.1.sig", prefix=prefix), "ask")
                    self.assertEqual(self.decision(name, mode="auto", prefix=prefix), None)

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
        self.assertEqual(self.output(payload), "")

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

    def test_hook_needs_no_path_tools_or_jq(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = json.dumps({"tool_name": "mcp__leadmagic__set_sheet_cells"})
            output = self.output(payload, env={"PATH": tmp})
            self.assertEqual(json.loads(output)["hookSpecificOutput"]["permissionDecision"], "ask")

    def test_ask_all_retains_normal_permissions(self):
        payload = json.dumps({"tool_name": "mcp__leadmagic__search_people"})
        self.assertEqual(self.output(payload, args=("true",)), "")
        self.assertEqual(self.output(payload, args=("1",)), "")
        # An absent opt-out argument keeps the policy on.
        self.assertEqual(self.output(payload, args=()), "")

    def test_hook_ignores_interpreter_startup_and_import_overrides(self):
        with tempfile.TemporaryDirectory() as tmp:
            startup = Path(tmp) / "startup.py"
            marker = Path(tmp) / "startup-ran"
            injected = f"open({str(marker)!r}, 'w').close()\nraise SystemExit(97)\n"
            startup.write_text(injected)
            for name in ("sitecustomize.py", "usercustomize.py", "json.py"):
                (Path(tmp) / name).write_text(injected)
            payload = json.dumps({"tool_name": "mcp__leadmagic__set_sheet_cells"})
            hook_env = {
                "PATH": TOOL_PATH,
                "PYTHONSTARTUP": str(startup),
                "PYTHONPATH": tmp,
                "PYTHONHOME": tmp,
                "PYTHONUSERBASE": tmp,
            }
            for ask_all in ("false", "true"):
                with self.subTest(ask_all=ask_all):
                    result = subprocess.run(configured_command(ask_all), input=payload, text=True,
                                            env=hook_env, cwd=tmp, capture_output=True, check=True)
                    if ask_all == "true":
                        self.assertEqual(result.stdout, "")
                    else:
                        self.assertEqual(json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"], "ask")
                    self.assertEqual(result.stderr, "")
                    self.assertFalse(marker.exists())

    def test_manifest_invocation_handles_install_paths_with_spaces(self):
        with tempfile.TemporaryDirectory(prefix="LeadMagic plugin ") as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            shutil.copyfile(HOOK, root / "scripts" / HOOK.name)
            payload = json.dumps({"tool_name": "mcp__leadmagic__set_sheet_cells"})
            output = subprocess.check_output(configured_command(root=root), input=payload, text=True)
            self.assertEqual(json.loads(output)["hookSpecificOutput"]["permissionDecision"], "ask")

    def test_input_values_cannot_inject_output_or_permission_modes(self):
        payload = json.dumps({
            "tool_name": "mcp__leadmagic__set_sheet_cells",
            "permission_mode": "auto\tdefault\n\"injected\"",
            "tool_input": {"confirmation_token": "private-receipt-value"},
        })
        output = self.output(payload)
        self.assertEqual(json.loads(output)["hookSpecificOutput"]["permissionDecision"], "ask")
        self.assertNotIn("private-receipt-value", output)

    def test_large_invalid_nesting_retains_normal_permissions(self):
        self.assertEqual(self.output("[" * 2000 + "]" * 2000), "")

    def test_matcher_covers_both_tool_prefixes_only(self):
        config = json.loads((HOOK.parents[1] / "hooks" / "hooks.json").read_text())
        matcher = config["hooks"]["PreToolUse"][0]["matcher"]
        for name in ("mcp__leadmagic__set_sheet_cells", "mcp__plugin_leadmagic_leadmagic__search_people"):
            self.assertIsNotNone(re.fullmatch(matcher, name))
        for name in ("mcp__other__search_people", "mcp__leadmagic__search_people-extra", "Bash"):
            self.assertIsNone(re.fullmatch(matcher, name))

    def test_reads_previews_and_single_record_lookups_use_host_permissions(self):
        for name in READ_OR_LOOKUP_TOOLS:
            with self.subTest(name=name):
                self.assertEqual(self.decision(name), None)
                self.assertEqual(self.decision(name, token="v1.1.sig"), None)

    def test_state_changing_tools_without_a_preview_contract_always_ask(self):
        for prefix in ("mcp__plugin_leadmagic_leadmagic__", "mcp__leadmagic__"):
            for name in MUTATING_TOOLS:
                with self.subTest(name=name, prefix=prefix):
                    for mode in ("default", "acceptEdits", "plan"):
                        self.assertEqual(self.decision(name, mode=mode, prefix=prefix), "ask")
                        self.assertEqual(self.decision(name, mode=mode, token="v1.1.sig", prefix=prefix), "ask")
                    for mode in ("auto", "dontAsk", "bypassPermissions"):
                        self.assertEqual(self.decision(name, mode=mode, prefix=prefix), None)


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
