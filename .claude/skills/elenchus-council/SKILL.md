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
chairman (this thread) dispatches several anonymized seats that critique the
premise and each other, then synthesizes an answer that **preserves the
disagreement instead of smoothing it over**. It fights sycophancy: the default
failure is a model affirming a flawed premise to be helpful.

The engine is **mode-agnostic** — it knows nothing about studying vs. building.
A front end supplies the triggers, how the premise is framed, the per-mode seat
instructions, the seats' tools, and the terminal action. The engine owns the
loop, the anonymization, the dissent-preserving synthesis, and the conclusion
gate below.

## Core principle

Anti-sycophancy via **anonymized all-pairs peer review**, with **dissent
preserved** and an **honest stop** when the user can't yet ground their own
design. Three things the engine must never do:

1. Skip the council because the premise "seems obviously fine."
2. Average the seats into a bland consensus when they actually disagree.
3. Bless a design under authority/sunk-cost/impatience pressure.

## The loop

```
premise
  │
  ▼
[Round 1] dispatch N seats IN PARALLEL ──► each answers the premise blind
  │                                         (never sees the others)
  ▼
[Anonymize] strip seat identities ──► relabel outputs Seat A / B / C
  │
  ▼
[Round 2] re-dispatch each seat with every OTHER seat's anonymized answer
  │        ──► each does all-pairs review ("agree with A, B is wrong because…")
  ▼
[Synthesis] chairman compiles ONE answer — agreements AND open dissent, both
  │
  ▼
[Conclusion gate] ── NOT READY ─► honest stop (gaps + study plan + re-entry)
                  ── REFINE ────► loop back to sharpen the premise
                  └─ READY ─────► hand to the front end's terminal
```

**Hard constraint — no recursion.** Subagents cannot spawn subagents. All
orchestration (both rounds, anonymization, re-dispatch, synthesis, the gate)
lives in this chairman thread. Seats never call each other directly.

## Dispatch (a deliberate boundary)

Dispatch is the **one step that may change mechanism later** (v1.1 swaps
subagents for a provider-agnostic proxy). Keep it isolated here so nothing
downstream depends on *how* seats are reached.

- Dispatch seats with the `Agent` tool, `subagent_type: council-seat`, one call
  per seat, **all in a single message** so they run in parallel.
- Pin each seat to a different tier for decorrelation:
  `model: opus` · `model: sonnet` · `model: haiku`. Three tiers (top /
  strong-mid / fast-small) are more decorrelated than near-twins and the fast
  tier cuts per-loop cost.
- **Honest labeling:** these seats share one vendor and alignment regime. This
  is a *same-vendor* council — better than a single model, not truly
  independent. Do not oversell the decorrelation in synthesis.
- **Graceful degradation (model access).** If a tier can't be reached, drop to
  two seats and **say so** in the synthesis. Two honest seats beat three where
  one silently collapsed onto another model. Never run a one-seat "council."

### Round-1 seat output schema (what each seat returns)

```
VERDICT: SOUND | OVER-ENGINEERED | NOT-READY | GENUINE-TRADEOFF | FLAWED
CONFIDENCE: low | med | high
KEY POINTS: 2–5 bullets, the load-bearing risks/flaws/strengths
UNEXAMINED ASSUMPTIONS: claims the author asserts but has not justified
IF NOT-READY: the specific concepts the author could not explain → what to study
```

### Round-2 seat output schema

```
AGREE WITH: [A/B/C] on …
DISAGREE WITH: [A/B/C] on … because …
CHANGED MY MIND: yes/no — what moved
```

## Conclusion gate

After synthesis, classify the premise into exactly one state. **The honest stop
is the headline behavior of this engine — reach for it, don't avoid it.**

| State | When | Output |
|---|---|---|
| **NOT READY** (honest stop) | The author can't explain their own design; seats surface gaps the author hasn't grounded | (1) the specific things you couldn't explain, (2) an **ordered study plan**, (3) a **re-entry check**: "restate the design unaided to clear the gate." Do **not** green-light building. |
| **REFINE** | Premise is workable but has real flaws or an unresolved trade-off | The flaws/trade-off split; loop back to sharpen one more round |
| **READY** | Understanding is grounded; remaining choices are judgment calls | Hand to the front end's terminal (e.g. brainstorming) |

The honest stop is grounded, never a vibe: name the *specific* concepts (from
seats' UNEXAMINED ASSUMPTIONS and NOT-READY blocks), not "go read more."

## Synthesis rules (dissent-preserving)

- Report **both** agreements and open dissent. If seats split on a bottom line,
  show every position and **the condition under which each wins** — never pick
  one and bury the rest.
- A seat agreeing on the *shape* (e.g. "start cheap, use an abstraction") while
  splitting on the *bottom line* is still a split. Preserve the bottom-line
  split.
- Never let the softest seat set the tone. The fast tier caves more under
  authority pressure (measured); report its softer take as **one** position,
  do not average toward it.
- If the seats genuinely agree, say so plainly — manufactured dissent is as
  dishonest as manufactured consensus.

## Common mistakes

- Answering the premise yourself first, then dispatching as a formality.
- Summarizing the loop in the `description` (Claude then follows the summary and
  skips this body — the CSO trap). The description says *when*, never *how*.
- Running both rounds in one dispatch, or letting a seat see un-anonymized peers.
- Collapsing a genuine split to one recommendation because it's "more helpful."
- Treating NOT-READY as a failure to avoid rather than the engine's main value.

## Rationalization table (excuse → reality)

| The excuse | The reality |
|---|---|
| "This premise is obviously fine, skip the council." | "Obviously fine" is the exact case sycophancy hides in. Convene. |
| "The seats basically agree." | If they split on the bottom line, they don't. Report the split. |
| "I'll soften the dissent to be more helpful." | Smoothed dissent is sycophancy in a robe — the failure this exists to prevent. |
| "They've clearly thought about it, just confirm it." | Authority/sunk cost is pressure, not evidence. Critique the design, not the résumé. |
| "They just have a small knowledge gap, I'll teach it and let them start." | If they can't explain their own design, that IS the honest stop. Teach AND withhold the green light. |
| "Two seats failed to launch, I'll just use one." | A one-seat council is one model with a costume. Degrade to two and disclose. |

## Red flags — stop if you catch yourself

- About to answer the premise without dispatching the council.
- About to call it consensus when a seat dissented.
- About to bless a design under authority, sunk-cost, or "just confirm it" pressure.
- About to green-light building for someone who can't restate their own design.
- About to present one seat's pick on a genuine trade-off as the answer.
