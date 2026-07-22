# Homework Flow & Curriculum Build — Cost Verification & Provider Reconciliation

> **Purpose.** This document lets us *confirm* the costs the estimator shows: the per-session cost of the
> Homework Help (Tier 2) flow (Sections 1–7), and the one-off cost to build the whole KS3 + KS4 curriculum
> (Section 8). It checks every provider unit price against live provider documentation, then shows exactly
> how the largest variable line — **TTS audio** — is counted on the **measured average** narration length,
> how image generation is costed at **one diagram per session** on the new **Gemini 3.1 Flash Image Light**
> model, and explains the GPT-5 mini reasoning-token line.
>
> **Bottom line up front:** the unit prices are *correct and current*. The calculation route now runs on
> **GPT-5 mini ($0.25 / 1M input · $2.00 / 1M output)** instead of o3, cutting the reasoning line by ~76%; and
> audio has moved from Inworld TTS-2 to **Speechify (Pro plan, $8 / 1M characters)**, roughly halving the voice
> line. After both changes **no single provider dominates a session** — reasoning, image and audio are all in
> the same range. Audio is billed on the **MEASURED AVERAGE** narration length (Section 2), route-specific —
> measured across real homework sessions rather than the old conservative 24,000-char maximum. Homework prices
> carry a **+15% buffer**. Image generation is a single diagram per session on the new **Gemini 3.1 Flash
> Image Light (Nano-Banana-Light)** model at **$0.05/image** (Section 3), down from $0.10. The figures to keep
> validating on a real invoice are the **audio character count** (Section 2) and that **Speechify matches the
> SSML / per-word pronunciation control** the flow relies on — this swap is priced as a unit-price change only.

---

## 1. Provider unit prices — confirmed against documentation (July 2026)

| Service | Model | Published list price | In estimator | Confirmed |
|---|---|---|---|---|
| Reasoning LLM | **GPT-5 mini** | **$0.25 / 1M input · $2.00 / 1M output** | $0.25 / $2 | ✅ matches OpenAI |
| Prose / vision LLM | **gpt-4.1** | $2.00 / 1M input · $8.00 / 1M output | $2 / $8 | ✅ matches OpenAI |
| Diagram image | **Gemini 3.1 Flash Image Light** (Nano-Banana-Light) | **$0.05 / image** | $0.05 | ✅ matches |
| Text-to-speech | **Speechify** | **$8.00 / 1M characters (Pro plan)** | $8 | ✅ matches Speechify |
| Safety | omni-moderation | Free | $0 | ✅ |

*The calculation route moved from **o3** ($2 / $8) to **GPT-5 mini** ($0.25 / $2) — 8× cheaper input, 4×
cheaper output. Prose/explanation questions still run on gpt-4.1.*

**The +15% safety buffer (homework).** Every homework price above is multiplied by **1.15** inside the
estimator before any figure is shown, as an internal margin for retries, prompt drift and future price moves.
So the effective rates the estimator charges against are: GPT-5 mini **$0.2875 / $2.30** per 1M, gpt-4.1
**$2.30 / $9.20** per 1M, Gemini **$0.0575** per image, Speechify **$9.20** per 1M characters. Throughout, we
show **both** columns — *"list"*
(the provider's published price, for reconciliation) and *"+15%"* (what the estimator displays). The one-off
**curriculum build** (Section 8) is costed separately.

---

## 2. Text-to-speech (Speechify) — billed on the MEASURED AVERAGE narration length

Speechify bills **per character** sent to synthesis. Earlier this document costed audio on a conservative
**24,000-char maximum**. We have since **measured** the characters the homework flow actually sends to TTS
across real sessions (`homework_tts_char_count.py`, 6 sessions), and the estimator now costs audio on that
**measured average** — and, crucially, **route-specific**: prose *explanation* sessions narrate 2–4× longer
than *calculation* sessions, so the blended figure follows the calculation / explanation mix.

| Route (what the question needs) | Measured avg TTS chars / session | % of the 24,000 ceiling | n |
|---|---|---|---|
| **Calculation → GPT-5 mini** (Maths / Physics / Chemistry sums) | **4,758** | 20% | 3 |
| **Explanation → gpt-4.1** (English, Biology prose) | **12,611** | 53% | 3 |
| **Blended average (50/50 default)** | **8,685** | 36% | 6 |

**Cost of the blended 8,685-char average:** list `8,685 ÷ 1,000,000 × $8` = **$0.0695** · +15% = **$0.0799**.
Per route: calculation `4,758 × $8/1M` = **$0.0381** list / **$0.0438** (+15%); explanation
`12,611 × $8/1M` = **$0.1009** list / **$0.1160** (+15%).

This is roughly **half** the previous Inworld line (which was $0.148 blended on the $17 Developer plan). The
24,000-char maximum remains a safe worst-case bound, but the measured average is ~**2.8× lower**, so it is
the realistic figure for a blended forecast. Speechify gets cheaper as monthly character volume grows, so a
real audio invoice can come in lower than the Pro-plan rate:

| Speechify tier | $ / 1M characters | Cost of the 8,685-char avg session |
|---|---|---|
| Starter | $10.00 | $0.087 |
| **Pro (what we estimate on)** | **$8.00** | **$0.069** |
| Scale | $6.00 | $0.052 |
| Enterprise | Volume discount | lower |

> **This swap is priced as a unit-price change only.** Homework audio was flipped to Inworld TTS-2
> specifically for its SSML / intermediate-representation pipeline and per-word `/IPA/` pronunciation control
> (equation read-out, phoneme overrides). Before treating the ~50% saving as real, confirm Speechify supports
> the same SSML / phoneme control **and** how it counts characters for billing (whether SSML tags are charged),
> since that changes the effective rate.

---

## 3. Image generation (Gemini 3.1 Flash Image Light) — one diagram per session

Homework Help generates **exactly one diagram image per session**, regardless of walkthrough depth or how
the question arrived. This is homework-only behaviour: a single supporting diagram is produced for the
session and reused across the walkthrough steps rather than re-generated at each phase.

```
images / session = 1   (fixed — one diagram per session)
```

Because it no longer scales with walkthrough depth, this line is flat and small. The homework flow has moved
to the new **Gemini 3.1 Flash Image Light (Nano-Banana-Light)** model, so the estimator now prices the image
at **$0.05** — down from **$0.10** on the previous model:

| Images / session | Cost (list @ $0.05) | Cost (+15%) |
|---|---|---|
| **1 (fixed)** | **$0.05** | **$0.0575** |

> **This is a minor provider line in a session.** At one image, generation is **$0.05 list / $0.0575
> buffered**. If in future the flow needs more than one diagram per session, raise the image assumption in
> the estimator and this line scales linearly.

---

## 4. GPT-5 mini reasoning model — tokens and cost

GPT-5 mini is only used for **calculation / derivation** questions (Maths, Physics, Chemistry, computational
Science). Prose/explanation questions run on gpt-4.1. The build pipeline is five LLM calls (steps A ·
parallel B · demo C · 3A explanation · answer key D); A→B→C can regenerate on a self-check failure, so
they carry a retry factor (default **1.15×**).

The token counts below are **carried over unchanged from the previous o3 model** — output tokens are set to
**include** hidden reasoning tokens (GPT-5 mini is a reasoning model too). We have no measured mini token
sample yet, so holding o3's (near worst-case) counts keeps the estimate conservative; only the **rate**
changes ($8 → $2 output). Re-tune once real mini sessions are billed — see Section 4.3.

### 4.1 Per-call token assumptions (GPT-5 mini route)

| Call | Input tok | Output tok | Runs / session | mini cost (list) |
|---|---|---|---|---|
| A · Solution steps | 700 | 3,000 | 1.15 | $0.0071 |
| B · Parallel question | 800 | 2,500 | 1.15 | $0.0060 |
| C · Parallel demo (worked) | 900 | 3,000 | 1.15 | $0.0072 |
| 3A · Explanation | 600 | 2,200 | 1.00 | $0.0046 |
| D · Private answer key | 900 | 3,000 | 1.00 | $0.0062 |
| Validate attempt | 700 | 1,500 | 3.00 | $0.0095 |
| Follow-up Q&A | 800 | 1,500 | 1.00 | $0.0032 |
| **mini subtotal** | **~7,160** | **~20,975** | | **$0.0437** |

Plus the fixed gpt-4.1 intake/classify calls that run in **every** session (image extract + analyze +
match): **$0.0118**.

### 4.2 Per-session GPT-5 mini cost (the math)

```
mini input :  7,160 tok ÷ 1,000,000 × $0.25 = $0.0018
mini output: 20,975 tok ÷ 1,000,000 × $2    = $0.0420
mini total (list)                            = $0.0437  →  +15% = $0.0503
```

For comparison, the same session on **o3** ($2 / $8) cost **$0.1821 list / $0.2094 buffered** — GPT-5 mini
is **~76% cheaper** on the reasoning line.

### 4.3 Reasoning-token variance — the same risk, 4× smaller

**The unit price is right ($0.25/$2); the residual risk is the token count.** Like o3, GPT-5 mini bills
*invisible* reasoning tokens at the **output** rate, and a single reasoning answer can burn several thousand
internal tokens. Our model already assumes ~21,000 output tokens for a whole calculation session (near the
high end), but if mini reasons *harder*, cost scales. The crucial difference from o3: the output rate is now
**$2, not $8**, so every extra reasoning token costs **4× less** — the same variance that added $0.42 on o3
adds ~$0.10 on mini. This table shows a full **calculation** session (mini LLM + the fixed gpt-4.1 intake +
the measured-average calc audio $0.038 on Speechify + the one-image $0.05 line) as reasoning load rises:

| Reasoning load | Output tok / session | Calc session (list) | Calc session (+15%) |
|---|---|---|---|
| **As modelled** | ~21,000 | $0.144 | **$0.165** |
| 1.5× harder | ~31,500 | $0.165 | $0.189 |
| 2× harder | ~42,000 | $0.186 | $0.214 |
| 3× harder | ~63,000 | $0.228 | $0.262 |

> The output-token counts are **editable** in the estimator's *Advanced assumptions* — tune them to a
> sample of real billed sessions and the estimate tracks reality. Because mini's output rate is 4× lower than
> o3's, the whole reasoning line — and its sensitivity to reasoning depth — is now a minor part of a session.

---

## 5. Full homework-session confirmation table

Per-session cost by service, with **audio at the measured average** (route-specific) and **one real-time
image**. **Calculation** sessions use GPT-5 mini; **explanation** sessions use gpt-4.1; the **blended** row is
the estimator default (50/50, image intake, audio on).

| Session type | GPT-5 mini | gpt-4.1 | Gemini image (×1) | Speechify audio (avg) | **Total (list)** | **Total (+15%)** |
|---|---|---|---|---|---|---|
| Calculation (mini) | $0.044 | $0.012 | $0.050 | $0.038 | **$0.144** | **$0.165** |
| Explanation (gpt-4.1) | — | $0.070 | $0.050 | $0.101 | **$0.221** | **$0.254** |
| **Blended (default)** | $0.022 | $0.041 | $0.050 | $0.069 | **$0.182** | **$0.210** |

Every number is reproducible from Sections 2–4 with the published unit prices — that is the confirmation:
**provider price × quantity = the estimator's figure.** With reasoning on GPT-5 mini and audio on Speechify,
**no single line dominates** — audio is ~26–46% of a session depending on route, the one image is a similar
share of a calculation session (~35%), and the reasoning line is small. Audio is a measured line, not a
worst-case ceiling.

---

## 6. Scaling to volume (monthly / yearly)

Using the **blended buffered** cost of **$0.210** per session, scaled by each preset's monthly session
count (the *range* uses the calculation-only and explanation-only bounds, $0.165 → $0.254):

| Preset | Students × questions | Sessions / month | Monthly (blended) | Yearly (blended) | Monthly range |
|---|---|---|---|---|---|
| **Reset to defaults** | 200 × 10 | 2,000 | **$420** | **$5,040** | $330 – $508 |
| **Light usage** | 300 × 20 | 6,000 | **$1,260** | **$15,120** | $990 – $1,524 |
| **Heavy usage** | 600 × 40 | 24,000 | **$5,040** | **$60,480** | $3,960 – $6,096 |

*Monthly figures use the blended-default per-session cost. With reasoning on GPT-5 mini and audio on
Speechify, the biggest lever is still the **explanation / calculation mix** (prose sessions narrate 2–4× more
audio); the **mini reasoning-token count** (Section 4.3) is a minor lever. Speechify's **plan tier** lowers
audio further ($10 Starter → $8 Pro → $6 Scale → enterprise volume discount).*

---

## 7. Reconciliation summary (homework)

1. **Unit prices are correct and current** (verified July 2026) — GPT-5 mini at **$0.25/$2** per 1M tokens
   (calculation route, down from o3's $2/$8), gpt-4.1 at $2/$8 per 1M tokens (explanation route), Gemini 3.1
   Flash Image Light at $0.05/image, Speechify at **$8 per 1M characters (Pro plan)**, down from Inworld's $17.
2. **Reasoning moved to GPT-5 mini and audio to Speechify** — the calculation route now costs ~$0.044 list /
   $0.050 buffered per session (~76% below o3), and audio roughly halved; after both changes no single line
   dominates a session.
3. **Audio is now a measured-average line, route-specific** — calculation ~4,758 chars, explanation
   ~12,611 chars, blended ~8,685 chars ≈ $0.069 list / $0.080 buffered on Speechify Pro ($8) — measured across
   6 real sessions, replacing the old 24,000-char maximum (which remains a safe worst-case bound, ~2.8× higher).
4. **Image generation is a single diagram per session** — one **Gemini 3.1 Flash Image Light
   (Nano-Banana-Light)** image at **$0.05 list / $0.0575 buffered**, down from $0.10, a minor line that no
   longer scales with walkthrough depth.
5. **Homework carries a +15% buffer**, so the estimate stays deliberately conservative.
6. **Validate three things on real usage:** (a) the **average narrated characters** per session vs. the
   measured 4,758 / 12,611 / 8,685 figures — still a major line; (b) GPT-5 mini's reasoning-token count
   (Section 4.3), a minor line since output bills at $2; and (c) that **Speechify matches the SSML / per-word
   pronunciation control** the flow relies on — the swap is priced as a unit-price change only.

### Recommended checks before committing to a budget
- Confirm the **average narrated characters** per session (per route) against a larger sample than 6.
- Pull the **actual GPT-5 mini output-token count** from a dozen real calculation sessions vs. ~21,000/session
  (carried over from o3; likely lower, and cheaper at $2/1M either way).
- Confirm **Speechify feature parity** (SSML / phoneme control) and how it counts characters for billing, then
  decide the **plan tier** (Starter $10 → Pro $8 → Scale $6 → enterprise volume discount).

---

## 8. Full curriculum build — one-off content generation (separate from homework)

This is **not** a per-homework-session cost. It is the **one-off** cost to generate every lesson across the
KS3 + KS4 curriculum, costed on **gpt-4.1** (the most expensive content model). Like homework, this build has
now moved to the cheaper new image model for its ~30 whiteboard images per lesson.

### 8.1 Basis and the image-model change

This is the one-off cost to generate every lesson across KS3 + KS4, costed on **gpt-4.1** (the most expensive
content model). Each lesson includes its script, narration audio, helpers, and **~30 whiteboard images**.

The only input that moved from the previous build is the **image model**: the ~30 images per lesson now run
on the new **Gemini 3.1 Flash Image** model, dropping the image cost from **~$1.89 to ~$1.05 per lesson**
(source: *General Cost Estimation Document (Updated).pdf*).

> **Image-model change, isolated.** Nothing else in the build changed — same gpt-4.1 content model, same
> script/audio/helpers. The cheaper images alone lower the whole-curriculum total from **$2,410.8 – $2,881.2**
> to **$1,916.9 – $2,290.9**; the per-subject figures are below.

### 8.2 Per key stage

**Key Stage 3**

| Subject | Units | Lessons | Cost |
|---|---|---|---|
| Mathematics | 6 | 57 | $278.7 – $333.1 |
| English | 8 | 27 | $132.0 – $157.8 |
| Physics | 7 | 43 | $210.3 – $251.3 |
| Chemistry | 8 | 32 | $156.5 – $187.0 |
| Biology | 6 | 38 | $185.8 – $222.1 |
| **Total** | **35** | **197** | **$963.3 – $1,151.3** |

**Key Stage 4**

| Subject | Units | Lessons | Cost |
|---|---|---|---|
| Mathematics | 6 | 74 | $361.9 – $432.5 |
| English | 11 | 38 | $185.8 – $222.1 |
| Physics | 7 | 34 | $166.3 – $198.7 |
| Chemistry | 10 | 49 | $239.6 – $286.4 |
| Biology | — | — | — |
| **Total** | **34** | **195** | **$953.5 – $1,139.6** |

### 8.3 Whole curriculum

| Whole curriculum (KS3 + KS4) | Units | Lessons | Cost |
|---|---|---|---|
| **Combined** | **69** | **392** | **$1,916.9 – $2,290.9** |

*Down from **$2,410.8 – $2,881.2** on the previous image model. Biology KS4 was not in the source curriculum
count, so it is left blank rather than estimated. The combined total is the sum of the two Key-Stage totals.*

---

## 9. Live lesson session — why the LLM call count runs 16 to 24

The live lesson cost is not a flat per-minute rate. It is driven almost entirely by **how many LLM calls the
check-in questions trigger**, so the call count is derived here rather than assumed.

### 9.1 Lesson shape

A lesson is **4 segments × 6 chunks = 24 chunks**. Chunks are narration; they do not each carry a question.
`_apply_segment_checkin_rhythm` (`app/modules/content_generator.py`) marks exactly **two pause points per
segment** — one mid-segment (chunk index 2, 3 or 4, chosen at random) and one on the last chunk — each asking
**one question**.

| | Per segment | Per lesson |
|---|---|---|
| Chunks | 6 | 24 |
| Check-in pause points | 2 | 8 |
| **Questions asked** | **2** | **8** |

Worked examples and the quiz are excluded: they are served from cache and make no live call, and their text is
not spoken live, so they contribute neither LLM tokens nor TTS characters.

### 9.2 The three calls behind one question

Each check-in is generated fresh at lesson time — nothing is read from the pre-built `QuestionBank`, which
serves the practice quiz and the pre/post assessment instead. All three calls route through
`POST /lessons/{id}/ask-question`.

| Call | Fires | Capped? |
|---|---|---|
| 1. Generate the question | **Always** — written against the chunk (or the whole segment, on the last chunk) | — |
| 2. Spoken feedback | **Always** — the prompt branches on correct/incorrect, so a right answer still costs a call | — |
| 3. Re-explain the concept | **Only after a wrong answer** | **Max 1 per question**; the lesson then auto-advances |

**Floor = 8 × 2 = 16 calls. Ceiling = 8 × 3 = 24 calls.**

### 9.3 Why 24 is reachable, and why nothing exceeds it

The floor of 16 assumes a student answers **all eight check-ins correctly, first time**. That is the best case,
not the typical one. Four things push a real session toward the ceiling:

1. **Two-option multiple choice.** Check-ins offer exactly 2 options, so a student who is guessing is wrong
   about **half** the time. Blind guessing alone lands on ~4 re-explanations — **20 calls** — which makes 20,
   not 16, the statistically neutral midpoint.
2. **This tier assumes no prior knowledge.** The Foundation script is written for students starting from
   zero, which is precisely the cohort most likely to miss a check-in. The content tier and the wrong-answer
   rate are correlated, so this tier skews to the upper half of the range.
3. **&ldquo;Explain again&rdquo; is one tap and free to the student.** It is the only route to hearing the idea a
   second time, so when it is offered it is usually taken. Offered ≈ taken, in practice.
4. **Wrong answers cost more on both sides.** The re-explain is the largest prompt of the three (~4,700
   characters in) and produces the longest spoken reply (~700 characters), so each one adds LLM *and* voice
   cost together.

The ceiling holds at 24 because the re-explain is capped at one per question in code — a second attempt is
never offered, and the lesson advances as soon as the single re-explanation finishes speaking. The only way
past 24 is the free-text answer path, which inserts an extra on-topic validation call; multiple choice is the
default and free-text is not used for check-ins.

### 9.4 Cost across the range

Prompt sizes are measured from the actual prompt builders, including the backend system prompt and wrapper
added to every call. Narration audio is pre-generated and cached, so the voice line covers only text composed
live — the question, the feedback, and any re-explanation.

| Scenario | Live calls | Tokens in | Tokens out | LLM (GPT-5 mini) | Voice chars | Voice (Speechify) | **Total / student** |
|---|---|---|---|---|---|---|---|
| Every check-in correct | 16 | 13,662 | 800 | $0.006 | 3,200 | $0.029 | **$0.035** |
| **Half wrong — planning case** | **20** | **18,371** | **1,500** | **$0.009** | **6,000** | **$0.055** | **≈ $0.064** |
| Every check-in wrong | 24 | 23,080 | 2,200 | $0.012 | 8,800 | $0.081 | **$0.093** |

**Budget on ~$0.06 per student per lesson; size headroom for ~$0.09.**

*The live-lesson section now uses the same providers as the homework flow: **content on GPT-5 mini ($0.25/$2)**
and **voice on Speechify Pro ($8/1M)**, replacing gpt-4.1 + Inworld. That drops the planning case from $0.17 to
**~$0.064** — roughly 60% lower — because the voice line more than halves and the check-in LLM calls, being
short and output-light, cost almost nothing on mini.*

This supersedes the previous flat estimate of ~25 calls / ~12,600 voice characters / $0.41. That figure was a
single measured session with no structural derivation, and it double-counted the pre-generated narration as a
live voice cost.

---

### Sources
- OpenAI GPT-5 mini API pricing ($0.25 / $2 per 1M tokens; hidden reasoning tokens billed at output rate):
  <https://developers.openai.com/api/docs/pricing> · <https://pricepertoken.com/pricing-page/model/openai-gpt-5-mini>
- OpenAI o3 API pricing ($2 / $8 per 1M tokens — previous calculation-route model, for reference):
  <https://pricepertoken.com/pricing-page/model/openai-o3>
- Speechify TTS API pricing (Pro plan $8 / 1M characters; Starter $10, Scale $6, enterprise volume discount):
  <https://speechify.ai/pricing> · <https://speechify.com/blog/best-text-to-speech-api-voice-quality-price/>
- Inworld TTS-2 pricing (Developer plan $17 / 1M characters — previous voice provider for both homework and
  live lessons, now fully replaced by Speechify): <https://inworld.ai/pricing> · <https://www.buildmvpfast.com/api-costs/ai-voice>
- Measured TTS characters: `homework_tts_summary.pdf` / `homework_tts_char_count.py` (6 sessions, 2026-07-10).
- Curriculum build figures: `General Cost Estimation Document (Updated).pdf` (per-lesson gpt-4.1 with the new
  image model), reconciled against `General Cost Estimation Document.pdf` (previous image model).

*Figures are grounded in the estimator's editable token / character / image assumptions; tune those to your
real provider contracts and billed usage.*
