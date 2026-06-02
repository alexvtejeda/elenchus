---
name: elenchus-build
description: >-
  Use when the user wants a build or architecture idea stress-tested before they
  commit to building it — "help me plan/design this app", "design the
  architecture for X", "review my architecture before I build", "is my mental
  model of X sound", "I want to build Y because Z — poke holes in it". For the
  still-articulating stage, before brainstorming. NOT for ideas already decided
  (that's brainstorming) and NOT for an over-engineering / flaw yes-no verdict
  ("is X over-engineering?") — a single high-tier model can answer those.
allowed-tools: Agent, Read, Write, Grep, Glob, WebSearch, WebFetch
---

# Elenchus — build front end

The **build/architecture** front end over the `elenchus-council` engine. The
engine owns the loop (Socratic questions → user answers → stress-test →
dissent-preserving synthesis → gate, no readiness verdict). **This skill does
not re-implement that — read `elenchus-council/SKILL.md` and run its loop.**
This file supplies only the build-mode specifics: triggers, premise shaping,
seat instructions, seat tools, the checkpoint file, and the terminal.

**Convening the engine is the first move, not a formality.** Do not answer the
premise yourself, even when the build "seems simple" — that shortcut is the
exact sycophancy this exists to prevent.

## Scope

- **In:** stress-testing a build/architecture premise — a single feature or a
  whole app from scratch — that the user is still articulating.
- **Out:** an idea the user has already settled (hand to brainstorming); and an
  over-engineering / flaw **verdict** ("is feature X over-engineering?"). That
  framing invites a yes/no and sycophancy; a single high-tier model can give it.
  Elenchus deliberately replaces the verdict with gap-exposure.

## Premise shaping (what to elicit before Round 1)

Get the user's **mental model in their own words**, enough for the seats to find
where it's thin. Draw out:

1. **What the app/feature is**, and **what they want to build** in this round.
2. **Why** — the goal behind it ("I want feature Y because I think it boosts
   activity"). The *why* is where the load-bearing assumptions hide.
3. **The key frameworks / APIs / services** they intend to use.
4. **Scope:** a feature on an existing app, or an app from scratch.

Pass this to the engine as the premise. Don't pre-critique it.

## Seat instructions & tools (build mode)

- **Lens:** architecture. Round 1 — ask the biting questions a senior reviewer
  would ask about *this* design (the un-named failure mode, the edge case, the
  "can you actually explain this part?"). Round 2 — stress-test the user's
  answers for contradictions, unjustified leaps, and hand-waving.
- **Tools:** the council-seat agent already has Read/Grep/Glob/WebSearch/WebFetch
  plus **Context7 MCP**. In build mode the seats should ground every framework /
  API the user named against **current docs** (Context7 first, web second) — both
  to ask accurate questions and to point at a concrete, current study path rather
  than generic advice.

## The checkpoint file (durable state)

One markdown file per premise is the durable record that survives a `/clear`.

- **Path:** `docs/elenchus/<premise-slug>.md` (slug = lowercase, hyphenated, from
  the premise; e.g. `docs/elenchus/pelu-geocoding.md`).
- **Write it DURING the round, before the user clears** — never rely on a
  `SessionEnd` hook. After Round 1, write the premise + anonymized, categorized
  questions, then tell the user to `/clear` or `/compact` and re-invoke. After
  Round 2, update with what held, the flagged contradictions, and the study path.
- **Resume = scan-on-invoke.** When convened, Read `docs/elenchus/` for an open
  session (`ready: false`) matching the premise. If found, resume from its
  `round`: read the premise + open questions back to the user and collect their
  answers, then dispatch Round 2. If none, start Round 1.

Frontmatter schema (mirrors the readiness-session prototype):

```
---
artifact: elenchus-build-session
premise: "<one-line premise>"
ready: false          # the USER self-declares this true; the council never sets it
round: 1              # 1 = questions posed, awaiting answers · 2 = answers stress-tested
seats: [opus, sonnet, haiku]
frameworks: [...]     # tools/APIs the seats grounded via Context7/web
open_questions: [Q1, Q2, ...]   # ids unanswered or returned "I don't know"
resolved: [...]
study_path: [...]     # concepts to study for any "I don't know" / flagged gap
created: <date>
updated: <date>
---
```

Body: the premise; questions grouped **by category** (anonymized — strip which
seat asked), each with an id; an **answers** section; a **stress-test**
section (held / didn't hold / still open + contradictions); and the **study
path**.

## Terminal

- **Success exit = the user self-declares ready.** Then hand the grounded premise
  to the **brainstorming skill** — the step Elenchus precedes (brainstorming
  assumes you already know what to build; Elenchus is the stress-test before
  that). Set `ready: true` in the checkpoint only because the *user* declared it.
- **Open questions / an "I don't know" → honest stop.** Present the ordered study
  path (grounded in current docs), keep the checkpoint open, and invite re-entry
  after study. An "I don't know" is a learning point, **not** a failure — and
  **not** your cue to teach the gap and green-light building anyway. Teach if
  asked, but the green light is the user's call. Never certify readiness.

## Common mistakes (build front end)

- Answering the architecture question directly because it "seems simple" instead
  of convening the council.
- Converting "the user can't explain their own design" into "a small gap I'll
  teach, then they can start." Surface the study path; withhold the green light.
- Letting the chairman declare the design ready. Readiness is the user's call.
- Writing state only at the end (lose it on `/clear`) instead of during the round.
- Smoothing a genuine bottom-line split between seats into "they basically agree."
