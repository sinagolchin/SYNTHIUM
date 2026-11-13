"""Emergent dimensions from citation structure -- the from-scratch measurement layer.

The 12 hand-coded units are gone. They violated the only rule a unit must obey:

    A dimension is admissible only if it can be extracted from the record
    REPRODUCIBLY, with no subjective coding, and it must EARN its place by
    carrying real structure -- not by doctrinal storytelling.

The first substrate that obeys that rule is the set of precedents each opinion
cites. A citation is a fact in the record (and in the API), needs zero human
judgment, and scales to every published case ever decided. So instead of
imposing dimensions, we let them emerge:

  * A HUB precedent (cited by many cases) is a candidate dimension: "does this
    case rely on precedent X?" is a reproducible 0/1 feature.
  * Cases that share citations form emergent FAMILIES -- candidate clusters,
    discovered, not declared.

Nothing here is validated yet. A candidate dimension becomes a real one only
when it predicts the independent outcome on held-out cases (synthium.core.
validation). This module finds candidates and hands them to that gate; it never
certifies them itself.
"""

from __future__ import annotations

import itertools
import json
from dataclasses import dataclass, field
from typing import Dict, FrozenSet, List, Optional, Sequence, Tuple

from ...paths import data_path

_SEED_NAME = "citation_seed.json"


@dataclass(frozen=True)
class CaseRecord:
    """A case as objective data: identity, the precedents it cites, maybe an outcome.

    No hand-coded units. ``citations`` is the feature substrate; ``outcome`` is the
    independent target, present only where read from the disposition.
    """

    id: str
    name: str
    court: str
    date: str
    citations: FrozenSet[int]
    outcome: Optional[str] = None


def load_cases(path: Optional[str] = None) -> List[CaseRecord]:
    path = path or str(data_path(_SEED_NAME))
    with open(path, encoding="utf-8") as f:
        blob = json.load(f)
    out: List[CaseRecord] = []
    for c in blob["cases"]:
        out.append(CaseRecord(
            id=c["id"], name=c["name"], court=c.get("court", ""), date=c.get("date", ""),
            citations=frozenset(c.get("citations", [])),
            outcome=c.get("outcome"),
        ))
    return out


# ---------------------------------------------------------------------------
# Hub precedents -- candidate dimensions, ranked by how many cases rely on them
# ---------------------------------------------------------------------------

@dataclass
class Hub:
    precedent_id: int
    degree: int                 # number of cases citing it
    cases: List[str] = field(default_factory=list)


def hub_precedents(cases: Sequence[CaseRecord], min_degree: int = 2) -> List[Hub]:
    counts: Dict[int, List[str]] = {}
    for c in cases:
        for cid in c.citations:
            counts.setdefault(cid, []).append(c.id)
    hubs = [Hub(p, len(ids), ids) for p, ids in counts.items() if len(ids) >= min_degree]
    hubs.sort(key=lambda h: (-h.degree, h.precedent_id))
    return hubs


# ---------------------------------------------------------------------------
# Emergent families -- cluster cases by shared citations (Jaccard)
# ---------------------------------------------------------------------------

def jaccard(a: FrozenSet[int], b: FrozenSet[int]) -> float:
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def similarity_pairs(cases: Sequence[CaseRecord], threshold: float = 0.0
                     ) -> List[Tuple[str, str, float]]:
    pairs = []
    for a, b in itertools.combinations(cases, 2):
        s = jaccard(a.citations, b.citations)
        if s > threshold:
            pairs.append((a.id, b.id, s))
    pairs.sort(key=lambda t: -t[2])
    return pairs


def families(cases: Sequence[CaseRecord], threshold: float = 0.05) -> List[List[str]]:
    """Single-linkage clusters: connect two cases sharing > threshold citations."""
    parent = {c.id: c.id for c in cases}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: str, y: str) -> None:
        parent[find(x)] = find(y)

    for a, b, s in similarity_pairs(cases, threshold):
        union(a, b)
    groups: Dict[str, List[str]] = {}
    for c in cases:
        groups.setdefault(find(c.id), []).append(c.id)
    return sorted(groups.values(), key=lambda g: -len(g))


# ---------------------------------------------------------------------------
# The validation hook -- can a hub feature predict the independent outcome?
# ---------------------------------------------------------------------------

@dataclass
class HubSignalReport:
    testable: bool
    detail: str
    n_with_outcome: int


def hub_outcome_signal(cases: Sequence[CaseRecord], hub: Hub) -> HubSignalReport:
    """Does presence of a hub precedent associate with the outcome?

    Honest by construction: returns 'not testable' until enough cases carry an
    independent outcome. A candidate dimension earns nothing here -- it only
    becomes eligible for the real held-out validation in synthium.core.validation.
    """
    labeled = [c for c in cases if c.outcome in ("GRANTED", "DENIED")]
    if len(labeled) < 8:
        return HubSignalReport(
            False,
            (f"only {len(labeled)} cases carry an independent outcome; need many "
             "more before any hub's predictive value can be assessed. Citations "
             "scale freely -- outcomes are the part still being gathered."),
            len(labeled))
    present = [c for c in labeled if hub.precedent_id in c.citations]
    absent = [c for c in labeled if hub.precedent_id not in c.citations]

    def grant_rate(group):
        return sum(1 for c in group if c.outcome == "GRANTED") / len(group) if group else 0.0

    return HubSignalReport(
        True,
        (f"precedent {hub.precedent_id}: grant-rate present={grant_rate(present):.0%} "
         f"(n={len(present)}) vs absent={grant_rate(absent):.0%} (n={len(absent)})"),
        len(labeled))


def summarize(cases: Sequence[CaseRecord]) -> Dict[str, object]:
    hubs = hub_precedents(cases)
    fams = families(cases)
    labeled = sum(1 for c in cases if c.outcome in ("GRANTED", "DENIED"))
    return {
        "n_cases": len(cases),
        "n_with_outcome": labeled,
        "n_distinct_precedents": len({cid for c in cases for cid in c.citations}),
        "n_hub_precedents": len(hubs),
        "n_families": len(fams),
        "largest_family": max((len(f) for f in fams), default=0),
    }
