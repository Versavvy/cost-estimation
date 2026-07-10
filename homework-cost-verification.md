# Homework Flow — Cost Verification & Provider Reconciliation

> **Purpose.** This document lets us *confirm* the per-session cost the estimator shows for the
> Homework Help (Tier 2) flow. It checks every provider unit price against the live provider
> documentation, then shows exactly how the biggest line — **TTS audio** — is now counted on the
> **measured average** narration length, how image generation is costed at **one diagram per session**,
> and explains the o3 reasoning-token risk.
>
> **Bottom line up front:** the unit prices are *correct and current*. Audio is now billed on the
> **MEASURED AVERAGE** narration length (Section 2), route-specific — measured across real homework
> sessions rather than the old conservative 24,000-char maximum. Every price carries a **+15% buffer**
> and Inworld is priced on the **Developer plan ($17 / 1M characters)**. Image generation is a single
> diagram per session (Section 3), a minor line. The figure to keep validating on a real invoice is
> o3's **hidden reasoning tokens** (Section 4.3).

---

## 1. Provider unit prices — confirmed against documentation (July 2026)

| Service | Model | Published list price | In estimator | Confirmed |
|---|---|---|---|---|
| Reasoning LLM | **o3** | **$2.00 / 1M input · $8.00 / 1M output** | $2 / $8 | ✅ matches OpenAI |
| Prose / vision LLM | **gpt-4.1** | $2.00 / 1M input · $8.00 / 1M output | $2 / $8 | ✅ matches OpenAI |
| Diagram image | **Gemini 3.1 Flash Image** | $0.067 / image (standard-tier list) | **$0.10** (conservative round-up) | ✅ ≥ list |
| Text-to-speech | **Inworld TTS-2** | **$17.00 / 1M characters (Developer plan)** | $17 | ✅ matches Inworld |
| Safety | omni-moderation | Free | $0 | ✅ |

**The +15% safety buffer.** Every price above is multiplied by **1.15** inside the estimator before any
figure is shown, as an internal margin for retries, prompt drift and future price moves. So the effective
rates the estimator charges against are: o3 / gpt-4.1 **$2.30 / $9.20** per 1M, Gemini **$0.115** per image,
Inworld **$19.55** per 1M characters. Throughout, we show **both** columns — *"list"* (the provider's
published price, for reconciliation) and *"+15%"* (what the estimator displays).

---

## 2. Text-to-speech (Inworld TTS-2) — billed on the MEASURED AVERAGE narration length

Inworld bills **per character** sent to synthesis. Earlier this document costed audio on a conservative
**24,000-char maximum**. We have since **measured** the characters the homework flow actually sends to TTS
across real sessions (`homework_tts_char_count.py`, 6 sessions), and the estimator now costs audio on that
**measured average** — and, crucially, **route-specific**: prose *explanation* sessions narrate 2–4× longer
than *calculation* sessions, so the blended figure follows the calculation / explanation mix.

| Route (what the question needs) | Measured avg TTS chars / session | % of the 24,000 ceiling | n |
|---|---|---|---|
| **Calculation → o3** (Maths / Physics / Chemistry sums) | **4,758** | 20% | 3 |
| **Explanation → gpt-4.1** (English, Biology prose) | **12,611** | 53% | 3 |
| **Blended average (50/50 default)** | **8,685** | 36% | 6 |

**Cost of the blended 8,685-char average:** list `8,685 ÷ 1,000,000 × $17` = **$0.1476** · +15% = **$0.1698**.
Per route: calculation `4,758 × $17/1M` = **$0.0809** list / **$0.0930** (+15%); explanation
`12,611 × $17/1M` = **$0.2144** list / **$0.2465** (+15%).

The 24,000-char maximum remains a safe worst-case bound, but the measured average is ~**2.8× lower**, so it
is the realistic figure for a blended forecast. Inworld also gets cheaper with commitment, so a real audio
invoice can only come in lower than the Developer-plan rate:

| Inworld TTS-2 tier | $ / 1M characters | Cost of the 8,685-char avg session |
|---|---|---|
| On-demand | $25.00 | $0.217 |
| **Developer (what we estimate on)** | **$17.00** | **$0.148** |
| Higher commit | $12.50 | $0.109 |
| Enterprise | $10.00 (as low as $5) | $0.087 (↓ $0.043) |

---

## 3. Image generation (Gemini 3.1 Flash Image) — one diagram per session

Homework Help generates **exactly one diagram image per session**, regardless of walkthrough depth or how
the question arrived. This is homework-only behaviour: a single supporting diagram is produced for the
session and reused across the walkthrough steps rather than re-generated at each phase.

```
images / session = 1   (fixed — one diagram per session)
```

Because it no longer scales with walkthrough depth, this line is flat and small. The estimator prices the
image at **$0.10** — a conservative round-up from Gemini's ~$0.067 standard-tier list, for headroom:

| Images / session | Cost (list @ $0.10) | Cost (+15%) |
|---|---|---|
| **1 (fixed)** | **$0.10** | **$0.115** |

> **This is a minor provider line in a session.** At one image, generation is **$0.10 list / $0.115
> buffered**. If in future the flow needs more than one diagram per session, raise the image assumption in
> the estimator and this line scales linearly.

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
**calculation** session (o3 LLM + the measured-average calc audio $0.081 + the one-image $0.10 line) as
reasoning load rises:

| o3 reasoning load | o3 output tok / session | Calc session (list) | Calc session (+15%) |
|---|---|---|---|
| **As modelled** | ~21,000 | $0.375 | **$0.431** |
| 1.5× harder | ~31,500 | $0.459 | $0.528 |
| 2× harder | ~42,000 | $0.543 | $0.624 |
| 3× harder | ~63,000 | $0.711 | $0.818 |

> The o3 output-token counts are **editable** in the estimator's *Advanced assumptions* — tune them to a
> sample of real billed sessions and the estimate tracks reality.

---

## 5. Full homework-session confirmation table

Per-session cost by service, with **audio at the measured average** (route-specific) and **one real-time
image**. **Calculation** sessions use o3; **explanation** sessions use gpt-4.1; the **blended** row is the
estimator default (50/50, image intake, audio on).

| Session type | o3 | gpt-4.1 | Gemini image (×1) | Inworld audio (avg) | **Total (list)** | **Total (+15%)** |
|---|---|---|---|---|---|---|
| Calculation (o3) | $0.182 | $0.012 | $0.100 | $0.081 | **$0.375** | **$0.431** |
| Explanation (gpt-4.1) | — | $0.070 | $0.100 | $0.214 | **$0.384** | **$0.442** |
| **Blended (default)** | $0.091 | $0.041 | $0.100 | $0.148 | **$0.380** | **$0.437** |

Every number is reproducible from Sections 2–4 with the published unit prices — that is the confirmation:
**provider price × quantity = the estimator's figure.** Audio is now a measured line (~35–55% of a session
depending on route), not a worst-case ceiling; the single image line is minor.

---

## 6. Scaling to volume (monthly / yearly)

Using the **blended buffered** cost of **$0.437** per session, scaled by each preset's monthly session
count (the *range* uses the calculation-only and explanation-only bounds, $0.431 → $0.442):

| Preset | Students × questions | Sessions / month | Monthly (blended) | Yearly (blended) | Monthly range |
|---|---|---|---|---|---|
| **Reset to defaults** | 200 × 10 | 2,000 | **$874** | **$10,488** | $862 – $884 |
| **Light usage** | 300 × 20 | 6,000 | **$2,622** | **$31,464** | $2,586 – $2,652 |
| **Heavy usage** | 600 × 40 | 24,000 | **$10,488** | **$125,856** | $10,344 – $10,608 |

*Monthly figures use the blended-default per-session cost. The two levers that move these most: the
**explanation / calculation mix** (prose sessions narrate 2–4× more audio) and the **o3 reasoning-token
count** (Section 4.3). The Inworld **commitment tier** lowers audio further ($17 Developer → $12.50 higher
commit → $10 enterprise).*

---

## 7. Reconciliation summary

1. **Unit prices are correct and current** (verified July 2026) — o3 & gpt-4.1 at $2/$8 per 1M tokens,
   Gemini image at $0.067, Inworld TTS-2 at **$17 per 1M characters (Developer plan)**.
2. **Audio is now a measured-average line, route-specific** — calculation ~4,758 chars, explanation
   ~12,611 chars, blended ~8,685 chars ≈ $0.148 list / $0.170 buffered — measured across 6 real sessions,
   replacing the old 24,000-char maximum (which remains a safe worst-case bound, ~2.8× higher).
3. **Image generation is a single diagram per session** — one Gemini image at **$0.10 list / $0.115
   buffered** (a conservative round-up from the ~$0.067 published list), a minor line that no longer scales
   with walkthrough depth.
4. **Everything carries a +15% buffer**, so the estimate stays deliberately conservative.
5. **Validate two things on real usage:** (a) the **average narrated characters** per session vs. the
   measured 4,758 / 12,611 / 8,685 figures — the dominant line; and (b) o3's reasoning-token count
   (Section 4.3).

### Recommended checks before committing to a budget
- Confirm the **average narrated characters** per session (per route) against a larger sample than 6.
- Pull the **actual o3 output-token count** from a dozen real calculation sessions vs. ~21,000/session.
- Decide the Inworld **commitment tier** (Developer $17 → higher commit $12.50 → enterprise $10).

---

### Sources
- OpenAI o3 API pricing ($2 / $8 per 1M tokens; hidden reasoning tokens billed at output rate):
  <https://developers.openai.com/api/docs/pricing> · <https://pricepertoken.com/pricing-page/model/openai-o3>
- Inworld TTS-2 pricing (Developer plan $17 / 1M characters; on-demand $25, tiered to $10 enterprise):
  <https://inworld.ai/pricing> · <https://www.buildmvpfast.com/api-costs/ai-voice>
- Measured TTS characters: `homework_tts_summary.pdf` / `homework_tts_char_count.py` (6 sessions, 2026-07-10).

*Figures are grounded in the estimator's editable token / character / image assumptions; tune those to your
real provider contracts and billed usage.*
