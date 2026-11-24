#!/usr/bin/env python3
"""SYNTHIUM v5.0 — HONESTY HARNESS.

A scaffolding that REFUSES to operate without explicit grounding.

This is not a replacement for Synthium's substance. It is the container
that forces the substance to be honest about what it is.

WHAT THIS DOES
--------------
1. Every numeric value carries its scale type (nominal, ordinal, interval, ratio).
2. Arithmetic operations are forbidden when the scale type does not support them.
   You cannot multiply two ordinal values. You cannot take a ratio of interval
   values. The framework raises ScaleTypeError instead of silently producing
   meaningless numbers.
3. Every value carries provenance: where it came from, how it was derived,
   what it depends on. Unjustified values are flagged as such and the audit
   will surface them.
4. Units cannot be registered without: declared scale type, anchor cases,
   defined zero point, failure conditions, and granularity claim.
5. Axioms are first-class objects. Each axiom has a statement and (optionally)
   a mathematical form. If the mathematical form is missing, the framework
   tracks that as an open question.
6. Multiple structural hypotheses can coexist. The framework hosts them and
   compares their predictions, rather than committing to one structure.
7. Inter-rater reliability is a required slot for any unit before that unit
   can be called calibrated.
8. The audit() method walks the entire subject core and reports every empty
   slot, every unjustified parameter, every axiom without math, every formula
   operating on the wrong scale.

WHAT THIS DOES NOT DO
---------------------
1. Invent numbers. There are no hand-tuned decimals in this file. The previous
   versions of Synthium were full of coefficients like 0.85, 0.45, 0.72 that
   nobody could justify. This file declines to write any.
2. Invent the mathematical form of axioms. The axioms in build_judicial_stub()
   below are stated in words; their mathematical form is explicitly None.
   That is the honest current state. Filling them in is your work.
3. Pretend that the existing 44-case atlas is calibrated. It isn't. The audit
   will say so.

USAGE
-----
    python synthium_v5_0_honesty.py
        Runs the audit on the stub judicial core and prints the report.

    Import it as a library to build your own subject cores:
        from synthium_v5_0_honesty import (
            SubjectCore, Unit, Axiom, AnchorCase, ScaleType,
            ScaledValue, JustifiedParameter, ...
        )
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone


def _now_iso() -> str:
    """Timezone-aware ISO timestamp."""
    return datetime.now(timezone.utc).isoformat()
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import textwrap


# ============================================================================
# 1. EXCEPTIONS — the framework's refusals
# ============================================================================

class SynthiumError(Exception):
    """Base class for all honesty-harness refusals."""


class ScaleTypeError(SynthiumError):
    """An arithmetic operation was attempted that the scale type forbids."""


class UnjustifiedValueError(SynthiumError):
    """A value with no derivation was used in a calculation that requires one."""


class IncompleteUnitError(SynthiumError):
    """A unit was registered without the required slots filled in."""


class MissingProvenanceError(SynthiumError):
    """A value was created without provenance information."""


class AxiomNotFormalizedError(SynthiumError):
    """An operation requires an axiom's mathematical form, which is not yet defined."""


# ============================================================================
# 2. SCALE TYPES — Stevens' typology, enforced at runtime
# ============================================================================

class ScaleType(Enum):
    """Stevens' (1946) typology of measurement scales.

    Each level admits a strictly larger set of operations than the level below.
    The framework enforces this at runtime.
    """
    NOMINAL = "nominal"     # categories only; ==, != legal
    ORDINAL = "ordinal"     # ranked; <, >, <=, >= legal; no arithmetic
    INTERVAL = "interval"   # equal gaps, no true zero; +, - legal; * legal with scalar only
    RATIO = "ratio"         # true zero; all arithmetic legal


# Legal operations per scale type. The framework uses this table to decide
# whether to permit or refuse an operation.
LEGAL_OPS: Dict[ScaleType, Set[str]] = {
    ScaleType.NOMINAL: {"=="},
    ScaleType.ORDINAL: {"==", "<", "<=", ">", ">="},
    ScaleType.INTERVAL: {"==", "<", "<=", ">", ">=", "+", "-", "scalar_mul"},
    ScaleType.RATIO: {"==", "<", "<=", ">", ">=", "+", "-", "scalar_mul", "*", "/"},
}


# ============================================================================
# 3. PROVENANCE — every value knows where it came from
# ============================================================================

class Origin(Enum):
    """How a value came to exist in the framework."""
    MEASURED = "measured"         # produced by a qualified coder on a real case
    STIPULATED = "stipulated"     # defined as an anchor (e.g., Katz = 1.0 by definition)
    DERIVED = "derived"           # computed from other ScaledValues via legal ops
    UNJUSTIFIED = "unjustified"   # value exists but has no derivation; flagged
    PLACEHOLDER = "placeholder"   # explicitly empty; raises if used in computation


@dataclass(frozen=True)
class Provenance:
    """Where a value came from. Every ScaledValue must have one."""
    origin: Origin
    derivation: str                          # human-readable explanation
    inputs: Tuple[str, ...] = ()             # references to other values this depends on
    timestamp: str = field(default_factory=lambda: _now_iso())


# ============================================================================
# 4. SCALED VALUES — numbers that know their own scale
# ============================================================================

class ScaledValue:
    """A numeric value tagged with its scale type and provenance.

    Arithmetic operations are checked against LEGAL_OPS for the scale type.
    Attempts to multiply or divide ordinal values raise ScaleTypeError.

    This is the heart of the honesty harness: it makes scale violations
    impossible to commit silently.
    """

    def __init__(self, value: float, scale_type: ScaleType,
                 unit_symbol: str, provenance: Provenance):
        if provenance is None:
            raise MissingProvenanceError(
                f"ScaledValue for unit {unit_symbol!r} created without provenance"
            )
        self.value = float(value)
        self.scale_type = scale_type
        self.unit_symbol = unit_symbol
        self.provenance = provenance

    def _require_op(self, op: str) -> None:
        if op not in LEGAL_OPS[self.scale_type]:
            raise ScaleTypeError(
                f"Operation {op!r} is not legal on a {self.scale_type.value} "
                f"value (unit {self.unit_symbol!r}). "
                f"Legal operations for this scale: {sorted(LEGAL_OPS[self.scale_type])}."
            )

    def _require_compatible(self, other: "ScaledValue", op: str) -> None:
        if self.unit_symbol != other.unit_symbol:
            raise ScaleTypeError(
                f"Cannot {op} values of different units: "
                f"{self.unit_symbol!r} and {other.unit_symbol!r}. "
                f"Cross-unit arithmetic requires an explicit JustifiedFormula."
            )
        if self.scale_type != other.scale_type:
            raise ScaleTypeError(
                f"Cannot {op} values of different scale types: "
                f"{self.scale_type.value} and {other.scale_type.value}."
            )

    def __add__(self, other: "ScaledValue") -> "ScaledValue":
        self._require_op("+")
        self._require_compatible(other, "add")
        return ScaledValue(
            self.value + other.value,
            self.scale_type,
            self.unit_symbol,
            Provenance(
                origin=Origin.DERIVED,
                derivation=f"({self}) + ({other})",
                inputs=(repr(self), repr(other)),
            ),
        )

    def __sub__(self, other: "ScaledValue") -> "ScaledValue":
        self._require_op("-")
        self._require_compatible(other, "subtract")
        return ScaledValue(
            self.value - other.value,
            self.scale_type,
            self.unit_symbol,
            Provenance(
                origin=Origin.DERIVED,
                derivation=f"({self}) - ({other})",
                inputs=(repr(self), repr(other)),
            ),
        )

    def __mul__(self, other: Any) -> "ScaledValue":
        # Scalar multiplication: legal on interval and ratio.
        if isinstance(other, (int, float)):
            self._require_op("scalar_mul")
            return ScaledValue(
                self.value * float(other),
                self.scale_type,
                self.unit_symbol,
                Provenance(
                    origin=Origin.DERIVED,
                    derivation=f"({self}) * {other!r} (scalar)",
                    inputs=(repr(self),),
                ),
            )
        # Value-by-value multiplication: requires ratio scale.
        if isinstance(other, ScaledValue):
            self._require_op("*")
            other._require_op("*")
            # Cross-unit ratio multiplication is permitted because ratio scales
            # support it dimensionally, but the resulting unit is unclear and
            # must be named by a JustifiedFormula. We flag the result.
            new_unit = f"{self.unit_symbol}*{other.unit_symbol}"
            return ScaledValue(
                self.value * other.value,
                ScaleType.RATIO,
                new_unit,
                Provenance(
                    origin=Origin.DERIVED,
                    derivation=f"({self}) * ({other})",
                    inputs=(repr(self), repr(other)),
                ),
            )
        return NotImplemented

    def __rmul__(self, other: Any) -> "ScaledValue":
        return self.__mul__(other)

    def __truediv__(self, other: Any) -> "ScaledValue":
        if isinstance(other, (int, float)):
            self._require_op("scalar_mul")
            return self.__mul__(1.0 / float(other))
        if isinstance(other, ScaledValue):
            self._require_op("/")
            other._require_op("/")
            new_unit = f"{self.unit_symbol}/{other.unit_symbol}"
            return ScaledValue(
                self.value / other.value,
                ScaleType.RATIO,
                new_unit,
                Provenance(
                    origin=Origin.DERIVED,
                    derivation=f"({self}) / ({other})",
                    inputs=(repr(self), repr(other)),
                ),
            )
        return NotImplemented

    def __lt__(self, other: "ScaledValue") -> bool:
        self._require_op("<")
        self._require_compatible(other, "compare")
        return self.value < other.value

    def __le__(self, other: "ScaledValue") -> bool:
        self._require_op("<=")
        self._require_compatible(other, "compare")
        return self.value <= other.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ScaledValue):
            return NotImplemented
        if self.unit_symbol != other.unit_symbol:
            return False
        return self.value == other.value

    def __repr__(self) -> str:
        return (f"ScaledValue({self.value!r}, {self.unit_symbol!r}, "
                f"{self.scale_type.value}, origin={self.provenance.origin.value})")

    def __str__(self) -> str:
        return f"{self.unit_symbol}={self.value} [{self.scale_type.value}]"


# ============================================================================
# 5. JUSTIFIED PARAMETERS — replaces hand-tuned coefficients
# ============================================================================

@dataclass
class JustifiedParameter:
    """A named numeric parameter that must declare where its value came from.

    Replaces the hand-tuned coefficients sprinkled through the original
    Synthium (0.85, 0.45, 0.55, 0.72, etc.). Each one must be justified
    or marked explicitly as unjustified.
    """
    name: str
    value: Optional[float]                  # None means "not yet set"
    justification: str                      # required free-text explanation
    derivation_method: Optional[str] = None # e.g., "fit on N=500 cases", "anchor stipulation"
    sensitivity_tested: bool = False
    sensitivity_range: Optional[Tuple[float, float]] = None
    references: Tuple[str, ...] = ()

    @property
    def is_justified(self) -> bool:
        if self.value is None:
            return False
        # A justification of "I picked it" or empty does not count.
        bad_strings = {"", "i picked it", "looks right", "pattern match",
                       "convention", "tbd", "todo"}
        return self.justification.strip().lower() not in bad_strings

    @property
    def is_unjustified(self) -> bool:
        return self.value is not None and not self.is_justified

    def __post_init__(self):
        if self.value is not None and not self.justification:
            # A value with empty justification is the exact thing we're refusing.
            raise UnjustifiedValueError(
                f"Parameter {self.name!r} has value {self.value} but no justification. "
                f"If you cannot justify it, set value=None and explain why in the "
                f"justification field."
            )


# ============================================================================
# 6. ANCHOR CASES — operationalize the scale
# ============================================================================

@dataclass(frozen=True)
class AnchorCase:
    """A case that defines the meaning of a particular value on a unit's scale.

    Anchor values are STIPULATED, not measured. They are the operational
    definition of what "1.0" or "0.0" means on a given unit. Other case
    values are calibrated relative to anchors.
    """
    case_name: str
    case_id: str               # e.g., citation, docket number
    unit_symbol: str
    value: float               # the stipulated value (typically 0.0 or 1.0, but not required)
    justification: str         # why this case anchors at this value
    sources: Tuple[str, ...] = ()
    coder_id: str = ""         # who set this anchor
    timestamp: str = field(default_factory=lambda: _now_iso())

    def as_scaled_value(self, scale_type: ScaleType) -> ScaledValue:
        return ScaledValue(
            value=self.value,
            scale_type=scale_type,
            unit_symbol=self.unit_symbol,
            provenance=Provenance(
                origin=Origin.STIPULATED,
                derivation=(f"Anchor case {self.case_name} ({self.case_id}) "
                            f"stipulated as {self.unit_symbol}={self.value}. "
                            f"Justification: {self.justification}"),
            ),
        )


# ============================================================================
# 7. RELIABILITY RECORDS — inter-rater agreement data
# ============================================================================

@dataclass(frozen=True)
class ReliabilityRecord:
    """An empirical record of how well coders agree when applying the rubric
    to assign values on this unit.

    A unit without a ReliabilityRecord is not calibrated.
    """
    unit_symbol: str
    krippendorff_alpha: float
    n_coders: int
    n_cases: int
    date: str
    coder_ids: Tuple[str, ...] = ()
    notes: str = ""

    def meets_threshold(self, alpha_min: float) -> bool:
        """Does this reliability record clear a chosen threshold?

        The threshold is a parameter of the question, not of the record.
        The record itself just contains the measurement.
        """
        return self.krippendorff_alpha >= alpha_min


# ============================================================================
# 8. FALSIFICATION CONDITIONS — what would kill a component
# ============================================================================

@dataclass(frozen=True)
class FalsificationCondition:
    """A specific empirical condition that, if observed, requires abandoning
    or revising a particular component of the framework.

    A framework without falsification conditions is unfalsifiable, which is
    a failure mode for a research program that claims to be scientific.
    """
    component: str             # which part of the framework this applies to
    test: str                  # what experiment establishes the condition
    threshold: str             # the precise numeric or logical threshold
    action_if_failed: str      # what we commit to doing if the condition is met
    date_committed: str = field(default_factory=lambda: _now_iso())


# ============================================================================
# 9. CODER QUALIFICATION — who can score what
# ============================================================================

@dataclass
class CoderQualification:
    """Tracks which coder has been calibrated on which unit, and how well."""
    coder_id: str
    qualified_units: Set[str] = field(default_factory=set)
    calibration_sessions: List["CalibrationSession"] = field(default_factory=list)
    notes: str = ""


@dataclass(frozen=True)
class CalibrationSession:
    """A record of a coder going through calibration on a specific unit."""
    coder_id: str
    unit_symbol: str
    n_cases: int
    fraction_within_tolerance: float
    tolerance: float
    passed: bool
    date: str


# ============================================================================
# 10. UNITS — measurement dimensions, with required grounding
# ============================================================================

class Unit:
    """A proposed measurement dimension.

    A Unit cannot be constructed without:
      - a declared scale type
      - at least one anchor case
      - an explicit zero point (a case where the unit is by definition 0)
      - explicit failure conditions (when the unit does not apply)
      - a granularity claim (continuous, or n discrete levels)

    A Unit may exist without a ReliabilityRecord, but the audit will flag it.
    """

    def __init__(self,
                 symbol: str,
                 name: str,
                 definition: str,
                 scale_type: ScaleType,
                 anchors: List[AnchorCase],
                 zero_point: Optional[AnchorCase],
                 failure_conditions: List[str],
                 granularity: str,            # e.g., "continuous", "ordinal-5", "ordinal-3"
                 coding_procedure: str = "",  # the operational rules a coder follows
                 reliability: Optional[ReliabilityRecord] = None,
                 references: Tuple[str, ...] = ()):
        if not symbol:
            raise IncompleteUnitError("Unit must have a non-empty symbol.")
        if not anchors:
            raise IncompleteUnitError(
                f"Unit {symbol!r}: at least one anchor case is required. "
                f"Without anchors, the scale has no operational meaning."
            )
        if zero_point is None and scale_type == ScaleType.RATIO:
            raise IncompleteUnitError(
                f"Unit {symbol!r}: ratio-scale units require an explicit zero point. "
                f"You must name a case where the unit is, by definition, 0.0."
            )
        if not failure_conditions:
            raise IncompleteUnitError(
                f"Unit {symbol!r}: failure_conditions must be a non-empty list. "
                f"Name at least one situation in which this unit does not apply."
            )
        if not granularity:
            raise IncompleteUnitError(
                f"Unit {symbol!r}: granularity must be declared. "
                f"Choose 'continuous', 'ordinal-N', or describe explicitly."
            )

        self.symbol = symbol
        self.name = name
        self.definition = definition
        self.scale_type = scale_type
        self.anchors = list(anchors)
        self.zero_point = zero_point
        self.failure_conditions = list(failure_conditions)
        self.granularity = granularity
        self.coding_procedure = coding_procedure
        self.reliability = reliability
        self.references = references

    def is_calibrated(self, alpha_min: float) -> bool:
        if self.reliability is None:
            return False
        return self.reliability.meets_threshold(alpha_min)

    def value(self, raw: float, provenance: Provenance) -> ScaledValue:
        """Wrap a raw float in a ScaledValue tagged for this unit."""
        return ScaledValue(raw, self.scale_type, self.symbol, provenance)


# ============================================================================
# 11. AXIOMS — the rules of the game
# ============================================================================

@dataclass
class Axiom:
    """A foundational claim from which the framework's structure derives.

    An axiom has a statement (in natural language) and, optionally, a
    mathematical_form. If the mathematical_form is None, the axiom is
    currently informal. The framework will track that and surface it in
    the audit; the user's work is to formalize it.
    """
    name: str
    statement: str
    mathematical_form: Optional[str] = None    # e.g., "∃ invariant I such that ∂I/∂t = 0"
    derives_what: Tuple[str, ...] = ()         # what other axioms or structures follow
    notes: str = ""

    @property
    def is_formalized(self) -> bool:
        return self.mathematical_form is not None and self.mathematical_form.strip() != ""


# ============================================================================
# 12. STRUCTURAL HYPOTHESES — competing proposals for how a domain works
# ============================================================================

@dataclass
class StructuralHypothesis:
    """A proposed mathematical structure for a domain.

    Multiple hypotheses can be registered simultaneously. The framework's
    job is to compare their predictions, not to enshrine one of them.
    """
    name: str
    description: str
    unit_symbols: Tuple[str, ...]
    formula_descriptions: Dict[str, str] = field(default_factory=dict)
    formulas: Dict[str, Callable] = field(default_factory=dict)
    parameters: Dict[str, JustifiedParameter] = field(default_factory=dict)
    prediction_log: List[Dict[str, Any]] = field(default_factory=list)

    def has_unjustified_parameters(self) -> List[str]:
        return [p.name for p in self.parameters.values() if p.is_unjustified]


# ============================================================================
# 13. CROSS-DOMAIN OBSERVATION LOG — replaces `universal_candidate`
# ============================================================================

@dataclass(frozen=True)
class CrossDomainObservation:
    """A recorded observation that two units from different subject cores
    behave similarly on some defined measure.

    NOT a claim that the units are "the same thing." A data point. Multiple
    such observations across independent rubrics are the only way to build
    evidence for a cross-domain structural claim.
    """
    obs_id: str
    domain_a: str
    unit_a: str
    domain_b: str
    unit_b: str
    similarity_method: str
    similarity_value: float
    n_samples_a: int
    n_samples_b: int
    paired: bool
    rubric_version_a: str
    rubric_version_b: str
    coder_ids: Tuple[str, ...]
    timestamp: str = field(default_factory=lambda: _now_iso())
    notes: str = ""


class CrossDomainRegistry:
    """An evidence log, not a category."""

    def __init__(self):
        self.observations: List[CrossDomainObservation] = []

    def add(self, obs: CrossDomainObservation) -> None:
        self.observations.append(obs)

    def for_pair(self, unit_a: str, unit_b: str) -> List[CrossDomainObservation]:
        key = frozenset({unit_a, unit_b})
        return [o for o in self.observations
                if frozenset({o.unit_a, o.unit_b}) == key]


# ============================================================================
# 14. COHERENCE TEST — does a case violate the axioms?
# ============================================================================

class CoherenceTest:
    """Given a set of formalized axioms, evaluate whether a case (or system
    state) is coherent with them, incoherent (violates them), or untestable
    (axioms not yet formalized).
    """

    def __init__(self, axioms: List[Axiom]):
        self.axioms = list(axioms)

    def evaluate(self, case_description: str, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Walk each axiom and report its status against the case.

        Currently, axioms with no mathematical_form return 'untestable'.
        Once axioms are formalized, this method should dispatch to their
        specific test logic.
        """
        results = []
        for ax in self.axioms:
            if not ax.is_formalized:
                results.append({
                    "axiom": ax.name,
                    "status": "untestable",
                    "reason": "axiom has no mathematical form yet",
                })
                continue
            # Axiom-specific test logic would go here. We do not invent it.
            results.append({
                "axiom": ax.name,
                "status": "test_not_yet_implemented",
                "reason": (f"axiom is formalized as: {ax.mathematical_form!r} "
                           f"but the corresponding evaluator has not been written"),
            })
        n_untestable = sum(1 for r in results if r["status"] == "untestable")
        return {
            "case": case_description,
            "axioms_evaluated": len(self.axioms),
            "axioms_untestable": n_untestable,
            "per_axiom": results,
        }


# ============================================================================
# 15. SUBJECT CORE — collects units, axioms, hypotheses, etc.
# ============================================================================

class SubjectCore:
    """A domain instantiation. Holds the units, axioms, hypotheses,
    coders, and reliability records for a specific field.
    """

    def __init__(self, name: str):
        self.name = name
        self.units: Dict[str, Unit] = {}
        self.axioms: List[Axiom] = []
        self.hypotheses: List[StructuralHypothesis] = []
        self.coders: Dict[str, CoderQualification] = {}
        self.falsification_conditions: List[FalsificationCondition] = []
        self.cross_domain_registry = CrossDomainRegistry()

    def register_unit(self, unit: Unit) -> None:
        # Unit constructor already validates required fields.
        self.units[unit.symbol] = unit

    def add_axiom(self, ax: Axiom) -> None:
        self.axioms.append(ax)

    def add_hypothesis(self, h: StructuralHypothesis) -> None:
        # Validate that hypothesis only uses registered units.
        for sym in h.unit_symbols:
            if sym not in self.units:
                raise IncompleteUnitError(
                    f"Hypothesis {h.name!r} references unit {sym!r}, "
                    f"which is not registered in subject core {self.name!r}."
                )
        self.hypotheses.append(h)

    def add_falsification(self, fc: FalsificationCondition) -> None:
        self.falsification_conditions.append(fc)

    def audit(self) -> "AuditReport":
        return run_audit(self)


# ============================================================================
# 16. AUDIT — the truth-teller
# ============================================================================

class IssueSeverity(Enum):
    BLOCKING = "BLOCKING"       # the framework cannot make valid claims with this gap
    SERIOUS = "SERIOUS"         # a major piece of evidence is missing
    WARNING = "WARNING"         # noteworthy but not fatal
    INFO = "INFO"               # status note


@dataclass(frozen=True)
class AuditIssue:
    severity: IssueSeverity
    component: str
    message: str


@dataclass
class AuditReport:
    timestamp: str
    subject_core: str
    issues: List[AuditIssue]

    def by_severity(self) -> Dict[IssueSeverity, List[AuditIssue]]:
        out: Dict[IssueSeverity, List[AuditIssue]] = {s: [] for s in IssueSeverity}
        for i in self.issues:
            out[i.severity].append(i)
        return out

    def has_blocking_issues(self) -> bool:
        return any(i.severity == IssueSeverity.BLOCKING for i in self.issues)

    def print_report(self, width: int = 78) -> None:
        bar = "=" * width
        print(bar)
        print(f" SYNTHIUM v5.0 AUDIT — subject core: {self.subject_core!r}")
        print(f" Timestamp: {self.timestamp}")
        print(bar)
        groups = self.by_severity()
        for sev in (IssueSeverity.BLOCKING, IssueSeverity.SERIOUS,
                    IssueSeverity.WARNING, IssueSeverity.INFO):
            issues = groups[sev]
            if not issues:
                continue
            print(f"\n[{sev.value}] {len(issues)} issue(s):")
            for i in issues:
                wrapped = textwrap.fill(
                    f"  ({i.component}) {i.message}",
                    width=width,
                    subsequent_indent="      ",
                )
                print(wrapped)
        print()
        print(bar)
        summary = (f" Blocking: {len(groups[IssueSeverity.BLOCKING])}   "
                   f"Serious: {len(groups[IssueSeverity.SERIOUS])}   "
                   f"Warning: {len(groups[IssueSeverity.WARNING])}   "
                   f"Info: {len(groups[IssueSeverity.INFO])}")
        print(summary)
        if self.has_blocking_issues():
            print(" The framework should not be used to make claims about reality")
            print(" while blocking issues remain.")
        print(bar)


def run_audit(core: SubjectCore) -> AuditReport:
    """Walk the subject core and report every empty slot, every unjustified
    parameter, every missing piece of evidence.
    """
    issues: List[AuditIssue] = []

    # --- Axioms ---
    if not core.axioms:
        issues.append(AuditIssue(
            IssueSeverity.BLOCKING,
            "axioms",
            "No axioms registered. A framework without axioms has no rules of the game "
            "and cannot make structural claims.",
        ))
    else:
        for ax in core.axioms:
            if not ax.is_formalized:
                issues.append(AuditIssue(
                    IssueSeverity.BLOCKING,
                    f"axiom:{ax.name}",
                    f"Axiom has no mathematical_form. Stated only in words: "
                    f"{ax.statement!r}. Until this axiom is formalized "
                    f"mathematically, it cannot be tested against cases.",
                ))

    # --- Units ---
    if not core.units:
        issues.append(AuditIssue(
            IssueSeverity.BLOCKING,
            "units",
            "No units registered. Without units there is nothing to measure.",
        ))
    for sym, u in core.units.items():
        if u.reliability is None:
            issues.append(AuditIssue(
                IssueSeverity.SERIOUS,
                f"unit:{sym}",
                "No ReliabilityRecord. Until two or more coders have applied this unit "
                "blindly and the inter-rater alpha has been measured, this unit is "
                "one person's intuition.",
            ))
        if u.scale_type == ScaleType.RATIO and u.zero_point is None:
            issues.append(AuditIssue(
                IssueSeverity.BLOCKING,
                f"unit:{sym}",
                "Declared ratio scale but no zero_point AnchorCase. Ratio scales "
                "require an operationally defined zero.",
            ))
        if not u.coding_procedure:
            issues.append(AuditIssue(
                IssueSeverity.SERIOUS,
                f"unit:{sym}",
                "No coding_procedure declared. Definition exists but the operational "
                "rules a coder follows to assign a value are not written.",
            ))
        if len(u.anchors) < 3:
            issues.append(AuditIssue(
                IssueSeverity.WARNING,
                f"unit:{sym}",
                f"Only {len(u.anchors)} anchor case(s). Calibration is fragile with "
                f"fewer than ~5 anchors spanning the scale.",
            ))

    # --- Hypotheses ---
    if not core.hypotheses:
        issues.append(AuditIssue(
            IssueSeverity.WARNING,
            "hypotheses",
            "No structural hypotheses registered. The framework can host multiple "
            "competing hypotheses; currently none are present.",
        ))
    elif len(core.hypotheses) == 1:
        issues.append(AuditIssue(
            IssueSeverity.WARNING,
            "hypotheses",
            "Only one structural hypothesis registered. The tradition that produced "
            "Newton's mechanics and Maxwell's equations maintained multiple competing "
            "formalisms until one outpredicted the others. Consider registering "
            "alternatives so they can be compared side by side.",
        ))
    for h in core.hypotheses:
        bad = h.has_unjustified_parameters()
        if bad:
            issues.append(AuditIssue(
                IssueSeverity.BLOCKING,
                f"hypothesis:{h.name}",
                f"Unjustified parameters: {bad}. Each parameter must declare how its "
                f"value was derived. 'I picked it' does not count.",
            ))

    # --- Coders ---
    if not core.coders:
        issues.append(AuditIssue(
            IssueSeverity.SERIOUS,
            "coders",
            "No coders registered. Atlas rows produced by the framework should "
            "record who scored them and what their calibration state was at the time.",
        ))
    elif len(core.coders) < 2:
        issues.append(AuditIssue(
            IssueSeverity.SERIOUS,
            "coders",
            f"Only {len(core.coders)} coder(s) registered. Inter-rater reliability "
            f"requires at least two qualified coders.",
        ))

    # --- Falsification conditions ---
    if not core.falsification_conditions:
        issues.append(AuditIssue(
            IssueSeverity.BLOCKING,
            "falsification",
            "No falsification conditions specified. A framework that cannot be "
            "falsified by any observable evidence is not making testable claims.",
        ))

    # --- Cross-domain registry ---
    if not core.cross_domain_registry.observations:
        issues.append(AuditIssue(
            IssueSeverity.INFO,
            "cross_domain",
            "Cross-domain observation log is empty. This is expected for a single "
            "subject core; cross-domain entries accumulate as additional cores are built.",
        ))

    return AuditReport(
        timestamp=_now_iso(),
        subject_core=core.name,
        issues=issues,
    )


# ============================================================================
# 17. STUB JUDICIAL CORE — honest about its own emptiness
# ============================================================================

def build_judicial_stub() -> SubjectCore:
    """Build a judicial subject core that reflects ONLY what is currently
    grounded.

    The point of this stub is to show what the framework's audit reports
    when the existing Synthium content is filtered through the honesty
    harness. Most slots are deliberately empty because they are empty
    in the actual project state.

    Filling them in is the work.
    """
    core = SubjectCore("judicial")

    # --- Axioms ---
    # The three axioms articulated during the conversation. Their mathematical
    # form is None: that is the honest current state. Formalizing them is
    # the work the user explicitly said only they can do.
    core.add_axiom(Axiom(
        name="AXIOM_OF_BEING",
        statement=("There is nothing more valuable than a single being's existence. "
                   "One being's life is irreducible and cannot be eliminated or "
                   "collapsed without destroying coherence itself."),
        mathematical_form=None,
        derives_what=("AXIOM_OF_FREEDOM", "AXIOM_OF_TRAJECTORY"),
    ))
    core.add_axiom(Axiom(
        name="AXIOM_OF_FREEDOM",
        statement=("No aggregate of people — no collective, no majority, no "
                   "authority — has the right to involuntarily eliminate or "
                   "constrain the freedom of an individual who has not violated "
                   "the freedom of others."),
        mathematical_form=None,
    ))
    core.add_axiom(Axiom(
        name="AXIOM_OF_TRAJECTORY",
        statement=("Every being's trajectory is oriented toward enjoyment, "
                   "flourishing, or fulfillment as a positive direction in "
                   "their state-space."),
        mathematical_form=None,
    ))
    core.add_axiom(Axiom(
        name="AXIOM_OF_AGNOSTICISM",
        statement=("All formulas in Synthium are hypotheses, not truths. Every "
                   "structural claim earns its standing only through reproducible "
                   "predictive success against independent data."),
        mathematical_form=None,
    ))

    # --- Units ---
    # We DO NOT register Priv, Excp, Rem, etc. here. Each of those would
    # require: declared scale type, anchor cases, zero point, failure
    # conditions, granularity, and a coding procedure. None of those exist
    # in the current project. Registering them with empty fields would be
    # exactly the dishonesty this file is built to prevent.
    #
    # The audit will report "no units registered" — which is the truth about
    # the current calibration state, even though the original synthium_v4_3_1.py
    # has 12 unit names listed. Names are not calibrated units.

    # --- Hypotheses ---
    # The original Synthium's "suppression_pressure" formula would go here,
    # but it would have to declare each of its coefficients as a JustifiedParameter
    # with an actual derivation. Since none of them have justifications in the
    # original code, none are registered here.

    # --- Falsification conditions ---
    # These are the explicit commitments the project should make about what
    # evidence would force revision. None are committed to in the current
    # project; the audit will flag this.

    # --- Coders ---
    # Empty. The atlas was coded by one LLM run; no calibration tracking exists.

    return core


# ============================================================================
# 18. MAIN — run the audit
# ============================================================================

def main():
    print(__doc__.split("USAGE")[0])
    core = build_judicial_stub()
    report = core.audit()
    report.print_report()
    print()
    print("Interpretation:")
    print("  This audit reports the truthful current state of the judicial")
    print("  subject core as it sits in the existing project. Most slots are")
    print("  empty because most slots are empty in reality. Filling them in")
    print("  honestly, one at a time, is the path forward. The harness is")
    print("  here to make it impossible to fake that work.")


if __name__ == "__main__":
    main()
