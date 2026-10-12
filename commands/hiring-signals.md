---
description: Rank target accounts by hiring activity with LeadMagic jobs search
argument-hint: [company domains] [optional: roles and time window]
---

Research hiring activity for: $ARGUMENTS

Follow the `hiring-intent` skill:
1. **One jobs search covers several accounts.** Make one `search_jobs` call with `company_domains` (up to 25 per call), plus `titles` and `posted_within` from the request. Page it with `cursor`. Don't make one call per domain.
   - Browse search is credit-free only on qualifying plans; elsewhere it costs per job returned. State the cost (`preview_cost`) first.
2. **Velocity for a shortlist.** For the shortlist, call `get_company_hiring_signals` (one credit each) when the user wants velocity rather than listings.
3. **Return a ranked table:** company, matching roles, posting dates, and links.
   - Derive trends only from dated postings the tools returned.
   - Label buying intent as a hypothesis.

Do not send outreach.
