# Homework Flow — Cost Estimator

`index.html` is a single, self-contained, interactive cost model for the
**ClevStudy Homework Help (Tier 2)** flow only. Open it in any browser — no server, build step,
or internet connection required. All CSS/JS is inline.

## Deploying

This is a pure static site (one HTML file, no dependencies, no build). To deploy, serve this
folder on any static host — the tool loads at `/` because the file is named `index.html`:

- **Drag-and-drop:** zip this folder and drop it on Netlify / Vercel / Cloudflare Pages.
- **Azure Static Web Apps / GitHub Pages:** point the app at this folder (app location = `/`).
- **Local check:** `python -m http.server 8080` in this folder, then open `http://localhost:8080`.

Files in this folder:
- `index.html` — the interactive estimator (the deployable app)
- `homework-cost-estimator-EXPLAINED.md` / `.pdf` — plain-English guide to every section
- `README.md` — this file
- `build_pdf.py` — regenerates the PDF from the EXPLAINED markdown (see bottom)

## What it models

Every cost driver is mapped to the actual code in `Clevstudy-tutor-engine/app/modules/homework/`.

| Phase | Code | Service | Per session |
|-------|------|---------|-------------|
| **Intake** | `extractor.py` | gpt-4.1 (vision for image / scanned PDF; text cleanup for PDF/docx) | 1 call **only for uploads** — typed text = 0 |
| **Classify & gate** | `analyzer.py` | gpt-4.1 | `analyze_question` + `match_lesson` (the safety/scope gate rides on the analyze call); `omni-moderation-latest` is **free** |
| **Build walkthrough** | `solver.py` `build()` | **o3** if `answer_type=calculation`, else **gpt-4.1** | 5 calls: steps (A) · parallel (B) · demo (C) · 3A explanation · answer key (D). A→B→C scale by a retry factor |
| **Interaction** | `solver.py` / `homework.py` | same route as build | 1 call per typed attempt + 1 per follow-up “ask” |
| **Visuals** | `visual_assets/illustration_providers.py` | Gemini 3.1 Flash Image (Nano Banana 2) | 1 image **only when an upload contains a real diagram** (`has_visual`) |
| **Audio** | `media.py` | Inworld TTS-2 (per character) | 3A + every solution & demo step + intros/completion + feedback + Q&A |

## Adjustable parameters

**Live sliders (left column):**
- Sessions / month, and the calculation-vs-explanation split (drives the o3 vs gpt-4.1 mix)
- Input mix: typed text / image / document, and the share of uploads that contain a diagram
- Average solution steps, and the build retry factor (A→B→C can regenerate on a failed self-check)
- Attempts per session and follow-up questions per session
- Audio toggle + characters per step / explanation / overhead / feedback

**Advanced assumptions (collapsible):**
- Unit prices for o3, gpt-4.1, Gemini image, Inworld TTS — **edit to match your contracts**
- Per-call input/output token counts for all 11 call types. o3 output figures sit near the
  `max_completion_tokens` budgets in `solver.py` because reasoning tokens count toward output.

## Outputs

- Blended **cost per session**, **per month**, **per year**
- Separate **calculation-session** vs **explanation-session** cost cards
- **By-service** bar breakdown (o3 / gpt-4.1 / Inworld / Gemini / moderation)
- **By-phase** table (Intake / Classify & gate / Build / Interaction / Visuals / Audio) with $/session, $/month, %

## Default prices — verified against live pricing (June 2026)

These defaults were checked against the providers' published pricing pages, **not** guessed.
They are list prices — your negotiated/volume rate may be lower, so still tune them:
- o3: **$2 / 1M input, $8 / 1M output** (cached input ~$0.50/1M) — [source](https://pricepertoken.com/pricing-page/model/openai-o3)
- gpt-4.1: **$2 / 1M input, $8 / 1M output** (Batch API ~50% off) — [source](https://pricepertoken.com/pricing-page/model/openai-gpt-4.1)
- Gemini 3.1 Flash Image (Nano Banana 2): **$0.067 / 1K image** standard tier ($0.034 batch) — [source](https://ai.google.dev/gemini-api/docs/pricing)
- Inworld TTS-2: **$25 / 1M characters on demand**, → $15 (@ $300/mo), $12.50 (@ $1,500/mo), **$10 at enterprise scale** — [source](https://inworld.ai/tts)
- omni-moderation: **free**

> Note: o3 and gpt-4.1 are no longer on OpenAI's headline pricing table (that now shows the
> gpt-5.x line); the $2/$8 figures are the current rates for these specific models as of May 2026.

Tune the unit prices in *Advanced assumptions* before trusting any total.

## Caveats

- It's an estimate, not billing. o3 reasoning-token volume is the biggest unknown — verify against
  real usage and adjust the output-token assumptions.
- Caching (audio clips cache on a content hash; identical text is not re-synthesised) is **not**
  modelled — real audio cost will be lower than the per-session figure on repeat content.
- `build()` retries beyond the bounded self-check, occasional truncation re-tries, and the rare
  scope-strip path are approximated by the single retry factor.

## Regenerating the PDF

`homework-cost-estimator-EXPLAINED.pdf` is built from the markdown. After editing the `.md`, run:

```powershell
python -m pip install markdown   # one-time
python build_pdf.py
```

It renders the markdown to styled HTML and prints it to PDF with headless Edge/Chrome (whichever
is installed) — no external services.
