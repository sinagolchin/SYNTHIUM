from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

class ConfidenceLevel(Enum):
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    SPECULATIVE = "SPECULATIVE"

@dataclass
class Confidence:
    level: ConfidenceLevel
    source: str
    limitations: List[str] = field(default_factory=list)
    numeric_score: Optional[float] = None
    source_type: str = "unspecified"
    age_steps: int = 0

    def decayed_score(self, decay_per_step: float = 0.02) -> float:
        base = self.numeric_score if self.numeric_score is not None else {
            ConfidenceLevel.HIGH: 0.9,
            ConfidenceLevel.MODERATE: 0.65,
            ConfidenceLevel.LOW: 0.35,
            ConfidenceLevel.SPECULATIVE: 0.15,
        }[self.level]
        return max(0.0, base * ((1.0 - decay_per_step) ** max(0, self.age_steps)))

AXIOM_0_AGNOSTICISM = """
AXIOM 0: AGNOSTICISM
ALL FORMULAS ARE HYPOTHESES, NOT TRUTHS.
Nothing in Synthium is absolute truth. We remain epistemically humble.
"""

def aggregate_confidence(confidences: List[Confidence]) -> Confidence:
    if not confidences:
        return Confidence(ConfidenceLevel.SPECULATIVE, "No data", ["No measurements available"], numeric_score=0.1)

    level_order = {
        ConfidenceLevel.HIGH: 3,
        ConfidenceLevel.MODERATE: 2,
        ConfidenceLevel.LOW: 1,
        ConfidenceLevel.SPECULATIVE: 0,
    }
    overall_level = min(confidences, key=lambda c: level_order[c.level]).level
    numeric = min(c.decayed_score() for c in confidences)
    sources = ", ".join(sorted(set(c.source for c in confidences)))
    limitations = sorted(set(item for c in confidences for item in c.limitations))
    return Confidence(
        level=overall_level,
        source=f"Aggregated from: {sources}",
        limitations=limitations,
        numeric_score=numeric,
        source_type="aggregated",
    )

class FormulaConfidenceRegistry:
    def __init__(self):
        self.registry = {}

    def register(self, formula_name: str, confidence: Confidence):
        self.registry[formula_name] = confidence

    def get(self, formula_name: str) -> Optional[Confidence]:
        return self.registry.get(formula_name)

FORMULA_CONFIDENCE = FormulaConfidenceRegistry()
