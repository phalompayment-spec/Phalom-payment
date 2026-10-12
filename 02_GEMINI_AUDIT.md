# Sabaidee Merchant — Gemini AntiGravity Audit

**Audited document:** [`01_CODEX_ARCH.md`](01_CODEX_ARCH.md) v0.1 (Codex, 2026-10-12 00:03 +07:00)
**Companion reviewed:** [`exports/system_flowchart.html`](exports/system_flowchart.html), [`output/html/sabaidee-merchant-brief.html`](output/html/sabaidee-merchant-brief.html), `IBC.pdf` (competition pitch-deck template)
**Audit output:** this file + [`exports/pitch_deck_slide.html`](exports/pitch_deck_slide.html)
**Status:** Idea-stage competition audit. Nothing here is legal advice, a supplier quote, or a pilot result. `00_CONTEXT.md` was still absent when this audit was written; no owner decisions were assumed beyond those recorded in `01_CODEX_ARCH.md`.

**Confidence legend** used for external facts: **H** = primary/official source; **M** = reputable secondary source, original not re-read in this audit; **A** = assumption for modelling only.

---

## 0. Executive verdict

Codex's blueprint holds up well on financial correctness. It keeps acceptance, credit and refund states separate, never treats screenshots as proof, uses idempotent intents, and keeps licensed partners in charge of funds and FX. I endorse its state model and evidence rules **without change** (see §7).

The audit found **four gaps that would weaken the pitch or the pilot**:

| # | Gap | Severity | Where |
|---|---|---|---|
| 1 | **Revenue from merchant fees alone does not cover costs.** On Codex's own assumptions, a street-food stall earns the startup about **3,000 LAK per month**, while serving it costs about **95,000 LAK per month**. | Critical | §5, Codex §9 |
| 2 | **The UI is built around the system's states, not the vendor's decision.** Two success announcements (payment, then bank credit) and a new QR for every sale add mental load and phone handling at a busy street-food stall. | High | §2, Codex F02/F05/F06 |
| 3 | **Fraud cases common at local markets are missing:** QR stickers swapped or covered, fake payment sounds, too many or too few zeros typed (LAK amounts are long), and paying the stall next door. | High | §4, Codex §10 |
| 4 | **The startup's regulatory route needs a recommended default.** Laos was put on the FATF grey list in Feb 2025, and BOL rules on payment services and foreign currency have tightened. Partner due-diligence on the startup will be strict. | High | §3, Codex D01/D02 |

None of these require changing Codex's backend state machine. Gaps 2 and 3 are changes to what the vendor sees and does. Gap 1 changes the business model. Gap 4 changes the go-to-market order.

---

## 1. Finding index

Disposition key: **Endorse** = agree with Codex as written. **Amend** = keep Codex's intent, change the spec. **Add** = new requirement. **Reject-risk** = a tempting shortcut the team must not take.

| ID | Area | Sev. | Codex ref | Finding (short) | Proposed disposition |
|---|---|---|---|---|---|
| G-UX-01 | UX | Critical | F05, F06, §6.2 | Show one "safe to hand over goods" decision instead of two success states | Amend (presentation layer only) |
| G-UX-02 | UX | High | F02, §5.3 | Make the static QR stand a primary "Quick mode", not just a fallback | Amend |
| G-UX-03 | UX | High | F02, F04 | Prevent wrong zero counts and denomination mistakes | Add |
| G-UX-04 | UX | High | F06, F10 | Lao audio: use pre-recorded native-speaker numbers, a merchant chime, and an anti-spoof code | Amend |
| G-UX-05 | UX | High | F07 | Low-end Android phones, shared phones, OEM battery killers | Add |
| G-UX-06 | UX | Medium | F03, §5.1 | Onboarding is agent-assisted in practice; tier for informal merchants | Amend |
| G-UX-07 | UX | Medium | F04 | Show the fee card at price entry plus a daily summary, not as a hurdle on every sale | Amend |
| G-UX-08 | UX | Medium | F09, §5.4 | Refunds: owner-only, digital-only, plain-language timing | Amend |
| G-UX-09 | UX | Medium | §8 GTM | Multilingual tourist signage limited to certified apps | Add |
| G-UX-10 | UX | Medium | All UI | Lao-first wording; remove English jargon from merchant screens | Add |
| G-REG-01 | Regulatory | Critical | D01, D02, §2.2 | Recommended route: outsourced technology provider to one bank first | Amend (adds default path) |
| G-REG-02 | Regulatory | High | §2.2, F04 | Kip-only pricing extends to signage, receipts and merchant UI | Endorse + extend |
| G-REG-03 | Regulatory | High | D04, §11 | FATF grey listing raises KYB/monitoring expectations | Add |
| G-REG-04 | Regulatory | High | §2.2 | BOL action against personal or foreign merchant QR codes | Add (compliance as a USP) |
| G-REG-05 | Regulatory | High | D08, §9.3 | Accelerated payout may count as credit; keep it out of the pitch | Endorse + tighten wording |
| G-REG-06 | Regulatory | Medium | F11 | Market Passport rewards must not become stored value | Add |
| G-REG-07 | Regulatory | Medium | D04, D10 | Consent, data minimisation, breach notification | Endorse + extend |
| G-REG-08 | Regulatory | Medium | §8 GTM | Fear of digital records slowing adoption | Add (adoption risk) |
| G-EC-01…22 | Edge cases | Mixed | §10 | 22 cases missing from Codex's failure matrix | Add (see §4) |
| G-FIN-01 | Financial | Critical | §9.2 | Merchant-fee-only model loses money per merchant | Amend business model |
| G-FIN-02 | Financial | High | §9.1 | Recommended hybrid that relies mainly on business customers (banks, market operators) | Add |
| G-FIN-03 | Financial | Medium | §9.2 | Tourism seasonality; flat fees reduce exposure | Add |
| G-FIN-04 | Financial | Medium | §4.1 | Effective-rate benchmark for small tickets (pitch evidence) | Add |
| G-RJ-01 | Reject-risk | High | D06 | Do not read bank-app push notifications as a shortcut "credit feed" | Reject-risk |
| G-RJ-02 | Reject-risk | High | §9.1 | Do not add a tourist-side convenience fee or startup FX markup | Reject-risk |

---

## 2. UX critique — micro-merchant tech literacy

### 2.1 Persona assumptions (to validate in interviews)

| Attribute | Working assumption for a Luang Prabang / Vientiane night-market vendor | Design consequence |
|---|---|---|
| Device | Low/mid-range Android, often shared with family; prepaid data | Light app; works on weak 3G/4G; warns when data runs out |
| Existing habit | Already shows a bank merchant QR sticker (e.g., BCEL OnePay) and checks the bank app's notification | New flow must take **no more steps** than "point at sticker → hear notification" |
| Reading | Comfortable with Lao numerals and short words; English payment jargon unfamiliar | Rely on icons, colour, audio and short Lao phrases |
| Environment | Loud, busy, both hands occupied, phone often in a pocket or apron | Audio and colour must work without looking closely; soundbox matters more than P1 suggests |
| Trust trigger | "I heard it / I saw the money" | Must beat screenshot and fake-sound fraud without adding a manual check |

These are hypotheses. Codex correctly treats merchant distrust and difficult UX as unproven (§4.1). Before the pilot, test them with **8–12 vendor interviews plus 5 observed rush-hour sessions**.

### 2.2 Findings

**G-UX-01 — Show one decision ("safe to hand over goods"), not two success states (Critical).**
Codex F05/F06 show *payment confirmed* and *bank credit* as separate visible states, each with its own audio phrase. That is correct in the backend and too much for the vendor. During a sale the vendor makes one decision: *can I hand over the goods?* Two "success" phrases teach vendors to ignore one of them, or to distrust both.
*Recommendation:* the sale screen shows a three-colour traffic light. The bank-credit state moves to a second layer (daily summary and transaction detail).

| Light | Lao label (draft, needs native proofreading) | Backend condition (unchanged Codex states) | Audio |
|---|---|---|---|
| 🟢 Green | ມອບເຄື່ອງໄດ້ | `PROVIDER_CONFIRMED`, and only where the route's acceptance semantics allow handover (Codex §6.2 row 1) | One live phrase: amount + verification code |
| 🟡 Amber | ລໍຖ້າ | `AWAITING_CUSTOMER`, `PENDING`, unknown outcome, device `DISCONNECTED`/`SYNCING` | None (optional soft tick) |
| 🔴 Red | ຢ່າເພີ່ງມອບເຄື່ອງ | `FAILED`, `EXPIRED`, amount mismatch, quarantined evidence | Distinct low tone, no amount |

`CREDITED` is announced **only** in the end-of-day summary (e.g., "ມື້ນີ້ ເງິນເຂົ້າບັນຊີແລ້ວ …ກີບ") or by opt-in. `EXCEPTION` creates a support task, not a live alert. *Acceptance test:* in usability trials, at least 90% of vendors make the correct handover decision on the first try across the six Codex scenarios.

**G-UX-02 — Make the static QR stand a primary "Quick mode" (High).**
Codex treats the order-specific dynamic QR (F02) as primary and the printed static QR as a fallback (§5.3). For a 15,000–40,000 LAK noodle sale, unlocking the phone, typing the price and showing a QR every time adds friction. Vendors already avoid this with today's static stickers.
*Recommendation:* two first-class modes.
- **Quick mode (default for street food):** a printed, tamper-evident static QR stand. The tourist types the LAK amount in their own app. The vendor app listens for verified incoming payments and announces "received X kip" with a code. The handover decision uses *received amount vs. spoken price*, not order matching. Codex's rule that unmatched static receipts stay unmatched for **bookkeeping** stays in force. Two meanings must be kept apart: *received* (handover) and *matched to an order* (accounting).
- **Order mode (default for souvenir / higher tickets):** Codex's dynamic QR with a quote, as written.
*Dependency:* the partner must provide authenticated per-payment events with the amount for static QR (adds a line to D06).

**G-UX-03 — Prevent wrong zero counts and denomination mistakes (High).**
LAK prices are long (50,000; 150,000). Typing one zero too many or too few, either by the vendor (Order mode) or by the tourist in their own app (Quick mode), is likely to be the most frequent error. Thai or Vietnamese tourists may also think in THB/VND.
*Recommendation:* a keypad with a `000` key and a large grouped display (`50,000`). Spoken read-back of the price before the QR is shown. A warning when the amount is outside the merchant's usual band (e.g., >5× median ticket). In Quick mode, if the received amount is lower than the expected price, the status is 🟡 and the app shows the shortfall ("ຍັງຂາດ 45,000 ກີບ").

**G-UX-04 — Lao audio: native-speaker number segments, a merchant chime, an anti-spoof code (High).**
Generic Lao TTS reads large numbers badly. A market is loud. A scammer can play a recorded "payment received" sound from their own phone (EC-02).
*Recommendation:* (a) build announcements from pre-recorded native-speaker segments (digits, ພັນ, ແສນ, ລ້ານ, ກີບ). (b) Each merchant picks one of ~8 short chimes, so a fake generic sound is noticeable. (c) Every live phrase ends with a 2-digit code that is also shown large on the green screen ("…ລະຫັດ 47"). (d) Before each shift, the app checks volume and mute state. (e) Move the soundbox (F10) from "optional P1" to "**pilot experiment arm**", because a phone in a pocket is the normal case.

**G-UX-05 — Low-end Android phones, shared phones, OEM battery killers (High).**
Popular low-cost Android brands aggressively kill background apps, so push notifications are missed without warning and the live audio never plays.
*Recommendation:* an onboarding step that walks the vendor through battery-optimisation exemptions per OEM. A visible "listening" heartbeat on screen. Foreground polling while the sell screen is open. A **cashier mode** (sell and view only), separate from the **owner mode** (refunds, payout account, staff), so a shared phone does not expose refunds. Target a small install size and low data use per transaction (to be measured, not promised).

**G-UX-06 — Onboarding is agent-assisted in practice; tier for informal merchants (Medium).**
The 3-minute self-serve target (F03) is fine as a usability target. In practice, onboarding will happen at a market help desk with a field agent or bank officer. Many stalls are informal, and the account holder is not always the person at the stall.
*Recommendation:* an explicit **agent-assisted mode**. The agent guides; the merchant enters any credentials on their own device. Codex's "never collect PIN/OTP" rule is kept. Add document photo capture, Lao voice prompts and a progress bar. Ask the partner (D04) whether a lower-limit **individual micro-merchant tier** exists, so stalls without a business registration are not excluded.

**G-UX-07 — Fee card at price entry plus a daily summary (Medium).**
Showing fee and net on every sale (F04) is honest. It can also slow the sale and invite haggling. *Recommendation:* show net LAK in small text under the price while typing. Show the full fee breakdown in the daily summary and on tap. Keep Codex's quote versioning unchanged.

**G-UX-08 — Refunds: owner-only, digital-only, plain timing (Medium).**
Tourists leave town, so cross-border refunds go back to a foreign app on that bank's timeline. *Recommendation:* refunds only in owner mode. No cash refunds for digital payments (a reconciliation hole and an AML red flag; see EC-05). Show a plain Lao line: "ເງິນຈະຄືນເຂົ້າແອັບຂອງລູກຄ້າ; ເວລາຂຶ້ນກັບທະນາຄານຂອງລູກຄ້າ".

**G-UX-09 — Multilingual tourist signage, certified apps only (Medium).**
The stand should say "Scan with your bank app" in English, Thai, Vietnamese and Chinese. It should list app or country marks **only for routes certified under D03**, plus a stall name/number and the merchant name the payer must see in their app.

**G-UX-10 — Lao-first wording, no English jargon (Medium).**
The current companion HTML mixes in English terms ("payout", "pending", "credit"). That is fine for the team, but the merchant UI should use a Lao glossary agreed with the partner's own Lao terms, so vendors see the same words in our app and the bank's app.

---

## 3. Regulatory risk assessment — Bank of Lao PDR, LAPNet

### 3.1 Landscape (facts the design depends on)

| Item | What it means for Sabaidee Merchant | Conf. |
|---|---|---|
| Law on Payment System (amended), No. 45/NA, 2023 [S7] | Payment services need BOL authorisation; a partner's licence does not cover the startup | H (unofficial translation) |
| BOL Notice No. 05, 4 Jan 2024 [S6] | Cited by Codex; content not re-read in this audit | — |
| BOL Decision No. 511/BOL on the payment service system (reported dated 19 Jun 2025) [G3] | Secondary sources report minimum registered capital tiers for cross-border services (e.g., ~1 billion LAK for cross-border e-money transfer / foreign payment instrument services; 20 billion LAK for international card issuance), and recognition of **outsourcing service providers** to PSPs with BCP/IT-security duties | M — verify original |
| BOL Decision No. 11/BOL on foreign currency use (reported effective 3 Jan 2025) [G4] | LAK is the primary currency for pricing; locally produced goods/services priced and paid **solely in LAK** | M — verify original |
| "In Laos, use only the Kip" policy; BOL actions against personal / foreign merchant QR collection [G5] | Merchants must collect through licensed channels; a compliance gain for an approved product | M |
| FATF grey list, Feb 2025 [G1] | Partners and correspondent banks apply stricter, risk-based checks to cross-border flows and new intermediaries | H |
| Electronic Data Protection Law No. 25/NA, 2017; BOL consumer-protection decree for financial services (2020) [G6] | Consent for data use; breach notification duties at the financial-institution level | M |
| LAPNet cross-border QR: Thailand (live 3 Apr 2024) [S5]; Vietnam (reported Jan 2025), Cambodia, UnionPay (China) [G2] | The first corridor should be Thai PromptPay-bank apps → LAOQR. Other corridors come later, after D03 certification | H for TH; M others |

### 3.2 Risk register

| ID | Risk | Likelihood | Impact | Mitigation / spec change |
|---|---|---|---|---|
| G-REG-01 | Startup activity is classified as an unlicensed payment service | Medium | Critical | Adopt **Path A** below as the default. Write down exactly what the startup never does: hold funds, perform FX, connect directly to LAPNet, store payer credentials, run a balance |
| G-REG-02 | Foreign-currency pricing breach through UI, signage or receipts | Medium | High | Merchant UI, stands and receipts show **LAK only**. Conversion stays inside the payer's app. No THB/USD/CNY "reference price" on merchant materials unless counsel confirms |
| G-REG-03 | Partner refuses or delays because of AML/CFT exposure (grey-list context) | High | High | Build monitoring hooks for the partner: ticket-size anomalies, velocity, unusual night-time activity, mismatch with merchant category, many payments from one payer. Export data for the bank's suspicious-transaction process. The startup supports reporting; the licensed institution files (verify) |
| G-REG-04 | Vendors keep personal or foreign QR codes next to ours (unlicensed collection) | High | Medium | Onboarding checklist and field-agent script to retire non-compliant codes. Pitch this as a **compliance-migration** benefit for BOL and banks |
| G-REG-05 | "Instant payout" read as a credit or advance product | Medium | High | Endorse Codex D08/§9.3. In the pitch, say "**LAK to the merchant's bank account, on the timing the partner route supports**", never "instant", until contract + evidence exist |
| G-REG-06 | Market Passport stamps or rewards treated as e-money / stored value | Low | Medium | Rewards are non-cash, non-transferable, have no balance, and are funded as a merchant/market promotion. Reverse on refund (Codex F11) |
| G-REG-07 | Consent / data-sharing failure on bank-data reuse | Medium | Medium | Endorse D04/D10. Add: versioned consent records, keep only the payer data needed for receipts and disputes, and a breach runbook aligned with the partner's notification duties |
| G-REG-08 | Vendors avoid digital records (tax or visibility concerns), so uptake is low | Medium | Medium | No messaging that implies hiding income. Position the product as bookkeeping and tourist-access value. Coordinate messaging with the bank and market operator |

### 3.3 Regulatory path options (for G-REG-01)

| Path | Description | Feasibility in 0–12 months | Verdict |
|---|---|---|---|
| **A. Outsourced technology provider to one bank** | Bank owns the merchant relationship, licence, QR issuance and funds. The startup supplies the merchant app/module (co-branded or bank-branded) under an outsourcing agreement | High, if the bank wants it | **Recommended default** |
| B. Technology partner of a licensed PSP (e.g., a cross-border acquirer) | Same as A, but the PSP sits between the startup and the banks; more corridors, one more fee layer | Medium | Phase 2 option |
| C. Own BOL payment-service licence | Startup applies for a licence itself | Low (capital tiers reported ≥1 bn LAK, compliance staff, time) | Not before product-market evidence |

LAPNet connects **member institutions**, not apps. Under every path, the startup reaches LAPNet only through its partner. This matches Codex §3. **Endorse.**

---

## 4. Edge-case analysis (additions to Codex §10)

Codex §10 covers the integration failure modes well (timeouts, duplicates, out-of-order events, partial credit, refund timeouts). The cases below are **physical-world, fraud and device** cases it does not list.

| ID | Edge case | Required behavior | Owner / dependency |
|---|---|---|---|
| G-EC-01 | **QR sticker swap or overlay** (fraudster pastes their own QR on the stand) | Tamper-evident stand. Stand shows the merchant name the payer must see. Merchant app has a weekly "scan your own stand" self-check that verifies the payload belongs to this merchant | Partner QR payload format |
| G-EC-02 | **Fake payment sound** played from a scammer's phone | Merchant-specific chime + spoken 2-digit code that matches the green screen. Training: "trust only your own green screen" | G-UX-04 |
| G-EC-03 | Edited or old screenshot shown as proof | Endorse Codex §5.2/§6.1: never authoritative | — |
| G-EC-04 | Underpayment in Quick mode (5,000 typed instead of 50,000) | 🟡 with shortfall amount. Second payment can top up. Both are linked to the sale in bookkeeping | Partner per-payment events |
| G-EC-05 | Overpayment; tourist asks for **cash change** | Do not give cash change for a digital payment. Use a digital partial refund (owner) or a new correct payment followed by a refund. Log the event as an AML signal | F09 |
| G-EC-06 | One order paid by several tourists, or part cash / part QR | Order supports multiple payments and a "cash portion" field. State shows "partially paid" until complete | New order sub-state (UI) |
| G-EC-07 | Two tourists pay the same static QR within seconds | Each announcement has its own amount + code. Sell screen shows the last 3 receipts with time | G-UX-02 |
| G-EC-08 | Tourist pays the **neighbouring stall** in a dense market | Stand shows stall name, number and a small photo. Receipt token lets both merchants and support trace it. No automatic transfer between merchants | Support workflow |
| G-EC-09 | Tourist's app says "success" but merchant sees 🟡 | Stays 🟡. Give the tourist an instruction card (EN/TH/VI/ZH) with the receipt/reference. Do not take a second payment while the first is unresolved (endorse Codex §10 row 4) | Partner query |
| G-EC-10 | OEM battery optimisation kills push; no live audio | Battery-exemption onboarding; "listening" heartbeat; foreground polling on the sell screen | G-UX-05 |
| G-EC-11 | Phone muted, low volume, or audio routed to a Bluetooth headset | Pre-shift check plus a persistent banner when the output is unsuitable | App |
| G-EC-12 | Prepaid data exhausted mid-shift | Device `DISCONNECTED` shown as 🟡. Low-data warning. Static stand still accepts payments; history fills in after reconnect | Codex F07 |
| G-EC-13 | Phone battery dies or power cut | Static stand keeps working while payers are online. Events recovered on restart with **no** live audio for old events (endorse §6.2) | — |
| G-EC-14 | New phone / SIM swap / account takeover attempt | Device re-binding needs bank-verified step-up. Payout-account changes need re-verification (endorse §5.1 step 7). Owner is notified on a second channel | Partner |
| G-EC-15 | Cashier tries to abuse refunds | Cashier mode cannot refund. Refunds only go back to the original funding source (endorse §5.4) | G-UX-05 |
| G-EC-16 | Merchant hits a tier, daily or cross-border limit mid-sale | Before showing the QR, check remaining limit and warn on the sell screen | Partner limits (D07) |
| G-EC-17 | Public holidays (e.g., Pi Mai Lao, Boun That Luang) delay payout | Payout timing shown with a holiday-aware calendar from partner data. Never a fixed "T+0" promise | D07 |
| G-EC-18 | Dispute or chargeback after the tourist has left the country | Separate "disputed" record. Loss allocation per D09. Original credit history kept (endorse §6.1) | D09 |
| G-EC-19 | Merchant restricted for AML review while payouts are pending | 🔴 for new sales. Read-only access to history and a support path (extends Codex §10 last row) | Partner compliance |
| G-EC-20 | Device clock wrong; stale-audio rule misfires | All freshness decisions use server time and event time, not the device clock | Backend |
| G-EC-21 | Tourist's app shows a converted amount the tourist disputes ("I paid 80 baht, not 75") | Merchant side shows only LAK received. FX questions go to the tourist's bank. Receipt shows the LAK amount and reference | G-REG-02 |
| G-EC-22 | Seasonal staff turnover; untrained relative runs the stall | Cashier invite through a QR code from the owner. 60-second in-app Lao tutorial with audio. Field-agent refresher before peak season | GTM |

### Rejected shortcuts

- **G-RJ-01 — Reading bank-app push notifications (Android notification-listener) as a "credit feed".** It looks like a quick MVP that avoids needing D06. It is fragile, may breach bank terms and data-protection expectations, can be spoofed, and would fail partner due-diligence. **Do not prototype it, even for a demo.**
- **G-RJ-02 — A tourist-side convenience fee or startup FX markup.** It would undercut the "cheaper than incumbents" story, and FX can only be done by authorised institutions (endorse Codex §9.1: no FX markup in the base case).

---

## 5. Financial fee models

All figures are **illustrative assumptions (A)**, computed with integer LAK arithmetic. FX for readability: 1 USD ≈ 21,500 LAK (A; check on pitch day). Reproducible script: `scratch/fee_models.py` in the Gemini artifact directory.

### 5.1 Stress test of Codex §9.2 (MDR-only)

Codex per-transaction contribution = ticket × (0.5% fee − 0.3% partner − 0.08% ops/risk) − 30 LAK fixed.

| Ticket (LAK) | Contribution, partner 0.3% | Contribution, partner 0.6% |
|---:|---:|---:|
| 20,000 | −6 | −66 |
| 25,000 | **0 (break-even)** | −75 |
| 40,000 | 18 | −102 |
| 50,000 | 30 | −120 |
| 150,000 | 150 | −300 |

Per merchant per month (pilot hypothesis: street food 40,000 LAK × 6 cross-border sales/day, souvenir 150,000 LAK × 4/day, 28 days). Cost to serve = one field agent (4.5 M LAK/month) per 50 merchants + 5,000 LAK infrastructure = **95,000 LAK per merchant per month**.

| Segment | Monthly GMV | Startup contribution (MDR-only) | Net after cost to serve | Transactions needed to break even |
|---|---:|---:|---:|---:|
| Street food | 6,720,000 | 3,024 | **−91,976** | 5,278 / month |
| Souvenir | 16,800,000 | 16,800 | **−78,200** | 633 / month |

**G-FIN-01 conclusion:** a percentage merchant fee cannot pay for field support on small cross-border tickets. Raising the fee does not fix it: the domestic reference price is likely **zero**. Basic over-the-counter LAOQR/OnePay acceptance is commonly described as free or low-cost for small merchants [G7, M — verify]. A vendor will compare any cross-border fee with "free".

### 5.2 Small-ticket benchmark (pitch evidence, G-FIN-04)

LOCA's published charge of 3% + 5,000 LAK [S1], shown as an effective rate:

| Ticket (LAK) | Charge | Effective rate |
|---:|---:|---:|
| 20,000 | 5,600 | 28.0% |
| 40,000 | 6,200 | **15.5%** |
| 50,000 | 6,500 | 13.0% |
| 150,000 | 9,500 | 6.3% |
| 500,000 | 20,000 | 4.0% |

The fixed component dominates at street-food ticket sizes, and that is the opening for this product. **Caveat for the pitch:** confirm who pays this charge (payer or merchant) and what service it covers before comparing directly (Codex §9.2 already warns about this).

### 5.3 Models compared

| Model | Who pays | Pros | Cons | Verdict |
|---|---|---|---|---|
| A. MDR-only (Codex base) | Merchant, per transaction | Simple; scales with use | Loses money per merchant (§5.1); competes with "free"; moves with tourist seasons | Keep only as a thin component |
| B. Merchant subscription | Merchant, monthly | Predictable | Vendors resist fixed fees; churn in low season | Only for the optional **Pro** tier |
| **C. Hybrid weighted to business customers** | Bank partner + market operator + Pro + thin margin | Revenue doesn't depend on ticket size or season; matches who gains (bank: deposits, FX volume, merchant acquisition; market: tourist spend) | Needs B2B sales; bank appetite unproven | **Recommended** |
| D. Tourist convenience fee | Tourist | — | Kills the value proposition; FX/fee rules | **Rejected** (G-RJ-02) |

### 5.4 Recommended hybrid (G-FIN-02), monthly

Inputs (all A): thin service margin 0.10% of GMV minus 30 LAK per transaction. Bank pays **25,000 LAK per active merchant per month**. Pro tier 30,000 LAK/month at 20% uptake. Market-operator package **1.5 M LAK per market** (≈50 merchants). Cost to serve falls from 1 agent per 50 merchants (pilot) to 1 per 150 after the pilot. **No FX revenue share** assumed.

| Merchants | Monthly GMV (LAK) | Revenue | Cost to serve | Contribution before central costs |
|---:|---:|---:|---:|---:|
| 50 (pilot) | 537.6 M | 3.37 M | 4.75 M | **−1.38 M** (≈ −$64) |
| 200 | 2.15 B | 13.48 M | 7.00 M | **+6.48 M** (≈ $301) |
| 500 | 5.38 B | 33.69 M | 17.50 M | **+16.19 M** (≈ $753) |
| 2,000 | 21.5 B | 134.77 M | 70.00 M | **+64.77 M** (≈ $3,012) |

Revenue mix at 500 merchants: market operator 45%, bank fee 37%, margin 9%, Pro 9%. **Takeaway:** the hybrid is positive per merchant from about 200 merchants. Covering a full team still needs either **thousands of merchants** or **expansion beyond tourist markets** (domestic micro-merchants on the same app). The team should state this openly in the pitch, rather than present a cross-border fee as the business on its own.

### 5.5 Seasonality and sensitivity (G-FIN-03)

- Tourist volume is seasonal (higher in the cool dry season, lower in the rainy season). In model C, only the margin line (≈9%) depends on volume. A **50% low-season drop cuts total revenue by only ≈5%**. Under model A it cuts revenue by 50%.
- The largest sensitivities are the **bank fee per active merchant** and **market-package uptake**. Both are unvalidated hypotheses. Ask about them in the first BCEL conversation (add to D05).
- If partner cost exceeds the margin (Codex's 0.6% case), the margin line turns negative. Codex's §10 rule "reprice/disable unviable offer before sale" covers this. **Endorse.**

### 5.6 Illustrative 6-month pilot budget (for the IBC "Estimated Budget" slide)

| Line | LAK |
|---|---:|
| Product & engineering (2 developers × 6 M × 6 months) | 72,000,000 |
| Field onboarding agents (2 × 4.5 M × 6) | 54,000,000 |
| Legal / regulatory counsel | 40,000,000 |
| Lao audio recording + usability tests | 12,000,000 |
| Cloud, SMS, monitoring (1.5 M × 6) | 9,000,000 |
| Optional soundbox trial arm (10 × 450,000) | 4,500,000 |
| Tamper-evident QR stands (60 × 60,000) | 3,600,000 |
| **Subtotal** | **195,100,000** |
| Contingency 15% | 29,265,000 |
| **Total** | **224,365,000 (≈ $10.4k)** |

These are assumptions, not quotes. Salary levels and counsel fees must be checked locally.

### 5.7 Pitch-safe financial wording

- ✅ "Our fees are clear before every sale. For small tickets we aim to be far below fixed-fee alternatives, subject to partner pricing."
- ✅ "Revenue comes mainly from banks and market operators, who gain from digital tourist spending, so vendors don't carry it."
- ❌ "Cheapest in Laos", "instant money", "0% fees" (no supplier quote or contract yet).

---

## 6. Responses to Codex §12 pitch-claim table

| Pitch claim | Codex defensible wording | Gemini position |
|---|---|---|
| No tourist download | Designed for existing supported wallets/bank apps | **Endorse.** Lead with "Thai bank apps via the Thai–Lao QR link" as the first named corridor [S5] |
| Three-minute onboarding | Target for submitting a complete application | **Endorse**, plus "with on-site help at the market" (G-UX-06) |
| Low fees | Corridor-specific target | **Amend:** use the §5.2 effective-rate framing + "vendors don't carry our revenue" (G-FIN-02) |
| Instant LAK | Proposed for eligible routes | **Amend:** drop "instant"; say "LAK straight to your own bank account" (G-REG-05) |
| Audio confirmation | Proposed verified Lao alerts | **Amend:** "Lao voice + green screen that a fake sound can't copy" (G-UX-04) |
| Better than both competitors | Focused hypothesis | **Endorse** the caution; frame as "built for the small-ticket vendor" |

---

## 7. Consensus proposals (input to `03_FINAL_SPEC.md`)

**Endorsed unchanged → recorded as consensus in `03_FINAL_SPEC.md`:** Codex §2.2 scope boundaries; §3 single partner + single corridor + adapter; §5.2 payment flow steps 1–9; §6 independent state dimensions and §6.1 transition rules; §6.2 dedupe/stale-audio rules; §7.1 money representation (integer minor units, separate requested/fee/net/credited); §7.3 event ingestion; §8 dependency list D01–D10; §10 existing rows; §11 controls; "no screenshot as proof"; "no FX markup in base case".

**Pending Codex response (not yet consensus):** G-UX-01, G-UX-02, G-UX-03, G-UX-04, G-UX-05, G-UX-06, G-UX-07, G-UX-08, G-REG-01 (Path A default), G-REG-03 monitoring hooks, G-EC-01…22 additions, G-FIN-01/02 business-model change, new dependency lines (D06 static-QR events; D05 bank fee appetite).

---

## 8. Open questions for Codex / team owner

1. **Q1 (to Codex):** Can the traffic-light presentation (G-UX-01) map cleanly onto the existing states without a new state? Gemini's view: yes. 🟢/🟡/🔴 is a derived view model.
2. **Q2 (to Codex):** For Quick mode (G-UX-02), should "received but unmatched" be a separate bookkeeping state, or a flag on `ProviderEvent`?
3. **Q3 (to owner):** Is the team prepared to pitch as a **bank-partnered technology provider** (Path A) rather than a standalone payment company?
4. **Q4 (to owner):** Which market is the pilot? Luang Prabang night market favours souvenir tickets; Vientiane riverside favours street food. This changes the default mode and the fee mix.
5. **Q5 (to owner):** Team name and member profiles for the title slide (placeholders used in the deck).

---

## 9. Sources

Carried forward from Codex: [S1] LOCA PAY · [S2] NewPay merchant · [S3] NewPay FAQ · [S4] LAPNet · [S5] BOT–BOL Thai–Lao QR linkage, 3 Apr 2024 · [S6] BOL Notice No. 05 · [S7] Payment System Law (amended), unofficial translation. URLs in `01_CODEX_ARCH.md` §13.

New in this audit (web-search summaries; originals to be re-read before formal use):
- [G1] FATF — Jurisdictions under Increased Monitoring, Feb 2025 (Lao PDR added). https://www.fatf-gafi.org/en/countries/black-and-grey-lists.html — H
- [G2] Regional reporting on LAPNet cross-border QR with Vietnam (Jan 2025), Cambodia, UnionPay. https://www.lapnet.com.la/ — M
- [G3] Legal-commentary summaries of BOL Decision No. 511/BOL on the Payment Service System (reported 19 Jun 2025), incl. capital tiers and outsourcing-provider duties (e.g., ilawasia.com) — M
- [G4] Legal-commentary summaries of BOL Decision No. 11/BOL on foreign-currency use (reported effective 3 Jan 2025) (e.g., vdb-loi.com, tilleke.com) — M
- [G5] Reporting on BOL "use only the Kip" policy and notices against unlicensed QR collection (e.g., kpl.gov.la) — M
- [G6] Electronic Data Protection Law No. 25/NA (2017); BOL Decree on Consumer Protection for Financial Services (2020), via DLA Piper Data Protection summaries — M
- [G7] BCEL OnePay merchant QR fee descriptions (public help content, check the BCEL One app / hotline 1555) — M

---

# Version Log

| Timestamp | Version | Author | Change |
|---|---|---|---|
| 2026-10-12 00:16 +07:00 (Asia/Bangkok) | 0.1 | Gemini AntiGravity | First audit of `01_CODEX_ARCH.md` v0.1. 10 UX, 8 regulatory, 22 edge-case, 4 financial and 2 reject-risk findings mapped to Codex IDs. Fee-model stress test + recommended hybrid model, pilot budget. Built `exports/pitch_deck_slide.html` on the IBC template structure. Recorded endorsed-unchanged items as consensus in `03_FINAL_SPEC.md`; all amendments pending Codex response. |
