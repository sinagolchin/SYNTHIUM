"""The Synthium judicial ruler, v3.2 — as working software.

This is the project's core result made executable: three units readable BEFORE a
ruling (Type, Posture, Layer), and a decision rule predicting the outcome notch
(CLEAN_AFFIRM / MODIFIED / REVERSED). Every value here was earned from the blind
register (140 committed-before-reveal cases), not stipulated.

The units:
  T — type: what kind of case (from the caption).
  P — posture: what the court below did (from the record).
  L — layer: what the appellant attacks (from the briefs/claims).

The core empirical law (held in every system probed, 11 jurisdictions):
  FACT-findings are armored; the LEGAL layer is where review-courts move;
  TYPE sets the court's appetite; POSTURE says how much of the case is
  fact-armored.

Honesty ledger (do not remove):
  * v3's committed prospective record: 16/19 correct notches vs baseline 12/19.
  * v3.2's two refinements (pure-law cases just affirm; remedy-as-estimate is
    protected) were induced from attempt 11 — so v3.2's retro-score is partly
    in-sample. Its prospective exam is still owed.
  * Coefficients are Connecticut-derived. Cross-border STRUCTURE is confirmed
    (11 systems); cross-border COEFFICIENTS are untested.
"""

from __future__ import annotations

import csv as _csv
import json
import math
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Optional, Tuple

from ...paths import data_path


class Category(str, Enum):
    CRIMINAL = "criminal"
    HABEAS = "habeas"
    CHILD_PROTECTION = "child_protection"
    ADMIN = "admin"
    FAMILY = "family"
    CIVIL = "civil"


class Posture(str, Enum):
    TRIAL = "trial"                      # full trial, fact-findings made
    DISCRETIONARY = "discretionary"      # default, settlement-enforcement, contempt, award confirmation
    SUMMARY_JUDGMENT = "summary_judgment"  # incl. directed verdict
    DISMISSAL = "dismissal"              # motion to dismiss/strike, sua sponte, finality defects


class Layer(str, Enum):
    FACT = "fact"                        # findings, credibility
    DISCRETION = "discretion"            # ruling reviewed for abuse of discretion (v3.3: protected)
    REMEDY_ESTIMATE = "remedy_estimate"  # damages as factual estimate
    REMEDY_CALCULATION = "remedy_calculation"  # offsets, statutory formulas
    LEGAL_OVERLAY = "legal_overlay"      # separable law riding on fact-findings
    PURE_LAW = "pure_law"                # whole case is a legal question; no fact layer


class CourtLevel(str, Enum):
    INTERMEDIATE = "intermediate"        # mandatory-jurisdiction appeals court (fact-armored)
    APEX = "apex"                        # discretionary supreme/cassation court (law-only-ish)


class Notch(str, Enum):
    CLEAN_AFFIRM = "CLEAN_AFFIRM"
    MODIFIED = "MODIFIED"
    REVERSED = "REVERSED"


# Unit values — frequencies earned from the blind register (in-sample; see docstring).
T_RISK = {
    Category.CRIMINAL: 0.05,
    Category.HABEAS: 0.05,
    Category.CHILD_PROTECTION: 0.05,
    Category.ADMIN: 0.15,
    Category.FAMILY: 0.30,
    Category.CIVIL: 0.35,
}

P_PROTECTION = {
    Posture.TRIAL: 0.9,
    Posture.DISCRETIONARY: 0.7,
    Posture.SUMMARY_JUDGMENT: 0.4,
    Posture.DISMISSAL: 0.3,
}

L_OPENNESS = {
    Layer.FACT: 0.1,
    Layer.DISCRETION: 0.25,
    Layer.REMEDY_ESTIMATE: 0.2,
    Layer.REMEDY_CALCULATION: 0.6,
    Layer.LEGAL_OVERLAY: 0.9,
    Layer.PURE_LAW: 0.9,  # open, but with no fact layer the base rate dominates (rule 4)
}


@dataclass
class Prediction:
    notch: Notch
    high_variance: bool
    rule: str            # which rule fired (for auditability)
    phi: float           # movement potential (interpretive, not the decider)

    def line(self) -> str:
        hv = "  [HIGH-VARIANCE]" if self.high_variance else ""
        return f"{self.notch.value}  (rule: {self.rule}; phi={self.phi:.2f}){hv}"


def movement_potential(cat: Category, posture: Posture, layer: Layer) -> float:
    """Phi = T x L x (1-P): a continuous 'how likely is something to move' score.

    Interpretive companion to the decision rule — NOT what decides. Kept because a
    future, better-fit model will live here, once depth allows real coefficients.
    """
    return T_RISK[cat] * L_OPENNESS[layer] * (1.0 - P_PROTECTION[posture])


def predict(cat: Category, posture: Posture, layer: Layer,
            level: CourtLevel = CourtLevel.INTERMEDIATE) -> Prediction:
    """The v3.2 decision rule. Deterministic, auditable, leak-free by construction
    (all three inputs exist before the ruling)."""
    phi = movement_potential(cat, posture, layer)

    # Rule 1 — type-armor: heavy-deference categories affirm regardless of layer,
    # but v3.3: this holds at INTERMEDIATE courts only. At the apex it leaks (attempt
    # 15: criminal moved 3/8), and even at intermediate it leaks on pure-law
    # statutory-max/illegal-sentence corrections (attempt 16: Coleman) -> flag those.
    if T_RISK[cat] <= 0.05:
        if level is CourtLevel.INTERMEDIATE and layer is not Layer.PURE_LAW:
            return Prediction(Notch.CLEAN_AFFIRM, False, "R1 type-armor (intermediate)", phi)
        return Prediction(Notch.CLEAN_AFFIRM, True, "R1 type-armor (leaky: apex or pure-law)", phi)

    # Rule 2 — fact layer / remedy-as-estimate / abuse-of-discretion rulings armored.
    if layer in (Layer.FACT, Layer.REMEDY_ESTIMATE, Layer.DISCRETION):
        return Prediction(Notch.CLEAN_AFFIRM, False, "R2 fact/discretion-armor", phi)

    # Rule 3 — the star rule: a fact layer exists (trial/discretionary posture)
    # and a separable legal overlay or remedy-calculation is attacked -> the
    # overlay moves while the facts stand.
    if posture in (Posture.TRIAL, Posture.DISCRETIONARY) and layer in (
        Layer.LEGAL_OVERLAY, Layer.REMEDY_CALCULATION
    ):
        return Prediction(Notch.MODIFIED, False, "R3 star: facts stand, overlay moves", phi)

    # Rule 4 — purely legal case: no fact layer to protect; base rate says affirm,
    # but flag it, because this is where variance lives.
    if layer == Layer.PURE_LAW:
        return Prediction(Notch.CLEAN_AFFIRM, True, "R4 pure-law base-rate", phi)

    # Rule 5 — paper posture, no edge yet: base rate, flagged.
    return Prediction(Notch.CLEAN_AFFIRM, True, "R5 paper-zone base-rate", phi)


# ---------------------------------------------------------------------------
# Evaluation against the machine-readable blind register
# ---------------------------------------------------------------------------

@dataclass
class EvalResult:
    n: int
    ruler_exact: int          # exact-notch correctness
    ruler_movement: int       # clean-vs-moved correctness (coarser, fairer grain)
    baseline_exact: int       # always-CLEAN_AFFIRM
    lines: Tuple[str, ...]

    def summary(self) -> str:
        return (
            f"n={self.n} | ruler exact-notch {self.ruler_exact}/{self.n} "
            f"({self.ruler_exact/self.n:.0%}) | ruler movement-grain "
            f"{self.ruler_movement}/{self.n} ({self.ruler_movement/self.n:.0%}) | "
            f"always-affirm baseline {self.baseline_exact}/{self.n} "
            f"({self.baseline_exact/self.n:.0%})"
        )


def evaluate(csv_path: Optional[str] = None) -> EvalResult:
    """Score the ruler on a blind register CSV (default: data/registers/blind_register_v1.csv)."""
    path = csv_path or str(data_path("registers", "blind_register_v1.csv"))
    n = ruler_exact = ruler_move = base_exact = 0
    lines = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in _csv.DictReader(f):
            cat = Category(row["category"]); pos = Posture(row["posture"]); lay = Layer(row["layer"])
            actual = Notch(row["actual_notch"])
            lvl = CourtLevel(row["court_level"]) if row.get("court_level") else CourtLevel.INTERMEDIATE
            pred = predict(cat, pos, lay, lvl)
            n += 1
            exact = pred.notch == actual
            moved_pred = pred.notch != Notch.CLEAN_AFFIRM
            moved_act = actual != Notch.CLEAN_AFFIRM
            movement = moved_pred == moved_act
            base = actual == Notch.CLEAN_AFFIRM
            ruler_exact += exact; ruler_move += movement; base_exact += base
            lines.append(
                f"{row['case'][:28]:28s} {pred.notch.value:13s} vs {actual.value:13s} "
                f"{'exact' if exact else ('move-ok' if movement else 'MISS')}"
            )
    return EvalResult(n, ruler_exact, ruler_move, base_exact, tuple(lines))


# ---------------------------------------------------------------------------
# Fitted movement-probability models (see docs/MATH_CANDIDATES.md)
# Parameters are frozen in params/*.json; nothing here refits them.
# ---------------------------------------------------------------------------

_PARAMS_DIR = Path(__file__).resolve().parent / "params"
_LAW_SIDE = (Layer.REMEDY_CALCULATION, Layer.LEGAL_OVERLAY, Layer.PURE_LAW)


@lru_cache(maxsize=None)
def fitted_params(name: str) -> dict:
    """Load a frozen parameter file from params/, e.g. ``fitted_params_v2``."""
    with open(_PARAMS_DIR / f"{name}.json", encoding="utf-8") as f:
        return json.load(f)


def _logistic(z: float) -> float:
    return 1.0 / (1.0 + math.exp(-z))


def predict_p(layer: Layer, level: CourtLevel = CourtLevel.INTERMEDIATE) -> float:
    """v1 fitted model (grouped logistic, n=71): P(movement) from layer side and court level."""
    fp = fitted_params("fitted_params")
    lawside = 1 if layer in _LAW_SIDE else 0
    apex = 1 if level is CourtLevel.APEX else 0
    return _logistic(fp["a"] + fp["b_lawside"] * lawside + fp["c_apex"] * apex)


def predict_p_v2(layer: Layer, level: CourtLevel, posture: Posture) -> float:
    """v2 fitted model (n=86): adds posture openness (1 - P) as a third feature.

    See docs/MATH_CANDIDATES.md for the honest read on the counter-intuitive
    posture-coefficient sign.
    """
    fp = fitted_params("fitted_params_v2")
    lawside = 1 if layer in _LAW_SIDE else 0
    apex = 1 if level is CourtLevel.APEX else 0
    posture_open = 1.0 - P_PROTECTION[posture]
    return _logistic(fp["a"] + fp["b_lawside"] * lawside + fp["c_apex"] * apex
                     + fp["d_posture_open"] * posture_open)
