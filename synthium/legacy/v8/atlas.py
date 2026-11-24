"""Loader for the 44-case judicial suppression atlas.

What the atlas IS: a set of case studies chosen to probe doctrinal structure,
each hand-coded against the Synthium rubric (12 unit values + 18 operator flags
+ a cluster label + an outcome).

What the atlas is NOT: a statistical sample, and not a source of ground truth
independent of the rubric. Its unit/operator/cluster columns all originate from
the same human coding whose validity a model would be trying to establish.
Predicting them is *rubric imitation*, not predictive validity. For an
independent target, label outcomes straight from the court record
(:mod:`synthium.data.courtlistener`).

This loader is leakage-aware by construction. The three leaks recorded in
``EMPIRICAL_STATUS.md`` are designed out rather than patched:

  1. The ``cluster`` label is NEVER folded into the model's input text.
  2. ``redact_outcome_words`` strips outcome-revealing phrases from the text.
  3. The cluster column is returned separately so it cannot be used as a
     supervised signal by accident.
"""

from __future__ import annotations

import csv
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

UNIT_COLUMNS: Tuple[str, ...] = (
    "Obs", "Priv", "Excp", "Rem", "Close", "Amb",
    "Temp", "Gate", "Bound", "Spec", "Scope", "JRem",
)

OPERATOR_COLUMNS: Tuple[str, ...] = (
    "op_abandonment", "op_consent", "op_exigency", "op_good_faith",
    "op_attenuation", "op_private_search", "op_scope_breach", "op_curtilage",
    "op_emergency_aid", "op_public_exposure", "op_automobile_exception",
    "op_protective_sweep", "op_probation_waiver", "op_search_incident",
    "op_boundary_reclassification", "op_digital_privacy", "op_home_core",
    "op_warrant_particularity",
)

# RESTORED 2026-11-24: path now points at this restored copy's data_files/.
_DEFAULT_ATLAS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data_files", "judicial_suppression_atlas_v0_2.csv",
)

# Phrases that leak the outcome directly. Stripped from input text before any
# text-based model sees it. (Leak 2 in EMPIRICAL_STATUS.md.)
_OUTCOME_PHRASES = re.compile(
    r"\b(?:suppression\s+(?:denied|granted)"
    r"|motion\s+to\s+suppress\s+(?:is\s+|was\s+)?(?:denied|granted)"
    r"|evidence\s+(?:is\s+|was\s+)?suppress(?:ed)?"
    r"|conviction\s+affirmed|affirmed|reversed|vacated|remanded"
    r"|violated|granted|denied)\b",
    re.IGNORECASE,
)


def redact_outcome_words(text: str) -> str:
    """Replace outcome-revealing tokens with a neutral placeholder."""
    return _OUTCOME_PHRASES.sub("[REDACTED]", text or "")


@dataclass
class Case:
    """One atlas row. ``cluster`` is held apart from features deliberately."""

    case_id: str
    case_name: str
    cluster: str               # kept OUT of features() -- near-deterministic for outcome
    outcome: str
    text: str
    units: Dict[str, float] = field(default_factory=dict)
    operators: Dict[str, float] = field(default_factory=dict)

    def features(self, *, redact: bool = True, include_text: bool = True) -> Dict[str, object]:
        """Model-facing view. Never includes cluster; text redacted by default."""
        feat: Dict[str, object] = {"case_name": self.case_name}
        if include_text:
            feat["text"] = redact_outcome_words(self.text) if redact else self.text
        feat.update(self.units)
        feat.update({k: self.operators[k] for k in self.operators})
        return feat


def load_atlas(path: Optional[str] = None) -> List[Case]:
    """Read the atlas CSV into ``Case`` records."""
    path = path or _DEFAULT_ATLAS
    cases: List[Case] = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            units = {u: _to_float(row.get(u)) for u in UNIT_COLUMNS}
            ops = {c[len("op_"):]: _to_float(row.get(c)) for c in OPERATOR_COLUMNS}
            cases.append(Case(
                case_id=row.get("case_id", ""),
                case_name=row.get("case_name", ""),
                cluster=row.get("cluster", ""),
                outcome=row.get("outcome", "UNKNOWN"),
                text=row.get("text", ""),
                units=units,
                operators=ops,
            ))
    return cases


def _to_float(v: object) -> float:
    try:
        return float(v)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0.0


def stratified_split(cases: Sequence[Case], *, test_fraction: float = 0.25,
                     seed: int = 42) -> Tuple[List[Case], List[Case]]:
    """Outcome-stratified train/test split, reproducible by seed.

    Stratifying on the outcome keeps the class balance comparable across the
    split, so the majority-class baseline means the same thing on both sides.
    """
    import random

    by_outcome: Dict[str, List[Case]] = {}
    for c in cases:
        by_outcome.setdefault(c.outcome, []).append(c)

    rng = random.Random(seed)
    train: List[Case] = []
    test: List[Case] = []
    for outcome, group in sorted(by_outcome.items()):
        group = list(group)
        rng.shuffle(group)
        n_test = max(1, round(len(group) * test_fraction)) if len(group) > 1 else 0
        test.extend(group[:n_test])
        train.extend(group[n_test:])
    rng.shuffle(train)
    rng.shuffle(test)
    return train, test


def outcome_distribution(cases: Sequence[Case]) -> Dict[str, int]:
    dist: Dict[str, int] = {}
    for c in cases:
        dist[c.outcome] = dist.get(c.outcome, 0) + 1
    return dist


def cluster_outcome_leakage(cases: Sequence[Case]) -> Dict[str, Dict[str, int]]:
    """How deterministically each cluster predicts outcome.

    Reproduces the leakage table from EMPIRICAL_STATUS.md so the danger is
    visible in code, not just prose. Clusters that map to a single outcome are
    exactly why the cluster label must never enter the features.
    """
    table: Dict[str, Dict[str, int]] = {}
    for c in cases:
        table.setdefault(c.cluster, {})
        table[c.cluster][c.outcome] = table[c.cluster].get(c.outcome, 0) + 1
    return table
