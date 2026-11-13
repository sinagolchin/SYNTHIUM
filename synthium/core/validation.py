"""The single refusal point of the whole framework.

A model is born ``PROPOSED``. Computing with it, inspecting it, tuning it -- all
fine, and none of it earns the model any standing. The ONLY path from
``PROPOSED`` to ``VALIDATED`` is passing a held-out, out-of-sample prediction
test against a baseline and margin that were frozen BEFORE the test outcomes
were seen.

``PredictiveModel.assert_validated()`` raises unless the model has actually
passed that test. That is the only place the framework says "no."

    Reality judges Synthium. Synthium never judges itself.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, Optional, Sequence

from .baseline import Baseline


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Metrics (higher is better, by convention)
# ---------------------------------------------------------------------------

def accuracy(y_true: Sequence[Any], y_pred: Sequence[Any]) -> float:
    if not y_true:
        return 0.0
    return sum(1 for a, b in zip(y_true, y_pred) if a == b) / len(y_true)


def macro_f1(y_true: Sequence[Any], y_pred: Sequence[Any]) -> float:
    """Unweighted mean F1 across classes -- fairer than accuracy on imbalance.

    On a skewed binary problem, accuracy can be high simply by echoing the
    majority class; macro-F1 punishes that, which is usually what we want when
    asking whether a model has learned anything real.
    """
    labels = set(y_true) | set(y_pred)
    if not labels:
        return 0.0
    f1s = []
    for label in labels:
        tp = sum(1 for t, p in zip(y_true, y_pred) if t == label and p == label)
        fp = sum(1 for t, p in zip(y_true, y_pred) if t != label and p == label)
        fn = sum(1 for t, p in zip(y_true, y_pred) if t == label and p != label)
        prec = tp / (tp + fp) if (tp + fp) else 0.0
        rec = tp / (tp + fn) if (tp + fn) else 0.0
        f1s.append(2 * prec * rec / (prec + rec) if (prec + rec) else 0.0)
    return sum(f1s) / len(f1s)


# ---------------------------------------------------------------------------
# Status + verdict
# ---------------------------------------------------------------------------

class Status(Enum):
    PROPOSED = "PROPOSED"    # exists, computes, has earned nothing
    VALIDATED = "VALIDATED"  # beat its pre-declared baseline by its margin
    FALSIFIED = "FALSIFIED"  # did not


class NotValidatedError(RuntimeError):
    """Raised by assert_validated() on any model that has not passed its test."""


@dataclass
class Verdict:
    status: Status
    metric_name: str
    model_score: float
    baseline_name: str
    baseline_score: float
    margin_required: float
    margin_observed: float
    n_test: int
    timestamp: str = field(default_factory=_now)

    def explain(self) -> str:
        passed = self.status == Status.VALIDATED
        return (
            f"[{self.status.value}] {self.metric_name}: "
            f"model={self.model_score:.3f} vs baseline "
            f"({self.baseline_name})={self.baseline_score:.3f} | "
            f"observed margin {self.margin_observed:+.3f}, "
            f"required {self.margin_required:+.3f} "
            f"-> {'cleared' if passed else 'did NOT clear'} on n={self.n_test}"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "metric": self.metric_name,
            "model_score": self.model_score,
            "baseline_name": self.baseline_name,
            "baseline_score": self.baseline_score,
            "margin_required": self.margin_required,
            "margin_observed": self.margin_observed,
            "n_test": self.n_test,
            "timestamp": self.timestamp,
        }


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

class PredictiveModel:
    """Wraps a predict() function. Computes freely; claims nothing until tested."""

    def __init__(self, name: str, predict_fn: Callable[[Dict[str, Any]], Any]):
        self.name = name
        self.predict_fn = predict_fn
        self.status = Status.PROPOSED
        self.verdict: Optional[Verdict] = None

    def predict(self, features: Dict[str, Any]) -> Any:
        return self.predict_fn(features)  # always allowed

    def assert_validated(self) -> None:
        """The one refusal in the whole framework."""
        if self.status != Status.VALIDATED:
            raise NotValidatedError(
                f"Model {self.name!r} is {self.status.value}. It may not be used to "
                f"make claims about reality until it has passed a held-out prediction "
                f"test against its pre-declared baseline and margin. Run validate() first."
            )


# ---------------------------------------------------------------------------
# Protocol + validation
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ValidationProtocol:
    """Everything frozen BEFORE the test outcomes are touched.

    metric:    (y_true, y_pred) -> score, higher is better
    baseline:  a frozen Baseline rule
    required_margin: how much the model must beat the baseline by (declared,
                     not derived by the framework)
    """

    metric_name: str
    metric: Callable[[Sequence[Any], Sequence[Any]], float]
    baseline: Baseline
    required_margin: float
    declared_at: str = field(default_factory=_now)


def validate(model: PredictiveModel,
             protocol: ValidationProtocol,
             test_features: Sequence[Dict[str, Any]],
             test_labels: Sequence[Any]) -> Verdict:
    """Run the model and the baseline on the SAME held-out cases. Compare.

    This function evaluates; it does not split. Guaranteeing that the model
    never saw these outcomes during fitting is the caller's responsibility --
    the harness cannot enforce what it cannot see.
    """
    model_pred = [model.predict(f) for f in test_features]
    base_pred = [protocol.baseline.predict(f) for f in test_features]

    model_score = protocol.metric(test_labels, model_pred)
    base_score = protocol.metric(test_labels, base_pred)
    observed = model_score - base_score

    status = Status.VALIDATED if observed >= protocol.required_margin else Status.FALSIFIED
    verdict = Verdict(
        status=status,
        metric_name=protocol.metric_name,
        model_score=model_score,
        baseline_name=protocol.baseline.name,
        baseline_score=base_score,
        margin_required=protocol.required_margin,
        margin_observed=observed,
        n_test=len(test_labels),
    )
    model.status = status
    model.verdict = verdict
    return verdict
