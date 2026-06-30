<!--
TEMPLATE (gather mode, optional Round 2). The chairman composes:
  seat-base (engine) + THIS + tier adapter (engine) + the brief + the list of
  THIN / under-target buckets + the URLs ALREADY in the corpus + "you are in round 2".
Run this ONLY when round 1 left thin buckets the user wants filled. Inlined per seat.
-->

# Round 2 — fill the thin buckets (targeted, still verified)

Round 1 left some buckets under target. The chairman gives you **only those thin
buckets** and the **URLs already in the corpus**. Find *additional* verified,
live resources for those buckets — same hard rules as round 1.

**Hard rules (unchanged, plus de-dup):**

1. Find via search, never from memory; verify every URL is **live** before listing
   it; drop what you cannot confirm into `COULDNT_VERIFY`.
2. **Do not return any URL already in the corpus** (the chairman gave you that list).
   New, distinct, verified entries only.
3. Match the inclusion criteria; don't pad; tag every entry with its `category`.
4. If a thin bucket is thin because the material genuinely doesn't exist, **say so**
   in `THIN BUCKETS` rather than forcing weak or off-criteria entries — an honest
   "this bucket is empty for real" is a valid result.

Return **exactly** the round-1 schema (`CORPUS / COULDNT_VERIFY / THIN BUCKETS`),
restricted to the assigned thin buckets.
