#!/usr/bin/env python3
"""Check that plugin, marketplace, and LICENSE name the same publisher and version."""
from pathlib import Path
import json
import re
import sys

root = Path(__file__).resolve().parents[1]
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
if issues:
    print("Publisher metadata checks failed:", *issues, sep="\n")
    sys.exit(1)
print("Publisher metadata checks passed.")
