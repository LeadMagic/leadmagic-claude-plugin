#!/usr/bin/env python3
"""Check tracked/public files without printing credential values. No network calls."""
from pathlib import Path
import json
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
paths = subprocess.check_output(
    ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=root
).decode().split("\0")
rules = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "leadmagic-key": re.compile(r"\blm_[A-Za-z0-9]{24,}\b"),
    "github-token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})\b"),
    "cloud-key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "stripe-secret": re.compile(r"\b(?:sk|rk)_live_[A-Za-z0-9]{24,}\b"),
}
issues = []
publisher = "LeadMagic Corporation"
try:
    plugin = json.loads((root / ".claude-plugin/plugin.json").read_text())
    marketplace = json.loads((root / ".claude-plugin/marketplace.json").read_text())
    identities = [("plugin author", plugin.get("author", {}).get("name")),
                  ("marketplace owner", marketplace.get("owner", {}).get("name"))]
    entries = marketplace.get("plugins", [])
    if len(entries) != 1:
        issues.append("marketplace must list exactly one LeadMagic plugin")
    for entry in entries:
        identities.append(("marketplace plugin author", entry.get("author", {}).get("name")))
        if entry.get("version") != plugin.get("version"):
            issues.append("marketplace plugin version must match plugin.json")
    for label, name in identities:
        if name != publisher:
            issues.append(f"{label} must be {publisher}")
    if plugin.get("displayName") != "LeadMagic":
        issues.append("plugin product displayName must remain LeadMagic")
    if marketplace.get("metadata", {}).get("version") != plugin.get("version"):
        issues.append("marketplace metadata version must match plugin.json")
    if not re.search(r"^Copyright \(c\) \d{4} LeadMagic Corporation$", (root / "LICENSE").read_text(), re.M):
        issues.append("LICENSE copyright holder must be LeadMagic Corporation")
except (OSError, ValueError, TypeError, AttributeError):
    issues.append("publisher metadata could not be validated")
for name in sorted(set(paths)):
    if not name:
        continue
    path = root / name
    if not path.is_file() or path.is_symlink():
        continue
    if path.name == ".env" or (path.name.startswith(".env.") and path.name not in (".env.example", ".env.sample", ".env.template")):
        issues.append(f"{name}: environment file must not be published")
    data = path.read_bytes()
    if b"\0" in data:
        continue
    text = data.decode("utf-8", errors="replace")
    for number, line in enumerate(text.splitlines(), 1):
        for label, rule in rules.items():
            if rule.search(line):
                issues.append(f"{name}:{number}: possible {label} (value omitted)")
if issues:
    print("Public-file checks failed:", *issues, sep="\n")
    sys.exit(1)
print("Public-file checks passed. Pattern checks supplement manual review and secret scanning.")
