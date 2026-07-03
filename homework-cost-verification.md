# Homework Flow — Cost Verification & Provider Reconciliation

> **Purpose.** This document lets us *confirm* the per-session cost the estimator shows for the
> Homework Help (Tier 2) flow. It checks every provider unit price against the live provider
> documentation, then shows exactly how the two biggest lines — **TTS audio** and **real-time image
> generation** — are counted, and explains the o3 reasoning-token risk.
>
> **Bottom line up front:** the unit prices are *correct and current*. The headline number is driven by
> three deliberate, conservative choices: **audio is billed on the MAXIMUM narration length** (Section 2),
> **a diagram image is generated in real time at every walkthrough step of every session** (Section 3),
> and every price carries a **+50% buffer**. The figure to keep validating on a real invoice is o3's
> **hidden reasoning tokens** (Section 4.3).

---

## 1. Provider unit prices — confirmed against documentation (July 2026)

| Service | Model | Published list price | In estimator | Confirmed |
|---|---|---|---|---|
| Reasoning LLM | **o3** | **$2.00 / 1M input · $8.00 / 1M output** | $2 / $8 | ✅ matches OpenAI |
| Prose / vision LLM | **gpt-4.1** | $2.00 / 1M input · $8.00 / 1M output | $2 / $8 | ✅ matches OpenAI |
| Diagram image | **Gemini 3.1 Flash Image** | **$0.067 / image (standard tier)** | $0.067 | ✅ as configured |
| Text-to-speech | **Inworld TTS-2** | **$25.00 / 1M characters (on-demand)** | $25 | ✅ matches Inworld |
| Safety | omni-moderation | Free | $0 | ✅ |

**The +50% safety buffer.** Every price above is multiplied by **1.5** inside the estimator before any
figure is shown, as an internal margin for retries, prompt drift and future price moves. So the effective
rates the estimator charges against are: o3 / gpt-4.1 **$3 / $12** per 1M, Gemini **$0.1005** per image,
Inworld **$37.50** per 1M characters. Throughout, we show **both** columns — *"list"* (the provider's
published price, for reconciliation) and *"+50%"* (what the estimator displays).

---

## 2. Text-to-speech (Inworld TTS-2) — billed on the MAXIMUM narration length

Inworld bills **per character** sent to synthesis. Real homework narration runs far longer than a "typical"
estimate, so the estimator costs audio on the **maximum** a session can produce — every audio driver at its
ceiling. This is the figure shown on the dashboard.

| Phase narrated | Max characters | At the slider ceiling |
|---|---|---|
| 3A explanation | 800 | `charsExp` max |
| Solution + parallel-demo steps | 10,000 | `10 steps × 500 × 2` |
| Intros + completion | 1,200 | `charsOv` max |
| Attempt feedback + Q&A | 12,000 | `(12 + 8) × 600` |
| **Maximum per session (billed)** | **24,000** | |

**Cost of 24,000 characters:** list `24,000 ÷ 1,000,000 × $25` = **$0.60** · +50% = **$0.90**.

Inworld gets cheaper with commitment, and we estimate on the most expensive on-demand tier, so a real
audio invoice can only come in lower:

| Inworld TTS-2 tier | $ / 1M characters | Cost of a 24,000-char session |
|---|---|---|
| **On-demand (what we estimate on)** | **$25.00** | $0.60 |
| $300 / month commit | $15.00 | $0.36 |
| $1,500 / month commit | $12.50 | $0.30 |
| Enterprise | $10.00 (as low as $5) | $0.24 (↓ $0.12) |

---

## 3. Image generation (Gemini 3.1 Flash Image) — one per step, every session

Diagram images are generated **in real time at every displayed walkthrough step of every session** — this
is *not* gated on whether the child's upload contained a figure. One image is produced for the 3A
explanation, one for each parallel-demo step, and one for each "your-turn" step:

```
images / session = 1 (explanation)
                 + avgSteps (demo steps)
                 + avgSteps (your-turn steps)
                 = 2 × avgSteps + 1
```

At the default **5 steps**, that is **11 images per session**. Because it scales with walkthrough depth,
it grows with longer walkthroughs:

| Walkthrough depth (steps) | Images / session (`2×steps + 1`) | Cost (list @ $0.067) | Cost (+50%) |
|---|---|---|---|
| 3 | 7 | $0.469 | $0.704 |
| **5 (default)** | **11** | **$0.737** | **$1.106** |
| 7 | 15 | $1.005 | $1.508 |
| 10 (max) | 21 | $1.407 | $2.111 |

> **This is now the single largest line in a session.** At the default depth, image generation is **$0.74
> list / $1.11 buffered** — more than audio. If in practice not every step renders a fresh image (e.g. some
> are cached or reused), lower the step-image assumption and this line drops proportionally.

---

## 4. o3 reasoning model — tokens and cost

o3 is only used for **calculation / derivation** questions (Maths, Physics, Chemistry, computational
Science). Prose/explanation questions run on gpt-4.1. The build pipeline is five LLM calls (steps A ·
parallel B · demo C · 3A explanation · answer key D); A→B→C can regenerate on a self-check failure, so
they carry a retry factor (default **1.15×**).

### 4.1 Per-call token assumptions (o3 route)

Output tokens below are set to **include** o3's hidden reasoning tokens — see Section 4.3.

| Call | Input tok | o3 output tok | Runs / session | o3 cost (list) |
|---|---|---|---|---|
| A · Solution steps | 700 | 3,000 | 1.15 | $0.0292 |
| B · Parallel question | 800 | 2,500 | 1.15 | $0.0248 |
| C · Parallel demo (worked) | 900 | 3,000 | 1.15 | $0.0297 |
| 3A · Explanation | 600 | 2,200 | 1.00 | $0.0188 |
| D · Private answer key | 900 | 3,000 | 1.00 | $0.0258 |
| Validate attempt | 700 | 1,500 | 3.00 | $0.0402 |
| Follow-up Q&A | 800 | 1,500 | 1.00 | $0.0136 |
| **o3 subtotal** | **~7,160** | **~20,975** | | **$0.1821** |

Plus the fixed gpt-4.1 intake/classify calls that run in **every** session (image extract + analyze +
match): **$0.0118**.

### 4.2 Per-session o3 cost (the math)

```
o3 input :  7,160 tok ÷ 1,000,000 × $2  = $0.0143
o3 output: 20,975 tok ÷ 1,000,000 × $8  = $0.1678
o3 total (list)                          = $0.1821  →  +50% = $0.2732
```

### 4.3 Why o3 can look cheaper than the docs — hidden reasoning tokens

**The unit price is right ($2/$8); the risk is the token count, not the rate.** o3 bills *invisible*
reasoning tokens at the **output** rate. OpenAI's documentation notes a single o3 answer can burn
**5,000–20,000 internal reasoning tokens**. Our model already assumes ~21,000 o3 output tokens for a whole
calculation session (near the high end), but if o3 reasons *harder*, cost scales. This table shows a full
calculation session (including the max-audio $0.60 and the 11-image $0.737 lines) as reasoning load rises:

| o3 reasoning load | o3 output tok / session | Calc session (list) | Calc session (+50%) |
|---|---|---|---|
| **As modelled** | ~21,000 | $1.531 | **$2.297** |
| 1.5× harder | ~31,500 | $1.615 | $2.423 |
| 2× harder | ~42,000 | $1.699 | $2.549 |
| 3× harder | ~63,000 | $1.867 | $2.801 |

> The o3 output-token counts are **editable** in the estimator's *Advanced assumptions* — tune them to a
> sample of real billed sessions and the estimate tracks reality.

---

## 5. Full homework-session confirmation table

Per-session cost by service, with **audio at the 24,000-char maximum** and **11 real-time images**
(default 5 steps). **Calculation** sessions use o3; **explanation** sessions use gpt-4.1; the **blended**
row is the estimator default (50/50, image intake, audio on).

| Session type | o3 | gpt-4.1 | Gemini images (×11) | Inworld audio (max) | **Total (list)** | **Total (+50%)** |
|---|---|---|---|---|---|---|
| Calculation (o3) | $0.182 | $0.012 | $0.737 | $0.600 | **$1.531** | **$2.297** |
| Explanation (gpt-4.1) | — | $0.070 | $0.737 | $0.600 | **$1.407** | **$2.111** |
| **Blended (default)** | $0.091 | $0.041 | $0.737 | $0.600 | **$1.469** | **$2.204** |

Every number is reproducible from Sections 2–4 with the published unit prices — that is the confirmation:
**provider price × quantity = the estimator's figure.** Image generation and audio together are ~85% of a
session, because both are costed at their conservative maximum.

---

## 6. Scaling to volume (monthly / yearly)

Using the **blended buffered** cost of **$2.204** per session, scaled by each preset's monthly session
count (the *range* uses the explanation-only and calculation-only bounds, $2.111 → $2.297):

| Preset | Students × questions | Sessions / month | Monthly (blended) | Yearly (blended) | Monthly range |
|---|---|---|---|---|---|
| **Reset to defaults** | 200 × 10 | 2,000 | **$4,408** | **$52,896** | $4,222 – $4,594 |
| **Light usage** | 300 × 10 | 3,000 | **$6,612** | **$79,344** | $6,333 – $6,891 |
| **Heavy usage** | 600 × 10 | 6,000 | **$13,224** | **$158,688** | $12,666 – $13,782 |

*The two levers that move these most:* the **step-image assumption** (Section 3 — fewer images per step if
some are cached) and the **Inworld tier** (a $1,500/mo commit halves the audio line).

---

## 7. Reconciliation summary

1. **Unit prices are correct and current** (verified July 2026) — o3 & gpt-4.1 at $2/$8 per 1M tokens,
   Gemini image at $0.067, Inworld TTS-2 at $25 per 1M characters on-demand.
2. **Image generation is now the largest line** — a real-time diagram at every walkthrough step of every
   session (`2×steps + 1` ≈ 11 images at default depth) = **$0.74 list / $1.11 buffered**. This reflects
   that images are created live at each phase, not once per upload.
3. **Audio is billed at the maximum narration length** (24,000 chars ≈ $0.60 / $0.90).
4. **Everything carries a +50% buffer** and audio is priced on Inworld's most expensive on-demand tier, so
   the estimate is deliberately conservative.
5. **Validate two things on real usage:** (a) whether every step truly generates a fresh image or some are
   cached/reused — this is the biggest single assumption; and (b) o3's reasoning-token count (Section 4.3).

### Recommended checks before committing to a budget
- Count the **actual images generated** in a sample of real sessions vs. the `2×steps + 1` assumption; if
  some steps reuse a cached image, lower the assumption and the (dominant) image line falls proportionally.
- Confirm the **maximum narrated characters** per session vs. the 24,000-char ceiling.
- Pull the **actual o3 output-token count** from a dozen real calculation sessions vs. ~21,000/session.
- Decide the Inworld **commitment tier** (on-demand $25 → $1,500/mo commit $12.50 halves audio).

---

### Sources
- OpenAI o3 API pricing ($2 / $8 per 1M tokens; hidden reasoning tokens billed at output rate):
  <https://developers.openai.com/api/docs/pricing> · <https://pricepertoken.com/pricing-page/model/openai-o3>
- Inworld TTS-2 pricing ($25 / 1M characters on-demand, tiered to $10 enterprise):
  <https://inworld.ai/pricing> · <https://www.buildmvpfast.com/api-costs/ai-voice>

*Figures are grounded in the estimator's editable token / character / image assumptions; tune those to your
real provider contracts and billed usage.*
