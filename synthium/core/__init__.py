"""Synthium Core -- the universal, domain-independent layer.

Three pieces, in dependency order:

  values      arithmetic that always runs and logs its assumptions
  baseline    prediction rules frozen before the test
  validation  the one refusal point: PROPOSED -> VALIDATED only via a held-out test
"""

from .values import (
    Assumption,
    Provenance,
    ScaleType,
    SUPPORTS,
    Value,
    measured,
    stipulated,
)
from .baseline import Baseline, keyword_baseline, majority_class_baseline
from . import axioms
from .axioms import Axiom, AxiomCase, AxiomResult, AxiomStatus
from .validation import (
    NotValidatedError,
    PredictiveModel,
    Status,
    ValidationProtocol,
    Verdict,
    accuracy,
    macro_f1,
    validate,
)

__all__ = [
    "Assumption", "Provenance", "ScaleType", "SUPPORTS", "Value",
    "measured", "stipulated",
    "Baseline", "keyword_baseline", "majority_class_baseline",
    "axioms", "Axiom", "AxiomCase", "AxiomResult", "AxiomStatus",
    "NotValidatedError", "PredictiveModel", "Status", "ValidationProtocol",
    "Verdict", "accuracy", "macro_f1", "validate",
]
