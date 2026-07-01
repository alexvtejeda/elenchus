---
name: elenchus-gather
description: >-
  Use when the user wants to build a CLOSED CORPUS of real, verified resources or
  links by fanning out parallel agents — "gather as many X links as possible",
  "harvest a curated set of sources", "build a closed space of playlists/repos/feeds
  for a model (or person) to choose from", "collect verified URLs across these
  categories". The harvest front end over the elenchus-council engine. NOT for
  stress-testing a build premise (elenchus-build), NOT for a reading list to learn a
  topic (elenchus-study), and NOT for a one-shot lookup (a single search answers that).
allowed-tools: Agent, Read, Write, Grep, Glob, WebSearch, WebFetch
---

# Elenchus — gather front end

The **harvest** front end over the `elenchus-council` engine. The engine owns the
mechanism (parallel anonymized seats → chairman dedups and synthesizes →
dissent/honesty preserved → gate, no "done" verdict). **This skill does not
re-implement that — read `elenchus-council/SKILL.md` and run its loop.** This file
supplies only the gather-mode specifics: triggers, corpus shaping, round templates,
the checkpoint + corpus files, and the terminal.

**Fanning out the council is the first move, not a formality.** Do not assemble the
corpus yourself from one model's memory — that single-model list is where invented
and dead links come from, the exact failure this skill exists to prevent. The seats
search the live web in parallel and **verify every URL before returning it**; the
chairman dedups and organizes, then reports coverage.

## What gather is (and how it differs from its siblings)

Build and study run a *critique* loop (questions → answers → stress-test). **Gather
does not critique anything** — there is no premise and no user understanding to test.
It reuses the council's *fan-out + decorrelated seats + dedup + honesty* to **collect
a closed corpus**: a set of verified, live resources organized into buckets, meant to
be **consumed by a downstream system or person** (e.g. give a small model a closed
space of voice-source playlists to pick from instead of open web search).

The engine's anti-sycophancy purpose maps, in gather mode, to two disciplines:

- **Anti-fabrication** — a seat must verify each URL is live before listing it, and
  never reconstruct/guess one. A made-up link is worse than a missing one. **Seats
  cannot be fully trusted on this** — a weaker tier may report "verified" off a search
  index without a real fetch (observed in practice, producing dead 404s). So the
  chairman **re-verifies every URL itself** before writing the corpus (see the loop).
- **Coverage honesty** — the chairman reports **thin buckets** and dropped candidates
  plainly; it never pads the corpus to look complete, and never declares it "done"
  (that's the user's call — the gate, below).

## The loop (gather mode)

Default **1 round + optional gap-fill rounds** (no user-answer step between R1 and
the synthesis — the "between rounds" pause is the user deciding whether thin buckets
are worth a round 2):

```
R1  HARVEST — user names the corpus + buckets + per-bucket target + inclusion rules.
    Chairman assigns bucket(s) to each seat and dispatches them IN PARALLEL. Each seat
    searches, VERIFIES every URL is live, and returns verified entries + what it
    dropped + thin buckets. Chairman DEDUPS across seats, **RE-VERIFIES every surviving
    URL itself** (batch-fetch a 404-on-dead endpoint, e.g. YouTube oEmbed — drop dead
    ones, and use the returned author/metadata to correct mis-tagged fields), writes the
    corpus file, and reports coverage (filled vs thin buckets, dropped counts, plus what
    the re-verify pass dropped/corrected).
      ▼  (user decides: good enough, or fill the gaps?)
R2… GAP-FILL (optional) — only the thin/under-target buckets, re-dispatched with the
    already-collected URLs so seats return new, distinct, still-verified entries.
```

**Hard constraint — no recursion.** All orchestration (dispatch, dedup, the corpus
write, coverage report, gate) lives in this chairman thread; seats never spawn seats.

## Corpus shaping (what to elicit before Round 1)

The seats harvest far better with a concrete brief. Draw out, briefly:

1. **What the corpus is and who consumes it** — e.g. "voice-source YouTube playlists
   for a TTS pipeline's find-voices skill to pick from." The consumer sets the bar.
2. **The buckets** — the categories to span (e.g. the voice-energy palette:
   firm-measured, sharp-biting, warm-narrative, …). One seat covers one or more.
3. **Per-bucket target** — roughly how many verified entries per bucket (light ~3,
   thorough ~8–10).
4. **Inclusion criteria** — what makes an entry valid (single-speaker, clean audio,
   language, recency, free/open) and the **resource type** (playlist, repo, feed,
   dataset, doc).
5. **Output location + format** — where the corpus file is written and its shape
   (YAML/JSON/MD), so the downstream consumer can read it.

Pass this to the engine as the round-1 brief. Don't pre-curate the entries yourself.

## Round templates (gather mode)

The engine composes each seat's prompt from `seat-base` + a **round template this
skill owns** + the tier adapter (see `elenchus-council` → *Templates & composition*).
Gather mode supplies two; **both explicitly override seat-base's adversarial framing**
(there is no premise to critique):

- **Round 1 — `templates/round-1-gather.md`.** Seats harvest verified, live resources
  for their assigned bucket(s). Schema: `CORPUS (category/url/title/source/why/verified)
  / COULDNT_VERIFY / THIN BUCKETS`. Every URL is fetched and confirmed live; unverifiable
  ones are dropped, never fabricated.
- **Round 2 (optional) — `templates/round-2-fill-gaps.md`.** Re-dispatch only the thin
  buckets with the already-collected URLs, for new distinct verified entries.

**Tools/grounding:** the seat sandbox carries Read/Grep/Glob/WebSearch/WebFetch +
Context7 MCP. In gather mode the seats use them to **search and to verify liveness** —
a real, current page must back every entry.

**Dispatch & tiers:** per the engine — one seat per tier (`opus`/`sonnet`/`haiku`) for
decorrelation, all in one message so they run in parallel. With many buckets, assign
each seat a slice of the buckets (still one tier each). Same `council-seat`/
`general-purpose` fallback rule as the engine.

## The checkpoint + corpus files (durable state)

Two files per corpus, both under `docs/elenchus/`.

**Gitignore `docs/elenchus/` first.** The checkpoint is private session scratch. Before
writing it, ensure the caller project's `.gitignore` contains a `docs/elenchus/` line —
append it if missing (create `.gitignore` if there is none). Do this once per session;
don't duplicate the line. (The corpus file is a real deliverable — if the user wants it
committed, they can force-add it with `git add -f`.)

- **Session checkpoint:** `docs/elenchus/<corpus-slug>-gather.md` — frontmatter below +
  the brief, coverage report, and dropped/thin notes. Written **during** the round,
  before any `/clear`.
- **Corpus file:** `docs/elenchus/<corpus-slug>-corpus.<yaml|json|md>` — the actual
  deduped, verified entries grouped by bucket, in the format the consumer reads. The
  corpus file may be written during the round (it carries data, not a recommendation).

**Resume = scan-on-invoke.** When convened, Read `docs/elenchus/` for an open gather
session (`ready: false`) matching the corpus. If found, resume from its `round`: report
current coverage + thin buckets and ask whether to run a gap-fill round. If none, start
Round 1.

Frontmatter schema:

```
---
artifact: elenchus-gather-session
corpus: "<one-line: what corpus, for which consumer>"
ready: false          # the USER self-declares this true; the chairman never sets it
round: 1              # 1 = first harvest done · 2+ = gap-fill rounds
seats: [opus, sonnet, haiku]
buckets: [...]            # the categories the corpus spans
target_per_bucket: <n>
inclusion: "<the validity bar, e.g. single-speaker, clean audio>"
verification: "<the liveness bar, e.g. fetched live, real title confirmed>"
corpus_file: docs/elenchus/<corpus-slug>-corpus.yaml
gathered: <count of verified entries>
thin_buckets: [...]      # buckets still under target
created: <date>
updated: <date>
---
```

Body: the brief; a **coverage report** (per bucket: verified count vs target); the
**dropped** candidates worth noting; and the **thin buckets** that remain.

## The gate (no "corpus complete" verdict)

After synthesis the chairman **surfaces, does not certify**:

- Report **coverage per bucket** (verified vs target) and the **thin buckets** by name.
- List notable **dropped** candidates (dead/placeholder/off-criteria) so the user sees
  what was excluded and why — silent truncation reads as "covered everything."
- **Do not declare the corpus complete.** Whether it has enough is the user's call.
  The loop terminates only when the *user* says it's enough; then hand to the terminal.
- Re-entry (more gap-fill rounds) is unlimited.

## Terminal

- **Success exit = the user self-declares the corpus is enough.** Set `ready: true`
  only because the *user* said so. Then hand the **corpus file** to its consumer — wire
  it into the downstream tool/skill (e.g. point `find-voices` at the corpus), or just
  leave the verified file for the user to use.
- **Thin buckets the user still wants filled → honest stop.** Keep the checkpoint open,
  name the sparse buckets, invite a gap-fill round. A genuinely empty bucket (no real
  material exists) is a valid, reportable result — not a failure to hide.

## Common mistakes (gather front end)

- **Assembling the corpus from the chairman's own memory** instead of dispatching seats
  to search and verify. That is the invented-URL failure, restated.
- **Listing a URL without confirming it is live.** Every entry must be fetched and
  confirmed; an unverifiable candidate goes in `COULDNT_VERIFY`, never in the corpus.
  "Appears in search results" is **not** liveness — only an actual fetch is.
- **Trusting the seats' `verified:` field and writing the corpus straight from it.** The
  chairman must re-fetch every surviving URL itself (404-on-dead endpoint) before writing
  — seats have shipped dead links and mis-tagged gender/source that only the re-verify
  pass caught.
- **Padding to hit the target.** Fewer verified entries beat the target count filled
  with guesses. Report the thin bucket honestly.
- **Running it as a critique** (build/study framing). Gather has no premise and asks the
  user nothing between rounds — it harvests and reports coverage.
- **Declaring the corpus complete.** Coverage is surfaced; "enough" is the user's call.
- **Writing state only at the end** (lose it on `/clear`) instead of during the round.
- **Skipping the consumer's bar.** A corpus not matched to how the downstream tool reads
  it (format, fields, criteria) is busywork — shape it to the consumer up front.
