"""Synthium Judicial Module Spec v0.2.

Domain instantiation for Fourth Amendment suppression doctrine.
This module does not replace Synthium Core. It supplies field-specific
units, operators, formula hierarchy, and confidence tags for one legal slice.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple


class DiscoveryConfidence(str, Enum):
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    MODERATE_LOW = "MODERATE_LOW"
    LOW = "LOW"
    SPECULATIVE = "SPECULATIVE"


@dataclass(frozen=True)
class JudicialUnit:
    symbol: str
    name: str
    definition: str
    confidence: DiscoveryConfidence
    canonical: bool = True


@dataclass(frozen=True)
class JudicialOperator:
    key: str
    name: str
    definition: str
    formula: str
    confidence: DiscoveryConfidence


CANONICAL_UNITS: Tuple[str, ...] = (
    "Obs", "Priv", "Excp", "Rem", "Close", "Amb"
)

EXTENDED_UNITS: Tuple[str, ...] = (
    "Obs", "Priv", "Excp", "Rem", "Close", "Amb",
    "Temp", "Gate", "Bound", "Spec", "Scope", "JRem"
)

UNIT_DEFINITIONS: Dict[str, JudicialUnit] = {
    "Obs": JudicialUnit(
        "Obs", "Observability",
        "Direct lawful perceptual grounding behind state action.",
        DiscoveryConfidence.MODERATE,
    ),
    "Priv": JudicialUnit(
        "Priv", "Privacy legitimacy",
        "Baseline legal weight of the privacy interest before exceptions.",
        DiscoveryConfidence.HIGH,
    ),
    "Excp": JudicialUnit(
        "Excp", "Exception strength",
        "Force of a doctrine that transforms or overrides baseline privacy.",
        DiscoveryConfidence.HIGH,
    ),
    "Rem": JudicialUnit(
        "Rem", "Remedial proximity",
        "Closeness between possible violation and evidence sought to be excluded.",
        DiscoveryConfidence.HIGH,
    ),
    "Close": JudicialUnit(
        "Close", "Doctrinal closure",
        "Compression of judicial movement by precedent, statute, or settled doctrine.",
        DiscoveryConfidence.MODERATE,
    ),
    "Amb": JudicialUnit(
        "Amb", "Factual ambiguity",
        "Instability or contestability of key threshold facts.",
        DiscoveryConfidence.MODERATE,
    ),
    "Temp": JudicialUnit(
        "Temp", "Temporal admissibility distance",
        "Procedural-time distance between original act and later evidentiary use.",
        DiscoveryConfidence.MODERATE_LOW,
        canonical=False,
    ),
    "Gate": JudicialUnit(
        "Gate", "State-action gateway weight",
        "Degree to which Fourth Amendment scrutiny narrows because action is private.",
        DiscoveryConfidence.MODERATE_LOW,
        canonical=False,
    ),
    "Bound": JudicialUnit(
        "Bound", "Boundary reclassification weight",
        "Degree to which privacy status collapses after protected-zone reclassification.",
        DiscoveryConfidence.MODERATE,
        canonical=False,
    ),
    "Spec": JudicialUnit(
        "Spec", "Warrant specificity",
        "Particularity and data-scope precision of a warrant or authorization.",
        DiscoveryConfidence.MODERATE_LOW,
        canonical=False,
    ),
    "Scope": JudicialUnit(
        "Scope", "Authorization-scope fidelity",
        "Match between legal authorization granted and action actually taken.",
        DiscoveryConfidence.MODERATE,
        canonical=False,
    ),
    "JRem": JudicialUnit(
        "JRem", "Jurisdictional remedial regime",
        "Availability of local remedy dampers such as good faith.",
        DiscoveryConfidence.MODERATE_LOW,
        canonical=False,
    ),
}

OPERATOR_KEYS: Tuple[str, ...] = (
    "abandonment", "consent", "exigency", "good_faith", "attenuation",
    "private_search", "scope_breach", "curtilage", "emergency_aid",
    "public_exposure", "automobile_exception", "protective_sweep",
    "probation_waiver", "search_incident", "boundary_reclassification",
    "digital_privacy", "home_core", "warrant_particularity",
)

OPERATOR_DEFINITIONS: Dict[str, JudicialOperator] = {
    "exigency": JudicialOperator(
        "exigency", "Exigency dominance",
        "Urgency can dominate locally and raise effective exception strength.",
        "Excp_eff = max(Excp_base, Exigency_strength)",
        DiscoveryConfidence.HIGH,
    ),
    "good_faith": JudicialOperator(
        "good_faith", "Good-faith damping",
        "Reasonable reliance can reduce suppression pressure in jurisdictions permitting it.",
        "Damping_eff += GF_avail * GoodFaith",
        DiscoveryConfidence.HIGH,
    ),
    "abandonment": JudicialOperator(
        "abandonment", "Abandonment collapse",
        "Abandonment can collapse effective privacy sharply.",
        "Priv_eff = Priv_base * (1 - A)",
        DiscoveryConfidence.HIGH,
    ),
    "boundary_reclassification": JudicialOperator(
        "boundary_reclassification", "Boundary reclassification",
        "Place or object is classified outside the protected zone.",
        "Priv_eff = Priv_base * B",
        DiscoveryConfidence.HIGH,
    ),
    "private_search": JudicialOperator(
        "private_search", "Private-search gateway",
        "Private non-state search narrows the Fourth Amendment gateway.",
        "GatewayTransform = f(state_action_boundary)",
        DiscoveryConfidence.MODERATE,
    ),
    "scope_breach": JudicialOperator(
        "scope_breach", "Scope authorization breach",
        "State action exceeds the actual authorization granted.",
        "ScopeBreach = max(0, ActionDepth - AuthorizedDepth)",
        DiscoveryConfidence.MODERATE,
    ),
    "emergency_aid": JudicialOperator(
        "emergency_aid", "Emergency-aid scope limit",
        "Emergency aid may justify entry but not unrelated exploratory search.",
        "Excp_valid = EmergencyAid_strength * ScopeFit",
        DiscoveryConfidence.MODERATE,
    ),
    "public_exposure": JudicialOperator(
        "public_exposure", "Public exposure visibility",
        "Exposure to ordinary public view can reduce effective privacy.",
        "Priv_eff = Priv_base * ExposureShield",
        DiscoveryConfidence.MODERATE_LOW,
    ),
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

OUTCOME_CLASSES: Tuple[str, ...] = (
    "DENIED", "GRANTED", "MIXED_REMAND", "PROCEDURAL", "UNKNOWN", "GRANTED_OR_REVERSED"
)


def summarize_spec() -> Dict[str, object]:
    return {
        "canonical_units": list(CANONICAL_UNITS),
        "extended_units": list(EXTENDED_UNITS),
        "operators": list(OPERATOR_KEYS),
        "formulas": list(FORMULA_HIERARCHY),
        "unit_confidence": {k: v.confidence.value for k, v in UNIT_DEFINITIONS.items()},
    }
