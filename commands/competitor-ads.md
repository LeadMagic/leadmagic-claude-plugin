---
description: Pull a competitor's ad creatives and mine messaging angles with LeadMagic ads search
argument-hint: [competitor domain(s)]
---

Research ads for: $ARGUMENTS

Follow the `ads-research` skill:
1. **Search each channel with a `limit`.** Per domain, call `search_google_ads`, `search_meta_ads`, and `search_b2b_ads`, each with `limit` (default 10). Ads are billed per ad returned, so `limit` caps spend.
2. **Dissect selectively.** Call `get_b2b_ad_details` only for creatives worth a closer look.
3. **Compare to earlier output.** If a previous run's output is in the conversation, flag new and retired creatives.
4. **Report:** active channels, core promises and offers, CTAs, and 2–3 counter-positioning angles for outreach.
   - An empty result means the company is not advertising on that network. That is a finding; don't retry.
   - Never invent ad copy.
