"""Rubric and symbolic formulas for the Synthium judicial module."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Mapping

from .spec import EXTENDED_UNITS


@dataclass(frozen=True)
class Band:
    low: float
    high: float
    label: str
    meaning: str


SCORING_BANDS = (
    Band(0.00, 0.19, "nearly_absent", "Nearly absent"),
    Band(0.20, 0.39, "weak", "Present but weak"),
    Band(0.40, 0.59, "moderate", "Moderate or mixed"),
    Band(0.60, 0.79, "strong", "Strong"),
    Band(0.80, 1.00, "dominant", "Very strong or dominant"),
)


def band_for(value: float) -> Band:
    value = max(0.0, min(1.0, float(value)))
    for band in SCORING_BANDS:
        if band.low <= value <= band.high:
            return band
    return SCORING_BANDS[-1]


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def effective_privacy(units: Mapping[str, float]) -> float:
    """Boundary-adjusted privacy value."""
    priv = float(units.get("Priv", 0.0))
    bound = float(units.get("Bound", 0.0))
    gate = float(units.get("Gate", 0.0))
    # Bound collapses privacy. Gate does not erase privacy, but narrows constitutional entry.
    return clamp01(priv * (1.0 - 0.85 * bound) * (1.0 - 0.45 * gate))


def effective_exception(units: Mapping[str, float], operators: Mapping[str, float]) -> float:
    excp = float(units.get("Excp", 0.0))
    if operators.get("exigency", 0.0) > 0.5:
        excp = max(excp, 0.82)
    if operators.get("consent", 0.0) > 0.5:
        excp = max(excp, 0.88)
    if operators.get("abandonment", 0.0) > 0.5:
        excp = max(excp, 0.92)
    if operators.get("search_incident", 0.0) > 0.5:
        excp = max(excp, 0.84)
    if operators.get("automobile_exception", 0.0) > 0.5:
        excp = max(excp, 0.75)
    return clamp01(excp)


def scope_breach(units: Mapping[str, float], operators: Mapping[str, float]) -> float:
    scope_fit = float(units.get("Scope", 0.75))
    spec = float(units.get("Spec", 0.70))
    breach = max(0.0, 1.0 - min(scope_fit, spec))
    if operators.get("scope_breach", 0.0) > 0.5:
        breach = max(breach, 0.75)
    return clamp01(breach)


def damping(units: Mapping[str, float], operators: Mapping[str, float]) -> float:
    gf_avail = float(units.get("JRem", 1.0))
    d = 0.0
    d += gf_avail * 0.72 * float(operators.get("good_faith", 0.0))
    d += 0.58 * float(operators.get("attenuation", 0.0))
    d += 0.35 * float(operators.get("private_search", 0.0))
    return clamp01(d)


def suppression_pressure(units: Mapping[str, float], operators: Mapping[str, float]) -> float:
    """Current symbolic Synthium formula for suppression pressure.

    This is a provisional hypothesis, not a validated legal estimator.
    """
    priv_eff = effective_privacy(units)
    excp_eff = effective_exception(units, operators)
    rem = float(units.get("Rem", 0.0))
    obs = float(units.get("Obs", 0.0))
    amb = float(units.get("Amb", 0.0))
    breach = scope_breach(units, operators)
    damp = damping(units, operators)

    violation_pressure = priv_eff * (1.0 - excp_eff) * (0.55 + 0.45 * breach)
    ambiguity_boost = 1.0 + 0.15 * amb
    observation_stabilizer = 1.0 - 0.12 * obs
    pressure = violation_pressure * rem * ambiguity_boost * observation_stabilizer * (1.0 - damp)
    # Scope breach can independently revive suppression pressure.
    pressure = max(pressure, 0.58 * breach * rem * (1.0 - damp))
    return clamp01(pressure)


def units_from_record(record: Mapping[str, object], unit_names: Iterable[str] = EXTENDED_UNITS) -> Dict[str, float]:
    return {name: float(record.get(name, 0.0)) for name in unit_names}


def operators_from_record(record: Mapping[str, object]) -> Dict[str, float]:
    return {k[3:]: float(v) for k, v in record.items() if k.startswith("op_")}
