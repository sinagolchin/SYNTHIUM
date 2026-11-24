"""Every restored formula that can be computed on a stage of a case.

The coefficients are copied from the catalogue (``synthium.phenomena.catalogue``) or from
the record's statement, never changed. Where a formula needs a part the stage scores do
not hold, a stand-in is used and named in ``STAND_INS``; that result is weaker than the
formula's own claim and is reported as such.

UNTESTED: none of these has passed a held-out test.
"""

from __future__ import annotations

import math
from typing import Dict, Optional

from ..phenomena.catalogue import computable
from .stages import FIVE, StagedCase


def _clip01(x: float) -> float:
    return max(0.0, min(1.0, x))


def _logistic(z: float) -> float:
    return 1.0 / (1.0 + math.exp(-z))


# Parts a formula needs that the stage scores do not hold directly, and what stands in.
STAND_INS = {
    "R-LOGIT-4": "lawside = lawside_error (0..1, the scorer's reading of how far the claimed error was pure law)",
    "R-LOGIT-V2": "lawside = lawside_error; P_posture = posture_protection",
    "R-LOGIT-V1": "Phi = lawside_error x (1 - posture_protection); case-type risk T set to 1 (not scored)",
    "R1-OMEGA": "E (error clarity) = lawside_error; D (deference) = posture_protection",
    "T1": "only the direction is tested (more protective standard of review, fewer moves); A_j and T_j not fitted",
    "A0": "a claimed error that is mostly fact or credibility (lawside_error < 0.5) is one the reviewer cannot see as well",
    "FEAR-LOSS": "Connection = Love + Obsession (FEAR-PARTS), each scored 0..1, so Connection runs 0..2",
}


def five_d(point: Dict[str, float]) -> Dict[str, float]:
    """Every catalogue formula with a compute function, plus the five-dimension ones whose
    compute needs more than one record (V3-POTENTIAL, V3.4-E-THRESH, V1-COHERENCE, V4-E/M/P)."""
    out = {r.id: float(r.compute(point)) for r in computable()}
    v, R, r, C, S = (point[k] for k in FIVE)
    stress = v * R + S
    if stress > 1.1:
        e_thresh = 0.0
    elif stress > 0.8:
        e_thresh = 0.25 * (1.1 - stress) / 0.3
    else:
        e_thresh = 1 - stress
    out["V3.4-E-THRESH"] = _clip01(e_thresh)
    out["V3-POTENTIAL"] = 2 * (1 - out["V3-E"]) + 1.5 * (1 - out["V3-M"]) + 3 * S + v * R
    out["V1-COHERENCE"] = float(not ((v > 0.9 and R > 0.9) or (S > 0.95 and C < 0.05) or (r > 0.9 and v > 0.9)))
    n = len(FIVE)
    sq = sum(point[k] ** 2 for k in FIVE)
    out["V4-E"] = 1 - sq / (2 * n)
    out["V4-M"] = sq / n
    out["V4-P"] = 1 / (1 + math.sqrt(sq))
    return out


def fear(case: StagedCase, stage: str) -> Optional[Dict[str, float]]:
    """FEAR-LOSS (Claude, Jan 2 2026) with Sina's parts (FEAR-PARTS). Also the same parts
    combined by the other operations, so the form itself can be compared."""
    love = case.get(stage, "fear_connection_love")
    obs = case.get(stage, "fear_connection_obsession")
    poss = case.get(stage, "fear_possibility")
    power = case.get(stage, "fear_powerlessness")
    if None in (poss, power) or (love is None and obs is None):
        return None
    conn = (love or 0.0) + (obs or 0.0)
    return {
        "connection": conn,
        "FEAR-LOSS": conn * poss * power,
        "fear_sum": conn / 2 + poss + power,
        "fear_weakest": min(conn / 2, poss, power),
        "fear_strongest": max(conn / 2, poss, power),
        "fear_love_only": (love or 0.0) * poss * power,
        "fear_obsession_only": (obs or 0.0) * poss * power,
    }


def appeal(case: StagedCase) -> Optional[Dict[str, float]]:
    """The V8 review rulers on a case's appeal stage (stand-ins in ``STAND_INS``)."""
    st = case.stages.get("appeal") or {}
    if not case.present("appeal"):
        return None
    lawside = case.get("appeal", "lawside_error")
    posture = case.get("appeal", "posture_protection")
    apex = st.get("apex")
    if lawside is None or posture is None or apex is None:
        return None
    apex = 1.0 if apex in (True, "true", "yes", 1) else 0.0
    out = {
        "R-LOGIT-4": _logistic(-2.37 + 1.86 * lawside + 0.39 * apex),
        "R-LOGIT-V2": _logistic(-2.17 + 2.56 * lawside + 0.28 * apex - 2.34 * (1 - posture)),
        "R-LOGIT-V1": _logistic(-0.58 + 1.57 * lawside * (1 - posture) + 0.41 * apex),
        "R1-OMEGA": float((lawside - posture) > 0 or lawside >= 0.7),
        "A0": float(lawside >= 0.5),
        "T1-barrier": posture,
    }
    moved = st.get("moved")
    if moved is not None:
        out["moved"] = 1.0 if moved in (True, "true", "yes", 1) else 0.0
    return out


def all_for_stage(case: StagedCase, stage: str) -> Dict[str, float]:
    out: Dict[str, float] = {}
    p = case.point(stage)
    if p is not None:
        out.update(five_d(p))
    f = fear(case, stage)
    if f is not None:
        out.update(f)
    return out
