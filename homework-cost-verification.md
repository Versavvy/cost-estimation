# Homework Flow — Cost Verification & Provider Reconciliation

> **Purpose.** This document lets us *confirm* the per-session cost the estimator shows for the
> Homework Help (Tier 2) flow. It checks every provider unit price against the live provider
> documentation, then shows exactly how the biggest line — **TTS audio** — is counted, how image
> generation is now costed at **one diagram per session**, and explains the o3 reasoning-token risk.
>
> **Bottom line up front:** the unit prices are *correct and current*. The headline number is driven by
> two deliberate, conservative choices: **audio is billed on the MAXIMUM narration length** (Section 2)
> and every price carries a **+15% buffer**. Image generation is now a single diagram per session
> (Section 3), so it is a minor line. The figure to keep validating on a real invoice is o3's
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

**The +15% safety buffer.** Every price above is multiplied by **1.15** inside the estimator before any
figure is shown, as an internal margin for retries, prompt drift and future price moves. So the effective
rates the estimator charges against are: o3 / gpt-4.1 **$2.30 / $9.20** per 1M, Gemini **$0.077** per image,
Inworld **$28.75** per 1M characters. Throughout, we show **both** columns — *"list"* (the provider's
published price, for reconciliation) and *"+15%"* (what the estimator displays).

---

## 2. Text-to-speech (Inworld TTS-2) — billed on the MAXIMUM narration length

Inworld bills **per character** sent to synthesis. Real homework narration runs far longer than a "typical"
estimate, so the estimator costs audio on the **maximum** a session can produce — every audio driver at its
ceiling. This is the figure shown on the dashboard, and it is now the **single largest line in a session**.

| Phase narrated | Max characters | At the slider ceiling |
|---|---|---|
| 3A explanation | 800 | `charsExp` max |
| Solution + parallel-demo steps | 10,000 | `10 steps × 500 × 2` |
| Intros + completion | 1,200 | `charsOv` max |
| Attempt feedback + Q&A | 12,000 | `(12 + 8) × 600` |
| **Maximum per session (billed)** | **24,000** | |

**Cost of 24,000 characters:** list `24,000 ÷ 1,000,000 × $25` = **$0.60** · +15% = **$0.69**.

Inworld gets cheaper with commitment, and we estimate on the most expensive on-demand tier, so a real
audio invoice can only come in lower:

| Inworld TTS-2 tier | $ / 1M characters | Cost of a 24,000-char session |
|---|---|---|
| **On-demand (what we estimate on)** | **$25.00** | $0.60 |
| $300 / month commit | $15.00 | $0.36 |
| $1,500 / month commit | $12.50 | $0.30 |
| Enterprise | $10.00 (as low as $5) | $0.24 (↓ $0.12) |

---

## 3. Image generation (Gemini 3.1 Flash Image) — one diagram per session

Homework Help generates **exactly one diagram image per session**, regardless of walkthrough depth or how
the question arrived. This is homework-only behaviour: a single supporting diagram is produced for the
session and reused across the walkthrough steps rather than re-generated at each phase.

```
images / session = 1   (fixed — one diagram per session)
```

Because it no longer scales with walkthrough depth, this line is flat and small:

| Images / session | Cost (list @ $0.067) | Cost (+15%) |
|---|---|---|
| **1 (fixed)** | **$0.067** | **$0.077** |

> **This is now the smallest provider line in a session.** At one image, generation is **$0.067 list /
> $0.077 buffered** — well below audio and the o3 reasoning cost. If in future the flow needs more than one
> diagram per session, raise the image assumption in the estimator and this line scales linearly.

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
o3 total (list)                          = $0.1821  →  +15% = $0.2094
```

### 4.3 Why o3 can look cheaper than the docs — hidden reasoning tokens

**The unit price is right ($2/$8); the risk is the token count, not the rate.** o3 bills *invisible*
reasoning tokens at the **output** rate. OpenAI's documentation notes a single o3 answer can burn
**5,000–20,000 internal reasoning tokens**. Our model already assumes ~21,000 o3 output tokens for a whole
calculation session (near the high end), but if o3 reasons *harder*, cost scales. This table shows a full
calculation session (including the max-audio $0.60 and the one-image $0.067 lines) as reasoning load rises:

| o3 reasoning load | o3 output tok / session | Calc session (list) | Calc session (+15%) |
|---|---|---|---|
| **As modelled** | ~21,000 | $0.861 | **$0.990** |
| 1.5× harder | ~31,500 | $0.945 | $1.087 |
| 2× harder | ~42,000 | $1.029 | $1.183 |
| 3× harder | ~63,000 | $1.197 | $1.377 |

> The o3 output-token counts are **editable** in the estimator's *Advanced assumptions* — tune them to a
> sample of real billed sessions and the estimate tracks reality.

---

## 5. Full homework-session confirmation table

Per-session cost by service, with **audio at the 24,000-char maximum** and **one real-time image**.
**Calculation** sessions use o3; **explanation** sessions use gpt-4.1; the **blended** row is the estimator
default (50/50, image intake, audio on).

| Session type | o3 | gpt-4.1 | Gemini image (×1) | Inworld audio (max) | **Total (list)** | **Total (+15%)** |
|---|---|---|---|---|---|---|
| Calculation (o3) | $0.182 | $0.012 | $0.067 | $0.600 | **$0.861** | **$0.990** |
| Explanation (gpt-4.1) | — | $0.070 | $0.067 | $0.600 | **$0.737** | **$0.848** |
| **Blended (default)** | $0.091 | $0.041 | $0.067 | $0.600 | **$0.799** | **$0.919** |

Every number is reproducible from Sections 2–4 with the published unit prices — that is the confirmation:
**provider price × quantity = the estimator's figure.** Audio alone is now ~70–80% of a session, because it
is costed at its conservative maximum; the single image line is minor.

---

## 6. Scaling to volume (monthly / yearly)

Using the **blended buffered** cost of **$0.919** per session, scaled by each preset's monthly session
count (the *range* uses the explanation-only and calculation-only bounds, $0.848 → $0.990):

| Preset | Students × questions | Sessions / month | Monthly (blended) | Yearly (blended) | Monthly range |
|---|---|---|---|---|---|
| **Reset to defaults** | 200 × 10 | 2,000 | **$1,838** | **$22,056** | $1,696 – $1,980 |
| **Light usage** | 300 × 20 | 6,000 | **$5,514** | **$66,168** | $5,088 – $5,940 |
| **Heavy usage** | 600 × 40 | 24,000 | **$22,056** | **$264,672** | $20,352 – $23,760 |

*Monthly figures use the blended-default per-session cost. The two levers that move these most: the
**Inworld tier** (a $1,500/mo commit more than halves the audio line, the dominant cost) and the **o3
reasoning-token count** (Section 4.3).*

---

## 7. Reconciliation summary

1. **Unit prices are correct and current** (verified July 2026) — o3 & gpt-4.1 at $2/$8 per 1M tokens,
   Gemini image at $0.067, Inworld TTS-2 at $25 per 1M characters on-demand.
2. **Audio is now the largest line** — billed at the maximum narration length (24,000 chars ≈ $0.60 list /
   $0.69 buffered).
3. **Image generation is a single diagram per session** — one Gemini image ≈ **$0.067 list / $0.077
   buffered**, a minor line that no longer scales with walkthrough depth.
4. **Everything carries a +15% buffer** and audio is priced on Inworld's most expensive on-demand tier, so
   the estimate is deliberately conservative.
5. **Validate two things on real usage:** (a) the **maximum narrated characters** per session vs. the
   24,000-char ceiling — the dominant line; and (b) o3's reasoning-token count (Section 4.3).

### Recommended checks before committing to a budget
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
