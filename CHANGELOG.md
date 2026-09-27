# Changelog

## 0.2.1 — 2026-09-23

One approval prompt per paid or destructive action. The hosted MCP now answers the first call to those tools with a preview and a `confirmation_token`, and acts only on a follow-up call carrying it, so the hook lets the preview through and asks on the follow-up. The CSV upload widget openers still ask every time.

## 0.2.0 — 2026-09-15

Approval policy hook. Read and single-record LeadMagic tools now run without a permission prompt; bulk jobs, paid runs, CRM/sequencer imports, outbound pushes and deletes still ask, with a reason naming the tool and what to check first. Replaces the bulk-only `credit-guard-bulk.sh` gate. Set `LEADMAGIC_ASK_ALL=1` to restore prompting for every tool. Plugin CI now smoke-tests the hook.

## Public-content privacy review — 2026-09-06

Use synthetic contact examples, remove unnecessary identity and credential-like samples, and clarify publication, attribution, and claims requirements.


## Unreleased — 2026-09-06

Clarify OAuth, credit-aware use, and source-aware email validation; add public-file safety checks.

