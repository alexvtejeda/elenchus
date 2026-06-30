---
name: elenchus-build
description: >-
  Use when the user wants a build or architecture idea stress-tested before they
  commit to building it — "help me plan/design this app", "design the
  architecture for X", "review my architecture before I build", "is my mental
  model of X sound", "I want to build Y because Z — poke holes in it". For the
  still-articulating stage, before brainstorming. NOT for ideas already decided
  (that's brainstorming), NOT for researching/learning a topic the user has no
  premise about yet ("I want to learn about X" / "gather resources on Y" — that's
  elenchus-study), and NOT for an over-engineering / flaw yes-no verdict ("is X
  over-engineering?") — a single high-tier model can answer those.
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

This is the premise. Don't pre-critique it — but **don't dispatch on it yet either.**
First run **Macro clarification** below to give the seats a macro vision, then propose a
**Seat roster**. Both happen in the chairman thread, before Round 1.

## Macro clarification (before Round 1)

The seats are strong on **architecture, tools, and logic** but **rarely reach for the
frontend** on their own. So before dispatching, the chairman builds a **macro vision** of
the project and feeds it into every seat's prompt — that is what lets the seats ask
grounded questions across *all* the project's aspects (frontend included), not just the
backend slice they gravitate to.

**Ask the macro questions one at a time, in chat.** Do **not** dump a list, and do **not**
spin up one markdown file per question. Ask one, wait for the answer, ask the next. Record
each Q&A into the checkpoint's *Clarifying Q&A* section as it lands (chairman asked / user
answered), so it survives a `/clear`.

Cover at least these axes — skip any the premise already settled, follow up where an answer
opens a new gap:

- **Platform.** Web app? Mobile (one OS or multiplatform)? Desktop (which framework)? CLI?
  A mix? "Is this multiplatform, or one target first?"
- **Frontend stack.** Framework / rendering model / component system in mind — or undecided.
- **Backend & services.** Runtime, data store, third-party APIs, auth, hosting.
- **Users & scale.** Who uses it, how many, what's the load-bearing UX path.
- **Greenfield vs existing.** New build, or a feature inside a running system with constraints.

**When a framework choice is undecided, offer elenchus-study.** If the user is unsure which
framework/library to pick, say so and offer to dispatch **elenchus-study** to benchmark the
candidates on community feedback before continuing — don't guess one into the premise.

## Seat roster (proposed, then approved)

After the clarifying questions — as a **separate** step — the chairman proposes a seat
roster, then the user approves or edits it. The engine's default is one seat per tier
(opus/sonnet/haiku); build mode **replaces that with the approved roster**: any seat count,
any model mix, each seat carrying a **lens**.

**Propose, grounded in the answers — never guessed.** State the count, the model per seat,
and *why each lens earns its seat*, tied to what the user actually said. Example shape:

> "Here's my proposed roster — 2 opus, 4 sonnet, 1 haiku. The two opus seats take the
> **frontend** (you're going multiplatform Flutter, that's where the load-bearing risk
> is). Three sonnet seats split the **backend** (sync engine, data model, auth). One sonnet
> takes **integrations** (the Stripe + push pieces). The haiku seat is a **macro-alignment**
> check — it holds the whole picture and flags aspects the others missed. Roughly N seat-calls
> per round."

- **Propose freely; add a one-line cost note** (≈ seat-calls per round) and let the user trim.
- **Lenses do the decorrelating within a tier.** Repeated tiers are fine (e.g. 4 sonnet) —
  give each a **distinct lens** (frontend / a specific backend slice / integrations /
  macro-alignment) so they don't collapse onto the same answer. The engine's honest-labeling
  still holds: same vendor, better than one model, not truly independent.
- **The user owns the final roster.** They approve as-is or specify their own count, models,
  and lens split. Record the approved roster in the checkpoint (`seats:` as `{model, lens}`).
- **Graceful degradation unchanged:** if an approved tier can't be reached, drop that seat,
  say so, never silently re-assign its lens to a duplicate model.

## Round templates (build mode)

The engine composes each seat's prompt from `seat-base` + a **round template this
skill owns** + the tier adapter (see `elenchus-council` → *Templates &
composition*). Build mode supplies three:

- **Round 1 — `templates/round-1-questions.md`.** The biting questions a senior reviewer
  would ask about *this* design (the un-named failure mode, the edge case, "can you actually
  explain this part?"). Schema: `QUESTIONS / UNEXAMINED ASSUMPTIONS / WHERE TO LOOK`. **The
  chairman injects, per seat, that seat's assigned LENS (from the roster) and the MACRO
  CONTEXT (from the clarifying Q&A)** into the composed prompt — so each seat asks within its
  lens (including the frontend the seats normally skip) while holding the whole-project view.
- **Round 2 — `templates/round-2-stress-test.md`.** Stress-test the user's answers
  for contradictions, unjustified leaps, and hand-waving. Schema:
  `HOLDS UP / DOESN'T HOLD / STILL OPEN`.
- **Round 3 — `templates/round-3-spec-check.md`** (terminal only, runs once the
  user self-declares ready — see *Terminal*). Seats audit the chairman's **draft
  spec** against the session record for fidelity and completeness, not the user's
  design. Schema: `CAPTURED FAITHFULLY / MISSING / MISREPRESENTED`.

**Tools/grounding:** the council-seat sandbox carries Read/Grep/Glob/WebSearch/
WebFetch + **Context7 MCP**. In build mode the seats ground every framework / API
the user named against **current docs** (Context7 first, web second) — both to ask
accurate questions and to point at a concrete, current study path, not generic
advice.

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
platform: "<web | mobile | desktop | cli | multiplatform | ...>"   # from clarifying Q&A
macro:                # the macro vision injected into every seat (from clarifying Q&A)
  frontend: "<stack or 'undecided'>"
  backend: "<runtime/data/services>"
  users_scale: "<who / how many / load-bearing path>"
  greenfield: <true|false>
seats:                # the USER-approved roster (replaces the engine's one-per-tier default)
  - {model: opus,   lens: frontend}
  - {model: sonnet, lens: backend-sync}
  - {model: haiku,  lens: macro-alignment}
frameworks: [...]     # tools/APIs the seats grounded via Context7/web
open_questions: [Q1, Q2, ...]   # ids unanswered or returned "I don't know"
resolved: [...]
study_path: [...]     # concepts to study for any "I don't know" / flagged gap
spec_path: null       # set to docs/superpowers/specs/<date>-<slug>.md once written
created: <date>
updated: <date>
---
```

Body: the premise; a **Clarifying Q&A** section (each macro question the chairman asked
in chat + the user's answer, in order — written as it lands, before any `/clear`); the
Round-1 questions grouped **by category** (anonymized — strip which seat asked), each with
an id; an **answers** section; a **stress-test** section (held / didn't hold / still open +
contradictions); and the **study path**.

## Terminal

- **Success exit = the user self-declares ready.** This does **not** end with a bare
  hand-off — it ends with a **verified spec** that pins down what the session settled,
  produced in four steps (Spec synthesis, below): the chairman drafts → the council
  verifies the draft (Round 3) → the chairman revises → the user finalizes it. The spec
  is the input the **brainstorming skill** then reviews (and from there, writing-plans).
  Elenchus is the stress-test *before* brainstorming; the spec is the bridge between them.
  Set `ready: true` in the checkpoint only because the *user* declared it.
- **Open questions / an "I don't know" → honest stop.** Present the ordered study
  path (grounded in current docs), keep the checkpoint open, and invite re-entry
  after study. An "I don't know" is a learning point, **not** a failure — and
  **not** your cue to teach the gap and green-light building anyway. Teach if
  asked, but the green light is the user's call. Never certify readiness. Do **not**
  write a spec while questions are still open unless the user explicitly asks for an
  interim spec that records the gaps as open.

## Spec synthesis (the terminal artifact)

Once the user self-declares ready, pin the session down into a spec the brainstorming
skill can consume. The spec is a **faithful record**, not a green light: it carries the
settled decisions *and* the dissents and open questions, with their reasoning intact.

1. **Draft.** From the checkpoint, the chairman writes a draft to
   `docs/elenchus/<slug>-spec-draft.md` covering:
   - **Premise & goal** — what's being built and the *why* behind it.
   - **Settled decisions** — each decision that survived stress-test, with the
     reasoning that made it hold (not flattened to a bare assertion).
   - **Grounded frameworks / APIs** — what was checked against current docs, and how firm.
   - **Constraints & non-goals** surfaced during the rounds.
   - **Preserved dissents** — where the seats split, *both* positions and the condition
     under which each wins. Never smooth these into "agreed."
   - **Open questions / study path** still outstanding (if the user chose to spec anyway).
2. **Verify (Round 3 — full parallel council).** Dispatch the seats via the engine with
   `templates/round-3-spec-check.md`, giving each the **session record + the draft**.
   They audit fidelity, not the design (`CAPTURED FAITHFULLY / MISSING / MISREPRESENTED`).
   Anonymize and synthesize as in any round.
3. **Revise.** The chairman fixes every `MISSING` / `MISREPRESENTED` finding — restoring
   dropped decisions, un-smoothing dissent, removing invented certainty. Re-verify if the
   revisions were substantial.
4. **Finalize on the user's say-so.** Present the verified draft. **Only after the user
   confirms**, the chairman writes the final to
   `docs/superpowers/specs/<YYYY-MM-DD>-<slug>.md` and records that path in the
   checkpoint's `spec_path`. The user owns this call — do not write into `specs/` or
   treat the spec as a build green light without explicit confirmation. Then point the
   user at the **brainstorming skill** over that spec file.

## Common mistakes (build front end)

- Answering the architecture question directly because it "seems simple" instead
  of convening the council.
- Skipping the macro clarification and dispatching seats with no macro vision — so the
  seats ask only backend questions and the frontend goes unexamined.
- Dumping all the clarifying questions at once, or spinning up a markdown file per
  question, instead of asking them one at a time in chat.
- Dispatching the fixed three opus/sonnet/haiku seats without proposing a roster, or
  proposing a roster the user never approved.
- Repeating a tier across seats without giving each a **distinct lens** — duplicate models
  with the same lens are one model in a costume.
- Converting "the user can't explain their own design" into "a small gap I'll
  teach, then they can start." Surface the study path; withhold the green light.
- Letting the chairman declare the design ready. Readiness is the user's call.
- Writing state only at the end (lose it on `/clear`) instead of during the round.
- Smoothing a genuine bottom-line split between seats into "they basically agree."
- Smoothing that same split *out of the spec* — dropping a preserved dissent or open
  question so the spec reads cleaner than the session actually was.
- Writing the spec yourself and skipping the Round 3 council verification, or treating
  its `CAPTURED FAITHFULLY` as a readiness sign-off rather than a fidelity check.
- Writing the final into `docs/superpowers/specs/` (or calling the spec a green light to
  build) before the user explicitly confirms. Drafting and placement are different calls.
