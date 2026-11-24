#!/usr/bin/env python3
"""SYNTHIUM v6.0 — PREDICTIVE HARNESS.

The correction to v5.0.

v5.0 gated COMPUTATION: it refused to do arithmetic on values whose scale type
didn't support it. That was the wrong place to put the gate. Refusing to
compute means you can never even propose a model, and a system that cannot
propose cannot discover. The diagnosis from that session: v5.0 gated the wrong
layer.

v6.0 inverts it. The gate moves from computation to CLAIMS.

    - Arithmetic ALWAYS runs. Always. No ScaleTypeError, ever.
    - When an operation rests on an assumption the data doesn't justify
      (multiplying two ordinals, treating a constructed scale as ratio), the
      framework does NOT refuse. It RECORDS the assumption in a provenance log
      attached to the result, and moves on.
    - A model is born PROPOSED. Computing with it, inspecting it, tuning it —
      all fine. None of that earns it any standing.
    - The ONLY path from PROPOSED to VALIDATED is passing a held-out,
      out-of-sample prediction test against a baseline and margin that were
      frozen BEFORE the test outcomes were seen.
    - assert_validated() is the single refusal point. It raises unless the
      model has actually passed that test. That is the only place the framework
      says "no."

The discipline this enforces:
    Reality judges Synthium. Synthium never judges itself.
    A baseline is a frozen RULE, not a number carried forward. Its score is
    produced by running it on the same future test cases the model is run on.
    The margin is declared by the experimenter, not invented by the framework.

USAGE
-----
    python synthium_v6_0_predictive.py            # runs the demo (VALIDATED + FALSIFIED)
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ============================================================================
# 1. SCALE TYPES + ASSUMPTIONS — arithmetic runs; violations are logged
# ============================================================================

class ScaleType(Enum):
    NOMINAL = "nominal"
    ORDINAL = "ordinal"
    INTERVAL = "interval"
    RATIO = "ratio"


# Which operations a scale type actually *supports*. Used not to forbid, but to
# decide whether an operation needs an assumption logged against its result.
_SUPPORTS: Dict[ScaleType, set] = {
    ScaleType.NOMINAL: {"=="},
    ScaleType.ORDINAL: {"==", "<", "<=", ">", ">="},
    ScaleType.INTERVAL: {"==", "<", "<=", ">", ">=", "+", "-", "scalar_mul"},
    ScaleType.RATIO: {"==", "<", "<=", ">", ">=", "+", "-", "scalar_mul", "*", "/"},
}


@dataclass(frozen=True)
class Assumption:
    """Something the arithmetic took for granted that the data didn't license.

    v5.0 would have raised here. v6.0 records it and keeps going. The assumption
    travels with the value, so the audit trail is complete without the gate ever
    blocking forward motion.
    """
    operation: str
    scale_type: str
    detail: str
    timestamp: str = field(default_factory=_now)


@dataclass
class Provenance:
    """Where a value came from and what was assumed to get there."""
    origin: str                         # "measured" | "stipulated" | "derived"
    derivation: str
    assumptions: Tuple[Assumption, ...] = ()

    def with_assumption(self, a: Assumption) -> "Provenance":
        return Provenance(self.origin, self.derivation, self.assumptions + (a,))


class Value:
    """A number tagged with scale type and provenance. Computes unconditionally.

    Every operation succeeds. If the scale type doesn't support the operation,
    the result simply carries an Assumption noting that. Nothing is refused at
    this layer — that's the whole v6.0 thesis.
    """

    def __init__(self, x: float, scale: ScaleType, unit: str, prov: Provenance):
        self.x = float(x)
        self.scale = scale
        self.unit = unit
        self.prov = prov

    def _derive(self, x: float, op: str, other: Optional["Value"], note: str) -> "Value":
        prov = Provenance(origin="derived", derivation=note)
        if op not in _SUPPORTS[self.scale]:
            prov = prov.with_assumption(Assumption(
                operation=op, scale_type=self.scale.value,
                detail=f"{op!r} is not supported by a {self.scale.value} scale; "
                       f"result assumes it behaves as if it were.",
            ))
        unit = self.unit if other is None or other.unit == self.unit else f"{self.unit}·{other.unit}"
        return Value(x, self.scale, unit, prov)

    def __add__(self, o: "Value") -> "Value":
        return self._derive(self.x + o.x, "+", o, f"{self} + {o}")

    def __sub__(self, o: "Value") -> "Value":
        return self._derive(self.x - o.x, "-", o, f"{self} - {o}")

    def __mul__(self, o: Any) -> "Value":
        if isinstance(o, (int, float)):
            return self._derive(self.x * float(o), "scalar_mul", None, f"{self} * {o}")
        return self._derive(self.x * o.x, "*", o, f"{self} * {o}")

    def __truediv__(self, o: Any) -> "Value":
        if isinstance(o, (int, float)):
            return self._derive(self.x / float(o), "scalar_mul", None, f"{self} / {o}")
        return self._derive(self.x / o.x, "/", o, f"{self} / {o}")

    def all_assumptions(self) -> Tuple[Assumption, ...]:
        return self.prov.assumptions

    def __repr__(self) -> str:
        n = len(self.prov.assumptions)
        return f"Value({self.x:.4g} {self.unit} [{self.scale.value}], assumptions={n})"


# ============================================================================
# 2. BASELINE — a frozen rule, not a number
# ============================================================================

@dataclass(frozen=True)
class Baseline:
    """A prediction rule frozen before the test. Its SCORE does not exist yet.

    The score is produced later, by running this rule on the same held-out
    cases the model is run on. That is the only honest way to compare: the
    baseline earns its number on the future, alongside the model.
    """
    name: str
    rule: Callable[[Dict[str, Any]], Any]   # features -> predicted label
    declared_at: str = field(default_factory=_now)

    def predict(self, features: Dict[str, Any]) -> Any:
        return self.rule(features)


def majority_class_baseline(train_labels: Sequence[Any]) -> Baseline:
    """The standard floor: always predict the training-majority label."""
    counts: Dict[Any, int] = {}
    for y in train_labels:
        counts[y] = counts.get(y, 0) + 1
    majority = max(counts, key=counts.get) if counts else None
    return Baseline(
        name=f"always-predict-{majority}",
        rule=lambda _features, _m=majority: _m,
    )


# ============================================================================
# 3. MODELS — born PROPOSED; only a held-out test changes that
# ============================================================================

class Status(Enum):
    PROPOSED = "PROPOSED"      # exists, computes, has earned nothing
    VALIDATED = "VALIDATED"    # beat its pre-declared baseline by its margin
    FALSIFIED = "FALSIFIED"    # failed to


class NotValidatedError(RuntimeError):
    """Raised by assert_validated() on any model that hasn't passed its test."""


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


class PredictiveModel:
    """Wraps a predict() function. Computes freely; claims nothing until tested."""

    def __init__(self, name: str, predict_fn: Callable[[Dict[str, Any]], Any]):
        self.name = name
        self.predict_fn = predict_fn
        self.status = Status.PROPOSED
        self.verdict: Optional[Verdict] = None

    def predict(self, features: Dict[str, Any]) -> Any:
        return self.predict_fn(features)            # always allowed

    def assert_validated(self) -> None:
        """The one refusal in the whole framework."""
        if self.status != Status.VALIDATED:
            raise NotValidatedError(
                f"Model {self.name!r} is {self.status.value}. It may not be used to "
                f"make claims about reality until it has passed a held-out prediction "
                f"test against its pre-declared baseline and margin. "
                f"Run validate() first."
            )


# ============================================================================
# 4. VALIDATION — reality judges; the framework only reports
# ============================================================================

@dataclass(frozen=True)
class ValidationProtocol:
    """Everything frozen BEFORE the test outcomes are touched.

    metric:   (y_true, y_pred) -> score, higher is better
    baseline: a frozen Baseline rule
    margin:   how much the model must beat the baseline by (declared, not derived)
    """
    metric_name: str
    metric: Callable[[Sequence[Any], Sequence[Any]], float]
    baseline: Baseline
    required_margin: float
    declared_at: str = field(default_factory=_now)


def accuracy(y_true: Sequence[Any], y_pred: Sequence[Any]) -> float:
    if not y_true:
        return 0.0
    return sum(1 for a, b in zip(y_true, y_pred) if a == b) / len(y_true)


def validate(model: PredictiveModel,
             protocol: ValidationProtocol,
             test_features: Sequence[Dict[str, Any]],
             test_labels: Sequence[Any]) -> Verdict:
    """Run the model and the baseline on the SAME held-out cases. Compare.

    The model never saw these outcomes during fitting (that is the caller's
    responsibility to guarantee; this function evaluates, it does not split).
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


# ============================================================================
# 5. ADAPTER — consume LabeledCase records from synthium_courtlistener.py
# ============================================================================

def load_labeled_cases(jsonl_path: str,
                       drop_unknown: bool = True) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Read cases.jsonl into (features, labels) for the validation harness.

    Only court-derived labels are used as targets, and only confident ones by
    default — that keeps the ground truth independent of any rubric and free of
    the extractor's own uncertainty.
    """
    features: List[Dict[str, Any]] = []
    labels: List[str] = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            outcome = rec.get("outcome", "UNKNOWN")
            if drop_unknown and (outcome == "UNKNOWN" or not rec.get("extractor_confident")):
                continue
            if outcome in ("NOT_SUPPRESSION",):
                continue
            features.append({"text": rec.get("text", ""), "case_name": rec.get("case_name", "")})
            labels.append(outcome)
    return features, labels


# ============================================================================
# 6. DEMO — show a VALIDATED and a FALSIFIED verdict on synthetic data
# ============================================================================

def _demo() -> None:
    print("=" * 70)
    print(" SYNTHIUM v6.0 — predictive harness demo")
    print("=" * 70)

    # ---- Synthetic world: label depends on a hidden keyword "warrant" --------
    import random
    rng = random.Random(0)

    def make_case(has_signal: bool) -> Tuple[Dict[str, Any], str]:
        present = rng.random() < 0.5
        text = ("warrant " if present else "") + " ".join(
            rng.choice(["search", "home", "vehicle", "phone", "consent"]) for _ in range(5)
        )
        # Ground truth: DENIED when 'warrant' present, else GRANTED — IF signal exists.
        if has_signal:
            label = "SUPPRESSION_DENIED" if present else "SUPPRESSION_GRANTED"
        else:
            label = rng.choice(["SUPPRESSION_DENIED", "SUPPRESSION_GRANTED"])
        return {"text": text}, label

    def split(has_signal: bool, n: int):
        data = [make_case(has_signal) for _ in range(n)]
        feats = [d[0] for d in data]
        labs = [d[1] for d in data]
        return feats, labs

    # ---- A model that reads the signal ('warrant' -> DENIED) -----------------
    def signal_model(f: Dict[str, Any]) -> str:
        return "SUPPRESSION_DENIED" if "warrant" in f["text"] else "SUPPRESSION_GRANTED"

    # ===== CASE A: signal exists -> model should VALIDATE =====================
    train_f, train_y = split(has_signal=True, n=80)
    test_f, test_y = split(has_signal=True, n=80)

    protocol = ValidationProtocol(
        metric_name="accuracy",
        metric=accuracy,
        baseline=majority_class_baseline(train_y),     # frozen BEFORE the test
        required_margin=0.10,                           # declared by the experimenter
    )
    model_a = PredictiveModel("warrant-reader", signal_model)
    verdict_a = validate(model_a, protocol, test_f, test_y)
    print("\nCASE A — real signal in the data:")
    print("  " + verdict_a.explain())
    try:
        model_a.assert_validated()
        print("  assert_validated(): passed — model may be used for claims.")
    except NotValidatedError as e:
        print(f"  assert_validated(): refused — {e}")

    # ===== CASE B: no signal -> same model should be FALSIFIED ================
    train_f2, train_y2 = split(has_signal=False, n=80)
    test_f2, test_y2 = split(has_signal=False, n=80)
    protocol2 = ValidationProtocol(
        metric_name="accuracy",
        metric=accuracy,
        baseline=majority_class_baseline(train_y2),
        required_margin=0.10,
    )
    model_b = PredictiveModel("warrant-reader", signal_model)
    verdict_b = validate(model_b, protocol2, test_f2, test_y2)
    print("\nCASE B — no signal in the data:")
    print("  " + verdict_b.explain())
    try:
        model_b.assert_validated()
        print("  assert_validated(): passed.")
    except NotValidatedError as e:
        print(f"  assert_validated(): refused — model stays PROPOSED/FALSIFIED.")

    # ---- show arithmetic runs but logs an assumption -------------------------
    print("\nArithmetic layer — runs even on unsupported ops, logs the assumption:")
    ordinal_a = Value(3, ScaleType.ORDINAL, "Excp",
                      Provenance("measured", "coder A on case X"))
    ordinal_b = Value(2, ScaleType.ORDINAL, "Excp",
                      Provenance("measured", "coder A on case Y"))
    product = ordinal_a * ordinal_b          # multiplying ordinals: not licensed
    print(f"  {product!r}")
    for a in product.all_assumptions():
        print(f"    assumption logged: {a.detail}")

    print("\n" + "=" * 70)
    print(" The framework computed everything and refused only at the claim layer.")
    print("=" * 70)


if __name__ == "__main__":
    _demo()
