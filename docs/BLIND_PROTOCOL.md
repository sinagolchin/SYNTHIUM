# Blind protocol — mechanical blinding for Synthium coding (`python -m synthium blind`)

Rebuilt 2026-11-10 from the roadmap's description. The July 13 original was later recovered
from the old project; its Chinese tenor classifier is kept as `synthium/blind/classify.py` and its
log as `data/blind_log_2026-07/`. The store defaults to `/mnt/project-files/synthium/blind`
(set `BLIND_HOME` or `--home` to change it).

## What it does

The disposition is cut out by code before any text reaches the coding model. The coder sees
only the blinded part, commits a prediction to an append-only, hash-chained log, and only then
can the rest be revealed.

```
courier-prompt -> (courier subagent fetches, replies DONE) -> ingest -> [read blinded text]
  -> commit -> reveal -> record
```

## Why a courier

This sandbox's egress proxy refuses every court site (CourtListener, eLitigation, BAILII,
Rechtspraak, txcourts.gov, govinfo and others all return 403 on 2026-11-10). So a script can't
fetch case text directly. MCP connectors (CourtListener, Legal Data Hunter) can, but they
return the full text into whoever calls them.

So a separate subagent (the courier) calls the connector and replies only `DONE`. The full text
then sits in the courier's transcript on disk, never in the coder's context. `ingest` reads it
from there by a per-request nonce, checks that the courier fetched the requested document and
that its reply was exactly DONE, and seals it. Large results that the harness saved to a
tool-results file are loaded from that file.

`fetch` (direct HTTP, with `COURTLISTENER_API_TOKEN` if set) and `seal-file` exist for when a
host is reachable or text arrives another way. `fetch` is untested live because every host was
blocked. `seal-file` intake is capped at `uncertain_exposure`, because the tool can't prove
nobody read the file.

## Usage (from a session with Bash and the Agent tool)

```
cd /mnt/project-files/synthium/codebase
python3 -m synthium blind courier-prompt --case us-tx-2026-uatp --source courtlistener --opinion-id 11504626
#   or: --source ldh --ldh-source SG/eLitigation --ldh-id 2026_SGCA_34
# -> paste the printed prompt into an Agent call (general-purpose, foreground). It must answer DONE.
python3 -m synthium blind ingest --case us-tx-2026-uatp            # seals, prints the FACTS section only
python3 -m synthium blind commit --case us-tx-2026-uatp \
    --prediction '{"layer":"pure_law","notch":"REVERSED"}' --prior-exposure none --rationale "..."
python3 -m synthium blind reveal --case us-tx-2026-uatp            # refused without a commit
python3 -m synthium blind record --case us-tx-2026-uatp --actual '{"layer":"pure_law","notch":"REVERSED"}'
python3 -m synthium blind status
python3 -m synthium blind verify
```

The store defaults to `/mnt/project-files/synthium/blind/` (`blindlog.jsonl` plus `sealed/`).
Set `BLIND_HOME` to use another one. The Nov 10 dry run is kept in `data/blind_dryrun_2026-11-10/`.

## Cut rules

| Kind | Front matter removed | Disposition cut |
|---|---|---|
| Common law | Syllabus; "Held:/Disposition:/Result:" lines; NZ/AU-style orders block before REASONS | Earliest of: conclusion/disposition/orders heading in last 50%, "for the foregoing reasons" in last 30%, concluding opener in last 25%, the court's own disposition sentence in last 25% |
| CN | 裁判要点 and 裁判结果 digest blocks | Start of the sentence containing 判决如下/裁定如下 (that sentence names the disposition article) |
| JP | 主文 block | First よって/以上 paragraph in the last 40% |

Then, anywhere in what's shown, the court's own outcome sentences ("we reverse", "the appeal is
allowed", "we will not set aside", 驳回上诉, 論旨は理由がない and similar) are redacted by sentence.
Procedural history ("the court of appeals reversed") is kept.

## Scopes and grades

- `--scope facts` (default): only the background/facts section. US opinions: from Background/Part I
  to Discussion/Analysis/Part II. CN: 审理查明 to 本院认为. JP: not supported (no reliable
  boundary), so it fails closed.
- `--scope reasoning`: everything before the disposition. Good for coding the layer, but the
  court's reasoning states its conclusions, so it is never graded blind.

Grades:
- **blind**: courier intake, facts scope, nothing redacted.
- **uncertain_exposure**: anything redacted, reasoning scope, file intake, or `--prior-exposure`
  other than none.
- **disclosed**: an outcome sentence survived.
- **no_cut**: no marker found. The tool shows nothing (fails closed).

## Log integrity

Every entry carries the previous entry's hash. `verify` detects edited, removed or reordered
lines, a changed sealed file, and a reveal without a commit. One commit per blind, and a sealed
case id can never be reused.

## Known limits

- **Not tamper-proof against the coder.** Anything with a shell can `cat` the sealed file, and
  `chmod 0400` doesn't hold on the shared project folder. The guarantees are that the default
  path never shows the outcome and that the log proves the order of events.
- **Courier trust.** The courier sees the full text. If its reply says anything beyond DONE,
  ingest marks provenance `courier_reply_not_clean` and the grade is capped. But the coder has
  already read that reply by then.
- **Case selection.** Picking cases from search results exposes snippets, which can contain
  dispositions (CORRECTIONS C2). Declare that with `--prior-exposure search_snippet`, or have the
  courier run the search too.
- **Front-loaded opinions.** Per curiam and short opinions (UATP, Jennions) state the result in
  the first paragraph. That sentence is redacted, but in reasoning scope the direction is still
  readable. Use facts scope.
- **Heuristic headings.** The facts boundary relies on headings. "Part I = background" is a US
  convention that the tool flags as CHECK. Opinions without headings fail closed.
- **Legal Data Hunter intake is untested.** Its daily quota was used up on Nov 10. The parser
  handles a `text` field and refuses `text_truncated`.
- **Tested so far**: CourtListener (US) only, plus synthetic CN/JP/NZ text. Real CN/JP sources
  remain blocked as in CORRECTIONS C9.
