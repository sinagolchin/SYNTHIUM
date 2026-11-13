"""Scale types, provenance, and the ``Value`` arithmetic layer.

The foundation of the package:

    Arithmetic ALWAYS runs. Refusal never lives here.

When an operation rests on an assumption the scale type does not license
(multiplying two ordinals, treating a constructed scale as if it were a ratio),
the framework does not raise. It records the assumption in a provenance log that
travels with the result and keeps going. The gate against unjustified *claims*
lives in :mod:`synthium.core.validation`, not in computation.

``all_assumptions()`` is *transitive*: it gathers assumptions from every operand
in the computation graph, so the audit trail of a derived value is complete.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional, Tuple


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ScaleType(Enum):
    """Stevens' typology. A measure's scale type is a *hypothesis* about a newly
    constructed instrument, to be tested -- not a precondition for computing."""

    NOMINAL = "nominal"
    ORDINAL = "ordinal"
    INTERVAL = "interval"
    RATIO = "ratio"


# Which operations a scale type genuinely supports. Used NOT to forbid an
# operation, but to decide whether the result must carry an assumption.
SUPPORTS = {
    ScaleType.NOMINAL: {"=="},
    ScaleType.ORDINAL: {"==", "<", "<=", ">", ">="},
    ScaleType.INTERVAL: {"==", "<", "<=", ">", ">=", "+", "-", "scalar_mul"},
    ScaleType.RATIO: {"==", "<", "<=", ">", ">=", "+", "-", "scalar_mul", "*", "/"},
}


@dataclass(frozen=True)
class Assumption:
    """Something the arithmetic took for granted that the data did not license.

    It is recorded, never raised. The assumption travels with the value, so the audit trail stays complete without
    the gate ever blocking forward motion.
    """

    operation: str
    scale_type: str
    detail: str
    timestamp: str = field(default_factory=_now)


@dataclass(frozen=True)
class Provenance:
    """Where a value came from and what was assumed to get there."""

    origin: str  # "measured" | "stipulated" | "derived"
    derivation: str
    assumptions: Tuple[Assumption, ...] = ()

    def with_assumption(self, a: Assumption) -> "Provenance":
        return Provenance(self.origin, self.derivation, self.assumptions + (a,))


class Value:
    """A number tagged with scale type and provenance. Computes unconditionally.

    Every operation succeeds. If the scale type does not support the operation,
    the result carries an :class:`Assumption` noting it. Nothing is refused at
    this layer -- that is the whole point.
    """

    __slots__ = ("x", "scale", "unit", "prov", "_operands")

    def __init__(self, x: float, scale: ScaleType, unit: str, prov: Provenance,
                 _operands: Tuple["Value", ...] = ()):
        self.x = float(x)
        self.scale = scale
        self.unit = unit
        self.prov = prov
        self._operands = _operands

    # -- helpers ----------------------------------------------------------------

    def _derive(self, x: float, op: str, other: Optional["Value"], note: str) -> "Value":
        prov = Provenance(origin="derived", derivation=note)
        if op not in SUPPORTS[self.scale]:
            prov = prov.with_assumption(Assumption(
                operation=op,
                scale_type=self.scale.value,
                detail=(f"{op!r} is not supported by a {self.scale.value} scale; "
                        f"result assumes the values behave as if they supported it."),
            ))
        unit = self.unit if other is None or other.unit == self.unit else f"{self.unit}.{other.unit}"
        operands = (self,) if other is None else (self, other)
        return Value(x, self.scale, unit, prov, _operands=operands)

    # -- arithmetic (always succeeds) ------------------------------------------

    def __add__(self, o: "Value") -> "Value":
        return self._derive(self.x + o.x, "+", o, f"{self.x:g} + {o.x:g}")

    def __sub__(self, o: "Value") -> "Value":
        return self._derive(self.x - o.x, "-", o, f"{self.x:g} - {o.x:g}")

    def __mul__(self, o: Any) -> "Value":
        if isinstance(o, (int, float)):
            return self._derive(self.x * float(o), "scalar_mul", None, f"{self.x:g} * {o:g}")
        return self._derive(self.x * o.x, "*", o, f"{self.x:g} * {o.x:g}")

    def __truediv__(self, o: Any) -> "Value":
        if isinstance(o, (int, float)):
            return self._derive(self.x / float(o), "scalar_mul", None, f"{self.x:g} / {o:g}")
        return self._derive(self.x / o.x, "/", o, f"{self.x:g} / {o.x:g}")

    # -- audit trail ------------------------------------------------------------

    def own_assumptions(self) -> Tuple[Assumption, ...]:
        """Assumptions logged directly against this value's last operation."""
        return self.prov.assumptions

    def all_assumptions(self) -> Tuple[Assumption, ...]:
        """Every assumption in this value's full computation graph (transitive)."""
        seen: list[Assumption] = list(self.prov.assumptions)
        for operand in self._operands:
            for a in operand.all_assumptions():
                if a not in seen:
                    seen.append(a)
        return tuple(seen)

    def is_grounded(self) -> bool:
        """True iff no assumption anywhere in the derivation was unlicensed."""
        return len(self.all_assumptions()) == 0

    def __repr__(self) -> str:
        n = len(self.all_assumptions())
        return f"Value({self.x:.4g} {self.unit} [{self.scale.value}], assumptions={n})"


def measured(x: float, scale: ScaleType, unit: str, source: str) -> Value:
    """Construct a directly-measured value."""
    return Value(x, scale, unit, Provenance("measured", source))


def stipulated(x: float, scale: ScaleType, unit: str, why: str) -> Value:
    """Construct a stipulated (hand-chosen) value. Honest about its origin."""
    return Value(x, scale, unit, Provenance("stipulated", why))
