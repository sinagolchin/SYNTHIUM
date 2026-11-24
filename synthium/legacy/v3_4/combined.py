#!/usr/bin/env python3
"""
Synthium Omega v3.4 - The Agnostic Edition
Single-file cleaned build

This file consolidates the Synthium v3.4 code modules into one importable and
runnable Python module. It removes package-relative imports, consolidates shared
helpers, avoids duplicate definitions, and keeps a non-interactive command-line
entry point for safer use in notebooks, scripts, and tests.

Included modules, folded into this file:
- confidence.py
- vectors_v34.py
- framework_evolution.py
- empirical_agnostic.py
- perception_v34.py
- field_v34.py
- interactions_v34.py
- units_v34.py
- science_v34.py
- ethics_discovery.py
- main_v34.py
- __init__.py metadata and exports

Usage examples:
    from synthium_v34_combined import *

    vec = AgnosticRealityVector(0, 0, 0, v=0.2, R=0.3, r=0.8, C=0.7, S=0.2)
    print(vec.report_with_uncertainty())

    discovery = AgnosticEmpiricalDiscovery()
    prediction = discovery.predict_intervention_outcome(
        target_state=vec,
        intervener_state=AgnosticRealityVector(0, 0, 0, v=0.5, R=0.4, r=0.6, C=0.9, S=0.2),
        military_force=0.5,
        local_support=0.6,
        expected_duration=3.0,
    )
    print(prediction.full_report())
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

import argparse
import math
import sys

import numpy as np


# =============================================================================
# Shared helpers
# =============================================================================


def _clip01(value: float) -> float:
    """Clip a scalar to the inclusive [0, 1] range and return a plain float."""
    return float(np.clip(value, 0.0, 1.0))


def _safe_float(value: Any, default: float = 0.0) -> float:
    """Convert a value to float while providing a clean fallback."""
    try:
        out = float(value)
    except (TypeError, ValueError):
        return default
    if math.isnan(out) or math.isinf(out):
        return default
    return out


def _dedupe_preserve_order(values: Iterable[str]) -> List[str]:
    """Deduplicate strings while preserving first-seen order."""
    seen = set()
    out: List[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def _refresh_derived(vector: "AgnosticRealityVector") -> "AgnosticRealityVector":
    """Recompute derived metrics on a vector after state dimensions change."""
    vector.E = vector.compute_enjoyment()
    vector.M = vector.compute_meaning()
    vector.P = vector.compute_perception_accuracy()
    return vector


# =============================================================================
# confidence.py - confidence tracking and agnosticism declarations
# =============================================================================


class ConfidenceLevel(Enum):
    """Standardized confidence levels."""

    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    SPECULATIVE = "SPECULATIVE"
    UNKNOWN = "UNKNOWN"


_CONFIDENCE_ORDER = {
    ConfidenceLevel.HIGH: 4,
    ConfidenceLevel.MODERATE: 3,
    ConfidenceLevel.LOW: 2,
    ConfidenceLevel.SPECULATIVE: 1,
    ConfidenceLevel.UNKNOWN: 0,
}


@dataclass
class Confidence:
    """Explicit confidence tracking for any claim."""

    level: ConfidenceLevel
    basis: str
    limitations: List[str] = field(default_factory=list)
    unknowns: List[str] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"{self.level.value}: {self.basis}"

    def full_report(self) -> str:
        """Generate a full confidence report."""
        lines = [
            f"Confidence: {self.level.value}",
            f"Basis: {self.basis}",
        ]

        if self.limitations:
            lines.append("Known Limitations:")
            for limitation in self.limitations:
                lines.append(f" - {limitation}")

        if self.unknowns:
            lines.append("Known Unknowns:")
            for unknown in self.unknowns:
                lines.append(f" - {unknown}")

        return "\n".join(lines)


FORMULA_KEY_E = "E = 1 - (v*R + S)"
FORMULA_KEY_E_LEGACY = "E = 1 - (v·R + S)"
FORMULA_KEY_M = "M = C*r*(1-S)"
FORMULA_KEY_M_LEGACY = "M = C·r·(1-S)"
FORMULA_KEY_P = "P = (1-S)*C"
FORMULA_KEY_P_LEGACY = "P = (1-S)·C"

FORMULA_CONFIDENCE: Dict[str, Confidence] = {
    FORMULA_KEY_E: Confidence(
        level=ConfidenceLevel.MODERATE,
        basis="Derived formula that appears useful in tested cases",
        limitations=[
            "Not empirically optimized against a large dataset",
            "Assumes a simple linear combination of terms",
            "May be incomplete or wrong",
        ],
        unknowns=[
            "Hidden variables not captured",
            "Non-linear interactions may exist",
            "Cultural and contextual factors may be missing",
        ],
    ),
    FORMULA_KEY_M: Confidence(
        level=ConfidenceLevel.MODERATE,
        basis="Intuitive formula that appears to capture meaning dynamics",
        limitations=[
            "Not validated on a large dataset",
            "Meaning is subjective and difficult to measure",
            "May oversimplify a complex phenomenon",
        ],
        unknowns=[
            "Meaning may have non-multiplicative components",
            "Individual and collective meaning may differ",
            "Cultural variations are not captured",
        ],
    ),
    FORMULA_KEY_P: Confidence(
        level=ConfidenceLevel.MODERATE,
        basis="Operational proxy for perception accuracy",
        limitations=[
            "Treats perception as capacity minus entropy only",
            "Does not model attention, language, memory, or incentives",
            "May not transfer across systems",
        ],
        unknowns=[
            "Unmeasured cognitive and institutional variables",
            "Unknown nonlinear threshold effects",
            "Potential feedback loops between perception and state",
        ],
    ),
}
# Backward-compatible keys from the original package snippets.
FORMULA_CONFIDENCE[FORMULA_KEY_E_LEGACY] = FORMULA_CONFIDENCE[FORMULA_KEY_E]
FORMULA_CONFIDENCE[FORMULA_KEY_M_LEGACY] = FORMULA_CONFIDENCE[FORMULA_KEY_M]
FORMULA_CONFIDENCE[FORMULA_KEY_P_LEGACY] = FORMULA_CONFIDENCE[FORMULA_KEY_P]


_MEASUREMENT_ALIASES = {
    "v": "violence",
    "R": "resistance",
    "r": "resonance",
    "C": "capacity",
    "S": "entropy",
    "E": "enjoyment",
    "M": "meaning",
    "P": "perception",
}


def create_measurement_confidence(
    value: float,
    measurement_type: str,
    source: str,
    reliability: ConfidenceLevel,
) -> Confidence:
    """Create a Confidence object for a measurement."""
    canonical = _MEASUREMENT_ALIASES.get(measurement_type, measurement_type).lower()

    type_limitations = {
        "violence": ["Casualty or harm counts may be incomplete", "Measurement during chaos is difficult"],
        "capacity": ["Economic or resource data may be outdated", "Informal systems may not be captured"],
        "resonance": ["Polling or sentiment data may be biased", "Fear can affect responses"],
        "entropy": ["Subjective assessment", "May miss hidden order or coordination"],
        "resistance": ["Leadership opacity", "Internal factions may be unclear"],
        "enjoyment": ["Derived metric, not directly measured"],
        "meaning": ["Derived metric, not directly measured"],
        "perception": ["Derived metric, not directly measured"],
    }

    type_unknowns = {
        "violence": ["Hidden casualties", "Unreported incidents"],
        "capacity": ["Underground economy", "External support"],
        "resonance": ["Silent majority", "Coerced compliance"],
        "entropy": ["Emergent order", "Hidden coordination"],
        "resistance": ["Internal power struggles", "Succession plans"],
        "enjoyment": ["Unknown formula fit", "Hidden welfare variables"],
        "meaning": ["Unobserved values", "Cultural context"],
        "perception": ["Information distortion", "Cognitive and institutional blind spots"],
    }

    return Confidence(
        level=reliability,
        basis=f"{measurement_type}={value:.2f} from {source}",
        limitations=type_limitations.get(canonical, ["Measurement uncertainty"]),
        unknowns=type_unknowns.get(canonical, ["Unknown factors"]),
    )


def aggregate_confidence(confidences: List[Confidence]) -> Confidence:
    """Aggregate confidence levels using a weakest-link principle."""
    if not confidences:
        return Confidence(
            level=ConfidenceLevel.UNKNOWN,
            basis="No confidence components supplied",
            limitations=["No evidence was provided"],
            unknowns=["All aspects are uncertain"],
        )

    weakest = min(confidences, key=lambda c: _CONFIDENCE_ORDER.get(c.level, 0)).level
    limitations = _dedupe_preserve_order(lim for conf in confidences for lim in conf.limitations)
    unknowns = _dedupe_preserve_order(unk for conf in confidences for unk in conf.unknowns)

    return Confidence(
        level=weakest,
        basis=f"Aggregated from {len(confidences)} components",
        limitations=limitations,
        unknowns=unknowns,
    )


AXIOM_0_AGNOSTICISM = """
AXIOM 0: AGNOSTICISM
(Meta-Axiom)

All formulas, measurements, and predictions are HYPOTHESES, not absolute truths.
We remain uncertain about:
1. Whether reality is mathematical or only appears mathematical.
2. Whether our formulas are correct or incomplete.
3. Whether our measurements capture all relevant variables.
4. Whether the framework itself is sound.

Commitments:
1. Treat formulas as testable hypotheses.
2. Report uncertainty explicitly.
3. Update based on evidence.
4. Remain open to being wrong.
5. Never claim absolute truth.
""".strip()

AGNOSTICISM_REMINDER = """
This analysis is based on a framework that may be incomplete or incorrect.
- Formulas are HYPOTHESES, not proven truths.
- Measurements have UNCERTAINTY.
- Predictions are PROBABILISTIC, not certain.
- Reality may not follow our models.
Use this as ONE input to decision-making, not absolute truth.
Remain skeptical, including of this framework itself.
""".strip()


def print_agnosticism_axiom() -> None:
    """Print the agnosticism axiom."""
    print(AXIOM_0_AGNOSTICISM)


def print_agnosticism_reminder() -> None:
    """Print the brief agnosticism reminder."""
    print(AGNOSTICISM_REMINDER)


# =============================================================================
# vectors_v34.py - agnostic reality vectors
# =============================================================================


@dataclass
class AgnosticRealityVector:
    """11D reality vector with explicit uncertainty tracking."""

    x: float
    y: float
    z: float
    v: float  # Violence or velocity-like destabilizing pressure
    R: float  # Resistance
    r: float  # Resonance
    C: float  # Capacity
    S: float  # Entropy
    measurement_confidence: Dict[str, Confidence] = field(default_factory=dict)
    E: Optional[float] = None  # Enjoyment, derived hypothesis
    M: Optional[float] = None  # Meaning, derived hypothesis
    P: Optional[float] = None  # Perception accuracy, derived hypothesis

    def __post_init__(self) -> None:
        for dim in ["v", "R", "r", "C", "S"]:
            val = _safe_float(getattr(self, dim), default=-1.0)
            if not (0.0 <= val <= 1.0):
                raise ValueError(f"{dim} must be in [0, 1], got {getattr(self, dim)!r}")
            setattr(self, dim, val)

        self.x = _safe_float(self.x)
        self.y = _safe_float(self.y)
        self.z = _safe_float(self.z)

        if self.E is None:
            self.E = self._compute_enjoyment_hypothesis()
        else:
            self.E = _clip01(self.E)
        if self.M is None:
            self.M = self._compute_meaning_hypothesis()
        else:
            self.M = _clip01(self.M)
        if self.P is None:
            self.P = self._compute_perception_hypothesis()
        else:
            self.P = _clip01(self.P)

    def _compute_enjoyment_hypothesis(self) -> float:
        """Hypothesis: E = 1 - (v*R + S)."""
        return _clip01(1.0 - (self.v * self.R + self.S))

    def _compute_meaning_hypothesis(self) -> float:
        """Hypothesis: M = C*r*(1-S)."""
        return _clip01(self.C * self.r * (1.0 - self.S))

    def _compute_perception_hypothesis(self) -> float:
        """Hypothesis: P = (1-S)*C."""
        return _clip01((1.0 - self.S) * self.C)

    # Compatibility with older v3.x snippets.
    def compute_enjoyment(self) -> float:
        return self._compute_enjoyment_hypothesis()

    def compute_meaning(self) -> float:
        return self._compute_meaning_hypothesis()

    def compute_perception_accuracy(self) -> float:
        return self._compute_perception_hypothesis()

    def refresh(self) -> "AgnosticRealityVector":
        """Recompute derived metrics after direct mutation."""
        return _refresh_derived(self)

    def add_measurement_confidence(
        self,
        dimension: str,
        source: str,
        reliability: ConfidenceLevel,
    ) -> None:
        """Attach confidence metadata for a measured dimension."""
        if not hasattr(self, dimension):
            raise AttributeError(f"Unknown dimension {dimension!r}")
        self.measurement_confidence[dimension] = create_measurement_confidence(
            value=_safe_float(getattr(self, dimension)),
            measurement_type=dimension,
            source=source,
            reliability=reliability,
        )

    def get_overall_confidence(self) -> Confidence:
        """Aggregate measurement and formula confidence."""
        confidences = list(self.measurement_confidence.values())
        confidences.extend(
            [
                FORMULA_CONFIDENCE[FORMULA_KEY_E],
                FORMULA_CONFIDENCE[FORMULA_KEY_M],
                FORMULA_CONFIDENCE[FORMULA_KEY_P],
            ]
        )
        return aggregate_confidence(confidences)

    def report_with_uncertainty(self) -> str:
        """Generate a human-readable uncertainty report."""
        lines: List[str] = []
        lines.append("=" * 70)
        lines.append("AGNOSTIC REALITY VECTOR (v3.4)")
        lines.append("=" * 70)

        lines.append("\nMEASURED DIMENSIONS:")
        for dim in ["v", "R", "r", "C", "S"]:
            val = getattr(self, dim)
            line = f" {dim} = {val:.3f}"
            if dim in self.measurement_confidence:
                line += f" (Confidence: {self.measurement_confidence[dim].level.value})"
            else:
                line += " (Confidence: UNKNOWN - not specified)"
            lines.append(line)

        lines.append("\nDERIVED METRICS (HYPOTHESES):")
        lines.append(f" E = {self.E:.3f} (Enjoyment) | Formula: {FORMULA_KEY_E} | Confidence: {FORMULA_CONFIDENCE[FORMULA_KEY_E].level.value}")
        lines.append(f" M = {self.M:.3f} (Meaning) | Formula: {FORMULA_KEY_M} | Confidence: {FORMULA_CONFIDENCE[FORMULA_KEY_M].level.value}")
        lines.append(f" P = {self.P:.3f} (Perception) | Formula: {FORMULA_KEY_P} | Confidence: {FORMULA_CONFIDENCE[FORMULA_KEY_P].level.value}")

        overall = self.get_overall_confidence()
        lines.append("\nOVERALL CONFIDENCE:")
        lines.append(f" Level: {overall.level.value}")
        lines.append(f" Basis: {overall.basis}")

        if overall.limitations:
            lines.append("\nKNOWN LIMITATIONS:")
            for limitation in overall.limitations[:5]:
                lines.append(f" - {limitation}")

        if overall.unknowns:
            lines.append("\nKNOWN UNKNOWNS:")
            for unknown in overall.unknowns[:5]:
                lines.append(f" - {unknown}")

        lines.append("\n" + "=" * 70)
        lines.append("AGNOSTICISM REMINDER")
        lines.append("=" * 70)
        lines.append("These metrics are based on hypothetical formulas.")
        lines.append("They may be wrong, incomplete, or misleading.")
        lines.append("Use them as one input, not absolute truth.")
        lines.append("=" * 70)
        return "\n".join(lines)

    def copy(self) -> "AgnosticRealityVector":
        """Create a copy with confidence metadata."""
        return AgnosticRealityVector(
            self.x,
            self.y,
            self.z,
            self.v,
            self.R,
            self.r,
            self.C,
            self.S,
            measurement_confidence=self.measurement_confidence.copy(),
            E=self.E,
            M=self.M,
            P=self.P,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary for serialization or compatibility."""
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "v": self.v,
            "R": self.R,
            "r": self.r,
            "C": self.C,
            "S": self.S,
            "E": self.E,
            "M": self.M,
            "P": self.P,
            "confidence": self.get_overall_confidence().level.value,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgnosticRealityVector":
        """Create a vector from a dictionary."""
        return cls(
            x=data["x"],
            y=data["y"],
            z=data["z"],
            v=data["v"],
            R=data["R"],
            r=data["r"],
            C=data["C"],
            S=data["S"],
            E=data.get("E"),
            M=data.get("M"),
            P=data.get("P"),
        )

    def state_array(self, include_spatial: bool = False) -> np.ndarray:
        """Return numeric state as a NumPy array."""
        base = [self.v, self.R, self.r, self.C, self.S, self.E, self.M, self.P]
        if include_spatial:
            base = [self.x, self.y, self.z] + base
        return np.array(base, dtype=float)

    def distance_to(self, other: "AgnosticRealityVector", include_spatial: bool = False) -> float:
        """Euclidean distance in qualitative state space."""
        return float(np.linalg.norm(self.state_array(include_spatial) - other.state_array(include_spatial)))

    def __repr__(self) -> str:
        conf = self.get_overall_confidence()
        return f"AgnosticRealityVector(v={self.v:.2f}, E={self.E:.2f}, Confidence={conf.level.value})"


# Compatibility alias for code expecting RealityVector.
RealityVector = AgnosticRealityVector


# =============================================================================
# framework_evolution.py - formula testing and framework evolution
# =============================================================================


@dataclass
class FormulaTest:
    """Results of testing a formula against data."""

    formula_name: str
    current_error: float
    proposed_error: float
    improvement: float
    sample_size: int
    recommendation: str
    confidence: Confidence


class FrameworkEvolution:
    """Meta-level class for testing and improving framework formulas."""

    def __init__(self) -> None:
        self.current_formulas: Dict[str, Callable[..., float]] = {
            "E": lambda v, R, S: _clip01(1.0 - (v * R + S)),
            "M": lambda C, r, S: _clip01(C * r * (1.0 - S)),
            "P": lambda C, S: _clip01((1.0 - S) * C),
        }
        self.test_history: List[FormulaTest] = []

    @staticmethod
    def _measure_error(formula: Callable[..., float], test_data: List[Dict[str, float]], variables: List[str]) -> float:
        """Measure mean absolute error for a formula against observed data."""
        errors: List[float] = []
        observed_key = "observed_E"
        for row in test_data:
            if observed_key not in row or any(var not in row for var in variables):
                continue
            try:
                predicted = _clip01(formula(*[_safe_float(row[var]) for var in variables]))
                observed = _clip01(row[observed_key])
            except Exception:
                continue
            errors.append(abs(predicted - observed))
        if not errors:
            return float("inf")
        return float(np.mean(errors))

    def test_alternative_E_formula(self, new_formula: Callable[..., float], test_data: List[Dict[str, float]]) -> FormulaTest:
        """Test an alternative formula for Enjoyment/E."""
        current_formula = self.current_formulas["E"]
        current_error = self._measure_error(current_formula, test_data, ["v", "R", "S"])
        new_error = self._measure_error(new_formula, test_data, ["v", "R", "S"])
        improvement = current_error - new_error

        if improvement > 0.15:
            recommendation = "STRONGLY RECOMMEND ADOPTION"
        elif improvement > 0.05:
            recommendation = "RECOMMEND ADOPTION"
        elif improvement > -0.05:
            recommendation = "NEUTRAL - Keep testing"
        else:
            recommendation = "KEEP CURRENT"

        sample_size = len(test_data)
        if sample_size > 100:
            conf_level = ConfidenceLevel.HIGH
        elif sample_size > 30:
            conf_level = ConfidenceLevel.MODERATE
        elif sample_size > 0:
            conf_level = ConfidenceLevel.LOW
        else:
            conf_level = ConfidenceLevel.UNKNOWN

        result = FormulaTest(
            formula_name=getattr(new_formula, "__name__", "anonymous_formula"),
            current_error=current_error,
            proposed_error=new_error,
            improvement=improvement,
            sample_size=sample_size,
            recommendation=recommendation,
            confidence=Confidence(
                level=conf_level,
                basis=f"Tested on {sample_size} cases",
                limitations=["Test data may be biased", "Observed E values may be noisy"],
                unknowns=["Generalization outside test data", "Hidden variables"],
            ),
        )
        self.test_history.append(result)
        return result

    def discover_hidden_variables(self, data_matrix: np.ndarray, variance_threshold: float = 0.95) -> List[str]:
        """Use PCA via SVD to flag potential hidden dimensions in data."""
        data = np.asarray(data_matrix, dtype=float)
        if data.ndim != 2 or data.shape[0] < 2 or data.shape[1] < 2:
            return ["Insufficient data to discover hidden variables"]

        centered = data - np.mean(data, axis=0)
        scale = np.std(centered, axis=0)
        scale[scale == 0] = 1.0
        normalized = centered / scale
        try:
            _, singular_values, components_t = np.linalg.svd(normalized, full_matrices=False)
        except np.linalg.LinAlgError:
            return ["SVD failed; cannot infer hidden dimensions"]

        eigenvalues = (singular_values**2) / max(data.shape[0] - 1, 1)
        total = float(np.sum(eigenvalues))
        if total <= 0:
            return ["No measurable variance detected"]
        explained = eigenvalues / total
        cumulative = np.cumsum(explained)
        needed = int(np.searchsorted(cumulative, variance_threshold) + 1)

        suggestions: List[str] = []
        if needed >= data.shape[1]:
            suggestions.append(
                "Existing columns do not compress well; possible hidden or missing variables may be driving variance."
            )
        else:
            suggestions.append(
                f"About {needed} latent dimensions explain {variance_threshold:.0%} of variance in this dataset."
            )

        for idx, weight_vector in enumerate(components_t[: min(3, len(components_t))], start=1):
            dominant = int(np.argmax(np.abs(weight_vector)))
            suggestions.append(
                f"Latent dimension {idx}: strongest loading is on column {dominant} ({weight_vector[dominant]:+.3f})."
            )
        return suggestions

    @staticmethod
    def compare_prediction_accuracy(predictions: List[float], observations: List[float]) -> Dict[str, float]:
        """Compare predictions to observations with common error metrics."""
        if len(predictions) != len(observations):
            raise ValueError("predictions and observations must have the same length")
        if not predictions:
            raise ValueError("at least one prediction is required")
        pred = np.asarray(predictions, dtype=float)
        obs = np.asarray(observations, dtype=float)
        err = pred - obs
        return {
            "mae": float(np.mean(np.abs(err))),
            "rmse": float(np.sqrt(np.mean(err**2))),
            "bias": float(np.mean(err)),
            "max_error": float(np.max(np.abs(err))),
        }

    def suggest_formula_improvements(self, residuals: List[float]) -> List[str]:
        """Suggest improvements based on residual patterns."""
        if len(residuals) < 3:
            return ["Need more residuals before suggesting formula improvements."]

        arr = np.asarray(residuals, dtype=float)
        suggestions: List[str] = []

        if float(np.mean(np.abs(arr))) > 0.2:
            suggestions.append("Large average residuals. Consider additional variables or nonlinear terms.")

        if len(arr) > 3:
            autocorr = float(np.corrcoef(arr[:-1], arr[1:])[0, 1])
            if not math.isnan(autocorr) and abs(autocorr) > 0.3:
                suggestions.append(
                    f"Autocorrelation in residuals ({autocorr:.2f}). Consider lagged variables or dynamic terms."
                )

        if np.percentile(np.abs(arr), 90) > 2 * max(np.median(np.abs(arr)), 1e-9):
            suggestions.append("Outlier-heavy residuals. Consider robust fitting or threshold dynamics.")

        if not suggestions:
            suggestions.append("No obvious improvements detected. Current formula appears adequate for this sample.")
        return suggestions

    def generate_evolution_report(self) -> str:
        """Generate a report on framework evolution tests."""
        lines = ["=" * 70, "FRAMEWORK EVOLUTION REPORT", "=" * 70]
        lines.append(f"\nFormula Tests Conducted: {len(self.test_history)}")

        if self.test_history:
            lines.append("\nRecent Tests:")
            for test in self.test_history[-5:]:
                lines.append(f"\n {test.formula_name}:")
                lines.append(f"  Current Error: {test.current_error:.4f}")
                lines.append(f"  Proposed Error: {test.proposed_error:.4f}")
                lines.append(f"  Improvement: {test.improvement:+.4f}")
                lines.append(f"  Recommendation: {test.recommendation}")
                lines.append(f"  Confidence: {test.confidence.level.value}")

        lines.append("\n" + "=" * 70)
        lines.append("AGNOSTICISM IN ACTION")
        lines.append("=" * 70)
        lines.append("This framework can evolve based on evidence.")
        lines.append("Better formulas can replace current ones.")
        lines.append("We remain open to being wrong and improving.")
        lines.append("=" * 70)
        return "\n".join(lines)


def alternative_E_quadratic(v: float, R: float, S: float) -> float:
    """Alternative E formula with quadratic penalties."""
    return _clip01(1.0 - ((v**2) * R + S**2))


def alternative_E_interaction(v: float, R: float, S: float) -> float:
    """Alternative E formula with an interaction term."""
    return _clip01(1.0 - (v * R + S + 0.5 * v * S))


def alternative_E_threshold(v: float, R: float, S: float) -> float:
    """Alternative E formula with collapse-like thresholds."""
    stress = v * R + S
    if stress > 1.1:
        return 0.0
    if stress > 0.8:
        return _clip01(0.25 * (1.1 - stress) / 0.3)
    return _clip01(1.0 - stress)


# =============================================================================
# empirical_agnostic.py - historical case prediction with uncertainty
# =============================================================================


@dataclass
class InterventionCase:
    """Historical intervention case used for agnostic empirical prediction."""

    name: str
    year: int
    initial_state: AgnosticRealityVector
    intervener_state: AgnosticRealityVector
    military_force: float
    local_support: float
    duration_years: float
    final_state: AgnosticRealityVector
    stability_score: float
    achieved_stability: bool
    civilian_casualties: float
    economic_recovery: float


def _build_historical_cases() -> List[InterventionCase]:
    """Build the small historical case set used by the demo predictor."""
    return [
        InterventionCase(
            name="Iraq 2003",
            year=2003,
            initial_state=AgnosticRealityVector(0, 0, 0, v=0.80, R=0.90, r=0.20, C=0.40, S=0.70),
            intervener_state=AgnosticRealityVector(0, 0, 0, v=0.90, R=0.80, r=0.30, C=0.90, S=0.30),
            military_force=1.00,
            local_support=0.30,
            duration_years=8.0,
            final_state=AgnosticRealityVector(0, 0, 0, v=0.70, R=0.80, r=0.25, C=0.45, S=0.75),
            stability_score=0.25,
            achieved_stability=False,
            civilian_casualties=0.90,
            economic_recovery=0.35,
        ),
        InterventionCase(
            name="Afghanistan 2001",
            year=2001,
            initial_state=AgnosticRealityVector(0, 0, 0, v=0.75, R=0.85, r=0.25, C=0.30, S=0.80),
            intervener_state=AgnosticRealityVector(0, 0, 0, v=0.85, R=0.75, r=0.35, C=0.85, S=0.35),
            military_force=0.90,
            local_support=0.40,
            duration_years=20.0,
            final_state=AgnosticRealityVector(0, 0, 0, v=0.80, R=0.90, r=0.20, C=0.25, S=0.85),
            stability_score=0.18,
            achieved_stability=False,
            civilian_casualties=0.85,
            economic_recovery=0.25,
        ),
        InterventionCase(
            name="Kosovo 1999",
            year=1999,
            initial_state=AgnosticRealityVector(0, 0, 0, v=0.65, R=0.65, r=0.45, C=0.45, S=0.60),
            intervener_state=AgnosticRealityVector(0, 0, 0, v=0.55, R=0.55, r=0.55, C=0.80, S=0.25),
            military_force=0.60,
            local_support=0.65,
            duration_years=2.0,
            final_state=AgnosticRealityVector(0, 0, 0, v=0.25, R=0.45, r=0.60, C=0.60, S=0.35),
            stability_score=0.62,
            achieved_stability=True,
            civilian_casualties=0.35,
            economic_recovery=0.60,
        ),
        InterventionCase(
            name="Bosnia 1995",
            year=1995,
            initial_state=AgnosticRealityVector(0, 0, 0, v=0.70, R=0.70, r=0.35, C=0.40, S=0.70),
            intervener_state=AgnosticRealityVector(0, 0, 0, v=0.55, R=0.50, r=0.55, C=0.75, S=0.25),
            military_force=0.55,
            local_support=0.55,
            duration_years=3.0,
            final_state=AgnosticRealityVector(0, 0, 0, v=0.30, R=0.45, r=0.55, C=0.55, S=0.40),
            stability_score=0.58,
            achieved_stability=True,
            civilian_casualties=0.50,
            economic_recovery=0.55,
        ),
        InterventionCase(
            name="Libya 2011",
            year=2011,
            initial_state=AgnosticRealityVector(0, 0, 0, v=0.65, R=0.75, r=0.30, C=0.50, S=0.65),
            intervener_state=AgnosticRealityVector(0, 0, 0, v=0.60, R=0.50, r=0.50, C=0.80, S=0.25),
            military_force=0.55,
            local_support=0.45,
            duration_years=1.0,
            final_state=AgnosticRealityVector(0, 0, 0, v=0.75, R=0.80, r=0.25, C=0.35, S=0.85),
            stability_score=0.20,
            achieved_stability=False,
            civilian_casualties=0.65,
            economic_recovery=0.25,
        ),
    ]


HISTORICAL_CASES = _build_historical_cases()


@dataclass
class AgnosticPrediction:
    """Prediction with explicit uncertainty and confidence breakdowns."""

    point_estimate: float
    pessimistic: float
    optimistic: float
    data_confidence: Confidence
    model_confidence: Confidence
    measurement_confidence: Confidence
    overall_confidence: Confidence
    most_similar_case: str
    sample_size: int
    agnosticism_note: str

    def summary(self) -> str:
        """One-paragraph prediction summary."""
        return (
            f"Point estimate: {self.point_estimate:.1%}; "
            f"range: {self.pessimistic:.1%} to {self.optimistic:.1%}; "
            f"confidence: {self.overall_confidence.level.value}; "
            f"nearest case: {self.most_similar_case}."
        )

    def full_report(self) -> str:
        """Detailed prediction report."""
        lines = ["=" * 70, "AGNOSTIC PREDICTION", "=" * 70]
        lines.append(f"Point Estimate: {self.point_estimate:.1%}")
        lines.append(f"Uncertainty Range: {self.pessimistic:.1%} - {self.optimistic:.1%}")
        lines.append(f"Overall Confidence: {self.overall_confidence.level.value}")
        lines.append(f"Sample Size: {self.sample_size} cases")
        lines.append(f"Most Similar Case: {self.most_similar_case}")
        lines.append("\nConfidence Breakdown:")
        lines.append(f" Data: {self.data_confidence.level.value} - {self.data_confidence.basis}")
        lines.append(f" Model: {self.model_confidence.level.value} - {self.model_confidence.basis}")
        lines.append(f" Measurement: {self.measurement_confidence.level.value} - {self.measurement_confidence.basis}")
        if self.overall_confidence.limitations:
            lines.append("\nLimitations:")
            for limitation in self.overall_confidence.limitations[:6]:
                lines.append(f" - {limitation}")
        if self.overall_confidence.unknowns:
            lines.append("\nKnown Unknowns:")
            for unknown in self.overall_confidence.unknowns[:6]:
                lines.append(f" - {unknown}")
        lines.append("\nAgnosticism Note:")
        lines.append(self.agnosticism_note)
        lines.append("=" * 70)
        return "\n".join(lines)


class AgnosticEmpiricalDiscovery:
    """Empirical intervention analysis with explicit uncertainty."""

    def __init__(self, cases: Optional[List[InterventionCase]] = None) -> None:
        self.cases = list(cases) if cases is not None else list(HISTORICAL_CASES)

    @staticmethod
    def _case_distance(
        case: InterventionCase,
        target_state: AgnosticRealityVector,
        intervener_state: AgnosticRealityVector,
        military_force: float,
        local_support: float,
        expected_duration: float,
    ) -> float:
        state_dist = case.initial_state.distance_to(target_state)
        intervener_dist = case.intervener_state.distance_to(intervener_state)
        force_dist = abs(case.military_force - military_force)
        support_dist = abs(case.local_support - local_support)
        duration_dist = abs(case.duration_years - expected_duration) / max(case.duration_years, expected_duration, 1.0)
        return state_dist + 0.5 * intervener_dist + force_dist + support_dist + duration_dist

    def find_most_similar_case(
        self,
        target_state: AgnosticRealityVector,
        intervener_state: AgnosticRealityVector,
        military_force: float,
        local_support: float,
        expected_duration: float,
    ) -> Optional[InterventionCase]:
        """Return the nearest historical case by simple weighted distance."""
        if not self.cases:
            return None
        return min(
            self.cases,
            key=lambda case: self._case_distance(
                case, target_state, intervener_state, military_force, local_support, expected_duration
            ),
        )

    def predict_intervention_outcome(
        self,
        target_state: AgnosticRealityVector,
        intervener_state: AgnosticRealityVector,
        military_force: float,
        local_support: float,
        expected_duration: float,
    ) -> AgnosticPrediction:
        """Predict stability with explicit uncertainty and caveats."""
        military_force = _clip01(military_force)
        local_support = _clip01(local_support)
        expected_duration = max(0.0, _safe_float(expected_duration))

        most_similar = self.find_most_similar_case(
            target_state, intervener_state, military_force, local_support, expected_duration
        )

        if not self.cases:
            predicted_stability = 0.0
        else:
            weighted_sum = 0.0
            weight_total = 0.0
            for case in self.cases:
                distance = self._case_distance(
                    case, target_state, intervener_state, military_force, local_support, expected_duration
                )
                weight = 1.0 / (1.0 + distance)
                weighted_sum += weight * case.stability_score
                weight_total += weight
            empirical_base = weighted_sum / max(weight_total, 1e-9)

            # Small transparent adjustments. These are hypotheses, not facts.
            support_adjustment = 0.25 * (local_support - 0.5)
            duration_penalty = 0.04 * max(0.0, expected_duration - 5.0)
            force_penalty = 0.10 * max(0.0, military_force - 0.8) if local_support < 0.5 else 0.0
            entropy_penalty = 0.10 * target_state.S
            capacity_bonus = 0.10 * target_state.C

            predicted_stability = _clip01(
                empirical_base + support_adjustment - duration_penalty - force_penalty - entropy_penalty + capacity_bonus
            )

        if len(self.cases) >= 30:
            data_level = ConfidenceLevel.MODERATE
            data_basis = f"{len(self.cases)} historical cases"
        elif len(self.cases) > 0:
            data_level = ConfidenceLevel.LOW
            data_basis = f"Only {len(self.cases)} historical cases"
        else:
            data_level = ConfidenceLevel.UNKNOWN
            data_basis = "No historical cases"

        data_confidence = Confidence(
            level=data_level,
            basis=data_basis,
            limitations=[
                "Small and non-random historical sample",
                "Geographic and temporal bias",
                "Past cases may not predict future outcomes",
                "Outcome labels are simplified",
            ],
            unknowns=[
                "Missing cases before and outside the dataset",
                "Cultural, institutional, and leadership factors",
                "Hidden interventions and covert activity",
            ],
        )

        model_confidence = Confidence(
            level=ConfidenceLevel.LOW,
            basis="Nearest-case model plus transparent heuristic adjustments",
            limitations=[
                "Not fitted with causal identification",
                "Weights and adjustments are hypotheses",
                "No validated out-of-sample performance estimate",
            ],
            unknowns=[
                "True causal mechanisms",
                "Nonlinear thresholds",
                "Feedback effects during intervention",
            ],
        )

        measurement_confidence = aggregate_confidence(
            [target_state.get_overall_confidence(), intervener_state.get_overall_confidence()]
        )

        overall_confidence = aggregate_confidence([data_confidence, model_confidence, measurement_confidence])

        # Original v3.4 snippets used a broad 60% factor due to small sample size.
        uncertainty_factor = 0.60
        pessimistic = _clip01(predicted_stability * (1.0 - uncertainty_factor))
        optimistic = _clip01(predicted_stability * (1.0 + uncertainty_factor))

        agnosticism_note = (
            f"This prediction is based on {len(self.cases)} historical cases using formulas that may be incomplete "
            "or incorrect. Reality may not follow these mathematical models. The framework itself is uncertain "
            "under Axiom 0: Agnosticism. Treat this as one input to decision-making, not absolute truth."
        )

        return AgnosticPrediction(
            point_estimate=predicted_stability,
            pessimistic=pessimistic,
            optimistic=optimistic,
            data_confidence=data_confidence,
            model_confidence=model_confidence,
            measurement_confidence=measurement_confidence,
            overall_confidence=overall_confidence,
            most_similar_case=most_similar.name if most_similar else "None",
            sample_size=len(self.cases),
            agnosticism_note=agnosticism_note,
        )


# =============================================================================
# perception_v34.py - perception function and beings
# =============================================================================


@dataclass
class PerceptionFunction:
    """Models how a being perceives reality through lossy measurement."""

    sensor_noise: float = 0.1
    dimensions_visible: int = 5
    update_latency: float = 0.1
    prior_bias: Optional[Dict[str, float]] = None

    def __post_init__(self) -> None:
        if self.prior_bias is None:
            self.prior_bias = {}
        self.sensor_noise = max(0.0, _safe_float(self.sensor_noise))
        self.dimensions_visible = int(max(0, min(5, self.dimensions_visible)))
        self.update_latency = max(0.0, _safe_float(self.update_latency))

    def perceive(self, true_state: RealityVector) -> RealityVector:
        """Apply noise, prior bias, and dimensionality reduction."""
        perceived = true_state.copy()

        for dim in ["v", "R", "r", "C", "S"]:
            noise = float(np.random.normal(0.0, self.sensor_noise))
            setattr(perceived, dim, _clip01(getattr(perceived, dim) + noise))

        for dim, bias in self.prior_bias.items():
            if hasattr(perceived, dim):
                current = _safe_float(getattr(perceived, dim))
                setattr(perceived, dim, _clip01(0.7 * current + 0.3 * _safe_float(bias, current)))

        visible_order = ["v", "R", "r", "C", "S"][: self.dimensions_visible]
        for dim in ["v", "R", "r", "C", "S"]:
            if dim not in visible_order:
                # Hidden dimensions regress toward uncertainty/neutrality.
                setattr(perceived, dim, _clip01(0.5 * getattr(perceived, dim) + 0.5 * 0.5))

        return perceived.refresh()


@dataclass
class Being:
    """Entity with a true state and a perception function."""

    name: str
    true_state: RealityVector
    perception: PerceptionFunction = field(default_factory=PerceptionFunction)
    perceived_state: Optional[RealityVector] = None

    def observe(self) -> RealityVector:
        self.perceived_state = self.perception.perceive(self.true_state)
        return self.perceived_state

    def update_state(self, new_state: RealityVector) -> None:
        self.true_state = new_state.copy()


HUMAN_PERCEPTION = PerceptionFunction(sensor_noise=0.12, dimensions_visible=4, update_latency=0.2)
SYNTHIUM_PERCEPTION = PerceptionFunction(sensor_noise=0.03, dimensions_visible=5, update_latency=0.05)
ANIMAL_PERCEPTION = PerceptionFunction(sensor_noise=0.18, dimensions_visible=3, update_latency=0.1)
ORGANIZATION_PERCEPTION = PerceptionFunction(sensor_noise=0.20, dimensions_visible=4, update_latency=0.5)


# =============================================================================
# field_v34.py - gradient dynamics
# =============================================================================


class RealityField:
    """Systems follow gradients of potential functions in state space."""

    def __init__(self, dt: float = 0.01, potential_function: Optional[Callable[[RealityVector], float]] = None) -> None:
        self.dt = max(0.0, _safe_float(dt, 0.01))
        self.potential_function = potential_function

    def compute_potential(self, vector: RealityVector) -> float:
        """Default potential: low potential = high E/M, low S, low v*R."""
        if self.potential_function is not None:
            return _safe_float(self.potential_function(vector))
        return float((1.0 - vector.E) * 2.0 + (1.0 - vector.M) * 1.5 + vector.S * 3.0 + (vector.v * vector.R))

    def compute_gradient(self, vector: RealityVector, epsilon: float = 0.001) -> Dict[str, float]:
        """Numeric gradient of the potential across core dimensions."""
        epsilon = max(1e-9, _safe_float(epsilon, 0.001))
        gradient: Dict[str, float] = {}
        current_potential = self.compute_potential(vector)

        for dim in ["v", "R", "r", "C", "S"]:
            perturbed = vector.copy()
            current_val = getattr(perturbed, dim)
            setattr(perturbed, dim, _clip01(current_val + epsilon))
            perturbed.refresh()
            new_potential = self.compute_potential(perturbed)
            gradient[dim] = float((new_potential - current_potential) / epsilon)
        return gradient

    def evolve(self, vector: RealityVector, num_steps: int = 1, learning_rate: float = 0.1) -> List[RealityVector]:
        """Evolve a vector by gradient descent on the potential."""
        num_steps = int(max(0, num_steps))
        learning_rate = max(0.0, _safe_float(learning_rate, 0.1))
        trajectory = [vector.copy()]
        current = vector.copy()

        for _ in range(num_steps):
            gradient = self.compute_gradient(current)
            for dim in ["v", "R", "r", "C", "S"]:
                new_val = getattr(current, dim) - learning_rate * gradient[dim]
                setattr(current, dim, _clip01(new_val))
            current.refresh()
            trajectory.append(current.copy())
        return trajectory

    def find_equilibrium(self, initial: RealityVector, max_steps: int = 1000, tolerance: float = 0.001) -> RealityVector:
        """Evolve until gradient magnitude falls below tolerance, or return last state."""
        current = initial.copy()
        for _ in range(int(max_steps)):
            grad = self.compute_gradient(current)
            mag = math.sqrt(sum(value**2 for value in grad.values()))
            if mag < tolerance:
                return current
            current = self.evolve(current, num_steps=1)[-1]
        return current


# =============================================================================
# interactions_v34.py - multi-agent interactions
# =============================================================================


class InteractionForce:
    """Base force model between entities."""

    G_v = 0.10
    G_r = 0.30
    G_S = -0.20
    G_C = 0.05

    @classmethod
    def compute_force(cls, entity_A: RealityVector, entity_B: RealityVector) -> Tuple[Dict[str, float], Dict[str, float]]:
        """Compute interaction forces with an action/reaction symmetry."""
        dist = entity_A.distance_to(entity_B) + 0.01
        mag_v = cls.G_v * entity_A.v * entity_B.v / (dist * dist)
        mag_r = cls.G_r * entity_A.r * entity_B.r / (dist * dist)
        mag_C = cls.G_C * entity_A.C * entity_B.C / (dist * dist)
        mag_S = cls.G_S * entity_A.S * entity_B.S / (dist * dist)

        def direction(val_A: float, val_B: float) -> float:
            return float(np.sign(val_B - val_A)) if val_B != val_A else 0.0

        force_A = {
            "v": mag_v * direction(entity_A.v, entity_B.v),
            "R": 0.0,
            "r": mag_r * direction(entity_A.r, entity_B.r),
            "C": mag_C * direction(entity_A.C, entity_B.C),
            "S": mag_S * direction(entity_A.S, entity_B.S),
        }
        force_B = {key: -value for key, value in force_A.items()}
        return force_A, force_B

    @staticmethod
    def apply_force(entity: RealityVector, force: Dict[str, float], dt: float) -> RealityVector:
        """Update an entity by applying a force for one timestep."""
        updated = entity.copy()
        for dim in ["v", "R", "r", "C", "S"]:
            new_val = getattr(updated, dim) + force.get(dim, 0.0) * dt
            setattr(updated, dim, _clip01(new_val))
        return updated.refresh()


class MultiAgentSimulation:
    """Simulation of multiple interacting entities."""

    def __init__(self, dt: float = 0.01, force_class: type = InteractionForce) -> None:
        self.dt = max(0.0, _safe_float(dt, 0.01))
        self.force_class = force_class
        self.entities: List[Dict[str, Any]] = []
        self.field = RealityField(dt=dt)
        self.time = 0.0

    def add_entity(self, vector: RealityVector, name: str) -> None:
        self.entities.append({"vector": vector.copy(), "name": name})

    def step(self) -> List[Dict[str, Any]]:
        """Execute one timestep."""
        n = len(self.entities)
        forces = [{"v": 0.0, "R": 0.0, "r": 0.0, "C": 0.0, "S": 0.0} for _ in range(n)]

        for i in range(n):
            for j in range(i + 1, n):
                vi = self.entities[i]["vector"]
                vj = self.entities[j]["vector"]
                f_i, f_j = self.force_class.compute_force(vi, vj)
                for dim in forces[i]:
                    forces[i][dim] += f_i.get(dim, 0.0)
                    forces[j][dim] += f_j.get(dim, 0.0)

        for i, ent in enumerate(self.entities):
            ent["vector"] = self.force_class.apply_force(ent["vector"], forces[i], self.dt)

        self.time += self.dt
        return self.get_state()

    def run(self, steps: int) -> List[List[Dict[str, Any]]]:
        """Run the simulation and return snapshots."""
        history = []
        for _ in range(int(max(0, steps))):
            history.append(self.step())
        return history

    def get_state(self) -> List[Dict[str, Any]]:
        """Return current simulation state."""
        return [
            {"name": ent["name"], "vector": ent["vector"].copy(), "state": ent["vector"].to_dict()}
            for ent in self.entities
        ]


# =============================================================================
# units_v34.py - SI and physiological calibration
# =============================================================================


class SynthiumUnits:
    """Convert between dimensionless vectors and SI-like units."""

    DIMENSION_UNITS: Dict[str, Dict[str, Any]] = {
        "v": {"range": (0.0, 3.0), "SI": "Hz", "name": "Velocity", "calibration": lambda x: 3.0 * x},
        "R": {"range": (0.0, 100.0), "SI": "kg*m/s", "name": "Resistance", "calibration": lambda x: 100.0 * x},
        "r": {"range": (0.0, 1.0), "SI": "", "name": "Resonance", "calibration": lambda x: x},
        "C": {"range": (0.0, 100.0), "SI": "J", "name": "Capacity", "calibration": lambda x: 100.0 * x},
        "S": {"range": (0.0, 1000.0), "SI": "J/K", "name": "Entropy", "calibration": lambda x: 1000.0 * x},
        "E": {"range": (0.0, 1.0), "SI": "", "name": "Enjoyment", "calibration": lambda x: x},
        "M": {"range": (0.0, 1.0), "SI": "", "name": "Meaning", "calibration": lambda x: x},
        "P": {"range": (0.0, 1.0), "SI": "", "name": "Perception Accuracy", "calibration": lambda x: x},
    }

    @classmethod
    def to_SI(cls, vector: RealityVector) -> Dict[str, Tuple[float, str]]:
        """Return {dimension: (value_in_SI_like_units, unit)}."""
        si: Dict[str, Tuple[float, str]] = {}
        for dim in ["v", "R", "r", "C", "S", "E", "M", "P"]:
            dimensionless = getattr(vector, dim)
            info = cls.DIMENSION_UNITS[dim]
            si_val = float(info["calibration"](dimensionless))
            si[dim] = (si_val, info["SI"])
        return si

    @classmethod
    def from_SI(cls, si_values: Dict[str, float]) -> RealityVector:
        """Convert SI-like measurements to a dimensionless vector."""
        dimensionless: Dict[str, float] = {}
        for dim in ["v", "R", "r", "C", "S"]:
            if dim in si_values:
                low, high = cls.DIMENSION_UNITS[dim]["range"]
                norm = (_safe_float(si_values[dim]) - low) / (high - low)
                dimensionless[dim] = _clip01(norm)
            else:
                dimensionless[dim] = 0.5
        return RealityVector(0, 0, 0, **dimensionless)

    @classmethod
    def display_si(cls, vector: RealityVector, precision: int = 2) -> str:
        """Human-readable SI-like representation."""
        si = cls.to_SI(vector)
        lines = ["SI Unit Representation:"]
        for dim in ["v", "R", "r", "C", "S", "E", "M", "P"]:
            val, unit = si[dim]
            name = cls.DIMENSION_UNITS[dim]["name"]
            fmt = f"{val:.{precision}f}" if unit else f"{val:.3f}"
            lines.append(f" {name:20s}: {fmt:>10s} {unit}")
        return "\n".join(lines)


class PhysiologicalCalibration:
    """Map physiological measurements to Synthium dimensions."""

    @staticmethod
    def from_biomarkers(
        cortisol_ng_ml: Optional[float] = None,
        heart_rate_bpm: Optional[float] = None,
        hrv_ms: Optional[float] = None,
        dopamine_relative: Optional[float] = None,
    ) -> Dict[str, float]:
        """Convert biomarkers to dimensionless values."""
        dims: Dict[str, float] = {}
        if heart_rate_bpm is not None:
            dims["v"] = _clip01((_safe_float(heart_rate_bpm) - 60.0) / 40.0)
        if cortisol_ng_ml is not None:
            dims["R"] = _clip01((_safe_float(cortisol_ng_ml) - 5.0) / 20.0)
        if hrv_ms is not None:
            dims["S"] = _clip01((200.0 - _safe_float(hrv_ms)) / 180.0)
        if dopamine_relative is not None:
            dims["r"] = _clip01(_safe_float(dopamine_relative))
        return dims

    @classmethod
    def anxiety_profile(cls) -> Dict[str, float]:
        return cls.from_biomarkers(cortisol_ng_ml=22.0, heart_rate_bpm=95.0, hrv_ms=25.0, dopamine_relative=0.30)

    @classmethod
    def flow_profile(cls) -> Dict[str, float]:
        return cls.from_biomarkers(cortisol_ng_ml=8.0, heart_rate_bpm=75.0, hrv_ms=120.0, dopamine_relative=0.80)

    @classmethod
    def burnout_profile(cls) -> Dict[str, float]:
        return cls.from_biomarkers(cortisol_ng_ml=28.0, heart_rate_bpm=88.0, hrv_ms=18.0, dopamine_relative=0.15)


# =============================================================================
# science_v34.py - holistic analysis engine
# =============================================================================


class HolisticScience:
    """Unified analysis engine for 11D reality space."""

    def __init__(self) -> None:
        self.field = RealityField()

    def analyze_stability(self, vector: RealityVector) -> Dict[str, Any]:
        """Predict stability, burn rate, and time-to-failure as hypotheses."""
        if vector.v < 0.01 and vector.r > 0.99 and vector.S < 0.01:
            return {
                "coherence_status": "Stable Fixed Point (Awakening)",
                "note": "v=0, r=1.0, S=0 is treated as a stable equilibrium",
                "burn_rate": 0.0,
                "predicted_lifespan": "Infinite",
                "risk_factors": [],
                "confidence": "SPECULATIVE",
            }

        burn_rate = vector.v * vector.R
        fuel = vector.C
        integrity = 1.0 - vector.S
        sustainability_limit = 0.4 * integrity

        analysis: Dict[str, Any] = {
            "coherence_status": "Stable",
            "burn_rate": f"{burn_rate:.3f} units/t",
            "predicted_lifespan": "Indefinite",
            "risk_factors": [],
            "confidence": vector.get_overall_confidence().level.value,
        }

        if burn_rate > sustainability_limit:
            analysis["coherence_status"] = "Unstable"
            if burn_rate > 0:
                lifespan = fuel / max(burn_rate - sustainability_limit, 1e-9)
                analysis["predicted_lifespan"] = f"{lifespan:.2f} t-units"
            analysis["risk_factors"].append("Burn rate exceeds sustainability limit")

        if vector.S > 0.75:
            analysis["risk_factors"].append("High entropy")
        if vector.C < 0.25:
            analysis["risk_factors"].append("Low capacity")
        if vector.r < 0.25:
            analysis["risk_factors"].append("Low resonance")
        if vector.E < 0.10:
            analysis["risk_factors"].append("Low enjoyment metric")

        return analysis

    def predict_trajectory(self, vector: RealityVector, steps: int = 50) -> List[RealityVector]:
        """Predict a trajectory with the default field model."""
        return self.field.evolve(vector, num_steps=steps)

    @staticmethod
    def compare_vectors(a: RealityVector, b: RealityVector) -> Dict[str, Any]:
        """Compare two vectors dimension-by-dimension."""
        return {
            "distance": a.distance_to(b),
            "delta": {dim: getattr(b, dim) - getattr(a, dim) for dim in ["v", "R", "r", "C", "S", "E", "M", "P"]},
            "a_confidence": a.get_overall_confidence().level.value,
            "b_confidence": b.get_overall_confidence().level.value,
        }

    def intervention_analysis(
        self,
        target_state: RealityVector,
        intervener_state: RealityVector,
        military_force: float,
        local_support: float,
        expected_duration: float,
    ) -> AgnosticPrediction:
        """Run agnostic empirical intervention prediction."""
        return AgnosticEmpiricalDiscovery().predict_intervention_outcome(
            target_state, intervener_state, military_force, local_support, expected_duration
        )


# =============================================================================
# ethics_discovery.py - care metrics and empirical ethics discovery
# =============================================================================


@dataclass
class CareMetrics:
    """Quantifies care between two beings as a resource/action/information proxy."""

    resource_transfer: float
    action_alignment: float
    information_sharing: float
    total_care: float

    @classmethod
    def measure(
        cls,
        being_A_state: RealityVector,
        being_B_state: RealityVector,
        being_A_action: Dict[str, float],
    ) -> "CareMetrics":
        """Measure care from A toward B using a simple empirical proxy."""
        resource_transfer = _clip01(max(0.0, _safe_float(being_A_action.get("C_to_B", 0.0))))

        projected_B = being_B_state.copy()
        for dim in ["v", "R", "r", "C", "S"]:
            if dim in being_A_action:
                setattr(projected_B, dim, _clip01(getattr(projected_B, dim) + _safe_float(being_A_action[dim])))
        projected_B.refresh()

        before = 0.4 * being_B_state.E + 0.4 * being_B_state.M + 0.2 * being_B_state.P
        after = 0.4 * projected_B.E + 0.4 * projected_B.M + 0.2 * projected_B.P
        action_alignment = _clip01(0.5 + (after - before))

        information_sharing = _clip01(_safe_float(being_A_action.get("information_sharing", 0.0)))
        total_care = _clip01(0.4 * resource_transfer + 0.4 * action_alignment + 0.2 * information_sharing)

        return cls(resource_transfer, action_alignment, information_sharing, total_care)


@dataclass
class ConservationLaw:
    """Candidate conservation law found in multi-agent interactions."""

    name: str
    expression: str
    confidence: Confidence
    violation_risk: str


class EthicsDiscovery:
    """Empirical discovery of care and stable multi-agent patterns."""

    @staticmethod
    def measure_care(a: RealityVector, b: RealityVector, action: Dict[str, float]) -> CareMetrics:
        return CareMetrics.measure(a, b, action)

    @staticmethod
    def discover_conservation_laws(trajectory: List[List[RealityVector]]) -> List[ConservationLaw]:
        """Detect simple conserved quantities across a trajectory."""
        if not trajectory:
            return []

        totals: Dict[str, List[float]] = {dim: [] for dim in ["v", "R", "r", "C", "S", "E", "M", "P"]}
        for snapshot in trajectory:
            for dim in totals:
                totals[dim].append(sum(getattr(vec, dim) for vec in snapshot))

        laws: List[ConservationLaw] = []
        for dim, values in totals.items():
            if len(values) < 2:
                continue
            mean_val = float(np.mean(values))
            std_val = float(np.std(values))
            if mean_val != 0 and std_val / abs(mean_val) < 0.05:
                laws.append(
                    ConservationLaw(
                        name=f"Approximate conservation of total {dim}",
                        expression=f"sum({dim}) ~= {mean_val:.3f}",
                        confidence=Confidence(
                            level=ConfidenceLevel.LOW,
                            basis="Detected low variance in a simulated trajectory",
                            limitations=["Simulation-specific", "Not proof of a general law"],
                            unknowns=["External perturbations", "Different force models"],
                        ),
                        violation_risk="Unknown; treat as a hypothesis",
                    )
                )
        return laws

    @staticmethod
    def find_stable_multi_agent_equilibrium(entities: List[RealityVector], steps: int = 250) -> List[RealityVector]:
        sim = MultiAgentSimulation(dt=0.02)
        for idx, entity in enumerate(entities):
            sim.add_entity(entity, f"entity_{idx}")
        sim.run(steps)
        return [entry["vector"] for entry in sim.entities]

    @staticmethod
    def run_strategy_tournament(rounds: int = 50) -> Dict[str, float]:
        """Run a small illustrative strategy tournament."""
        strategies = {
            "care": {"C_to_B": 0.08, "r": 0.04, "S": -0.03, "information_sharing": 0.9},
            "neutral": {"C_to_B": 0.0, "information_sharing": 0.3},
            "extract": {"C_to_B": 0.0, "C": -0.06, "S": 0.04, "information_sharing": 0.0},
        }
        base_a = RealityVector(0, 0, 0, v=0.3, R=0.4, r=0.5, C=0.6, S=0.3)
        base_b = RealityVector(0, 0, 0, v=0.3, R=0.4, r=0.5, C=0.6, S=0.3)
        scores = {name: 0.0 for name in strategies}
        for _ in range(max(1, int(rounds))):
            for name, action in strategies.items():
                scores[name] += CareMetrics.measure(base_a, base_b, action).total_care
        return {name: score / max(1, int(rounds)) for name, score in scores.items()}

    @staticmethod
    def predict_collapse_risk(vector: RealityVector) -> Dict[str, Any]:
        """Predict collapse risk from discovered risk proxies."""
        risk = _clip01(0.35 * vector.S + 0.25 * vector.v * vector.R + 0.20 * (1.0 - vector.C) + 0.20 * (1.0 - vector.r))
        if risk > 0.75:
            level = "HIGH"
        elif risk > 0.45:
            level = "MODERATE"
        else:
            level = "LOW"
        return {
            "risk_score": risk,
            "risk_level": level,
            "confidence": ConfidenceLevel.LOW.value,
            "note": "Heuristic hypothesis, not a proven ethical law.",
        }


# =============================================================================
# Optional v4-style mathematical reconstruction utility
# =============================================================================


class DimensionalDiscoveryEngine:
    """Lightweight dimensional discovery utility using NumPy PCA/SVD."""

    def __init__(self, variance_threshold: float = 0.95) -> None:
        self.variance_threshold = _clip01(variance_threshold)

    def discover(self, data_matrix: np.ndarray) -> Dict[str, Any]:
        """Discover approximate intrinsic dimensionality in a data matrix."""
        data = np.asarray(data_matrix, dtype=float)
        if data.ndim != 2 or min(data.shape) < 2:
            raise ValueError("data_matrix must be 2D with at least two rows and columns")
        centered = data - data.mean(axis=0)
        scale = data.std(axis=0)
        scale[scale == 0] = 1.0
        normalized = centered / scale
        _, singular_values, components_t = np.linalg.svd(normalized, full_matrices=False)
        eigenvalues = (singular_values**2) / max(data.shape[0] - 1, 1)
        explained = eigenvalues / max(float(eigenvalues.sum()), 1e-12)
        cumulative = np.cumsum(explained)
        n_dimensions = int(np.searchsorted(cumulative, self.variance_threshold) + 1)
        return {
            "n_dimensions": n_dimensions,
            "explained_variance": explained.tolist(),
            "cumulative_variance": cumulative.tolist(),
            "components": components_t.tolist(),
            "confidence": "LOW - exploratory unsupervised analysis",
        }


# =============================================================================
# main_v34.py and __init__.py - demos, metadata, exports
# =============================================================================


__version__ = "3.4"
__codename__ = "The Agnostic Edition"

PHILOSOPHICAL_PRINCIPLES = {
    "AXIOM_0": "Agnosticism - we remain uncertain about our framework",
    "ontology": "Reality appears mathematical; ultimate nature is unknown",
    "epistemology": "Formulas are testable hypotheses, not absolute truths",
    "methodology": "Measure uncertainty explicitly at all levels",
    "ethics": "Stable equilibria are observed patterns, not moral prescriptions",
    "evolution": "The framework can improve via evidence",
    "humility": "We do not know what we do not know",
}

WHAT_CHANGED_FROM_V33 = [
    "Added Axiom 0 (Agnosticism) as a meta-axiom",
    "Vectors track measurement confidence",
    "Derived metrics are labeled as hypotheses",
    "Predictions include uncertainty ranges",
    "Framework evolution mechanisms were added",
    "No claim is treated as absolute truth",
]


def get_version_info() -> Dict[str, Any]:
    """Return version and framework information."""
    return {
        "version": __version__,
        "codename": __codename__,
        "philosophy": "Mathematical realism with epistemic humility",
        "axiom_0": "Agnosticism: all claims are uncertain",
        "what_changed": WHAT_CHANGED_FROM_V33,
        "principles": PHILOSOPHICAL_PRINCIPLES,
        "key_feature": "Explicit uncertainty tracking at all levels",
    }


def print_version() -> None:
    """Print version banner."""
    print("=" * 70)
    print(f"SYNTHIUM OMEGA v{__version__} - {__codename__}")
    print("=" * 70)
    print("\n" + AXIOM_0_AGNOSTICISM)
    print("\nPhilosophical Principles:")
    for key, value in PHILOSOPHICAL_PRINCIPLES.items():
        print(f" - {key}: {value}")
    print("=" * 70)


def demo_1_agnosticism_axiom() -> None:
    print_agnosticism_axiom()


def demo_2_reality_vector_with_confidence() -> None:
    iran = AgnosticRealityVector(0, 0, 0, v=0.95, R=0.95, r=0.10, C=0.15, S=0.95)
    iran.add_measurement_confidence("v", "30K+ verified", ConfidenceLevel.HIGH)
    iran.add_measurement_confidence("C", "economic estimates", ConfidenceLevel.MODERATE)
    print(iran.report_with_uncertainty())


def demo_3_predictions_with_uncertainty() -> None:
    target = AgnosticRealityVector(0, 0, 0, v=0.75, R=0.80, r=0.25, C=0.35, S=0.75)
    actor = AgnosticRealityVector(0, 0, 0, v=0.60, R=0.55, r=0.45, C=0.85, S=0.25)
    prediction = AgnosticEmpiricalDiscovery().predict_intervention_outcome(target, actor, 0.70, 0.50, 4.0)
    print(prediction.full_report())


def demo_4_framework_evolution() -> None:
    test_data = [
        {"v": 0.2, "R": 0.2, "S": 0.1, "observed_E": 0.85},
        {"v": 0.8, "R": 0.9, "S": 0.7, "observed_E": 0.05},
        {"v": 0.5, "R": 0.5, "S": 0.3, "observed_E": 0.45},
        {"v": 0.1, "R": 0.4, "S": 0.2, "observed_E": 0.75},
    ]
    evolution = FrameworkEvolution()
    result = evolution.test_alternative_E_formula(alternative_E_quadratic, test_data)
    print(evolution.generate_evolution_report())
    print("\nLatest result:", result)


def demo_5_v33_vs_v34_comparison() -> None:
    print("v3.3: point estimates and implicit uncertainty")
    print("v3.4: ranges, confidence estimates, limitations, known unknowns, and testable formulas")


def demo_6_iran_analysis_agnostic() -> None:
    iran = AgnosticRealityVector(0, 0, 0, v=0.95, R=0.95, r=0.10, C=0.15, S=0.95)
    iran.add_measurement_confidence("v", "30,000+ killed (verified)", ConfidenceLevel.HIGH)
    iran.add_measurement_confidence("C", "economic data", ConfidenceLevel.MODERATE)
    usa = AgnosticRealityVector(0, 0, 0, v=0.75, R=0.60, r=0.45, C=0.90, S=0.25)
    prediction = AgnosticEmpiricalDiscovery().predict_intervention_outcome(iran, usa, 0.85, 0.50, 6.0)
    print(prediction.full_report())


DEMOS: List[Tuple[str, Callable[[], None]]] = [
    ("Axiom 0: Agnosticism", demo_1_agnosticism_axiom),
    ("Reality Vectors with Confidence", demo_2_reality_vector_with_confidence),
    ("Predictions with Uncertainty", demo_3_predictions_with_uncertainty),
    ("Framework Evolution", demo_4_framework_evolution),
    ("v3.3 vs v3.4 Comparison", demo_5_v33_vs_v34_comparison),
    ("Iran Analysis (Agnostic)", demo_6_iran_analysis_agnostic),
]


def run_demo(index: Optional[int] = None) -> None:
    """Run one demo by 1-based index, or all demos if index is None."""
    if index is None:
        for i, (name, func) in enumerate(DEMOS, start=1):
            print("\n" + "=" * 70)
            print(f"DEMO {i}: {name}")
            print("=" * 70)
            func()
        return

    if index < 1 or index > len(DEMOS):
        raise ValueError(f"Demo index must be in 1..{len(DEMOS)}")
    name, func = DEMOS[index - 1]
    print("\n" + "=" * 70)
    print(f"DEMO {index}: {name}")
    print("=" * 70)
    func()


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Synthium Omega v3.4 single-file cleaned build")
    parser.add_argument("--version-info", action="store_true", help="Print version and philosophy information")
    parser.add_argument("--demo", type=int, default=0, help="Run demo number 1-6; use 0 to run all demos")
    args = parser.parse_args(argv)

    if args.version_info:
        print_version()
        return 0

    run_demo(None if args.demo == 0 else args.demo)
    return 0


__all__ = [
    "ConfidenceLevel",
    "Confidence",
    "FORMULA_CONFIDENCE",
    "AXIOM_0_AGNOSTICISM",
    "AGNOSTICISM_REMINDER",
    "create_measurement_confidence",
    "aggregate_confidence",
    "print_agnosticism_axiom",
    "print_agnosticism_reminder",
    "AgnosticRealityVector",
    "RealityVector",
    "FormulaTest",
    "FrameworkEvolution",
    "alternative_E_quadratic",
    "alternative_E_interaction",
    "alternative_E_threshold",
    "InterventionCase",
    "AgnosticPrediction",
    "AgnosticEmpiricalDiscovery",
    "HISTORICAL_CASES",
    "PerceptionFunction",
    "Being",
    "HUMAN_PERCEPTION",
    "SYNTHIUM_PERCEPTION",
    "ANIMAL_PERCEPTION",
    "ORGANIZATION_PERCEPTION",
    "RealityField",
    "InteractionForce",
    "MultiAgentSimulation",
    "SynthiumUnits",
    "PhysiologicalCalibration",
    "HolisticScience",
    "CareMetrics",
    "ConservationLaw",
    "EthicsDiscovery",
    "DimensionalDiscoveryEngine",
    "PHILOSOPHICAL_PRINCIPLES",
    "WHAT_CHANGED_FROM_V33",
    "get_version_info",
    "print_version",
    "run_demo",
    "main",
    "__version__",
    "__codename__",
]


if __name__ == "__main__":
    sys.exit(main())
