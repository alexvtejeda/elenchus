---
name: elenchus-plan
description: >-
  Use when you have an approved spec (or firm requirements) for a multi-step build
  and want the implementation plan itself stress-tested before you execute it —
  "write the plan and have the council check it", "verify this plan against the
  spec", "turn this spec into a plan I can trust", or the writing-plans stage of the
  Elenchus pipeline. The plan/verification front end over the elenchus-council
  engine. NOT for stress-testing a build PREMISE that isn't settled yet (that's
  elenchus-build), NOT for authoring plan craft from scratch with no council
  (that's plain writing-plans), and NOT for verifying a finished implementation in
  the browser (that's finishing-implementation-elenchus).
allowed-tools: Agent, Read, Write, Grep, Glob, WebSearch, WebFetch
---

# Elenchus — plan front end

The **plan/verification** front end over the `elenchus-council` engine. It takes an
approved spec, writes an implementation plan, and has the **anonymized council verify
the written plan** — replacing the solo "fresh eyes" self-review that plain
`writing-plans` ships with. It also lets the deepest-reasoning tier propose whether
the spec should become **several** plans, as a suggestion the user approves.

**Two skills compose here — read both, re-teach neither:**

- **`writing-plans`** is the **base layer**: it owns the plan-authoring *craft* —
  file-structure mapping, bite-sized task granularity, the plan header + task schema,
  the no-placeholders rules, and the Execution Handoff. **REQUIRED SUB-SKILL: Use
  writing-plans** to draft the plan. Do not re-explain its rules here.
- **`elenchus-council`** owns the **loop** — parallel anonymized seats, tier
  decorrelation, dissent-preserving synthesis, the gate. **Read
  `elenchus-council/SKILL.md` and run its loop** for the verification round. Do not
  re-implement it.

This file supplies only the plan-mode specifics: what to add on top of `writing-plans`,
the two round templates, the roster gate, the checkpoint, and the terminal.

## What this changes about plain writing-plans

`writing-plans` does two things solo that this front end **moves to the council / the
user** — this is the whole point of the skill, and baseline agents skip it because
`writing-plans` explicitly prescribes the solo versions:

| writing-plans (solo) | elenchus-plan (replaces it) |
|---|---|
| **Self-Review** — "look at the spec with fresh eyes … a checklist you run yourself, **not a subagent dispatch**." | **Plan-check council round** — dispatch the anonymized seats to audit the plan against the spec (`COVERED / GAPS / DEFECTS`). The solo Self-Review is **REPLACED**, not run in addition. |
| **Scope Check** — the author decides to split "one plan per subsystem" and acts on it. | **Split suggestion** — one deep-tier seat proposes the split; the chairman **returns it to the user for approval BEFORE any plan file is written.** The author never splits-and-writes unprompted. |

**Do not run writing-plans' Self-Review or act on its Scope Check yourself.** Use
writing-plans for craft; the verification and the split decision belong to the council
and the user respectively.

## Flow

1. **Input:** an approved spec (from the build → brainstorming pipeline, or any spec
   the user points at). Read it.
2. **Split suggestion (deep-tier, one seat, BEFORE writing anything).** Confirm the
   roster (see gate), then dispatch **one** seat on the deepest tier (Fable; Opus
   fallback) via the engine with `templates/split-suggestion.md` + the spec. It
   returns an advisory `RECOMMENDATION / SEAM / RATIONALE / RISK IF IGNORED`.
   **Present it to the user and get their call** — one plan, the proposed split, or
   their own division. Nothing is written until they choose. Record the approved
   division in the checkpoint.
3. **Draft the plan(s).** Using **writing-plans**, write the draft plan(s) to
   `docs/superpowers/plans/<YYYY-MM-DD>-<slug>.md` — one file per approved plan (if
   split, also write the shared-contract/foundational plan the seam needs first).
4. **Verify (plan-check council round — replaces Self-Review).** Confirm the roster
   again, then dispatch the **full** anonymized council via the engine with
   `templates/round-plan-check.md`, giving each seat **the spec + the draft plan**
   (one dispatch set per plan file if split). Anonymize + synthesize dissent-preserving
   as any engine round. Schema: `COVERED / GAPS / DEFECTS`.
5. **Revise.** The chairman fixes **every** GAP and DEFECT inline — add the missing
   task, kill the placeholder, reconcile the mismatched signature, re-ground the stale
   API. If the revisions were substantial, re-verify.
6. **Terminal = writing-plans' Execution Handoff**, unchanged: offer Subagent-Driven
   (recommended) vs Inline execution, and hand to the chosen sub-skill.

**No readiness/verdict** — the engine invariant holds. The council flags coverage
gaps and defects; it never certifies the plan "ready to build." The user owns that.

## Roster gate (suite invariant — every dispatching round)

**Confirm the seat roster with the user before EVERY dispatch** — the split-suggestion
dispatch (step 2) *and* the plan-check dispatch (step 4), and on **resume**. Present
the roster you intend to use (models + per-seat lens), and dispatch only after the user
agrees or edits it. The split-suggestion step is a single Fable seat by default — say
so and let the user change it. Never dispatch on a silently-reused or assumed roster.

## Round templates (plan mode)

Owned by this front end; composed by the engine (`seat-base` + template + tier row):

- **`templates/split-suggestion.md`** — one deep-tier seat, advisory split proposal,
  run before drafting. Returned to the user, not acted on.
- **`templates/round-plan-check.md`** — full council, audits the written plan against
  the spec for coverage + executability. `COVERED / GAPS / DEFECTS`.

Reuses engine `seat-base.md` + `tiers.md` unchanged. **Grounding:** seats verify every
framework/API a task leans on against current docs (Context7 first, web second).

## The checkpoint file (durable state)

One markdown file per plan session survives `/clear`.

- **Path:** `docs/elenchus/<slug>-plan.md` (slug from the spec/feature name).
- **Gitignore `docs/elenchus/` first** — append the line to the caller project's
  `.gitignore` (create it if absent) before the first checkpoint write. The **plan
  files** under `docs/superpowers/plans/` are real deliverables and are NOT gitignored.
- **Write it DURING the round, before the user clears** — never a `SessionEnd` hook.
  After the split suggestion + user's choice, record the approved division. After the
  plan-check round, record COVERED/GAPS/DEFECTS and what was revised.
- **Resume = scan-on-invoke.** When convened, Read `docs/elenchus/` for an open
  (`ready: false`) plan session; resume from its `round`.

Frontmatter schema:

```
---
artifact: elenchus-plan-session
spec_path: "<path to the approved spec>"
ready: false          # user self-declares; the council never sets it
round: split          # split = suggestion posed, awaiting user's plan-count call
                      # · plan-check = plan drafted, awaiting/under council audit
split: "<one plan | N plans: names>"   # the USER-approved division
plan_paths: [docs/superpowers/plans/<...>.md, ...]
seats:                # the USER-approved roster for the current dispatch
  - {model: fable, lens: split-suggestion}   # step 2 default: one deep seat
gaps: [...]           # unresolved GAPS/DEFECTS from the plan-check round
created: <date>
updated: <date>
---
```

Body: the spec path + one-line premise; a **Split** section (the seat's proposal +
the user's decision); the **plan paths**; a **Plan-check** section (COVERED / GAPS /
DEFECTS + what was revised).

## Common mistakes (plan front end)

Drawn from observed baseline behavior — both are the default pull, not edge cases:

- **Running writing-plans' solo Self-Review instead of the council.** The baseline
  agent literally ran that checklist verbatim and called the plan verified. A solo
  pass is not verification here — it is REPLACED by the plan-check council.
- **Deciding the plan count yourself and writing the files.** The baseline agent
  wrote three plan files to disk unprompted, citing writing-plans' Scope Check. The
  split is a **suggestion returned for approval**; write nothing until the user picks.
- Dispatching either round on a roster the user didn't confirm *this* round.
- Treating `COVERED` as a readiness sign-off — it is a fidelity check, not a green light.
- Leaving a `GAP`/`DEFECT` unrevised because it seems minor. Fix every one, then
  re-verify if the fixes were substantial.
- Smoothing a genuine split between seats in the plan-check synthesis into "they agree."

## Rationalization table (excuse → reality)

| The excuse | The reality |
|---|---|
| "I ran the skill's Self-Review checklist, the plan's verified." | That is writing-plans' SOLO check — REPLACED here by the plan-check council. Convene it. |
| "The spec says two subsystems, so I'll split and write the plans." | The split is a suggestion for the USER to approve. Propose, then wait — write nothing yet. |
| "I decided it's three plans." | Plan-count is the user's call. Give the proposal + rationale; let them decide. |
| "The plan-check found only minor gaps, ship it." | Fix every GAP/DEFECT. Minor-looking signature drift is exactly what breaks at integration. |
| "COVERED means the plan is ready to build." | COVERED is fidelity, not readiness. The engine never certifies ready. |

## Red flags — stop if you catch yourself

- About to run a solo "fresh eyes" review of the plan instead of dispatching the council.
- About to write plan files before the user approved the plan count.
- About to dispatch a round on a roster the user didn't confirm this round.
- About to call the plan "ready to build" — that's the user's declaration, never yours.
- About to leave a plan-check GAP/DEFECT unfixed because it "looks small."

## Install / sync

Skill lives at `skills/elenchus-plan/` (version-controlled archive) and must be
**synced to `~/.claude/skills/elenchus-plan/`** (the runtime copy Claude Code loads).
It dispatches the existing `council-seat` agent — no new agent, but a fresh session is
still required if council-seat was (re)installed this session.
