"""Confidence labels (restored from V4). Every geometry result starts as UNTESTED.

V4's Axiom 0 is kept: all formulas are hypotheses, not truths.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class ConfidenceLevel(Enum):
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    SPECULATIVE = "SPECULATIVE"
    UNTESTED = "UNTESTED"  # added: computed, never checked on new cases


_RANK = {
    ConfidenceLevel.HIGH: 4,
    ConfidenceLevel.MODERATE: 3,
    ConfidenceLevel.LOW: 2,
    ConfidenceLevel.SPECULATIVE: 1,
    ConfidenceLevel.UNTESTED: 0,
}


@dataclass
class Confidence:
    level: ConfidenceLevel
    source: str
    limitations: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        return f"{self.level.value}: {self.source}"


AXIOM_0_AGNOSTICISM = (
    "AXIOM 0 (V4): all formulas are hypotheses, not truths. Discovered dimensions, "
    "metrics, geodesics and curvatures are estimates from finite data, and so is this axiom."
)


def aggregate_confidence(confidences: List[Confidence]) -> Confidence:
    """Weakest link: the overall level is the lowest input level."""
    if not confidences:
        return Confidence(ConfidenceLevel.UNTESTED, "No data", ["No measurements available"])
    worst = min(confidences, key=lambda c: _RANK[c.level])
    lims: List[str] = []
    for c in confidences:
        for l in c.limitations:
            if l not in lims:
                lims.append(l)
    return Confidence(worst.level, "Aggregated from: " + ", ".join(c.source for c in confidences), lims)


class FormulaConfidenceRegistry:
    def __init__(self) -> None:
        self.registry: Dict[str, Confidence] = {}

    def register(self, name: str, confidence: Confidence) -> None:
        self.registry[name] = confidence

    def get(self, name: str) -> Optional[Confidence]:
        return self.registry.get(name)

    def list_all(self) -> Dict[str, Confidence]:
        return dict(self.registry)


FORMULA_CONFIDENCE = FormulaConfidenceRegistry()
_COMMON = [
    "Scores are rankings from counted signs, with no real unit yet",
    "Most cases carry only a few qualities; analyses use the cases that share them",
    "Not yet checked on new cases",
]
for _name, _src in [
    ("build_up", "Dot -> line -> area -> volume on case scores"),
    ("is_new_dimension", "Best straight-line fit from other qualities vs shuffled"),
    ("parallel_analysis", "Eigenvalues vs shuffled qualities"),
    ("mahalanobis_distance", "Inverse-covariance distance with shrinkage"),
    ("curvature_index", "Paths along cases vs straight lines, vs shuffled"),
    ("metric_field_curvature", "Scalar curvature of a metric built from local spread"),
    ("rate_along", "Slope along reading order or filing date vs shuffled order"),
]:
    FORMULA_CONFIDENCE.register(_name, Confidence(ConfidenceLevel.UNTESTED, _src, list(_COMMON)))
