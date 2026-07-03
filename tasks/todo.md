# Plan — `elenchus-plan` + `finishing-implementation-elenchus`

Spec: `docs/2026-07-02-elenchus-plan-and-finishing-spec.md` (approved shape:
front-end-over-engine for plan; parallel Playwright harness for finishing;
bundled skill-scoped `.mcp.json`).

**Guardrails:** minimal changes; do not touch the engine's mode-agnostic core;
sync every skill edit into `~/.claude/skills/` (runtime); mirror any agent into
`.claude/agents/` + restart before dispatch.

## Part A — `elenchus-plan` (front end over the engine)

- [x] **RED (writing-skills):** DONE — 2 baseline runs (Trailhead fixture), recorded in
      `docs/validation/runs/2026-07-02-elenchus-plan-RED-baseline.md`. Both failed the same
      two ways: (1) verification entirely SOLO (one literally ran writing-plans' Self-Review
      checklist verbatim — no council); (2) split decision made unilaterally and ACTED ON
      (one wrote 3 plan files to disk unprompted). Rationalization table captured.
- [x] Create `skills/elenchus-plan/SKILL.md` — front end over `elenchus-council`;
      reuses `writing-plans` (base layer) + engine loop, re-teaches neither.
- [x] `skills/elenchus-plan/templates/split-suggestion.md` — one deep-tier (Fable→Opus)
      advisory split proposal, returned to user for approval.
- [x] `skills/elenchus-plan/templates/round-plan-check.md` — full-council `COVERED /
      GAPS / DEFECTS` audit; replaces writing-plans' solo Self-Review.
- [x] Wired the flow in SKILL.md (split-suggestion → user approves → draft → plan-check
      → revise → Execution Handoff), roster gate before EVERY dispatch, checkpoint spec.
- [x] Checkpoint `docs/elenchus/<slug>-plan.md` documented; plan files → `docs/superpowers/plans/`.
- [x] Synced `skills/elenchus-plan/` → `~/.claude/skills/elenchus-plan/` (diff clean).
- [x] **GREEN/REFACTOR:** 2 runs WITH skill (neutral + pressure) — both PASS both RED
      failures; no new loophole → no extra counters. Recorded in
      `docs/validation/runs/2026-07-02-elenchus-plan-GREEN.md`.
- [x] Wired `elenchus-plan` into repo `CLAUDE.md` (architecture + editing-skills list +
      durable-state checkpoint sections).

## Part B — `finishing-implementation-elenchus` (sequential verify→fix loop)

> **Reshaped 2026-07-02 (spec v0.2).** After the plan-check council + user decisions,
> Part B is a **sequential verify→fix loop** (NOT a parallel report-only harness): the
> **chairman implements the fixes** (reverses the old "does not fix" non-goal). Spec:
> `docs/2026-07-02-…-spec.md` Part B v0.2. Council findings: `docs/validation/runs/2026-07-02-partB-plan-check.md`.

### B0 — pre-checks — RESOLVED by user (2026-07-02)

- [x] **B0a — MCP registration.** Wire Playwright MCP the **same way Context7 is** — a
      **project-root `.mcp.json` entry** (no skill-directory scope, which Claude Code does
      not load), config from env, documented in `CLAUDE.md`, no secrets. Pkg
      `@playwright/mcp`, cmd `npx @playwright/mcp@latest` (confirm current invocation via
      Context7 at build time). Resolves the council's load-bearing dissent in favor of the
      project-`.mcp.json` pattern.
- [x] **B0b — No parallelization → SEQUENTIAL passes, all customizable, gated once.**
      Scrap the fan-out. After deriving the checklist, propose `{iterations, verifier
      structure}` **once**; user confirms/edits; loop runs unattended. Defaults: **N = 3
      fix-passes + 1 free final no-fix confirm pass** (run = N+1 verifications). Verifier
      structure default: **two independent, cross-checked** per pass — **Sonnet + highest
      tier (Fable; Opus fallback)** — each over the *full* checklist; chairman merges; a
      PASS/FAIL disagreement is itself flagged.
- [x] **B0c — Subagent tool exposure.** Verifier subagents reach the Playwright MCP the
      **same way they reach Context7** (session-scoped project `.mcp.json`) — no bespoke
      per-skill wiring. Restart-to-register applies to any new custom agent.
- [x] **B0d — Shared report format; subagents report-only, chairman fixes.** Every
      subagent reports in ONE format: per checklist item **PASSED / FAILED / NEEDS-HUMAN /
      MISSING**, may **cite screenshots**, and **flags missing features** the checklist
      implies but the build lacks. **Subagents never touch code.** The **chairman** merges
      + reconciles against the full checklist, then **implements fixes one by one** (FAILED
      + MISSING) between passes. NEEDS-HUMAN surfaced, never faked.

### B1 — RED baseline (writing-skills)

- [x] **RED — DONE.** 2 runs, planted fixture (F1 ok / F2 broken / F3 missing / F4 ok).
      Both failed 3 ways: asserted PASS/FAIL from source ("verdicts are certain from
      source"), used no shared schema, buried NEEDS-HUMAN. Both DID flag F3 missing + stayed
      report-only. Recorded: `docs/validation/runs/2026-07-02-partB-RED-baseline.md`.

### B2 — Build (writing-skills GREEN) — DONE (2026-07-02)

- [x] Used `/writing-skills` discipline (RED-first Iron Law honored).
- [x] Created `skills/finishing-implementation-elenchus/SKILL.md` — sequential verify→fix
      loop with ALL steps explicit: precondition/URL gate (never start server); discrete
      checklist derivation; config gate once (iterations default 3 + free confirm pass;
      verifiers default two cross-checked Sonnet + highest tier); fix-pass loop (verifiers
      dispatched SEQUENTIALLY — single browser session — report-only schema; chairman merges
      + flags disagreements + reconciles every item; chairman implements fixes one by one);
      final free confirm pass; NEEDS-HUMAN surfacing; gitignore `docs/elenchus/`. Includes
      Common Mistakes + rationalization table seeded from the RED baseline, and the
      named-agent fallback + restart note.
- [x] Created **`agents/finishing-verifier.md`** (canonical + mirrored to `.claude/agents/`)
      — thin sandbox: Read/Grep/Glob + Context7 + Playwright `browser_*` tools, **no
      Write/Edit, no recursion** → report-only enforced structurally (the RED insight).
- [x] Wired Playwright MCP: repo-root `.mcp.json` already had it (B0a); aligned formatting
      (added `"type": "stdio"`). Grounded tool names/flags via Context7.
- [x] Run report contract → `docs/elenchus/<slug>-finishing.md` (per-item results across
      passes + chairman's fixes + NEEDS-HUMAN) specified in SKILL.md. (Emitted at runtime.)
- [x] Synced `skills/finishing-implementation-elenchus/` → `~/.claude/skills/…` (diff clean).
- [x] **GREEN/REFACTOR — DONE.** 2 runs WITH the discipline (fallback path): both refused
      source-substitution → all NEEDS-HUMAN, exact schema, report-only. No new loophole → no
      REFACTOR. `finishing-verifier` registered live with Playwright tools + no Write (report-
      only structural). Recorded: `docs/validation/runs/2026-07-02-partB-GREEN.md`.

## Docs / wiring

- [x] Updated repo `CLAUDE.md`: "What Elenchus Is" (post-execution stage + full pipeline),
      editing-skills skill list, agents section (finishing-verifier as 2nd two-copy agent +
      restart note), durable-state (finishing report, no resume loop), MCP section (Playwright
      wired alongside Context7).
- [ ] Note in README/handoff if appropriate (defer unless asked).

## Open checks before building — RESOLVED

- **B0a — DONE.** Repo-root `.mcp.json` already wires a `playwright` server
  (`npx @playwright/mcp@latest`), alongside `context7`. Project-root scope = the
  Context7 pattern; the dissent is settled. (Align its formatting with the context7
  entry — add `"type": "stdio"` — during B2.)
- **Playwright MCP facts (grounded via Context7 `/microsoft/playwright-mcp`, 2026-07-02):**
  - Run: `npx @playwright/mcp@latest`.
  - Tools surface as `mcp__playwright__<name>`: `browser_navigate`, `browser_click`,
    `browser_type`, `browser_fill_form`, `browser_snapshot` (accessibility tree —
    primary "read the page" tool), `browser_take_screenshot`, `browser_wait_for`,
    `browser_console_messages`, `browser_network_requests`, `browser_evaluate`.
  - Flags worth knowing: `--headless`, `--isolated` (in-memory profile),
    `--browser <chrome|firefox|webkit|msedge>`, `--storage-state <path>` (reuse the
    existing cookie-auth session so verifiers land authenticated), `--output-dir`,
    `--caps vision,pdf`.
- `elenchus-plan` embeds `writing-plans` **by reference** (Skill invoke), not inlined —
  decided in Part A; keep the same discipline referencing `dispatching-parallel-agents`.

## Review

### Part A — `elenchus-plan` — COMPLETE (2026-07-02)

Built the plan/verification front end via the writing-skills TDD cycle (RED→GREEN→REFACTOR).

**Files created (archive + synced to `~/.claude/skills/`):**
- `skills/elenchus-plan/SKILL.md` — front end over the engine. Composes over
  `writing-plans` (base-layer craft) + `elenchus-council` (loop), re-teaching neither.
  Explicitly **replaces** writing-plans' two solo steps.
- `skills/elenchus-plan/templates/split-suggestion.md` — single deep-tier (Fable→Opus)
  advisory split proposal (`RECOMMENDATION / SEAM / RATIONALE / RISK IF IGNORED`),
  returned to the user before any file is written.
- `skills/elenchus-plan/templates/round-plan-check.md` — full anonymized council audit
  of the written plan vs. the spec (`COVERED / GAPS / DEFECTS`); replaces the solo Self-Review.

**Validation (writing-skills TDD):**
- RED (`docs/validation/runs/2026-07-02-elenchus-plan-RED-baseline.md`): 2 baseline runs
  both failed the same 2 ways — solo verification (one ran writing-plans' Self-Review
  verbatim) + unilateral split acted on (one wrote 3 plan files unprompted).
- GREEN (`…-GREEN.md`): 2 runs WITH the skill (neutral + "make it bulletproof" pressure)
  both fixed both failures — council instead of solo review, split returned for approval
  with nothing written first, roster gate on every dispatch, no readiness verdict.
- REFACTOR: no new rationalization surfaced → tables from RED sufficed; no extra counters.

**Docs:** repo `CLAUDE.md` updated in three places (architecture front-end list,
editing-skills skill list, durable-state checkpoint section).

**Key design decision:** the split is a *suggestion the user approves before drafting*,
not a self-authorized action — directly targeting the strongest observed baseline failure
(agents cite writing-plans' Scope Check as license to split-and-write files unprompted).

**Not yet run end-to-end:** GREEN was narrated (subagents can't dispatch council-seat —
no recursion). A real convene happens from a main-thread chairman; `elenchus-plan` reuses
the existing `council-seat` agent, so no new agent registration / restart is required for it.

### Part B — plan verified by council, build pending

**Plan-check council round run 2026-07-02** (first live, non-narrated use of
`elenchus-plan` — validates the skill end-to-end). 4 seats (Fable/Opus/Sonnet/Haiku),
user-approved roster. Full synthesis: `docs/validation/runs/2026-07-02-partB-plan-check.md`.

- **Core flow: COVERED** by consensus.
- **Preserved dissent (load-bearing):** 1 seat says Claude Code has no skill-directory
  MCP scope, so a skill-bundled `.mcp.json` never loads (chain dies); 3 seats marked it
  covered. Resolution is empirical → new blocking task **B0a**. Not smoothed.
- **GAPs closed in the plan:** port-closed→confirm-URL branch; no-verdict/report-only +
  no-fix contract; gitignore `docs/elenchus/`.
- **DEFECTs closed:** checklist-derivation made a discrete rule; aggregator reconciliation
  (no silent skips); single-Playwright-server contention (B0b); subagent type/exposure
  (B0c); output schema (B0d); RED acceptance criterion.

Plan revised accordingly (B0 pre-checks + exploded B2 sub-steps). No readiness verdict.

**Update — B0 resolved by user (2026-07-02), Part B reshaped (spec v0.2):** pivoted from
parallel report-only harness → **sequential verify→fix loop**. B0a: Playwright MCP wired
like Context7 (project-root `.mcp.json`) — resolves the dissent toward the deep seat's read.
B0b: no parallelization; N sequential passes (default/max 3); verifier = Sonnet + highest
tier. B0c: subagents reach Playwright like Context7 (session scope). B0d: shared report
format (PASSED/FAILED/NEEDS-HUMAN/MISSING + screenshots + flag-missing); **chairman now
implements fixes one by one** across the loop (reverses old "does not fix" non-goal). The
council's single-server-contention defect is dissolved by going sequential. Ready to build
B1 (RED) when resumed.

### Part B — `finishing-implementation-elenchus` — COMPLETE (2026-07-02)

Built the post-execution verify→fix loop via the writing-skills TDD cycle.

**Files (archive + synced to `~/.claude/skills/`; agent mirrored to `.claude/agents/`):**
- `skills/finishing-implementation-elenchus/SKILL.md` — sequential verify→fix loop:
  precondition/URL gate (never starts the server) → discrete checklist derivation →
  config gate once (N=3 fix-passes + 1 free confirm pass; verifiers = two cross-checked
  Sonnet + highest tier) → per pass: dispatch verifiers **sequentially** (single browser),
  chairman merges + flags disagreements + reconciles every item, chairman implements fixes
  one by one → final confirm pass → report. Common Mistakes + rationalization table from RED.
- `agents/finishing-verifier.md` (+ `.claude/agents/` mirror) — thin report-only sandbox:
  Playwright `browser_*` + Context7 + Read/Grep/Glob, **no Write/Edit, no recursion**.
- `.mcp.json` — Playwright entry aligned (`type: stdio`); already project-scoped (B0a).

**Validation (writing-skills TDD):**
- RED (`…-partB-RED-baseline.md`): 2 runs, planted fixture — both asserted PASS/FAIL from
  source, no schema, buried NEEDS-HUMAN.
- GREEN (`…-partB-GREEN.md`): 2 runs with the discipline — both refused source-substitution
  (all NEEDS-HUMAN), exact schema, report-only. No new loophole → no REFACTOR.
- Plan-check council (`…-partB-plan-check.md`): earlier live elenchus-plan round that shaped
  the B0 pre-checks.

**Key design decision:** report-only is enforced **structurally** (verifier sandbox has no
Write/Edit), not just by prompt — the RED insight, mirroring how `council-seat` structurally
forbids recursion. Verifiers observe; only the chairman fixes.

**Runtime notes:** `finishing-verifier` registered live this session (dispatchable now;
carries the Playwright tools). **Live end-to-end** (real verifier + Playwright + a running
app with planted bugs → fixes) needs the **user to start a dev server** — the natural next
step, since the skill never starts one itself.
