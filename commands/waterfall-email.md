---
description: Cheapest-first email waterfall for one contact — stop at the first hit
argument-hint: "[name + company, an email, or a profile URL]"
---

Find a reachable email for: $ARGUMENTS

This is for **one** contact. For more than 5, use `/leadmagic:enrich-sheet` or the `bulk-enrichment` skill instead of repeating the waterfall.

1. **Estimate first.** Call `preview_cost` for the step(s) you expect to run and state the estimate.
2. **Run in order, stopping only at a valid result:**
   1. **They gave an email** → `validate_work_email`. Stop only when the exact returned status is `valid`. `invalid` and `unknown` (including catch-all) are not hits; continue only if the user also provided a name + company/domain or profile URL that supports another step. If the email is the only identifier, report its status and stop without claiming success.
   2. **Name + company/domain** → `find_work_email`. Finder emails are already validated; don't re-validate them. Treat a result as a hit only when its status is `valid`.
   3. **Profile URL** (the full URL; the path ends in `in/{slug}`) → `b2b_profile_to_work_email`. Treat a result as a hit only when its status is `valid`.
   4. **A personal email is acceptable** for this lawful B2B use and the user explicitly asked for that channel → `find_personal_email`. Treat a result as a hit only when its status is `valid`.
3. **Phone:** only if the user explicitly asks for a phone, `find_mobile_number`, as a separate step.
4. **Don't overspend.** Never run a step past the one that answered. Never run `email_to_b2b_profile` just to get an email.
5. **Report:** the email found, its exact validation status (`valid`, `invalid`, or `unknown`), the steps run, and the credits spent. Only `valid` is a success; `unknown` includes catch-all and is not deliverable. Misses are usually free.
