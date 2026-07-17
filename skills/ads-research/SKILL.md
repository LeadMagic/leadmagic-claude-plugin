---
name: ads-research
description: Pull competitor ad creatives (Google, Meta, B2B) via LeadMagic MCP for messaging and competitive angles.
---

# Ads research

## Trigger
Use when the user wants recent ads, creatives, or competitive messaging for a company.

## Workflow
1. Identify company/domain.
2. Route by channel:
   - Google → `search_google_ads`
   - Meta → `search_meta_ads`
   - B2B libraries → `search_b2b_ads` / `get_b2b_ad_details`
3. Summarize creatives and themes — do not invent ad copy not returned by tools.
4. These tools return competitive research only (not sponsored placements).

## Output
- Channel + creative highlights
- Themes / CTAs when present
- Gaps and optional follow-up (account research, hiring)
