---
description: Validate a work email with LeadMagic
---

Using LeadMagic MCP `validate_work_email`, validate the email the user provided from another source.

Pass the real address in the `email` argument (e.g. `email: "jane@acme.com"`). Do not call the tool with empty args. If the user only gave a name + company, use `find_work_email` instead.

Report the exact returned status: `valid`, `invalid`, or `unknown`. Only `valid` counts as deliverable. `unknown` includes catch-all results and must not be described as valid or deliverable. Report any company/title signals returned; do not invent fields.
