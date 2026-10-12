---
description: Find the buyers at a target account and optionally their work emails
argument-hint: [company domain] [optional: titles you sell to]
---

Find decision-makers at: $ARGUMENTS

Follow the `decision-makers` skill:
1. **Preview the cost.** Call `preview_cost` for `find_decision_makers` with the same `titles` (1–5) and flags, and state the estimate.
2. **Search.** Call `find_decision_makers` with `company_domain` and the titles.
   - Set `include_email_discovery: true` only if the user wants emails. Discovered emails come back already validated.
3. **Fall back** for a specific title or a broader sweep: `find_people_by_role` or `search_people` with `company_domain` + `titles`.
4. **Return 2–4 named buyers** with title and company. Flag the likely economic buyer vs. the champion. Offer `/leadmagic:waterfall-email` for anyone still missing an email.
