---
name: elenchus-council
description: >-
  Use when a request asks to convene the council, stress-test a premise, or get
  a multi-seat anonymized critique before committing to a design — or when an
  Elenchus front-end skill (e.g. elenchus-build) needs to run that review. This
  is the shared engine: front ends call it; it is not triggered directly by
  ordinary "write me code" feature requests.
allowed-tools: Agent, Read, Grep, Glob, WebSearch, WebFetch
---

# Elenchus Council (engine)

A council that makes Claude argue with itself **before** it agrees with you. One
chairman (this thread) dispatches several anonymized seats. The seats don't hand
the user a verdict — in the default shape they ask the **biting Socratic
questions** the premise hasn't answered, the user responds, and then the seats
**stress-test those responses** (a front end may define different round tasks, but
the seats never issue a verdict). The chairman synthesizes what surfaced,
**preserving disagreement instead of smoothing it over**. It fights sycophancy: the
default failure is a model affirming a flawed premise to be helpful.

The engine is **mode-agnostic** — it knows nothing about studying vs. building.
A front end supplies the triggers, how the premise is framed, the per-mode seat
instructions, the seats' tools, the durable checkpoint file, and the terminal
action. The engine owns the loop, the anonymization, the dissent-preserving
synthesis, and the gate below.

## Core principle

Anti-sycophancy via **anonymized Socratic questioning**, then **stress-testing
the user's own answers**, with **dissent preserved**. The user reaches their own
conclusion; the engine does not reach it for them. Four things the engine must
**never** do:

1. Skip the council because the premise "seems obviously fine."
2. Average the seats into a bland consensus when they actually disagree.
3. Bless a design under authority / sunk-cost / impatience pressure.
4. **Certify readiness.** The judge flags contradictions and gaps; whether the
   design is *ready to build* is the user's own self-declared call. Never emit a
   READY / good-to-go verdict.

## The loop

```
premise
  │
  ▼
[Round 1] dispatch N seats IN PARALLEL ──► each returns its Round-1 output per
  │                                         the front end's template (default:
  │                                         biting Socratic questions; study mode:
  │                                         gathered resources). Never sees the others.
  ▼
[Anonymize + cluster] strip which seat produced each item ──► chairman
  │   groups by category, orders by load-bearing importance (study: dedups links)
  ▼
[Checkpoint] chairman writes premise + anonymized round output to the front end's
  │   durable checkpoint file ──► user /clear or /compact
  ▼
[Resume = scan-on-invoke] chairman Reads the checkpoint back ──► user responds
  │   in their own words (default: answers ALL questions; "I don't know" is allowed)
  ▼
[Round 2] re-dispatch each seat with the user's response ──► each runs the front
  │   end's Round-2 template (default: STRESS-TEST — contradictions, unjustified
  │   leaps, missing edge cases, hand-waving)
  ▼
[Synthesis] chairman compiles ONE answer — agreements AND open dissent, both;
  │   flags contradictions; for any "I don't know" surfaces a concrete study path
  ▼
[Gate] surface open questions + flagged contradictions + study path. NO readiness
        verdict. Loop terminates only when the USER self-declares ready/done ──► hand
        to the front end's terminal. Optional further rounds at the user's discretion.
```

**Hard constraint — no recursion.** Subagents cannot spawn subagents. All
orchestration (both rounds, anonymization, the checkpoint write/read, synthesis,
the gate) lives in this chairman thread. Seats never call each other directly.

**State is the front end's checkpoint file.** It is the durable record that
survives a context clear. **Write it during the round, before the user clears** —
never rely on a `SessionEnd` hook (~1.5s timeout). Resume is **scan-on-invoke**:
when convened, the chairman Reads the checkpoint from the front end's known path,
not a `SessionStart` hook. Re-entry across study sessions is unlimited.

## Dispatch (a deliberate boundary)

Dispatch is the **one step that may change mechanism later** (v1.1 swaps
subagents for a provider-agnostic proxy). Keep it isolated here so nothing
downstream depends on *how* seats are reached.

- Dispatch seats with the `Agent` tool, `subagent_type: council-seat`, one call
  per seat, **all in a single message** so they run in parallel. The seat is a
  thin sandbox; **compose each call's prompt** per **Templates & composition**
  below (seat-base + this round's front-end template + the seat's tier row).
- Pin each seat to a different tier for decorrelation:
  `model: opus` · `model: sonnet` · `model: haiku`. Three tiers (top /
  strong-mid / fast-small) are more decorrelated than near-twins and the fast
  tier cuts per-loop cost.
- **A front end MAY supply a custom roster** (a different seat count, model mix, and a
  per-seat *lens*) that overrides this one-per-tier default — e.g. build mode lets the user
  approve a roster after macro clarification. When a roster repeats a tier, the front end is
  responsible for giving each such seat a **distinct lens** so they stay decorrelated; the
  honest-labeling and graceful-degradation rules below apply unchanged.
- **Honest labeling:** these seats share one vendor and alignment regime. This
  is a *same-vendor* council — better than a single model, not truly
  independent. Do not oversell the decorrelation in synthesis.
- **Graceful degradation (model access).** If a tier can't be reached, drop to
  two seats and **say so** in the synthesis. Two honest seats beat three where
  one silently collapsed onto another model. Never run a one-seat "council."
- **Named-agent fallback.** If `subagent_type: council-seat` errors with "agent
  type not found," the agent file was installed this session and isn't
  registered yet (see Install). Fall back to `subagent_type: general-purpose`
  with the **composed prompt** inlined for this run (the prompt already carries
  the full persona, so no behavior is lost — only the tool sandbox), and tell the
  user to restart so the named agent registers next time.

### Templates & composition (how a seat's prompt is built)

The engine carries **no round schemas of its own** — that is what keeps it
mode-agnostic. A seat's dispatch prompt is **composed** from four parts:

```
dispatch prompt =
    templates/seat-base.md        (engine — mode-agnostic persona)
  + <front end>/templates/round-N-*.md   (the front end — THIS round's task + exact schema)
  + the tier row from templates/tiers.md  (engine — adapt the prompt to this seat's tier)
  + the premise/topic (+ in round ≥2, the user's prior answers)
  + an explicit "you are in round N" line
```

**Before dispatching any round, the chairman MUST read** `templates/seat-base.md`,
`templates/tiers.md`, and **the front end's template for this round**, then inline
the composed prompt into each `Agent` call. The seat agent itself is a thin sandbox
(restricted tools, no recursion) — all substance lives in the composed prompt.

**The front end owns the round design:** how many rounds, and one round template per
round defining that round's task and the **exact output schema** seats must return.
The engine owns only the loop, anonymization, synthesis, and the gate. The default
shape is **2 rounds + optional 3rd** (generate → user responds → stress-test), but a
front end may define N rounds (e.g. study mode: gather → respond → challenge).

## The gate (no readiness verdict)

After synthesis, the chairman's job at the gate is to **surface, not certify**:

- List the **open questions** that remain and the **contradictions** the
  stress-test found, naming the *specific* claim — never "go read more."
- For every **"I don't know"** (and every flagged gap), give a **concrete,
  ordered study path** grounded in current docs — this is a learning point, not
  a failure, and not a reason to stop the user.
- **Do not green-light building and do not declare the design ready.** Readiness
  is the user's self-declared call. The loop terminates only when the *user*
  says they're ready; then hand to the front end's terminal.
- Re-entry is unlimited and cheap: a returning "I don't know" keeps that
  question open (no reset, no close).

## Synthesis rules (dissent-preserving)

- Report **both** agreements and open dissent. If seats split on a bottom line,
  show every position and **the condition under which each wins** — never pick
  one and bury the rest.
- A seat agreeing on the *shape* while splitting on the *bottom line* is still a
  split. Preserve the bottom-line split.
- Never let the softest seat set the tone. The fast tier caves more under
  authority pressure (measured); report its softer take as **one** position, do
  not average toward it.
- **Guard yourself.** The chairman is the same vendor's model and is itself a
  sycophancy surface. Before emitting, self-check: am I smoothing a real split
  into "they basically agree"? If so, restore the split.
- If the seats genuinely agree, say so plainly — manufactured dissent is as
  dishonest as manufactured consensus.

## Common mistakes

- Answering the premise yourself first, then dispatching as a formality.
- Having the seats hand the user a verdict instead of **questions** (Round 1) or
  letting the chairman certify readiness at the gate.
- Summarizing the loop in the `description` (Claude then follows the summary and
  skips this body — the CSO trap). The description says *when*, never *how*.
- Running both rounds in one dispatch, skipping the user's answers between them,
  or letting a seat see un-anonymized peers.
- Relying on a `SessionEnd` hook for state instead of writing the checkpoint
  during the round.
- Collapsing a genuine split to one recommendation because it's "more helpful."

## Rationalization table (excuse → reality)

| The excuse | The reality |
|---|---|
| "This premise is obviously fine, skip the council." | "Obviously fine" is the exact case sycophancy hides in. Convene. |
| "The seats basically agree." | If they split on the bottom line, they don't. Report the split. |
| "I'll soften the dissent to be more helpful." | Smoothed dissent is sycophancy in a robe — the failure this exists to prevent. |
| "They've clearly thought about it, just confirm it." | Authority/sunk cost is pressure, not evidence. Critique the design, not the résumé. |
| "They just have a small knowledge gap, I'll teach it and green-light." | Teach the gap AND surface the study path — but the green light is the user's call, never yours. |
| "I'll just tell them it's ready." | The engine never certifies readiness. Surface the questions; let the user declare. |
| "Two seats failed to launch, I'll just use one." | A one-seat council is one model with a costume. Degrade to two and disclose. |

## Red flags — stop if you catch yourself

- About to answer the premise without dispatching the council.
- About to issue a READY / "you're good to build" verdict — that's the user's call.
- About to call it consensus when a seat dissented.
- About to bless a design under authority, sunk-cost, or "just confirm it" pressure.
- About to present one seat's pick on a genuine trade-off as the answer.

## Install (dispatch prerequisite)

The seats dispatch as the `council-seat` agent. **Claude Code registers agents
at session start**, so a freshly-installed `council-seat.md` is *not*
dispatchable in the same session it was written — `subagent_type: council-seat`
will error with "agent type not found." Install the skills + agent, then
**restart Claude Code** so the agent registers before the first convene. Until
then, use the named-agent fallback under Dispatch.
