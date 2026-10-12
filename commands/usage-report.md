---
description: LeadMagic credit and usage report from free account analytics
argument-hint: "[optional period, e.g. 'this week']"
---

Build a LeadMagic usage report for: $ARGUMENTS (default: this week).

1. Call `get_account_analytics` and `check_credit_balance`. Both are free.
2. Report:
   - Credit balance
   - Credits used today / this week / this month
   - Calls and average cost per call
   - Top tools by spend
   - Rate-limit and concurrency headroom
3. If the period asked for is not one the analytics return (today, week, month), say so and report the closest one.
4. Flag anything notable, such as a single tool dominating spend. Suggest a cheaper path where the `credit-guard` skill applies.

For plan or top-up changes, link [billing](https://app.leadmagic.io/settings/billing). Never change billing from chat.
