---
description: Validate a work email with LeadMagic
---

Using LeadMagic MCP `validate_work_email`, validate the email the user provided.

Pass a real address in the `email` argument (e.g. `email: "jane@acme.com"`). Do not call the tool with empty args. If the user only gave a name + company, use `find_work_email` first.

Report status and any company/title signals returned — do not invent fields.
