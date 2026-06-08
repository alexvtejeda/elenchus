# Plan — Refine elenchus-study Round 1: chairman proposes a phased study roadmap

## Goal
Change Round 1 (link gathering) so that, **before any deliverable markdown file is
written**, the chairman:
1. takes the seats' gathered **valid links only**,
2. **organizes them into categories**,
3. **proposes a phased study roadmap** (Phase A / B / C… — letter labels, neutral
   order, content in a sensible learning sequence),
4. **iterates with the user in-chat until they explicitly approve**, and
5. **only then saves** a new `docs/elenchus-study/<slug>-study-plan.md`.

Seats' job narrows to *gathering valid grounded links*; all organizing, categorizing,
and sequencing is the **chairman's** job.

## Decisions (confirmed with user)
- **Phase ordering:** letter-labeled `Phase A / B / C…`, presented in letter order;
  content arranged in a sensible learning sequence (letters = neutral labels).
- **Ranking rule:** **RELAXED for study mode.** The chairman may now propose a
  recommended learning sequence (the roadmap). This rewrites the current "present
  unranked / no 'start here' / ordering is a verdict" rule — for study mode only.
  (The terminal "no 'you've learned it' verdict" is untouched.)
- **Save target:** new `docs/elenchus-study/<slug>-study-plan.md` for the roadmap;
  `<slug>-resources.md` stays the raw deduped link list.
- **Revise loop:** propose in-chat → user can request changes any number of times →
  save the study-plan file **only after explicit approval**.

## Durability resolution (flagging for your OK)
The skill's discipline is "write durable state DURING the round, before /clear."
That conflicts with "save nothing before approval." Proposed reconciliation:
- **Checkpoint `<slug>.md`** and **`<slug>-resources.md` (raw deduped links)** are
  written **during the round** for durability — they carry no verdict, so they're safe
  to persist early.
- **`<slug>-study-plan.md` (the roadmap = the recommendation)** is the only artifact
  gated on user approval.
This honors both "only then save *the plan*" and "don't lose work on /clear."

## Files to edit (each in repo archive + global runtime mirror)
1. `skills/elenchus-study/SKILL.md`  ·  `~/.claude/skills/elenchus-study/SKILL.md`
   - Intro: rewrite "presents without ranking / a 'start here' is a verdict" for the
     relaxed study-mode roadmap behavior.
   - Inverted-loop diagram (R1): add categorize → propose roadmap → revise → save.
   - "Round templates" R1 bullet: seats gather valid links only; chairman categorizes
     + proposes the phased roadmap; user revises; save after approval.
   - Checkpoint-files section: add `<slug>-study-plan.md`; state the durability split.
   - Common mistakes: reframe the "chairman ranking" item — in study mode the chairman
     DOES propose a sequenced roadmap, but (a) seats never rank, (b) the plan file is
     never written before the user approves it.
2. `skills/elenchus-study/templates/round-1-resources.md`  ·  global mirror
   - Narrow the seat task to "valid, grounded links only — no structure, no plan, no
     ordering; the chairman builds the roadmap." Keep `COVERAGE GAPS` (tells the
     chairman where material is thin). Keep grounding/no-fabrication rules.

## Testing (writing-skills Iron Law — no skill edit without a test)
- Baseline (RED): current R1 behavior — seats gather → chairman dedups → writes
  resources.md immediately, no roadmap, no revision gate.
- After (GREEN): dry-run R1 against a sample topic (e.g. "software architecture
  fundamentals") in a fresh session and confirm: seats return links only; chairman
  proposes Phase A/B/C roadmap; no `-study-plan.md` exists until I approve; file
  appears only after approval. (Fresh session required — agents register at start.)
- Record the run under `docs/validation/runs/` per `docs/validation/harness.md`.

## Open question for you
- Keep `COVERAGE GAPS` in the seat schema (my recommendation — it helps the chairman
  spot thin categories), or strip it so seats truly return "links only"?

## Review — done

**What changed (Round 1 now ends in a user-revised roadmap, not an auto-saved list):**
- **Seat job narrowed to valid links only.** `round-1-resources.md` now tells seats they
  gather links and explicitly **do not** organize/categorize/order/plan. Added a `covers:`
  field per link (tag the sub-area) and a directive to **span the sub-areas for depth**.
  Renamed `COVERAGE GAPS` → `THIN SUB-AREAS` (sub-areas searched but found weak).
- **Chairman builds the roadmap.** New *Round 1 roadmap* section in SKILL.md: dedup →
  organize into categories (driven by `covers:` tags) → propose **Phase A/B/C…** (neutral
  letter labels, contents in a sensible learning sequence) → **revise in-chat until the
  user approves** → only then save the plan file.
- **Ranking rule relaxed for study mode** in the intro: the council gathers a spread; the
  chairman proposes a sequenced roadmap — framed as a *proposal the user shapes*, not a
  verdict. (Terminal "you've learned it" verdict still never the council's.)
- **Third artifact + durability split.** Added `<slug>-study-plan.md` (approved roadmap,
  written only post-approval). Checkpoint + raw `-resources.md` still written during the
  round (no recommendation in them). Resume: presence of `-study-plan.md` = roadmap
  approved; if missing but `-resources.md` exists, re-propose from saved links without
  re-dispatching seats.
- **Common mistakes** reframed: seats categorizing/ordering/planning; saving the plan
  before approval; phases ordered by "quality" / labeled "start here."

**Files touched (repo + global mirror, verified in sync):**
- `skills/elenchus-study/SKILL.md` (+ `~/.claude/skills/elenchus-study/SKILL.md`)
- `skills/elenchus-study/templates/round-1-resources.md` (+ global mirror)

**Testing status (honest):**
- Edits reviewed for coherence end-to-end; repo↔global parity confirmed via `diff`.
- **No live convene run yet** — a real R1 dry-run needs a **fresh session** (agents/skills
  register at startup). Recommended GREEN check next session: convene on a sample topic and
  confirm seats return links-only with `covers:` tags; chairman proposes Phase A/B/C; no
  `-study-plan.md` exists until approval; file appears only after approval. Record under
  `docs/validation/runs/`.
- Not committed (commit-only-when-asked).

---
---

# (Archived) Prior plan — Templatize the council + add elenchus-study

## Goal
Two outcomes:
1. **Kill the static `council-seat` agent as the "persona."** Replace it with a
   **composable template system** the chairman reads before dispatching, so each of the
   three tiers (Opus/Sonnet/Haiku) can get tier-tuned prompts and each mode can define its
   own rounds.
2. **Make the engine genuinely mode-agnostic** (today it bakes build-specific round schemas
   into its body) so a new **`elenchus-study`** front end can reuse the same 2+N-round loop
   for research.

Guiding constraint (global): **simplicity** — smallest change that works; no new infra
unless proven necessary.

## Honest answer on the dedup hook
**Not needed.** The chairman dedups the round-1 resource links inline (normalize
http/https + www + trailing slash, then collapse). A hook only pays off if dedup must be
deterministic or runs over dozens of links; neither holds. Ship without it; revisit only if
inline dedup visibly fails at scale.

## Composition model
`dispatch prompt = seat-base (engine) + round template (front end/mode) + tier adapter
(engine) + premise/topic + round indicator`.
The chairman **reads the relevant templates first**, composes, inlines per seat. The
registered `council-seat` agent becomes a **thin sandbox** (restricted tools, no recursion,
"follow the chairman's dispatch prompt exactly") — NOT the persona.

## Forks — RESOLVED
- **A. Template location → HYBRID.** Shared `seat-base` + `tiers` in
  `elenchus-council/templates/`; each front end owns its round templates in
  `<front-end>/templates/`.
- **B. Seat sandbox → THIN `council-seat` agent.** Keep it registered, strip to a
  restricted-tools/no-recursion sandbox; persona+rounds+tiers come from the chairman's
  composed prompt.
- **C. Scope → PHASE 1 ONLY this session** (todos 1–5). Study skill is a follow-up.

## Todo (Phase 1 — engine becomes template-driven, build still works) — DONE
- [x] 1. `elenchus-council/templates/seat-base.md` — mode-agnostic seat persona.
- [x] 2. `elenchus-council/templates/tiers.md` — per-tier adapter table (Opus/Sonnet/Haiku).
- [x] 3. Generalized `elenchus-council/SKILL.md`: removed baked build round schemas; added
  "Templates & composition"; generalized the intro + loop diagram to N-round/mode-agnostic.
- [x] 4. `council-seat.md` → thin sandbox agent; removed the drifting 3rd copy
  (`skills/elenchus-council/council-seat.md` + global); canonical `agents/` + `.claude/agents/`
  mirror in parity.
- [x] 5. `elenchus-build` round templates added; SKILL.md points at them; behavior unchanged.
- [x] 6. Global installs synced; CLAUDE.md documents the composition convention.

## Todo (Phase 2 — new elenchus-study skill) — DONE
- [x] 6–9. SKILL.md, 3 round templates, global sync, review (see review below).

## Review — Phase 1 done
- Seat prompt is now **composed**, not one static agent. Engine is mode-agnostic (no round
  schemas). `council-seat` is a thin sandbox. New `elenchus-council/templates/{seat-base,tiers}`.

## Review — Phase 2 done (elenchus-study, via /writing-skills TDD)
- **RED:** "convene a research council to learn X" was hijacked by elenchus-build; a seat
  returned prose with no URLs/types + a verdict.
- **GREEN:** new study SKILL.md + 3 round templates; NOT-clause added to build's description.
  Comprehension + Haiku R1 tests passed (grounded URLs, spread, no ranking).
- **Open notes:** restart required to convene; dedup hook not built (by design); not committed;
  no study validation-harness fixtures yet.
