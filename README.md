# Phalom · Sabaidee Merchant

Project files for Team ພັດລົມ (Phalom), Innovative Business Challenge – MSME, Challenge No. 10. **Slides are due 15 October 2026; the final pitch is 17 October 2026.**

## Pitch materials (start here)

- [`exports/Sabaidee-Merchant-Pitch-Deck.pdf`](exports/Sabaidee-Merchant-Pitch-Deck.pdf): final 13-slide deck in Lao, for submission. Generated from [`exports/pitch_deck_slide.html`](exports/pitch_deck_slide.html) (open in a browser to present; the PDF button saves a new PDF after edits).
- [`exports/merchant_app_prototype.html`](exports/merchant_app_prototype.html): clickable merchant-app prototype for the live demo (v2.0: selling with the traffic light, reports and forecast, points and rewards, bill payment, support, consumer protection, account security, Lao/English). Works offline.
- [`04_PITCH_SCRIPT.md`](04_PITCH_SCRIPT.md): speaker script, demo steps, short version and judge Q&A for practice.
- [`00_CONTEXT.md`](00_CONTEXT.md): deadlines and owner decisions. Read this first before changing anything.

The **Lao team overview** at [`output/html/sabaidee-merchant-brief.html`](output/html/sabaidee-merchant-brief.html) explains the customer problem, who uses each app and one payment from start to finish.

## Project documents

- [`01_CODEX_ARCH.md`](01_CODEX_ARCH.md): proposed technical architecture, features, money states, partner requirements, and failure handling.
- [`02_GEMINI_AUDIT.md`](02_GEMINI_AUDIT.md): adversarial UX, finance, compliance, and fraud review.
- [`03_FINAL_SPEC.md`](03_FINAL_SPEC.md): agreement ledger, including the owner decisions of 2026-10-12 (C16–C23).
- [`exports/system_flowchart.html`](exports/system_flowchart.html): interactive payment architecture and six scenarios.
- [`output/discord-server-blueprint.md`](output/discord-server-blueprint.md) and [`output/discord/`](output/discord/): team workspace plan and optional one-time setup script.
- Root PDFs: the IBC pitch-deck template and challenge list for reference.

`output/pdf/Sabaidee-Merchant-Team-Brief-Lao.pdf` is the earlier v1.0 brief retained for history. The current, fuller team overview is the v2.0 HTML file above; use that version when onboarding teammates.

## Status

This is a pitch-stage proposal. Payment integrations, partner agreements, legal approvals, fee rates, settlement timing, user research, and pilot results have not been established by these documents. Mark ideas as proposals until the team validates them with vendors and appropriately authorized financial partners.

Before using the Discord script, read its `output/discord/README.md`. It can create roles and channels on a Discord server when run with `--apply`; it is not part of the payment system.

# Version Log

| Timestamp | Version | Author | Change |
|---|---|---|---|
| 2026-10-12 23:09:45 +07:00 (Asia/Bangkok) | 1.0 | Codex | Added a team entry point and project index for the initial public repository upload. Identifies the current overview, proposal status, and historical PDF. |
| 2026-10-12 (Asia/Bangkok) | 1.1 | Claude Code | Added deadlines and the pitch materials section (final Lao deck + PDF, clickable prototype, speaker script, `00_CONTEXT.md`). Claude Code is now the sole author. |
| 2026-10-12 (Asia/Bangkok) | 1.2 | Claude Code | Described prototype v2.0 features. |
