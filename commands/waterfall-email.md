---
description: Cheapest-first email waterfall for one contact — stop at the first hit
argument-hint: [name + company, an email, or a profile URL]
---

Find a reachable email for: $ARGUMENTS

This is for **one** contact. For more than 5, use `/leadmagic:enrich-sheet` or the `bulk-enrichment` skill instead of repeating the waterfall.

1. **Estimate first.** Call `preview_cost` for the step(s) you expect to run and state the estimate.
2. **Run in order, stopping at the first success:**
   1. **They gave an email** → `validate_work_email`. If it is valid, you're done.
   2. **Name + company/domain** → `find_work_email`. Finder emails are already validated; don't re-validate them.
   3. **Profile URL** (the full URL; the path ends in `in/{slug}`) → `b2b_profile_to_work_email`.
   4. **A personal email is acceptable** for this lawful B2B use → `find_personal_email`.
3. **Phone:** only if the user explicitly asks for a phone, `find_mobile_number`, as a separate step.
4. **Don't overspend.** Never run a step past the one that answered. Never run `email_to_b2b_profile` just to get an email.
5. **Report:** the email found, its validation status, the steps run, and the credits spent. Misses are usually free.
