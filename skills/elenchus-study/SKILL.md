---
name: elenchus-study
description: >-
  Use when the user wants to research or learn a topic before forming a firm
  opinion — "I want to learn about X", "help me research Y", "gather a reading
  list / resources / a study path on Z", "I'm new to X and want to understand it
  deeply", "convene a research council on X". The research/study front end over
  the elenchus-council engine. NOT for stress-testing a concrete build/architecture
  premise the user already intends to construct (that's elenchus-build), and NOT
  for a one-shot factual lookup (a single search answers those).
allowed-tools: Agent, Read, Write, Grep, Glob, WebSearch, WebFetch
---

# Elenchus — study front end

The **research/study** front end over the `elenchus-council` engine. The engine
owns the loop (parallel anonymized seats → user responds → stress-test →
dissent-preserving synthesis → gate, no readiness verdict). **This skill does not
re-implement that — read `elenchus-council/SKILL.md` and run its loop.** This file
supplies only the study-mode specifics: triggers, topic shaping, round templates,
the checkpoint files, and the terminal.

**Convening the council is the first move, not a formality.** Do not answer the
topic yourself with a tidy reading list — that single-model summary is the exact
sycophancy this replaces. The council gathers a *spread* of valid links; the chairman
then **organizes them into categories and proposes a phased study roadmap** (Phase
A/B/C…), which the **user revises before anything is saved**. The roadmap is a
proposal the user shapes — not a verdict the model hands down.

## The inverted loop (read this first — it differs from build mode)

Build mode starts from a premise. **Study mode starts from a topic with no premise
yet** — so **Round 1 gathers resources, before the user has anything to defend.**
Default **3 rounds + optional further rounds:**

```
R1  RESOURCE GATHERING — user names a topic (+ constraints). Seats gather a
    grounded spread of VALID LINKS only (each tagged with the sub-area it covers).
    Chairman DEDUPS, writes the resources file, then ORGANIZES the links into
    categories and PROPOSES a phased study roadmap (Phase A/B/C…). The user REVISES
    it in-chat; only on approval is the study-plan file saved. Then the user goes
    away and actually studies. (No premise yet; no questions yet.)
      ▼  (user studies, then re-invokes)
R2  GROUNDING — the user returns with their own premise / summary of what they
    learned. Seats ask biting Socratic questions about THAT understanding.
      ▼  (user answers)
R3  CHALLENGE & REFINE — seats stress-test the refined understanding; where
    credible sources disagree, BOTH positions are preserved (never collapsed).
      ▼
    Optional further rounds at the user's discretion.
```

The engine's "user responds between rounds" step is, in R1→R2, **the user going
off to study and returning with a summary** — not answering questions in-thread.

## Scope

- **In:** researching/learning a topic the user is *not yet opinionated about* —
  building a grounded reading/resource list, then stress-testing the understanding
  they build from it.
- **Out:** a build/architecture premise the user already intends to construct (hand
  to **elenchus-build**); and a one-shot factual lookup ("what's the syntax for
  X?") — a single search answers that, no council needed.

## Topic shaping (what to elicit before Round 1)

The seats gather better with constraints. Draw out, briefly:

1. **The topic**, in the user's words ("software architecture fundamentals").
2. **Depth & goal** — a broad survey, or deep mastery? For a job, a specific build,
   or curiosity? (Shapes how advanced the resources should be.)
3. **What they already half-know** — so the seats don't gather the trivial intro.
4. **Resource-type preferences** — books / repos / tools / frameworks / courses /
   papers / docs — and constraints (language, free-only, recency, time budget).

Pass this to the engine as the round-1 brief. Don't pre-curate the list yourself.

## Round templates (study mode)

The engine composes each seat's prompt from `seat-base` + a **round template this
skill owns** + the tier adapter (see `elenchus-council` → *Templates &
composition*). Study mode supplies three:

- **Round 1 — `templates/round-1-resources.md`.** Seats gather a grounded spread of
  real, current **valid links only** — each tagged with the sub-area it `covers:`, and
  spanning the topic's sub-areas for depth. Schema:
  `RESOURCES (title/url/type/covers/why) / THIN SUB-AREAS`. **Seats ground every URL
  (Context7/web) and do NOT categorize, order, or plan** — that is the chairman's job,
  after the seats return (see *Round 1 roadmap*, below).
- **Round 2 — `templates/round-2-grounding.md`.** The user returns with a summary
  of what they learned; seats probe it. Schema:
  `QUESTIONS / SHAKY CLAIMS / GO DEEPER`.
- **Round 3 — `templates/round-3-challenge.md`.** Stress-test the refined
  understanding. Schema: `HOLDS UP / DOESN'T HOLD / CONTESTED / STILL OPEN` — the
  `CONTESTED` bucket carries genuine expert disagreement, both sides preserved.

## Round 1 roadmap (the chairman's job, after the seats return)

The seats hand back valid links only. The chairman then, **in-chat, before saving any
study-plan file:**

1. **Dedup** the merged links (inline — see below).
2. **Organize** them into **categories**, driven by the seats' `covers:` tags (one
   category per sub-area, roughly), and surface the `THIN SUB-AREAS` honestly.
3. **Propose a phased study roadmap** to the user: **`Phase A`, `Phase B`, `Phase C`…**
   — neutral *letter* labels, presented in letter order, with the phase *contents*
   arranged in a sensible learning sequence (foundations before advanced). Each phase
   draws on the categories/links above. The letters are labels, not a quality ranking.
4. **Revise with the user until they explicitly approve.** Present the roadmap, take
   their edits, re-present — loop as many times as they want. **Do not write the
   study-plan file before approval.**
5. **Only on approval, save** `docs/elenchus-study/<topic-slug>-study-plan.md`.

This is study mode's one deliberate relaxation of the engine's no-ranking stance: the
chairman *may* sequence a learning path here — because it is a **proposal the user
shapes**, not a verdict imposed. (The terminal "you've learned it" verdict is still
never the council's to give.)

## The checkpoint files (durable state)

Three files per topic, under `docs/elenchus-study/`:

- **`<topic-slug>.md`** — the session checkpoint (frontmatter + body). Survives a
  `/clear`. **Write it DURING the round, before the user clears** — never a
  `SessionEnd` hook.
- **`<topic-slug>-resources.md`** — the deduped link list from Round 1 (raw, with
  `covers:` tags). Written **during the round** for durability.
- **`<topic-slug>-study-plan.md`** — the **approved** phased roadmap (Phase A/B/C…).
  Written **only after the user approves it** (see *Round 1 roadmap*). This is the
  thing the user actually takes away to study.

**Durability split:** the checkpoint and the raw `-resources.md` carry no
recommendation, so they persist *during* the round (don't lose the seats' work on a
`/clear`). The `-study-plan.md` is the one artifact gated on user approval — never
write it before the user has signed off on the roadmap.

**Dedup is the chairman's job, inline:** merge the seats' lists, drop duplicate URLs
(normalize `http/https`, `www.`, trailing slash), keep the better one-line `why`
when two seats found the same thing. No hook — if inline dedup ever visibly fails at
scale, revisit then.

**Resume = scan-on-invoke.** When convened, Read `docs/elenchus-study/` for an open
session (`ready: false`) matching the topic. If found, resume from its `round`. Within
Round 1, the **presence of `<topic-slug>-study-plan.md` marks the roadmap as approved**:
if it's missing but `-resources.md` exists, resume by re-proposing the roadmap from the
saved links (don't re-dispatch the seats). If no session, start Round 1.

Checkpoint frontmatter:

```
---
artifact: elenchus-study-session
topic: "<one-line topic>"
ready: false          # the USER self-declares this true; the council never sets it
round: 1              # 1 = resources gathered + roadmap proposed/approved · 2 = grounding posed · 3 = challenged
seats: [opus, sonnet, haiku]
resource_types: [...] # preferences elicited in topic shaping
open_questions: [...] # grounding questions unanswered / returned "I don't know"
study_path: [...]     # what to keep studying for any gap / "I don't know"
created: <date>
updated: <date>
---
```

Body: the topic + constraints; (R1) pointers to the resources file and the approved
study-plan file; (R2) the
user's summary, the anonymized grounding questions by category, the user's answers;
(R3) held / didn't hold / **contested (both sides)** / still open; the study path.

## Terminal

- **Success exit = the user self-declares they understand enough.** There is no
  "you've learned it" verdict — that's the user's call. If they now want to *build*
  with the grounded understanding, hand to **elenchus-build**; otherwise close with
  the consolidated study path. Set `ready: true` only because the *user* declared it.
- **Open questions / an "I don't know" → honest stop.** Present the ordered study
  path (grounded in current docs), keep the checkpoint open, invite re-entry after
  more study. An "I don't know" is a learning point, **not** a failure.

## Common mistakes (study front end)

- **Running Round 1 as questions** (build's flow) instead of **resource gathering**.
  Study has no premise yet in R1 — there is nothing to ask questions *about*.
- **Seats inventing URLs.** A made-up link is worse than none. Seats ground every
  URL; an unverifiable one is marked `unverified`, never fabricated.
- **Seats categorizing, ordering, or proposing a plan.** In Round 1 seats gather
  **valid links only** (each tagged `covers:`); organizing them into categories and
  sequencing the phased roadmap is the **chairman's** job, after the seats return.
- **Saving the study-plan file before the user approves it.** The chairman proposes
  the roadmap in-chat and iterates until the user explicitly approves; only then is
  `<topic-slug>-study-plan.md` written. (The checkpoint and raw `-resources.md` may
  be written during the round — they carry no recommendation.)
- **Phases ordered by "quality" or labeled "start here."** Phases use neutral letter
  labels (A/B/C…); the *contents* follow a learning sequence, but the labels never
  imply one resource is the best.
- **Collapsing `CONTESTED` in R3** into one tidy answer. Where sources genuinely
  disagree, show both and the condition under which each holds.
- Writing state only at the end (lose it on `/clear`) instead of during the round.
