# Phalom

Project files for Team ພັດລົມ (Phalom), Innovative Business Challenge – MSME, Challenge No. 10. **Slides are due 15 October 2026; the final pitch is 17 October 2026.**

## Pitch materials (start here)

- [`exports/Phalom-Pitch-Deck.pdf`](exports/Phalom-Pitch-Deck.pdf): final 13-slide deck in Lao, for submission. Generated from [`exports/pitch_deck_slide.html`](exports/pitch_deck_slide.html) (open in a browser to present; the PDF button saves a new PDF after edits).
- [`exports/phalom_prototype.html`](exports/phalom_prototype.html): clickable Phalom prototype (Mekong design, light theme by default). Open it in any browser; it works offline. Online copy: https://claude.ai/artifact/2miJ6xArT31gXvaqn1WvXF. It includes a presenter demo panel for bank results, offline mode, a fake-screenshot test, the market-operator view and the tourist sign. Source and build script: [`prototype/`](prototype/).
- [`blueprint_phalom_prototype.md`](blueprint_phalom_prototype.md): research-based list of every feature the prototype needs (P0–P2), competitor check and research plan.
- [`ui_design_brainstorm.md`](ui_design_brainstorm.md): UI research, seven design directions, logo ideas and the chosen design (D · Mekong, P-QR logo) with its colour tokens.
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
| 2026-10-12 (Asia/Bangkok) | 1.3 | Claude Code | Added the prototype blueprint; marked the earlier prototype as history. |
| 2026-10-12 (Asia/Bangkok) | 1.4 | Claude Code | Renamed project to Phalom; deleted the old prototype; added the UI design brainstorm; deck PDF renamed to Phalom-Pitch-Deck.pdf. |
| 2026-10-12 (Asia/Bangkok) | 1.5 | Claude Code | Added the new Mekong-design prototype (`exports/phalom_prototype.html`, source in `prototype/`); updated the design brainstorm entry. |
