"""Generative axioms -- the friction surface, with mathematical form.

Every prior axiom in Synthium's history had ``mathematical_form = None``: a
sentence that could be nodded at but never violated. The axioms here are the
opposite. Each carries a mathematical form and a ``test(dataset)`` that returns
SATISFIED, VIOLATED, or an honest "cannot test on this data" -- so the data is
free to say no. An axiom that cannot fail generates nothing.

These are the project's generative axioms. They do NOT
replace the epistemic axioms (agnosticism, proposed-until-proven, no-leakage);
those govern how claims are made. These govern what structure is forced.

Status vocabulary, kept deliberately honest:
  SATISFIED            no violation found, with non-trivial coverage
  VIOLATED             a counterexample exists -> the axiom is false on this data
  INSUFFICIENT_DATA    the data cannot exercise the axiom (e.g. no zero cases)
  REQUIRES_COMMITMENT  needs a modeling choice the user must make first
  REQUIRES_PAIRWISE    needs pairwise human judgments the data does not contain
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional, Sequence, Tuple


class AxiomStatus(Enum):
    SATISFIED = "SATISFIED"
    VIOLATED = "VIOLATED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    REQUIRES_COMMITMENT = "REQUIRES_COMMITMENT"
    REQUIRES_PAIRWISE = "REQUIRES_PAIRWISE_DATA"


@dataclass
class AxiomResult:
    status: AxiomStatus
    detail: str
    coverage: float = 0.0                 # fraction of the axiom actually exercised
    violations: List[str] = field(default_factory=list)
    stats: Dict[str, float] = field(default_factory=dict)

    def line(self, name: str) -> str:
        cov = f" cov={self.coverage:.0%}" if self.coverage else ""
        nv = f" violations={len(self.violations)}" if self.violations else ""
        return f"[{self.status.value:18s}] {name}{cov}{nv} -- {self.detail}"


@dataclass
class AxiomCase:
    """One case as the axioms see it: dimensions plus an ordering proxy."""

    case_id: str
    dimensions: Dict[str, float]
    outcome: str
    outcome_rank: Optional[float]   # numeric proxy for the empirical ordering, or None


# ---------------------------------------------------------------------------
# Axiom base
# ---------------------------------------------------------------------------

@dataclass
class Axiom:
    name: str
    statement: str
    mathematical_form: str          # NOT None -- that is the whole point
    generative: bool                # does it constrain units/formulas, or only claims?
    test_fn: Callable[[Sequence[AxiomCase]], AxiomResult]

    def test(self, dataset: Sequence[AxiomCase]) -> AxiomResult:
        return self.test_fn(dataset)


# ---------------------------------------------------------------------------
# Small stdlib stats
# ---------------------------------------------------------------------------

def _pearson(xs: Sequence[float], ys: Sequence[float]) -> Optional[float]:
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return None
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return sxy / math.sqrt(sxx * syy)


def _quantile_levels(values: Sequence[float], n_levels: int) -> List[int]:
    """Assign each value a level 0..n_levels-1 by rank (equal-frequency bins)."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    levels = [0] * len(values)
    for rank, idx in enumerate(order):
        levels[idx] = min(n_levels - 1, rank * n_levels // len(values))
    return levels


# ---------------------------------------------------------------------------
# Axiom 1 -- Weak order
# ---------------------------------------------------------------------------

def _test_weak_order(ds: Sequence[AxiomCase]) -> AxiomResult:
    ranked = [c for c in ds if c.outcome_rank is not None]
    if not ranked:
        return AxiomResult(AxiomStatus.INSUFFICIENT_DATA,
                           "no cases carry an ordering value.")
    distinct = len(set(c.outcome_rank for c in ranked))
    if distinct <= 2:
        return AxiomResult(
            AxiomStatus.REQUIRES_PAIRWISE,
            (f"the only ordering available is the {distinct}-level outcome; "
             "transitivity is vacuous without pairwise human comparisons. "
             "Weak order becomes richly testable once cases are ranked, not just "
             "labeled granted/denied."),
            coverage=0.0,
        )
    # A real-valued rank is automatically a weak order; report it as trivially held.
    return AxiomResult(AxiomStatus.SATISFIED,
                       f"ordering over {len(ranked)} cases is a weak order "
                       f"({distinct} distinct ranks).", coverage=1.0)


# ---------------------------------------------------------------------------
# Axiom 3 -- Double cancellation (additive conjoint)
# ---------------------------------------------------------------------------

def make_double_cancellation(dim_a: str, dim_b: str, n_levels: int = 3) -> Axiom:
    def _test(ds: Sequence[AxiomCase]) -> AxiomResult:
        cases = [c for c in ds if c.outcome_rank is not None
                 and dim_a in c.dimensions and dim_b in c.dimensions]
        if len(cases) < n_levels * n_levels:
            return AxiomResult(AxiomStatus.INSUFFICIENT_DATA,
                               f"{len(cases)} usable cases for a "
                               f"{n_levels}x{n_levels} grid on ({dim_a},{dim_b}).")
        la = _quantile_levels([c.dimensions[dim_a] for c in cases], n_levels)
        lb = _quantile_levels([c.dimensions[dim_b] for c in cases], n_levels)
        # cell score = mean outcome rank
        cell: Dict[Tuple[int, int], List[float]] = {}
        for c, a, b in zip(cases, la, lb):
            cell.setdefault((a, b), []).append(c.outcome_rank)  # type: ignore[arg-type]
        score = {k: sum(v) / len(v) for k, v in cell.items()}
        filled = len(score)
        coverage = filled / (n_levels * n_levels)

        def ge(p: Tuple[int, int], q: Tuple[int, int]) -> Optional[bool]:
            if p not in score or q not in score:
                return None
            return score[p] >= score[q]

        testable = 0
        violations: List[str] = []
        idx = range(n_levels)
        for a1, a2, a3 in itertools.permutations(idx, 3):
            for b1, b2, b3 in itertools.permutations(idx, 3):
                ante1 = ge((a1, b2), (a2, b1))
                ante2 = ge((a2, b3), (a3, b2))
                cons = ge((a1, b3), (a3, b1))
                if ante1 and ante2 and cons is not None:
                    testable += 1
                    if not cons:
                        violations.append(
                            f"({dim_a}{a1},{dim_b}b3)>=({dim_a}a3,{dim_b}b1) failed "
                            f"given the two antecedents")
        if testable == 0:
            return AxiomResult(AxiomStatus.INSUFFICIENT_DATA,
                               f"grid too sparse: {filled}/{n_levels**2} cells "
                               f"filled, 0 testable triples.", coverage=coverage)
        status = AxiomStatus.VIOLATED if violations else AxiomStatus.SATISFIED
        return AxiomResult(status,
                           f"({dim_a},{dim_b}): {testable} testable triples, "
                           f"{len(violations)} violations.",
                           coverage=coverage,
                           violations=violations[:5],
                           stats={"testable_triples": testable, "cells_filled": filled})

    return Axiom(
        name=f"double_cancellation[{dim_a}x{dim_b}]",
        statement=("Consistent trade-offs between two dimensions force an additive "
                   "interval representation of both."),
        mathematical_form=("(a1,b2)>=(a2,b1) and (a2,b3)>=(a3,b2)  =>  (a1,b3)>=(a3,b1)"),
        generative=True,
        test_fn=_test,
    )


# ---------------------------------------------------------------------------
# Axiom 4 -- Multiplicative zero (absorption)
# ---------------------------------------------------------------------------

def make_absorption(factor_dim: str, active_outcome: str, eps: float = 1e-6,
                    near: float | None = None) -> Axiom:
    """Absorption: factor_dim ~ 0 should preclude the active outcome.

    `near` widens the zero band from literal `eps` to a small magnitude (e.g.
    0.12), because a rubric whose floor for 'no privacy interest' is ~0.05 never
    emits literal zeros -- testing only at eps would leave the axiom permanently
    unexercised. `near` makes 'negligible privacy' testable honestly.
    """
    band = near if near is not None else eps

    def _test(ds: Sequence[AxiomCase]) -> AxiomResult:
        zero_cases = [c for c in ds if c.dimensions.get(factor_dim, 1.0) <= band]
        if not zero_cases:
            return AxiomResult(
                AxiomStatus.INSUFFICIENT_DATA,
                (f"no case has {factor_dim} ~ 0, so absorption on {factor_dim} "
                 f"cannot be exercised. To test it, code cases with a genuinely "
                 f"absent {factor_dim}."),
                coverage=0.0)
        violators = [c.case_id for c in zero_cases if c.outcome == active_outcome]
        coverage = len(zero_cases) / len(ds)
        if violators:
            return AxiomResult(
                AxiomStatus.VIOLATED,
                (f"{len(violators)} case(s) have {factor_dim}~0 yet outcome="
                 f"{active_outcome}; {factor_dim} is not an absorbing factor."),
                coverage=coverage, violations=violators[:5])
        return AxiomResult(
            AxiomStatus.SATISFIED,
            (f"all {len(zero_cases)} cases with {factor_dim}~0 avoid "
             f"'{active_outcome}'. Consistent with {factor_dim} absorbing."),
            coverage=coverage)

    return Axiom(
        name=f"absorption[{factor_dim}]",
        statement=(f"If {factor_dim} is zero, the derived quantity is zero "
                   "regardless of the other dimensions."),
        mathematical_form=f"{factor_dim} = 0  =>  outcome != {active_outcome}",
        generative=True,
        test_fn=_test,
    )


# ---------------------------------------------------------------------------
# Axiom 5 -- Dominance (limiting / weakest-or-strongest link)
# ---------------------------------------------------------------------------

def make_dominance(trigger_dim: str, forced_outcome: str, threshold: float = 0.5) -> Axiom:
    def _test(ds: Sequence[AxiomCase]) -> AxiomResult:
        fired = [c for c in ds if c.dimensions.get(trigger_dim, 0.0) > threshold]
        if not fired:
            return AxiomResult(AxiomStatus.INSUFFICIENT_DATA,
                               f"no case has {trigger_dim} > {threshold}.")
        violators = [c.case_id for c in fired if c.outcome != forced_outcome]
        coverage = len(fired) / len(ds)
        if violators:
            return AxiomResult(
                AxiomStatus.VIOLATED,
                (f"{len(violators)}/{len(fired)} cases fire {trigger_dim} but "
                 f"outcome != {forced_outcome}; it does not dominate."),
                coverage=coverage, violations=violators[:5])
        return AxiomResult(
            AxiomStatus.SATISFIED,
            (f"all {len(fired)} cases firing {trigger_dim} resolve to "
             f"{forced_outcome}; consistent with dominance."),
            coverage=coverage)

    return Axiom(
        name=f"dominance[{trigger_dim}]",
        statement=(f"When {trigger_dim} is high, it dictates the outcome; the "
                   "other dimensions cannot override it."),
        mathematical_form=f"{trigger_dim} > t  =>  outcome = {forced_outcome}",
        generative=True,
        test_fn=_test,
    )


# ---------------------------------------------------------------------------
# Axiom 8 -- Independence of basis (no dimension is a mix of the others)
# ---------------------------------------------------------------------------

def make_independence(dims: Sequence[str], strong: float = 0.9,
                      moderate: float = 0.8) -> Axiom:
    def _test(ds: Sequence[AxiomCase]) -> AxiomResult:
        cols = {d: [c.dimensions[d] for c in ds if d in c.dimensions] for d in dims}
        cols = {d: v for d, v in cols.items() if len(set(v)) > 1}  # drop constants
        usable = list(cols)
        if len(usable) < 2:
            return AxiomResult(AxiomStatus.INSUFFICIENT_DATA,
                               "fewer than two non-constant dimensions.")
        strong_pairs: List[str] = []
        mod_pairs: List[str] = []
        worst = 0.0
        for a, b in itertools.combinations(usable, 2):
            r = _pearson(cols[a], cols[b])
            if r is None:
                continue
            worst = max(worst, abs(r))
            if abs(r) >= strong:
                strong_pairs.append(f"{a}~{b} r={r:+.2f}")
            elif abs(r) >= moderate:
                mod_pairs.append(f"{a}~{b} r={r:+.2f}")
        if strong_pairs:
            return AxiomResult(
                AxiomStatus.VIOLATED,
                (f"{len(strong_pairs)} pair(s) near-collinear (|r|>={strong}); "
                 "at least one dimension is redundant, not basis."),
                coverage=1.0, violations=strong_pairs,
                stats={"max_abs_r": worst, "moderate_pairs": float(len(mod_pairs))})
        return AxiomResult(
            AxiomStatus.SATISFIED,
            (f"no pair exceeds |r|={strong} (worst {worst:.2f}); "
             f"{len(mod_pairs)} moderately correlated pair(s) to watch."),
            coverage=1.0, violations=mod_pairs,
            stats={"max_abs_r": worst})

    return Axiom(
        name="independence_of_basis",
        statement="Each base dimension is not expressible as a combination of the others.",
        mathematical_form="rank(D) = #dimensions  (here: pairwise |r| < threshold as a screen)",
        generative=True,
        test_fn=_test,
    )


# ---------------------------------------------------------------------------
# Axioms 7, 9, 10 -- declared, not yet data-testable (honest scaffolding)
# ---------------------------------------------------------------------------

def _requires_commitment(msg: str):
    def _t(_ds: Sequence[AxiomCase]) -> AxiomResult:
        return AxiomResult(AxiomStatus.REQUIRES_COMMITMENT, msg)
    return _t


DIMENSIONAL_HOMOGENEITY = Axiom(
    name="dimensional_homogeneity",
    statement="Only quantities of the same dimension may be added; laws must balance dimensionally.",
    mathematical_form="[lhs] = [rhs] for every additive term",
    generative=True,
    test_fn=_requires_commitment(
        "Requires first fixing the base dimensions and the combination operation "
        "(adopt absorption/multiplicative structure). Then most writable formulas "
        "are ruled out before any data."),
)

BOUNDARY_EQUILIBRIUM = Axiom(
    name="boundary_equilibrium",
    statement="Court-flagged 'close' cases sit exactly on the decision threshold.",
    mathematical_form="balance(case) = threshold  for each boundary case  ->  solve for coefficients",
    generative=True,
    test_fn=_requires_commitment(
        "Requires (1) a committed conserved 'currency' and (2) a list of cases the "
        "court itself flagged as on the line. Then the boundary cases form a linear "
        "system that SOLVES for the coefficients instead of fitting them."),
)

INVARIANCE_CONSERVATION = Axiom(
    name="invariance_conservation",
    statement="The balance law is the shadow of a transformation that leaves the structure invariant.",
    mathematical_form="symmetry S of the structure  =>  conserved quantity Q  (Noether-style discipline)",
    generative=True,
    test_fn=_requires_commitment(
        "The horizon axiom. Requires naming the symmetry of the privacy structure "
        "that the balance law conserves. Hold until a balance law survives."),
)
