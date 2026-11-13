"""Synthium -- a framework for constructing and TESTING measurement rulers for
abstract concepts.

Synthium is not a discovered theory of qualitative reality. It is scaffolding in
which testable hypotheses about qualitative phenomena (privacy, exception
strength, suppression pressure, ...) can be expressed in a common language and
then validated -- or falsified -- against independent data.

    Synthium proposes rulers. Rulers earn the right to be called "structural"
    only through predictive success on independent data, never through
    architectural elegance.

The whole package is organised around one rule:

    Arithmetic always runs (synthium.core.values).
    Claims are refused until a held-out test passes (synthium.core.validation).

See README.md and docs/STATUS.md for the current evidence picture.
"""

from . import core, data
from .paths import data_dir, data_path
from .core import (
    PredictiveModel,
    ScaleType,
    Status,
    ValidationProtocol,
    Value,
    accuracy,
    macro_f1,
    majority_class_baseline,
    validate,
)

__version__ = "9.0.0"

__all__ = [
    "core", "data", "data_dir", "data_path",
    "PredictiveModel", "ScaleType", "Status", "ValidationProtocol", "Value",
    "accuracy", "macro_f1", "majority_class_baseline", "validate",
    "__version__",
]
