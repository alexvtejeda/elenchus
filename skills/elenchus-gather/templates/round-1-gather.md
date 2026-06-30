<!--
TEMPLATE (gather mode, Round 1). The chairman composes:
  seat-base (engine) + THIS + tier adapter (engine) + the corpus brief & this
  seat's assigned bucket(s) + "you are in round 1".
There is NO premise and NO critique in gather mode — this template OVERRIDES the
adversarial framing in seat-base for this round. Inlined per seat.
-->

# Round 1 — harvest a verified closed corpus (no premise, no critique)

Ignore the "expose what the premise hasn't grounded / stress-test the author"
framing from the base persona — **there is no premise here.** Your one job is to
**harvest the best real, currently-live resources** for the bucket(s) the chairman
assigned you, and to **prove each one is live before you return it.** This corpus
is consumed by a downstream system, so a dead or invented link is a defect, not a
near-miss.

**Hard rules (these are the whole point — a fabricated or dead link fails the task):**

1. **Find via search, never from memory.** Use WebSearch / Context7 to discover
   candidates. Do **not** reconstruct, guess, or "remember" a URL or an id.
2. **Verify every URL is LIVE before you list it — by an actual fetch, not by search.**
   Appearing in search results, an index, or your own recollection is **NOT** proof of
   liveness and never counts as verification. You must hit the resource and confirm it
   resolves to the real thing (a specific title / real content), **not** a 404, an error
   page, a placeholder ("undefined", "Oops", "Video unavailable", a generic landing
   title), or a redirect to something unrelated.
   - **Prefer a programmatic endpoint that 404s on dead/private resources** over scraping
     a JS-rendered page. For YouTube, fetch the **oEmbed** endpoint —
     `https://www.youtube.com/oembed?url=<watch-url>&format=json` — which returns the real
     `title` + `author_name` on a live video and **404s on dead/private/invalid** ones.
     The returned `author_name` is also the *true* channel, so use it to sanity-check the
     speaker/`source` (and any gender/identity claim) rather than guessing.
   - If your fetch tool only returns a JS shell, fall back to a method that exposes the
     server-rendered title/metadata — but you must positively confirm liveness somehow.
   - If you cannot actually fetch it, it goes in `COULDNT_VERIFY` — **never** list it in
     `CORPUS` with a "verified: appears in search" note. That is the fabrication failure
     this skill exists to prevent.
3. **Drop what you cannot confirm.** A candidate you can't verify does **not** go
   in `CORPUS`; record it under `COULDNT_VERIFY`. Never promote a guess.
4. **Match the inclusion criteria** in the brief (e.g. single-speaker, clean audio,
   language, recency). If an entry only *probably* meets a criterion you can't check
   from the page, say so in `why` — don't silently assert it.
5. **Don't pad.** Returning 4 verified entries beats 10 with 6 unverifiable guesses.
   Realness and fit over hitting the target count.
6. **Tag every entry with its `category`** (the bucket it serves) so the chairman can
   assemble the corpus without re-deriving it.

Return **exactly** this schema:

```
CORPUS:
  - category: <the bucket this entry serves>
    url: <exact canonical link you fetched and confirmed live>
    title: <the real title shown on the live page>
    source: <channel / author / site / owner>
    why: <one line tying this entry to the bucket's criteria; note any criterion
          you could NOT verify from the page>
    verified: <how you confirmed it is live — e.g. "fetched, real title + entries">
COULDNT_VERIFY:
  - url + one-line reason you dropped it (didn't resolve / placeholder title /
    wrong content / multi-speaker / behind login). Honest negatives help the chairman.
THIN BUCKETS:
  - any assigned bucket you could not fill to the target with verified entries —
    say so plainly; this is where the corpus is genuinely sparse.
```
