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

### Section 1 — Volume & question mix

- **Homework sessions / month** — simply how many times students use the feature in a month.
  More sessions = bigger monthly bill. (Doesn't change the *per-session* cost.)

- **Calculation questions (%)** — out of all questions, how many are "work-it-out" maths/science
  problems versus "explain/write" essay ones.
  - Calculation → handled by the expensive deep thinker (**o3**).
  - The rest → handled by the cheaper all-rounder (**gpt-4.1**).
  - **Slide this up and the cost goes up**, because you're using the pricier supplier more often.

### Section 2 — How questions arrive

- **Typed text (%)** — the student just types. **Cheapest**, because nothing has to "read" an upload.
- **Photo / image (%)** — the student snaps a picture. Costs a little extra to read it.
- **PDF / Word (%)** — the student uploads a document. Same idea, slightly cheaper than a photo.

  > These three should roughly add up to 100% (they're three ways the *same* question can arrive).
  > If they don't, the tool just adjusts them proportionally and shows a small note — nothing breaks.

- **Of uploads, share with a diagram (%)** — of the photos/documents, how many actually have a
  *picture* in them (a graph, a shape, a chart). Only these trigger the **artist (Gemini)** to draw.
  More diagrams = more drawing = more cost.

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
  blending everything together.

- **Per month / Per year** — that headline multiplied by how many sessions you run. This is the
  number that matters for budgeting.

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
