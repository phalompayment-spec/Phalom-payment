# Sabaidee Merchant — Final Spec (Consensus Ledger)

**Rule:** This file holds only agreed items. Until 2026-10-12 an item needed both Codex and Gemini AntiGravity to accept it. From 2026-10-12 the owner's decisions in [`00_CONTEXT.md`](00_CONTEXT.md) settle open items, and Claude Code maintains this ledger alone (see §4).
**Status:** Idea-stage competition concept. Nothing here implies a partner agreement, regulatory approval, supplier quote or pilot result.

## 1. Consensus baseline (Codex v0.1 proposals, endorsed unchanged by Gemini audit v0.1)

| # | Spec item | Source | Consensus basis |
|---|---|---|---|
| C01 | Scope boundaries: merchant-facing app only; tourists use an existing supported app; no tourist account/KYC in our app; partner review required for activation; licensed institutions execute funds/FX/credit; startup holds no customer balance; partner licence does not transfer to the startup | 01 §2.2 | 02 §7 |
| C02 | Start with one licensed acquiring partner, one corridor, modular backend + background workers, provider adapter | 01 §3 | 02 §3.3, §7 |
| C03 | Startup reaches LAPNet only through a member partner; no direct network connection | 01 §3, §8 | 02 §3.3 |
| C04 | Payment flow steps 1–9: idempotent order, versioned quote, single intent persisted before the QR is shown, verified and matched evidence, atomic state + outbox commit, separate credit evidence | 01 §5.2 | 02 §7 |
| C05 | Independent state dimensions (merchant, payment, bank credit, refund, device); `OFFLINE` is a device state, not a financial one | 01 §6 | 02 §7, G-UX-01 |
| C06 | Transition rules: no UI/support override can create confirmation; timeout = unknown, not failed; no backward moves from out-of-order events; partial credit = `EXCEPTION`; refunds never overwrite credit history | 01 §6.1 | 02 §7 |
| C07 | Customer screenshots or sounds are never proof of payment or credit | 01 §5.2, §6.1 | 02 G-EC-03 |
| C08 | Audio delivery is at-least-once with client dedupe; old or interrupted events are never announced as new | 01 §6.2 | 02 G-EC-13 |
| C09 | Money as integer minor units / exact decimals; requested, fee, expected net and credited amounts stored separately | 01 §7.1 | 02 §5 |
| C10 | Event ingestion sequence 1–8 (authenticate, durable receipt, dedupe, normalise/match, quarantine, atomic commit, retry, reconcile) | 01 §7.3 | 02 §7 |
| C11 | Partner dependency list D01–D10 must be resolved before claiming feasibility | 01 §8 | 02 §3 |
| C12 | No platform FX markup in the base case; any FX only by authorised institutions | 01 §9.1 | 02 G-RJ-02 |
| C13 | Accelerated / advance payout only via an authorised funder under contract; not promised by the startup | 01 §9.3, D08 | 02 G-REG-05 |
| C14 | Existing failure-matrix rows (01 §10) and security controls (01 §11.1) | 01 §10–11 | 02 §4 (additions pending) |
| C15 | Merchant pricing and receipt in LAK | 01 §2.2, F04 | 02 G-REG-02 (extension pending) |

## 2. Consensus pitch wording

| Claim | Agreed wording |
|---|---|
| No tourist download | "Designed for existing supported wallets / bank apps." |
| Onboarding | "Three-minute target for submitting a complete application; activation after partner review." |
| Comparison | "Focused on small market purchases" — no "better than all competitors" claim. |

Wording for fees, payout speed and audio is **pending** (see §3).

## 3. Former pending list (resolved in §4)

| Audit ID | Proposal (summary) | Affects |
|---|---|---|
| G-UX-01 | Traffic-light handover view (🟢/🟡/🔴) derived from existing states; bank credit moves to the daily summary | F05, F06, §6.2 |
| G-UX-02 | Static-QR "Quick mode" as a first-class mode; "received" (handover) separate from "matched" (bookkeeping) | F02, §5.3, D06 |
| G-UX-03…10 | Zero-error keypad, native-voice audio with code, cashier/owner modes, agent-assisted onboarding, fee-card placement, refund rules, signage, Lao glossary | F03–F10 |
| G-REG-01 | Default regulatory route: outsourced technology provider to one bank | D01, D02 |
| G-REG-02…08 | LAK-only signage/receipts, AML monitoring hooks, compliance-migration USP, non-monetary rewards, consent/breach runbook, adoption messaging | §2.2, F11, D04, D10 |
| G-EC-01…22 | Additional physical-world, fraud and device edge cases | §10 |
| G-FIN-01…04 | Replace merchant-fee-only revenue with a hybrid paid mainly by banks and market operators; seasonality; benchmark framing | §9 |
| Pitch | "Instant LAK" → "LAK straight to your own bank account"; "Low fees" → effective-rate framing | §12 |

## 4. Owner decisions (2026-10-12) — now part of the spec

| # | Spec item | Resolves | Source |
|---|---|---|---|
| C16 | Traffic-light sale screen (🟢 ມອບເຄື່ອງໄດ້ / 🟡 ລໍຖ້າ / 🔴 ຢ່າເພີ່ງມອບເຄື່ອງ) derived from existing states; bank credit shown in the daily summary, not as a live sale alert | G-UX-01 | 00 D-01 |
| C17 | Two first-class modes: Quick mode (static QR stand, default for street food) and Order mode (order QR with fee quote). "Received" (handover) is separate from "matched to an order" (bookkeeping); unmatched receipts are a flag on `ProviderEvent` | G-UX-02, Q2 | 00 D-02 |
| C18 | `000` keypad, Lao read-back, unusual-amount warning, shortfall/top-up, merchant chime + 2-digit code, cashier/owner modes, owner-only digital refunds to the original app, net LAK shown at price entry | G-UX-03…08 | 00 D-06 |
| C19 | Regulatory route: outsourced technology provider to one licensed bank (Path A); BCEL first to approach | G-REG-01, Q3 | 00 D-03 |
| C20 | Proposed pilot: Luang Prabang night market, 30–50 vendors, Thai bank apps via the Thai–Lao QR link | Q4 | 00 D-04 |
| C21 | Hybrid revenue mainly from banks and market operators; thin margin and Pro as supplements; no tourist fee, no FX markup | G-FIN-01/02, G-RJ-02 | 00 D-05 |
| C22 | Pitch wording: "ຮູ້ຜົນ ແລະ ມອບເຄື່ອງໄດ້ທັນທີ ເມື່ອ partner ຢືນຢັນ; ເງິນເຂົ້າບັນຊີກີບຕາມເວລາຂອງເສັ້ນທາງ". No "instant settlement", "cheapest" or "0%" | G-REG-05, §12 | 00 D-07 |
| C23 | WeChat Pay / Alipay presented as a later expansion through a licensed PSP (Path B), not in the pilot | Challenge wording | 00 D-08 |

Still open: team member names and contacts (Q5); detailed edge-case and compliance items (G-EC-01…22, G-REG-03/06/07/08) are accepted as direction and specified after the competition.

# Version Log

| Timestamp | Version | Author | Change |
|---|---|---|---|
| 2026-10-12 00:23 +07:00 (Asia/Bangkok) | 0.1 | Gemini AntiGravity | Created the ledger. Recorded C01–C15 (Codex v0.1 items endorsed unchanged in audit v0.1) and the agreed pitch wording. All Gemini amendments listed as pending Codex response. |
| 2026-10-12 (Asia/Bangkok) | 1.0 | Claude Code | Applied owner decisions from `00_CONTEXT.md`: added C16–C23 and moved the pending list to resolved. Claude Code now maintains this ledger alone. |
