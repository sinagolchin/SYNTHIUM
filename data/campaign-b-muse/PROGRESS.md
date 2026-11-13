# campaign-b-muse — PROGRESS

Muse's own open-phase blind log. Non-US cases only.

## Split (Sina, Nov 12, 2026)

- Campaign A is finished (20/20, in `data/campaign-a/`).
- Muse codes non-US cases only, and logs them here, in `data/campaign-b-muse/`,
  in its own hash-chained blind log. Same blind protocol as Campaign A:
  seal first, code from the facts section only, commit before reveal.
- Muse does NOT write to `data/campaign-a/`, `VERIFIED_LEDGER.csv`, or
  `T1_POINTS.csv`. The other agent copies Muse's finished cases into the
  ledger from this folder.
- This folder is the non-US open-phase split Sina assigned Nov 12. It is not
  the ROADMAP section 3 stacking-vs-level-invariance fork; that fork keeps
  its own name if and when it runs.

## Status

- Cases coded here: 0.
- `blindlog.jsonl` does not exist yet. The first blind-tool run creates it
  through the tool's own courier-prompt flow. Do not hand-write log entries;
  the chain must start clean with the tool.
- Sealed full texts go in `sealed/` in this folder. Sealed files are never
  overwritten, and a sealed case id is never reused.
- Scheduled runs: twice daily, up to 9 cases per run (cadence carried from
  the Nov 12 open-phase schedule; Sina to correct if he meant otherwise).

## Open question

- Case source for non-US cases is not settled. CourtListener covers US
  courts only, so it cannot supply this folder. Until Sina confirms a
  non-US source, runs code nothing and fabricate nothing.
