---
artifact: elenchus-build-summary
status: scan-clean
author: alexvtejeda
contradiction_scan: clean
source_session: 2026-06-01 readiness session (Elenchus run on Elenchus)
engine: .claude/skills/elenchus-council (committed)
---

# Elenchus — build summary (v0.1 spec)

> The author's own articulation, written as the success-exit of the readiness loop and
> verified contradiction-free by the judge against the logged decisions (A–E) and facts.
> Readiness is the author's self-declared call; the judge only confirmed the scan is clean.

Elenchus is a Claude Code skill that helps me **verify my own understanding of what I'm about
to build**, instead of getting sycophantic reassurance from a single model. It uses the
Socratic method: a **chairman (judge)** talks to me directly and dispatches **subagent seats
across same-vendor tiers (Opus, Sonnet, Haiku)**. Same-vendor tier diversity is honestly
enough to surface gaps and contradictions in my own design — and it's useful to hear different
opinions on the same tools even within one model family.

**What the judge does — and doesn't:**
- It **flags contradictions and gaps.** It does **not certify readiness** — that's my call.
- I must be **honest about my own knowledge** and say "I don't know" when I don't, accepting
  the residual risk that I might bluff past a gap.

**When it's helpful (and when it isn't):**
1. **Readiness / study [primary].** I describe my app and the feature I want and *why* (e.g.
   "my app does X; I want feature Y because I think it boosts user activity"); the seats analyze
   it and surface gaps via **Socratic questions that bite**. Those questions lead *me* to my own
   conclusion.
2. **Benchmarking tools / weighing multiple approaches under constraints [secondary].** Different
   models give different opinions on the same tools.
- **Out of scope:** asking for an over-engineering / flaw **verdict** ("is feature X
  over-engineering?"). That framing invites a yes/no and sycophancy. A single high-tier model
  can give that verdict if I ever want it; Elenchus deliberately replaces it with gap-exposure.

**Flow (2 rounds, optional 3rd):**
- **Round 1.** I state my premise — mental model, key frameworks, scope (a feature or an app
  from scratch). The seats analyze it and produce biting Socratic questions. The chairman lists
  **all** questions, **anonymized**, grouped **by category**, into a **markdown checkpoint file
  with frontmatter**. I then `/clear` or `/compact` the session.
- **Re-invoke.** The chairman **reads the checkpoint** (my premise + questions) and I answer all
  of them. The goal is surviving without an "I don't know."
- **Round 2.** The seats **stress-test my answers**; survive again without "I don't know." An "I
  don't know" is **not a failure** — it's a learning point I study before building.
- **Optional Round 3**, at my discretion.

**Grounding.** The seats use **Context7 MCP** for up-to-date docs on the tools/frameworks/APIs I
mention — to build honest, consistent benchmarks and to point me toward a **concrete study
path** (current docs, not generic advice).

**State & mechanics** (per the committed `elenchus-council` engine):
- Chairman orchestrates everything; **no subagent recursion**; seats are **anonymized**.
- The **checkpoint markdown file is the durable state** — it survives a context clear.
- **Resume = scan-on-invoke** (the skill Reads the checkpoint when convened), *not* a
  SessionStart hook (which would tax/pollute unrelated sessions). A project-scoped resume hook
  is an optional enhancement only if a whole repo is one Elenchus project.
- **Write state during the round**, before clearing — never rely on a `SessionEnd` hook (~1.5s).
- The loop **terminates when I self-declare ready**; re-entry across study sessions is unlimited.

**Purpose, in one line:** help me study, give me a relevant study path, and build confidence in
my own knowledge before I start building — surfacing architectural gaps via the Socratic method
so I reach the conclusions myself.
