---
name: contact-lookup
description: Find, validate, or identify one B2B contact with LeadMagic MCP — work email, profile, or reverse email lookup. Use when the user has a person plus company, a profile URL, or an email and wants a work email, deliverability check, or who-is-this answer.
---

# Contact lookup

## Trigger
Use when the user needs a work email for a specific person, wants to check an address, or wants the professional profile behind a URL or email. For more than 5 people, use the `bulk-enrichment` or `sheets` skill — never loop these tools per row.

## Workflow
1. Start from the strongest identifier the user gave:
   - Existing email from elsewhere (CRM, list, sign-up) → `validate_work_email`. Its public status is exactly `valid`, `invalid`, or `unknown`; treat only `valid` as deliverable. `unknown` includes catch-all results and must never be reported as deliverable.
   - Full name + company/domain → `find_work_email`, or composite `enrich_contact` when they want the full picture
   - Profile URL (the full URL; the path ends in `in/{slug}`) → `b2b_profile_to_work_email` for the work email, `search_profile` for name, role, company, and work history
   - Email only, and they want the person behind it → `email_to_b2b_profile` (returns a profile URL), then `search_profile` if they want details
   - "Has this person moved on?" → `detect_job_change` with `profile_url` (most reliable) or `work_email`, plus the expected company when known
2. Take the cheapest path that answers the question:
   - Do not re-find an email that already validates.
   - Never validate an email a LeadMagic finder just returned: finder emails are already validated. For any validation result, only the exact status `valid` is a success; `invalid` and `unknown` are not. Do not present catch-all/unknown results as deliverable.
   - Use `email_to_b2b_profile` only when the user actually needs the profile. It is pricier than the email tools, so check `preview_cost` first.
3. Prefer one composite over chaining many primitives, and don't repeat a lookup already made for the same inputs.
4. Personal email (`find_personal_email`) and mobile (`find_mobile_number`) are lawful B2B fallbacks. Use them only when the user explicitly asks for that channel.
5. Report only fields the tools returned — never invent contacts, emails, or titles.

## Output
- The best contact field found and its validation status
- The inputs used and the tools called
- Not-found cases (usually free)
- A concise next action
