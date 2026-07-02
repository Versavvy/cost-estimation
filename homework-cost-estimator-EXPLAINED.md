# Homework Cost Estimator — Explained in Plain English

This is a friendly walkthrough of the cost estimator tool. No jargon. If you only read one
thing, read **"The big idea"** below, then dip into whichever section you're curious about.

---

## The big idea

Every time a student uses **Homework Help**, your app quietly pays a few different companies for
the work behind the scenes — a bit like a restaurant paying for ingredients every time it serves
a meal.

The estimator answers one question:

> **"On average, how much does one homework session cost me — and what does that add up to per month?"**

You change the dials (how many students, what kind of questions, etc.), and it instantly
recalculates the bill.

There is **no real money being spent** by this tool. It's a calculator, like a mortgage estimator.

---

## The Executive Summary (top of the tool) — for management & stakeholders

The blue panel at the very top is the **only part most people need**. It has no technical jargon.

**Two dials:**

- **How many students use it** — distinct students in a month.
- **Questions each student asks** — how many homework questions an average student brings per month.

These two are the same as the detailed "Users & volume" sliders lower down — move either place and both update together.

**Four headline cards:**

- **Cost per question** — the average price of one student taking one question through the whole flow. This is *the* number to remember.
- **Per student / month** — what one student costs you over a month.
- **Total / month** — the whole monthly bill.
- **Total / year** — the same, annualised.

**"Average cost by activity" cards** — this answers "what does each *thing* cost?" in plain terms:

| Card | What it means |
|------|---------------|
| **Typed-in question** | A whole session where the student typed the question (cheapest — nothing to "read"). |
| **Photo / document upload** | A whole session where the student uploaded a picture/PDF (a little extra to read it). |
| **Reading it aloud (audio)** | Just the voice-narration slice of one session. |
| **Drawing a diagram** | The cost of drawing **one** picture, when homework contains a figure. |
| **Maths / science question** | A whole session that used the pricey deep-thinking model. |
| **Explanation / essay question** | A whole session that used the cheaper all-rounder model. |

Cards marked *full session* are the all-in price of that kind of session; *part of a session* / *per diagram* are single building blocks. Everything under this panel (the toolbar, Sections 1–5, Advanced assumptions) simply lets you refine the assumptions behind these headline numbers.

---

## Who gets paid, and for what

Think of it as **five suppliers**. Each does one job:

| Supplier | Plain-English job | When it costs money |
|----------|-------------------|---------------------|
| **o3** | The "deep thinker." Solves maths/science problems that need careful step-by-step calculation. | Only on *calculation* questions. It's the most expensive because thinking hard costs more. |
| **gpt-4.1** | The "all-rounder." Reads uploaded photos, understands the question, and writes the friendly explanations for essay-type subjects. | Reading uploads, sorting every question, and explanation-type walkthroughs. |
| **Gemini Flash Image** | The "artist." Draws a fresh diagram when the homework has a picture in it. | Only when a student uploads something that *contains a diagram*. |
| **Inworld** | The "voice actor." Reads everything out loud. | Whenever audio is switched on. Charged per character (per letter spoken). |
| **Moderation** | The "safety guard." Checks the question isn't inappropriate. | **Free.** Always runs, never costs anything. |

The colour-coded dots in the tool (orange, blue, green, pink, grey) match these five suppliers.

---

## What happens in ONE session (the story)

Imagine a student named Ade opens Homework Help. Here's the journey the tool is pricing,
step by step:

1. **Ade gives the question** — either *types it* (free) or *uploads a photo/PDF*.
   If it's an upload, **gpt-4.1** has to "read" it first. That costs a little.

2. **The app figures out what the question is** — what subject, is it safe, is it a real
   homework question, and which lesson it relates to. This is **gpt-4.1** doing two quick checks,
   plus the **free** safety guard.

3. **The app builds the walkthrough** — this is the main event. It does **5 pieces of work**:
   - works out the *method* (the steps),
   - invents a *similar practice question* (so it never just hands Ade the answer — that's the law),
   - *solves that practice question* fully as a demo,
   - writes a *plain-English explanation* of what Ade's question is asking,
   - and quietly works out the *answer key* so it can mark Ade's attempts.

   If the question is a **calculation**, the deep thinker **o3** does all five. If it's an
   **explanation/essay** type, the cheaper all-rounder **gpt-4.1** does them.

4. **Ade has a go** — every time Ade types an answer, the app checks it (one small charge).
   Every time Ade asks a follow-up question, the app answers it (another small charge).

5. **If there was a diagram**, the artist **Gemini** draws a fresh one for the practice question.

6. **Everything gets read aloud** by **Inworld** (if audio is on).

That whole journey is **one session**. The big number at the top of the tool is the average
cost of that journey.

---

## The dials, explained one by one

### Section 1 — Users & volume

- **Active users / month** — how many distinct students use Homework Help in a month.
- **Sessions per user / month** — how many questions an average student brings. One *session* =
  one student taking one question through the whole flow (upload → walkthrough → complete).
- **Total sessions / month** (shown, not a slider) — the two multiplied together. This is the real
  volume driver: more users *or* more sessions each = a bigger monthly bill. (Neither changes the
  *per-session* cost — that's set by the dials further down.)

- **Calculation questions (%)** — out of all questions, how many are "work-it-out" maths/science
  problems versus "explain/write" essay ones.
  - Calculation → handled by the expensive deep thinker (**o3**).
  - The rest → handled by the cheaper all-rounder (**gpt-4.1**).
  - **Slide this up and the cost goes up**, because you're using the pricier supplier more often.

### Section 2 — How the question arrives

A student only ever uses **one** way to give their question per session, so by default you just
**pick one** from a short list (like ticking a box):

- **Typed text** — the student types it in. **Cheapest**, because nothing has to "read" an upload.
- **Photo / image** — the student snaps a picture. Costs a little extra to "read" it.
- **PDF / Word** — the student uploads a document. Same idea, slightly cheaper than a photo.

Whatever you pick is treated as *the* method for the session you're pricing.

- **"Model a mix across sessions" switch** — flip this on only if you want to be realistic about a
  *whole month* where different students use different methods. It swaps the single choice for three
  percentage sliders (e.g. 60% type, 30% photo, 10% document). The tool blends them and, if they
  don't add to 100%, quietly adjusts — nothing breaks. Leave it **off** for the simple "one session,
  one method" view.

- **"Does it contain a diagram?"** — only relevant when the method is an upload. It asks: of those
  uploads, how many actually have a *picture* in them (a graph, a shape, a chart). Only those trigger
  the **artist (Gemini)** to draw. If you chose *Typed text*, this is greyed out — typed questions
  never produce a drawing.

### Section 3 — Walkthrough depth

- **Average solution steps** — how many steps a typical walkthrough breaks into. More steps means
  more to **read aloud** (so more audio cost), and slightly longer explanations.

- **Build retry factor** — sometimes the app's first attempt at a walkthrough isn't good enough
  and it tries again. This dial says *how often* that happens, on average:
  - **1.0×** = it always nails it first time (cheapest),
  - **2.0×** = it always has to redo it (most expensive),
  - **1.15×** (the default) = it occasionally retries.

  Think of it as "how many do-overs the kitchen needs on average."

### Section 4 — Interaction

- **Attempts / session** — how many times the student types an answer to be checked. Each check
  is one small charge.
- **Follow-up questions / session** — how many times the student asks something mid-way
  ("why did we do that?"). Each answer is one small charge.

  More back-and-forth = more helpful for the student, but a bit more cost.

### Section 5 — Audio (the voice)

- **Generate audio (on/off switch)** — turn the voice on or off. Off = the **Inworld** cost
  drops to zero.

- The four sliders below it control **how much gets spoken**, measured in *characters* (letters):
  - **Chars / step** — how long each spoken step is.
  - **Chars / explanation** — how long the opening "here's what your question means" bit is.
  - **Fixed overhead chars** — the little intros and the "well done!" at the end.
  - **Chars / feedback + Q&A** — how long each spoken bit of feedback or answer is.

  Because Inworld charges *per letter*, more talking = more cost. The note under the sliders
  shows the total letters spoken per session so you can sanity-check it.

---

## Reading the results (right-hand side)

- **Big number ($ per session)** — the headline: average cost of one student's full session,
  blending everything together. This *is* "the cost of one user going through a homework session."

- **Per month / Per year** — that headline multiplied by how many sessions you run. This is the
  number that matters for budgeting.

- **Per user** (the two cards just below) —
  - *One session · 1 user, 1 question* — same as the headline, restated: what a single trip
    through the flow costs.
  - *Per user / month* — that single-session cost multiplied by the "sessions per user" slider, i.e.
    what one student costs you over a whole month. Slide *sessions per user* up and watch it climb.

- **Calculation session vs Explanation session** — two example price tags side by side:
  - A pure *calculation* session (uses the pricey deep thinker) — usually noticeably more.
  - A pure *explanation* session (uses the cheaper all-rounder) — usually less.

  Seeing both tells you *why* the calculation-% dial moves the total so much.

- **Cost per session by service** — coloured bars showing which supplier eats the most of your
  money. Usually it's a tug-of-war between **o3** (thinking) and **Inworld** (talking).

- **Cost per session by phase** — a table showing where the money goes across the *journey*
  (reading the upload, sorting the question, building the walkthrough, interaction, drawing,
  audio). Handy for spotting "oh, audio is half my cost" type insights.

---

## Advanced assumptions (the fine print at the bottom)

This section is for when you want the numbers to be *accurate to your real bills* rather than
my best-guess defaults.

- **Unit prices** — what each supplier actually charges you. My defaults are public list prices,
  **not your contract**. If you've negotiated rates, type them in here and everything above
  recalculates.

- **Per-call token assumptions** — a more technical table showing, for each piece of work, how
  much "reading" and "writing" it does. *You can leave this alone* unless you want to fine-tune.
  The one thing worth knowing: the deep thinker (**o3**) does a lot of invisible "thinking" that
  you still pay for, which is why its numbers look big.

---

## Three quick-start buttons (top of the tool)

- **Reset to defaults** — puts everything back to the sensible starting point.
- **Light usage preset** — a small, cheap deployment (few students, simple questions).
- **Heavy usage preset** — a big, busy deployment (lots of students, lots of calculation,
  lots of audio). Great for seeing your "worst case" bill.

---

## Content generation cost — the one-off build (separate section)

Near the bottom of the page there is a **separate** block titled *"Content generation cost — one-off build."*
It answers a different question from everything above it:

- Everything else on the page = the **running cost** of a student *using* Homework Help (pay-per-use, forever).
- This block = the **one-time cost** to *build the lesson content* in the first place — writing each lesson's
  script, recording its audio, drawing its ~30 whiteboard images, and the small helper calls. You pay it once
  per lesson when the content is generated, not every time a student opens it.

The figures here are **copied exactly** from the *General Cost Estimation Document* — the tool does not recompute
them, so they always match that source.

**Cost per lesson** (two possible content models):

| Content model | TTS | Content LLM | Image gen (×30) | Helpers | Total / lesson |
|---------------|-----|-------------|-----------------|---------|----------------|
| gpt-4.1 (OpenAI) | $1.5 – $2.0 | $0.7 – $1.0 | ~$1.89 | ~$0.01 | **≈ $4.1 – $4.9** |
| gpt-oss-120b (OpenRouter) | $1.5 – $2.0 | ~$0.50 | ~$1.89 | ~$0.01 | **≈ $3.9 – $4.4** |

**Whole curriculum, by key stage:**

| Key Stage 3 | Units | Lessons | Cost |
|-------------|-------|---------|------|
| Mathematics | 6 | 57 | $222.3 – $250.8 |
| English | 8 | 27 | $110.7 – $132.3 |
| Physics | 7 | 43 | $167.7 – $189.2 |
| Chemistry | 8 | 32 | $124.8 – $140.8 |
| Biology | 6 | 38 | $155.8 – $167.2 |
| **Total** | **35** | **197** | **$781.3 – $880.3** |

| Key Stage 4 | Units | Lessons | Cost |
|-------------|-------|---------|------|
| Mathematics | 6 | 74 | $288.6 – $325.6 |
| English | 11 | 38 | $155.8 – $186.2 |
| Physics | 7 | 34 | $132.6 – $149.6 |
| Chemistry | 10 | 49 | $179.4 – $202.4 |
| Biology | — | — | — |
| **Total** | **34** | **195** | **$756.4 – $863.8** |

**Whole curriculum (KS3 + KS4 combined): 69 units · 392 lessons · $1,537.7 – $1,744.1.**

> Two honesty notes: **Biology KS4** was left blank in the source document, so it is shown blank here rather than
> guessed. The **combined total** is simply the two Key-Stage totals added together — every other number is copied
> verbatim from the source.

---

## The honest caveats

- It's an **estimate**, like a fuel-cost calculator — close, but verify against your real invoices.
- The biggest unknown is how much "thinking" the deep thinker (**o3**) does. If your real bill is
  higher, nudge its output numbers up in the advanced section.
- The tool **doesn't** account for savings from caching (when the same audio or text is reused,
  you don't pay twice). So real costs will often be a little **lower** than what it shows —
  it errs on the safe side.

---

**Bottom line:** play with the dials in Sections 1–5, watch the big number and the coloured bars
move, and you'll quickly build an intuition for what makes Homework Help cheap or expensive to run.
