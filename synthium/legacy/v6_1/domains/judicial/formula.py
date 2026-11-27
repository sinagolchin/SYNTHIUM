"""The symbolic suppression-pressure formula -- with its coefficients exposed.

This is the heart of the honesty problem the project diagnosed. The v4.3.1
formula is studded with numbers like 0.85, 0.45, 0.82, 0.72 that were
hand-chosen, never derived and never fit to data. Buried inline, they read as
if they carried authority. They do not.

So here every such constant is a ``Coefficient``: a named object that knows it
is ungrounded. ``suppression_pressure`` returns the score AND the list of
ungrounded coefficients it relied on, so no caller can use the number without
the framework handing them the receipt for what was assumed to produce it.

This formula is a PROPOSED hypothesis. Running it earns it nothing. The only
thing that can promote it is :func:`synthium.domains.judicial.model.validate_*`
beating a pre-declared baseline on held-out, court-derived outcomes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Mapping, Tuple


@dataclass(frozen=True)
class Coefficient:
    """A constant in a formula, tagged with whether it is empirically grounded.

    ``grounded`` is False for every coefficient below, because not one of them
    was fit, derived, or measured. The day one is estimated from data with a
    confidence interval, flip its flag and record the source.
    """

    name: str
    value: float
    grounded: bool
    note: str

    def __float__(self) -> float:
        return self.value


# -- the registry: every magic number in the formula, named and owned ---------

C: Dict[str, Coefficient] = {
    "bound_collapse":     Coefficient("bound_collapse", 0.85, False, "how far boundary reclassification collapses privacy"),
    "gate_narrowing":     Coefficient("gate_narrowing", 0.45, False, "how far the private-action gateway narrows privacy"),
    "exigency_floor":     Coefficient("exigency_floor", 0.82, False, "exception strength floor once exigency fires"),
    "consent_floor":      Coefficient("consent_floor", 0.88, False, "exception strength floor once consent fires"),
    "abandonment_floor":  Coefficient("abandonment_floor", 0.92, False, "exception strength floor once abandonment fires"),
    "incident_floor":     Coefficient("incident_floor", 0.84, False, "exception strength floor for search-incident"),
    "automobile_floor":   Coefficient("automobile_floor", 0.75, False, "exception strength floor for the automobile exception"),
    "scope_default":      Coefficient("scope_default", 0.75, False, "assumed scope fidelity when unspecified"),
    "spec_default":       Coefficient("spec_default", 0.70, False, "assumed warrant specificity when unspecified"),
    "breach_floor":       Coefficient("breach_floor", 0.75, False, "breach floor when scope_breach operator fires"),
    "gf_damping":         Coefficient("gf_damping", 0.72, False, "good-faith damping weight"),
    "atten_damping":      Coefficient("atten_damping", 0.58, False, "attenuation damping weight"),
    "private_damping":    Coefficient("private_damping", 0.35, False, "private-search damping weight"),
    "violation_base":     Coefficient("violation_base", 0.55, False, "base term of violation pressure"),
    "violation_breach":   Coefficient("violation_breach", 0.45, False, "breach contribution to violation pressure"),
    "amb_boost":          Coefficient("amb_boost", 0.15, False, "factual-ambiguity boost"),
    "obs_stabilizer":     Coefficient("obs_stabilizer", 0.12, False, "observability stabilizer"),
    "breach_revival":     Coefficient("breach_revival", 0.58, False, "independent breach revival of pressure"),
}


def ungrounded_coefficients() -> List[Coefficient]:
    return [c for c in C.values() if not c.grounded]


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


# -- the formula, faithful to v4.3.1 but routed through the registry ----------

def effective_privacy(u: Mapping[str, float]) -> float:
    priv = float(u.get("Priv", 0.0))
    bound = float(u.get("Bound", 0.0))
    gate = float(u.get("Gate", 0.0))
    return clamp01(priv * (1.0 - C["bound_collapse"].value * bound)
                   * (1.0 - C["gate_narrowing"].value * gate))


def effective_exception(u: Mapping[str, float], op: Mapping[str, float]) -> float:
    excp = float(u.get("Excp", 0.0))
    if op.get("exigency", 0.0) > 0.5:
        excp = max(excp, C["exigency_floor"].value)
    if op.get("consent", 0.0) > 0.5:
        excp = max(excp, C["consent_floor"].value)
    if op.get("abandonment", 0.0) > 0.5:
        excp = max(excp, C["abandonment_floor"].value)
    if op.get("search_incident", 0.0) > 0.5:
        excp = max(excp, C["incident_floor"].value)
    if op.get("automobile_exception", 0.0) > 0.5:
        excp = max(excp, C["automobile_floor"].value)
    return clamp01(excp)


def scope_breach(u: Mapping[str, float], op: Mapping[str, float]) -> float:
    scope_fit = float(u.get("Scope", C["scope_default"].value))
    spec = float(u.get("Spec", C["spec_default"].value))
    breach = max(0.0, 1.0 - min(scope_fit, spec))
    if op.get("scope_breach", 0.0) > 0.5:
        breach = max(breach, C["breach_floor"].value)
    return clamp01(breach)


def damping(u: Mapping[str, float], op: Mapping[str, float]) -> float:
    gf_avail = float(u.get("JRem", 1.0))
    d = 0.0
    d += gf_avail * C["gf_damping"].value * float(op.get("good_faith", 0.0))
    d += C["atten_damping"].value * float(op.get("attenuation", 0.0))
    d += C["private_damping"].value * float(op.get("private_search", 0.0))
    return clamp01(d)


def suppression_pressure(u: Mapping[str, float],
                         op: Mapping[str, float]) -> Tuple[float, List[Coefficient]]:
    """Return (pressure in [0,1], the ungrounded coefficients it relied on).

    The second element is the point. The caller receives the score and, in the
    same breath, the full list of hand-chosen constants that produced it. A
    number you cannot separate from its assumptions is harder to over-trust.
    """
    priv_eff = effective_privacy(u)
    excp_eff = effective_exception(u, op)
    rem = float(u.get("Rem", 0.0))
    obs = float(u.get("Obs", 0.0))
    amb = float(u.get("Amb", 0.0))
    breach = scope_breach(u, op)
    damp = damping(u, op)

    violation_pressure = priv_eff * (1.0 - excp_eff) * (
        C["violation_base"].value + C["violation_breach"].value * breach)
    ambiguity_boost = 1.0 + C["amb_boost"].value * amb
    observation_stabilizer = 1.0 - C["obs_stabilizer"].value * obs
    pressure = violation_pressure * rem * ambiguity_boost * observation_stabilizer * (1.0 - damp)
    pressure = max(pressure, C["breach_revival"].value * breach * rem * (1.0 - damp))
    return clamp01(pressure), ungrounded_coefficients()
