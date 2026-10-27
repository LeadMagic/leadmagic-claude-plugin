---
description: Find the buyers at a target account and optionally their work emails
argument-hint: "[company domain] [optional: titles you sell to]"
---

Find decision-makers at: $ARGUMENTS

Follow the `decision-makers` skill:
1. **Choose the lookup.** For a specific role or title at the company, use `find_people_by_role` first. For a broad buyer briefing, use `find_decision_makers` with 1–5 `titles`.
2. **Preview the cost.** Call `preview_cost` for the chosen tool with the same inputs and flags, and state the estimate.
3. **Look up buyers.** Call the chosen tool with the company domain and requested role or titles.
   - Set `include_email_discovery: true` on `find_decision_makers` only if the user wants emails. Discovered emails come back already validated.
   - If Role Finder finds no one, report the miss. Do not substitute `search_people` results; people search is for a separately requested broad discovery list.
4. **Return only the buyers found** with title and company. For a broad briefing, flag the likely economic buyer vs. the champion. Offer `/leadmagic:waterfall-email` for anyone still missing a requested email.
