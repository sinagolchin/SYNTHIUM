"""Judicial Module v0.2 -- Fourth Amendment suppression doctrine.

A PROPOSED subject core: a set of units, operators, and formulas hypothesised
for one domain. A subject core never becomes Core. Core is the universal
ruler-building infrastructure (:mod:`synthium.core`); a subject core is a
falsifiable claim about a particular field, carried at ``Status.PROPOSED``
until a held-out test says otherwise.

Everything here is a constructed instrument under development, not a coordinate
of reality. The unit "confidence" tags below describe how settled the *coder*
felt the dimension was -- they are NOT evidence of predictive validity.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class Unit:
    key: str
    name: str
    description: str
    coder_confidence: str   # qualitative coder note, NOT empirical support
    canonical: bool = True


@dataclass(frozen=True)
class Operator:
    key: str
    name: str
    description: str
    symbolic_form: str
    coder_confidence: str


CANONICAL_UNITS: Tuple[str, ...] = ("Obs", "Priv", "Excp", "Rem", "Close", "Amb")

EXTENDED_UNITS: Tuple[str, ...] = CANONICAL_UNITS + (
    "Temp", "Gate", "Bound", "Spec", "Scope", "JRem",
)

UNIT_DEFINITIONS: Dict[str, Unit] = {
    "Obs":   Unit("Obs", "Observability", "Direct lawful perceptual grounding behind state action.", "moderate"),
    "Priv":  Unit("Priv", "Privacy legitimacy", "Baseline legal weight of the privacy interest before exceptions.", "high"),
    "Excp":  Unit("Excp", "Exception strength", "Force of a doctrine that transforms or overrides baseline privacy.", "high"),
    "Rem":   Unit("Rem", "Remedial proximity", "Closeness between possible violation and evidence sought to be excluded.", "high"),
    "Close": Unit("Close", "Doctrinal closure", "Compression of judicial movement by precedent, statute, or settled doctrine.", "moderate"),
    "Amb":   Unit("Amb", "Factual ambiguity", "Instability or contestability of key threshold facts.", "moderate"),
    "Temp":  Unit("Temp", "Temporal admissibility distance", "Procedural-time distance between original act and later evidentiary use.", "moderate-low", canonical=False),
    "Gate":  Unit("Gate", "State-action gateway weight", "Degree to which Fourth Amendment scrutiny narrows because action is private.", "moderate-low", canonical=False),
    "Bound": Unit("Bound", "Boundary reclassification weight", "Degree to which privacy status collapses after protected-zone reclassification.", "moderate", canonical=False),
    "Spec":  Unit("Spec", "Warrant specificity", "Particularity and data-scope precision of a warrant or authorization.", "moderate-low", canonical=False),
    "Scope": Unit("Scope", "Authorization-scope fidelity", "Match between legal authorization granted and action actually taken.", "moderate", canonical=False),
    "JRem":  Unit("JRem", "Jurisdictional remedial regime", "Availability of local remedy dampers such as good faith.", "moderate-low", canonical=False),
}

OPERATOR_KEYS: Tuple[str, ...] = (
    "abandonment", "consent", "exigency", "good_faith", "attenuation",
    "private_search", "scope_breach", "curtilage", "emergency_aid",
    "public_exposure", "automobile_exception", "protective_sweep",
    "probation_waiver", "search_incident", "boundary_reclassification",
    "digital_privacy", "home_core", "warrant_particularity",
)

OPERATOR_DEFINITIONS: Dict[str, Operator] = {
    "exigency": Operator("exigency", "Exigency dominance",
        "Urgency can dominate locally and raise effective exception strength.",
        "Excp_eff = max(Excp_base, Exigency_strength)", "high"),
    "good_faith": Operator("good_faith", "Good-faith damping",
        "Reasonable reliance can reduce suppression pressure where permitted.",
        "Damping_eff += GF_avail * GoodFaith", "high"),
    "abandonment": Operator("abandonment", "Abandonment collapse",
        "Abandonment can collapse effective privacy sharply.",
        "Priv_eff = Priv_base * (1 - A)", "high"),
    "boundary_reclassification": Operator("boundary_reclassification", "Boundary reclassification",
        "Place or object is classified outside the protected zone.",
        "Priv_eff = Priv_base * B", "high"),
    "private_search": Operator("private_search", "Private-search gateway",
        "Private non-state search narrows the Fourth Amendment gateway.",
        "GatewayTransform = f(state_action_boundary)", "moderate"),
    "scope_breach": Operator("scope_breach", "Scope authorization breach",
        "State action exceeds the actual authorization granted.",
        "ScopeBreach = max(0, ActionDepth - AuthorizedDepth)", "moderate"),
    "emergency_aid": Operator("emergency_aid", "Emergency-aid scope limit",
        "Emergency aid may justify entry but not unrelated exploratory search.",
        "Excp_valid = EmergencyAid_strength * ScopeFit", "moderate"),
    "public_exposure": Operator("public_exposure", "Public exposure visibility",
        "Exposure to ordinary public view can reduce effective privacy.",
        "Priv_eff = Priv_base * ExposureShield", "moderate-low"),
}

FORMULA_HIERARCHY: Tuple[str, ...] = (
    "J_case = [Obs, Priv, Excp, Rem, Close, Amb]",
    "J_case_ext = [Obs, Priv, Excp, Rem, Close, Amb, Temp, Gate, Bound, Spec, Scope, JRem]",
    "P0 = PrivacySurface(J_case_ext, t)",
    "P1 = BoundaryTransform(P0, Bound)",
    "P2 = ExceptionTransform(P1, Excp)",
    "P3 = GatewayTransform(P2, Gate)",
    "P4 = ScopeTransform(P3, Scope, Spec)",
    "Outcome ~= RemedyFilter(P4, Rem, JRem)",
)

# The atlas uses these outcome labels. The binary suppression question the
# courtlistener labeler answers is GRANTED vs DENIED; the others are atlas-only
# bookkeeping for cases that do not reduce to a clean grant/deny.
OUTCOME_CLASSES: Tuple[str, ...] = (
    "DENIED", "GRANTED", "MIXED_REMAND", "PROCEDURAL", "UNKNOWN", "GRANTED_OR_REVERSED",
)


def summarize_spec() -> Dict[str, object]:
    return {
        "status": "PROPOSED",
        "canonical_units": list(CANONICAL_UNITS),
        "extended_units": list(EXTENDED_UNITS),
        "operators": list(OPERATOR_KEYS),
        "formulas": list(FORMULA_HIERARCHY),
        "n_units": len(EXTENDED_UNITS),
        "n_operators": len(OPERATOR_KEYS),
    }
