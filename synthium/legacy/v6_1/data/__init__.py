"""Synthium data layer.

  atlas          load the 44-case rubric-coded atlas (leakage-aware)
  courtlistener  label real court records with rubric-INDEPENDENT outcomes

These play different roles. The atlas supplies rubric-derived features; the
court record supplies a target that no rubric touched. A model graded against
its own rubric is grading its own homework -- so validation targets come from
courtlistener, never from the atlas's outcome column alone.
"""

from .atlas import (
    Case,
    OPERATOR_COLUMNS,
    UNIT_COLUMNS,
    cluster_outcome_leakage,
    load_atlas,
    outcome_distribution,
    redact_outcome_words,
    stratified_split,
)

__all__ = [
    "Case", "UNIT_COLUMNS", "OPERATOR_COLUMNS",
    "load_atlas", "stratified_split", "redact_outcome_words",
    "outcome_distribution", "cluster_outcome_leakage",
]
