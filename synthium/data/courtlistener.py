#!/usr/bin/env python3
"""SYNTHIUM — CourtListener ingestion + rubric-independent outcome labeling.

WHAT THIS IS
------------
This module does ONE job: turn real court records into labeled cases whose
outcome label is *independent of any Synthium rubric*.

It is deliberately harness-agnostic: it produces a flat record that any model
can consume. The point is to supply the keystone the project needs: an outcome target that exists
in the court record, not one inferred from the same rubric whose validity is
being tested. A model graded against its own rubric is grading its own homework.

WHAT THIS IS NOT
----------------
- It is NOT a "ruler." Rulers are calibrated instruments (scale type, anchors,
  zero point, inter-rater reliability). This file builds none of those. It
  builds the *target* a proposed ruler must learn to predict.
- It is NOT itself validated. The rule-based extractor below is a FIRST-PASS
  labeler. Its own accuracy is an open empirical question and must be measured
  against human-coded cases before its labels can be trusted as ground truth.
  Outcome extraction from appellate opinions is a hard NLP problem; this code
  is conservative and emits UNKNOWN whenever the evidence is weak or conflicting
  rather than guessing. See extract_outcome() and the self-test at the bottom.

API NOTES (verified against CourtListener REST v4, mid-2026)
------------------------------------------------------------
- Search endpoint: /api/rest/v4/search/?type=o  (o = opinions)
- A token is now REQUIRED. Anonymous requests return 401. Get one from your
  CourtListener profile and pass it in (or set COURTLISTENER_TOKEN or
  COURTLISTENER_API_TOKEN).
- Pagination is cursor-based via the "next" URL. Paging past page 100 is
  blocked; for bulk work, narrow with filters (court, date) rather than deep
  paging.
- Full opinion text lives on the opinion object (plain_text); search snippets
  are short excerpts only. Clusters carry a structured "disposition" field.

USAGE (via the package CLI)
---------------------------
    export COURTLISTENER_TOKEN="...."
    python -m synthium courtlistener-selftest                # offline, no network
    python -m synthium.data.courtlistener --build --max 50 --out cases.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, Iterable, List, Optional, Tuple

BASE_URL = "https://www.courtlistener.com/api/rest/v4/"
USER_AGENT = "Synthium/research (rubric-independent outcome labeling)"


# ============================================================================
# 1. OUTCOME TAXONOMY — independent of the Synthium judicial rubric
# ============================================================================

class Outcome(str, Enum):
    """Disposition of a Fourth Amendment suppression question, as decided by
    the court itself. These categories describe the *court's* action, not any
    rubric's prediction of it.
    """
    SUPPRESSION_GRANTED = "SUPPRESSION_GRANTED"   # evidence suppressed / excluded
    SUPPRESSION_DENIED = "SUPPRESSION_DENIED"     # motion to suppress denied
    MIXED = "MIXED"                               # granted in part, denied in part
    NOT_SUPPRESSION = "NOT_SUPPRESSION"           # opinion isn't about suppression
    UNKNOWN = "UNKNOWN"                           # evidence too weak/conflicting


# ============================================================================
# 2. LABELED CASE — carries its own provenance so it stays auditable
# ============================================================================

@dataclass
class LabeledCase:
    """One case with a court-derived outcome label and the evidence for it.

    `outcome_origin` is fixed to "court_record" to make explicit, at the data
    layer, that this label did NOT come from a Synthium rubric. The matched
    evidence span is retained so a human can audit (or overturn) every label.
    """
    case_id: str
    case_name: str
    court: str
    date_filed: str
    absolute_url: str
    citation: str
    text: str                      # opinion plain_text (or snippet if that's all)
    outcome: str                   # Outcome value
    outcome_origin: str = "court_record"
    outcome_evidence: str = ""     # the exact phrase the label was read from
    outcome_source_field: str = "" # "cluster.disposition" or "opinion.plain_text"
    extractor_confident: bool = False
    raw: Dict = field(default_factory=dict)

    def to_json(self) -> str:
        d = asdict(self)
        d.pop("raw", None)  # keep export small; raw stays in memory only
        return json.dumps(d, ensure_ascii=False)


# ============================================================================
# 3. THE EXTRACTOR — transparent rules, conservative, auditable
# ============================================================================
#
# Appellate dispositions compose two things:
#   ACTION  : did the deciding court grant or deny suppression?
#   POSTURE : is this court affirming or reversing a lower ruling?
# A reversal FLIPS the lower court's action. We only emit a confident label
# when action + posture compose unambiguously. Everything else -> UNKNOWN.

_GRANT = re.compile(
    r"\b(?:motion\s+to\s+suppress\s+(?:is|was|be)\s+granted"
    r"|grant(?:ed|ing)?\s+the\s+motion\s+to\s+suppress"
    r"|evidence\s+(?:is|was|be)?\s*suppress(?:ed)?"
    r"|order(?:ing)?\s+suppression"
    r"|suppress(?:ion)?\s+(?:is|was)\s+granted)\b",
    re.I,
)
_DENY = re.compile(
    r"\b(?:motion\s+to\s+suppress\s+(?:is|was|be)\s+denied"
    r"|den(?:ied|ying|y)\s+the\s+motion\s+to\s+suppress"
    r"|suppress(?:ion)?\s+(?:is|was)\s+(?:properly\s+)?denied"
    r"|deni(?:al|ed)\s+of\s+(?:the\s+)?(?:motion\s+to\s+)?suppress(?:ion)?)\b",
    re.I,
)
_AFFIRM = re.compile(r"\b(?:we\s+)?affirm(?:ed|s|ing)?\b", re.I)
_REVERSE = re.compile(r"\b(?:we\s+)?(?:reverse|vacate)(?:d|s|ing)?\b", re.I)
_MIXED = re.compile(
    r"\b(?:granted\s+in\s+part[,;\s]+(?:and\s+)?denied\s+in\s+part"
    r"|affirmed\s+in\s+part[,;\s]+(?:and\s+)?reversed\s+in\s+part)\b",
    re.I,
)
_IS_SUPPRESSION = re.compile(r"\bsuppress|fourth\s+amendment|motion\s+to\s+suppress\b", re.I)


def _first_match(pat: re.Pattern, text: str) -> Optional[str]:
    m = pat.search(text or "")
    return m.group(0) if m else None


def extract_outcome(disposition: str, opinion_text: str) -> Tuple[Outcome, str, str, bool]:
    """Return (outcome, evidence_phrase, source_field, confident).

    Strategy, most-reliable first:
      1. If the structured cluster `disposition` field resolves cleanly, use it.
      2. Otherwise scan the opinion text.
    Conservative by design: ambiguity -> UNKNOWN, never a guess.
    """
    # Quick relevance gate: if neither field mentions suppression/4A, it's
    # almost certainly not a suppression ruling.
    blob = f"{disposition}\n{opinion_text}"
    if not _IS_SUPPRESSION.search(blob):
        return Outcome.NOT_SUPPRESSION, "", "relevance_gate", True

    for field_name, source in (("cluster.disposition", disposition),
                               ("opinion.plain_text", opinion_text)):
        if not source:
            continue
        out, evidence, confident = _resolve(source)
        if out is not None:
            return out, evidence, field_name, confident

    return Outcome.UNKNOWN, "", "none", False


def _resolve(text: str) -> Tuple[Optional[Outcome], str, bool]:
    """Resolve one text field into an outcome, or (None,...) if it can't."""
    if _MIXED.search(text):
        return Outcome.MIXED, _first_match(_MIXED, text), True

    grant = _first_match(_GRANT, text)
    deny = _first_match(_DENY, text)
    affirm = bool(_AFFIRM.search(text))
    reverse = bool(_REVERSE.search(text))

    # Conflicting action signals in the same field -> not safe to call here.
    if grant and deny:
        return None, "", False

    action: Optional[str] = "grant" if grant else ("deny" if deny else None)
    if action is None:
        return None, "", False

    evidence = grant or deny or ""

    # No posture verb: trial-court-style flat ruling. Take the action at face
    # value but mark it lower-confidence (could be quoting the court below).
    if not affirm and not reverse:
        out = Outcome.SUPPRESSION_GRANTED if action == "grant" else Outcome.SUPPRESSION_DENIED
        return out, evidence, True

    # Both affirm and reverse present -> appellate posture is ambiguous here.
    if affirm and reverse:
        return None, "", False

    # Compose action with posture. Reversal flips the lower court's action.
    if affirm:
        effective = action
    else:  # reverse / vacate
        effective = "deny" if action == "grant" else "grant"

    out = Outcome.SUPPRESSION_GRANTED if effective == "grant" else Outcome.SUPPRESSION_DENIED
    posture = _first_match(_AFFIRM if affirm else _REVERSE, text)
    return out, f"{evidence} | {posture}", True


# ============================================================================
# 4. COURTLISTENER v4 CLIENT — token-required, cursor-paginated
# ============================================================================

class CourtListenerError(RuntimeError):
    pass


class CourtListenerV4Client:
    def __init__(self, token: Optional[str] = None, base_url: str = BASE_URL,
                 min_interval_s: float = 1.0):
        self.token = (token or os.environ.get("COURTLISTENER_TOKEN")
                      or os.environ.get("COURTLISTENER_API_TOKEN"))
        self.base_url = base_url
        self.min_interval_s = min_interval_s
        self._last_call = 0.0
        if not self.token:
            raise CourtListenerError(
                "CourtListener v4 requires a token (anonymous requests get 401). "
                "Set COURTLISTENER_TOKEN or pass token=... . "
                "Get one from your CourtListener profile."
            )

    def _throttle(self) -> None:
        wait = self.min_interval_s - (time.time() - self._last_call)
        if wait > 0:
            time.sleep(wait)
        self._last_call = time.time()

    def _get(self, url: str) -> Dict:
        self._throttle()
        req = urllib.request.Request(
            url,
            headers={"Authorization": f"Token {self.token}", "User-Agent": USER_AGENT},
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 401:
                raise CourtListenerError("401 Unauthorized — token missing or invalid.") from e
            if e.code == 429:
                raise CourtListenerError("429 Throttled — raise min_interval_s and retry.") from e
            raise CourtListenerError(f"HTTP {e.code} for {url}") from e

    def search_opinions(self, query: str, max_results: int = 50,
                        **filters) -> Iterable[Dict]:
        """Yield raw search-result dicts (type=o), following cursor pages."""
        params = {"q": query, "type": "o"}
        params.update({k: v for k, v in filters.items() if v is not None})
        url = self.base_url + "search/?" + urllib.parse.urlencode(params)
        yielded = 0
        while url and yielded < max_results:
            data = self._get(url)
            for row in data.get("results", []):
                yield row
                yielded += 1
                if yielded >= max_results:
                    break
            url = data.get("next")

    def fetch_opinion_text(self, opinion_id: int) -> str:
        url = f"{self.base_url}opinions/{opinion_id}/"
        data = self._get(url)
        return data.get("plain_text") or data.get("html_with_citations") or ""

    def fetch_cluster(self, cluster_id: int) -> Dict:
        return self._get(f"{self.base_url}clusters/{cluster_id}/")


# Standard suppression query set (kept here so it's versioned with the labeler).
SUPPRESSION_QUERIES: Tuple[str, ...] = (
    '"motion to suppress" "Fourth Amendment" "good faith"',
    '"motion to suppress" "exigent circumstances"',
    '"motion to suppress" curtilage',
    '"motion to suppress" "geofence warrant"',
    '"motion to suppress" "private search"',
    '"motion to suppress" abandonment',
    '"motion to suppress" "search incident to arrest"',
)


def build_dataset(client: CourtListenerV4Client, queries: Iterable[str],
                  max_per_query: int = 20, fetch_full_text: bool = True) -> List[LabeledCase]:
    """Pull cases, label each via the court record, retain evidence + provenance."""
    cases: List[LabeledCase] = []
    seen: set = set()
    for q in queries:
        for row in client.search_opinions(q, max_results=max_per_query):
            cid = str(row.get("cluster_id") or row.get("id") or "")
            if not cid or cid in seen:
                continue
            seen.add(cid)

            disposition = ""
            opinion_text = row.get("snippet", "") or ""
            try:
                if fetch_full_text and row.get("cluster_id"):
                    cluster = client.fetch_cluster(int(row["cluster_id"]))
                    disposition = cluster.get("disposition", "") or ""
                    subs = cluster.get("sub_opinions", []) or []
                    if subs:
                        op_id = _opinion_id_from_uri(subs[0])
                        if op_id:
                            opinion_text = client.fetch_opinion_text(op_id) or opinion_text
            except CourtListenerError:
                pass  # fall back to snippet; label may be UNKNOWN, which is honest

            outcome, evidence, src, confident = extract_outcome(disposition, opinion_text)
            cites = row.get("citation") or []
            cases.append(LabeledCase(
                case_id=cid,
                case_name=row.get("caseName") or row.get("case_name") or "",
                court=row.get("court") or "",
                date_filed=row.get("dateFiled") or row.get("date_filed") or "",
                absolute_url=row.get("absolute_url") or "",
                citation="; ".join(map(str, cites)) if isinstance(cites, list) else str(cites),
                text=(opinion_text or "")[:20000],
                outcome=outcome.value,
                outcome_evidence=evidence,
                outcome_source_field=src,
                extractor_confident=confident,
                raw=row,
            ))
    return cases


def _opinion_id_from_uri(uri: str) -> Optional[int]:
    m = re.search(r"/opinions/(\d+)/", uri or "")
    return int(m.group(1)) if m else None


def write_jsonl(cases: List[LabeledCase], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for c in cases:
            f.write(c.to_json() + "\n")


def label_distribution(cases: List[LabeledCase]) -> Dict[str, int]:
    dist: Dict[str, int] = {}
    for c in cases:
        dist[c.outcome] = dist.get(c.outcome, 0) + 1
    return dist


# ============================================================================
# 5. SELF-TEST — verifies the extractor offline, against synthetic fixtures
# ============================================================================

# (disposition, opinion_text, expected_outcome)
_FIXTURES: List[Tuple[str, str, Outcome]] = [
    ("", "The motion to suppress is denied. The Fourth Amendment claim fails.",
     Outcome.SUPPRESSION_DENIED),
    ("", "We grant the motion to suppress the evidence seized from the home.",
     Outcome.SUPPRESSION_GRANTED),
    ("Affirmed.", "The trial court denied the motion to suppress; we affirm.",
     Outcome.SUPPRESSION_DENIED),
    ("Reversed.", "The court below denied the motion to suppress. We reverse.",
     Outcome.SUPPRESSION_GRANTED),  # reversal flips a denial -> grant
    ("Reversed.", "The order granting the motion to suppress is reversed.",
     Outcome.SUPPRESSION_DENIED),   # reversal flips a grant -> deny
    ("", "Granted in part and denied in part as to the suppression motion.",
     Outcome.MIXED),
    ("", "This appeal concerns a breach-of-contract dispute over a lease.",
     Outcome.NOT_SUPPRESSION),
    ("", "The parties dispute whether the Fourth Amendment motion to suppress "
         "should be granted or denied; the question is left for remand.",
     Outcome.UNKNOWN),  # both signals present -> refuse to guess
]


def run_self_test() -> bool:
    ok = True
    print("Offline extractor self-test")
    print("-" * 60)
    for i, (disp, text, expected) in enumerate(_FIXTURES, 1):
        out, evidence, src, conf = extract_outcome(disp, text)
        passed = out == expected
        ok &= passed
        flag = "PASS" if passed else "FAIL"
        print(f"[{flag}] case {i}: got {out.value:<20} (expected {expected.value})")
        if not passed:
            print(f"        evidence={evidence!r} src={src} confident={conf}")
    print("-" * 60)
    print("ALL PASS" if ok else "SOME FAILED")
    return ok


# ============================================================================
# 6. CLI
# ============================================================================

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("API NOTES")[0])
    p.add_argument("--self-test", action="store_true",
                   help="Run the offline extractor self-test (no network, no token).")
    p.add_argument("--build", action="store_true",
                   help="Pull cases from CourtListener and label them (needs token).")
    p.add_argument("--max", type=int, default=20, help="Max cases per query.")
    p.add_argument("--out", type=str, default="synthium_cases.jsonl")
    p.add_argument("--no-full-text", action="store_true",
                   help="Use search snippets only; skip cluster/opinion fetches.")
    args = p.parse_args()

    if args.self_test:
        raise SystemExit(0 if run_self_test() else 1)

    if args.build:
        client = CourtListenerV4Client()
        cases = build_dataset(client, SUPPRESSION_QUERIES,
                              max_per_query=args.max,
                              fetch_full_text=not args.no_full_text)
        write_jsonl(cases, args.out)
        dist = label_distribution(cases)
        confident = sum(1 for c in cases if c.extractor_confident)
        print(f"Wrote {len(cases)} cases -> {args.out}")
        print(f"Label distribution: {dist}")
        print(f"Extractor confident on {confident}/{len(cases)} "
              f"({confident / max(1, len(cases)):.0%}).")
        print("\nReminder: these labels are a FIRST-PASS read of the court record. "
              "Their accuracy is itself unmeasured. Hand-check a sample before "
              "treating them as ground truth.")
        return

    p.print_help()


if __name__ == "__main__":
    main()
