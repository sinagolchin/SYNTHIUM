"""What each restored formula predicts, set against what happened in the cases.

Each check turns one record's claim into something the stage scores can show, runs it,
and gives a verdict on these cases only:

- ``holds (on these cases)``: the predicted direction, beyond what shuffled data gives (p < 0.05);
- ``breaks (on these cases)``: the opposite direction beyond chance, or a law with a counter-case;
- ``no signal``: neither;
- ``untestable here``: too few cases, or nothing in a court record can show it.

Every verdict is UNTESTED in Synthium's sense (no held-out cases) and NOT BLIND (the
stage scores were made after every ending was known). A "holds" here can be the scorer's
hindsight; a "breaks" is harder to explain away.
"""

from __future__ import annotations

import re
from datetime import date
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np

from ..phenomena.structure import spearman
from .formulas import all_for_stage, appeal, fear
from .stages import FIVE, STAGES, StagedCase, val

MIN_CASES = 8


# ------------------------------------------------------------------ outcome readers


def amount(x) -> Tuple[Optional[float], str]:
    """``{"v": 78, "unit": "months"}``, ``"78 months"``, ``78`` -> (number, unit)."""
    if x is None:
        return None, ""
    if isinstance(x, dict):
        unit = str(x.get("unit", "") or x.get("why", ""))
        return val(x), unit
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return float(x), ""
    if isinstance(x, str):
        m = re.match(r"\s*\$?(-?[\d,]*\.?\d+)\s*(.*)", x)
        if m:
            try:
                return float(m.group(1).replace(",", "")), m.group(2)
            except ValueError:
                return None, x
    return None, ""


def stage_unit(case: StagedCase, stage: str) -> str:
    s = case.stages.get(stage) or {}
    return str(s.get("unit", "") or "")


def granted(case: StagedCase, stage: str = "sentence_or_remedy") -> Tuple[Optional[float], str]:
    s = case.stages.get(stage) or {}
    n, unit = amount(s.get("granted"))
    return n, (unit or stage_unit(case, stage)).lower()


def months(case: StagedCase) -> Optional[float]:
    n, unit = granted(case)
    return n if (n is not None and "month" in unit) else None


def split_position(case: StagedCase, stage: str = "sentence_or_remedy") -> Optional[float]:
    """p = (granted - accused's ask) / (accuser's ask - accused's ask), when all share a unit."""
    s = case.stages.get(stage) or {}
    g, _ = amount(s.get("granted"))
    a, _ = amount(s.get("ask_accuser"))
    d, _ = amount(s.get("ask_accused"))
    if None in (g, a, d) or a == d:
        return None
    return (g - d) / (a - d)


def final_H(case: StagedCase) -> Optional[float]:
    for st in ("appeal", "sentence_or_remedy", "trial_or_hearing", "plea_or_answer"):
        if case.present(st) and case.get(st, "H_enjoyment") is not None:
            return case.get(st, "H_enjoyment")
    return None


def _date(case: StagedCase, stage: str) -> Optional[date]:
    d = str((case.stages.get(stage) or {}).get("date") or "")
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", d)
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def duration_days(case: StagedCase) -> Optional[float]:
    a, b = _date(case, "filing"), _date(case, "sentence_or_remedy")
    return float((b - a).days) if (a and b and b >= a) else None


def chosen_ending(case: StagedCase) -> Optional[float]:
    """1 when the case ended without a contested merits stage (plea, consent, settlement,
    default), 0 when there was one; None when unknown."""
    s = (case.stages.get("trial_or_hearing") or {}).get("present")
    if s is None or str(s).lower() == "unknown":
        return None
    return 0.0 if str(s).lower() in ("yes", "true") else 1.0


def entry_stage(case: StagedCase) -> Optional[str]:
    """The first stage after the act with a full five-dimension point: filing, or the
    plea/answer when the accused side had not yet responded at filing (R unscored)."""
    for st in ("filing", "plea_or_answer"):
        if case.present(st) and case.point(st) is not None:
            return st
    return None


def has_death(case: StagedCase) -> bool:
    hk = (case.stages.get("act") or {}).get("harm_kind") or []
    if isinstance(hk, str):
        hk = [hk]
    return any("death" in str(h).lower() for h in hk)


# ------------------------------------------------------------------ statistics


def perm_spearman(x: Sequence[float], y: Sequence[float], n_perm: int = 2000, seed: int = 0) -> dict:
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = ~(np.isnan(x) | np.isnan(y))
    x, y = x[ok], y[ok]
    n = len(x)
    if n < 3:
        return {"n": n, "rho": float("nan"), "p": float("nan")}
    rho = spearman(x, y)
    rng = np.random.default_rng(seed)
    null = np.array([spearman(x, rng.permutation(y)) for _ in range(n_perm)])
    p = float((np.sum(np.abs(null) >= abs(rho) - 1e-12) + 1) / (n_perm + 1))
    return {"n": int(n), "rho": float(rho), "p": p}


def sign_test(k_good: int, n: int) -> float:
    """Two-sided binomial p for k_good of n against one half."""
    from math import comb

    if n == 0:
        return float("nan")
    k = min(k_good, n - k_good)
    tail = sum(comb(n, i) for i in range(0, k + 1)) / 2 ** n
    return float(min(1.0, 2 * tail))


def verdict(stat: dict, sign: int) -> str:
    if stat.get("n", 0) < MIN_CASES or not np.isfinite(stat.get("rho", float("nan"))):
        return "untestable here (too few cases)"
    if stat["p"] < 0.05:
        return "holds (on these cases)" if np.sign(stat["rho"]) == sign else "breaks (on these cases)"
    return "no signal"


# ------------------------------------------------------------------ the checks


def _row(rid, records, claim, tested_as, stat, v, note=""):
    return {"id": rid, "records": records, "claim": claim, "tested_as": tested_as,
            "result": stat, "verdict": v, "note": note}


def _corr_check(rid, records, claim, tested_as, xs, ys, sign, note=""):
    stat = perm_spearman(xs, ys)
    return _row(rid, records, claim, tested_as, stat, verdict(stat, sign), note)


def run_checks(cases: List[StagedCase], reading_order: Optional[Dict[str, int]] = None) -> List[dict]:
    out: List[dict] = []
    F = {c.case_id: {st: all_for_stage(c, st) for st in c.present_stages()} for c in cases}

    def f(c, st, key):
        if st == "entry":
            st = entry_stage(c)
            if st is None:
                return np.nan
        return F[c.case_id].get(st, {}).get(key, np.nan)

    sev = [1 - final_H(c) if final_H(c) is not None else np.nan for c in cases]
    dur = [duration_days(c) if duration_days(c) is not None else np.nan for c in cases]
    chosen = [chosen_ending(c) if chosen_ending(c) is not None else np.nan for c in cases]
    h_filing = [c.get(entry_stage(c), "H_enjoyment") if entry_stage(c) else None for c in cases]
    h_loss = [(a - (1 - s)) if (a is not None and np.isfinite(s)) else np.nan for a, s in zip(h_filing, sev)]

    # 1. Collapse risk
    out.append(_corr_check(
        "C01", ["V3.4-COLLAPSE"], "Risk = 0.35 S + 0.25 vR + 0.20 (1 - C) + 0.20 (1 - r) measures how near a system is to collapse",
        "collapse risk of the accused side at entry (filing, or plea/answer if R was unscored at filing) vs how badly the case ended for them (1 - final H)",
        [f(c, "entry", "V3.4-COLLAPSE") for c in cases], sev, +1))

    # 2. Enjoyment formulas vs the scorer's own reading of the accused side's standing
    for rid in ("V3-E", "V3.4-E", "V3.4-E-QUAD", "V3.4-E-INTER", "V3.4-E-THRESH", "V4-E"):
        xs = [f(c, "sentence_or_remedy", rid) for c in cases]
        ys = [c.get("sentence_or_remedy", "H_enjoyment") for c in cases]
        ys = [np.nan if y is None else y for y in ys]
        px, py = [], []
        for c in cases:
            for st in c.present_stages():
                if st != "act" and c.get(st, "H_enjoyment") is not None:
                    px.append(f(c, st, rid))
                    py.append(c.get(st, "H_enjoyment"))
        pooled = perm_spearman(px, py, n_perm=500)
        out.append(_corr_check(
            "C02-" + rid, [rid], "This formula gives a being's enjoyment from (v, R, r, C, S)",
            "formula value at sentence/remedy vs the scored standing H there (one point per case)",
            xs, ys, +1, f"All stages pooled: rho {pooled['rho']:.2f} on {pooled['n']} points (not independent)."))

    # 3. A1-PRIME / SINA-A1: H does not fall along chosen steps
    chosen_steps, imposed_steps = [], []
    for c in cases:
        seq = [(st, c.get(st, "H_enjoyment")) for st in c.present_stages() if st != "act"]
        seq = [(st, h) for st, h in seq if h is not None]
        for (a, ha), (b, hb) in zip(seq, seq[1:]):
            d = hb - ha
            if b == "plea_or_answer" and chosen_ending(c) == 1.0:
                chosen_steps.append(d)
            elif b in ("sentence_or_remedy", "trial_or_hearing"):
                imposed_steps.append(d)
    k = sum(1 for d in chosen_steps if d >= 0)
    n = len(chosen_steps)
    p = sign_test(k, n)
    v = ("untestable here (too few cases)" if n < MIN_CASES else
         "breaks (on these cases)" if (k < n / 2 and p < 0.05) else
         "holds (on these cases)" if (k > n / 2 and p < 0.05) else "no signal")
    out.append(_row("C03", ["A1-PRIME", "SINA-A1", "V5-AXIOMS"],
                    "Along a trajectory a being chooses, enjoyment does not fall (dH/dt >= 0)",
                    "H change from filing to the accused's own plea/consent/settlement, in cases that ended without a contest",
                    {"n": n, "share_not_falling": (k / n if n else float("nan")), "p": p,
                     "imposed_steps_n": len(imposed_steps),
                     "imposed_share_not_falling": (float(np.mean([d >= 0 for d in imposed_steps])) if imposed_steps else float("nan"))},
                    v, "A plea is chosen under threat of a worse imposed outcome, so 'absent constraint' is never met; this is the nearest the record gets."))

    # 4. V3-POTENTIAL: states roll toward low U
    dn = up = 0
    for c in cases:
        seq = [f(c, st, "V3-POTENTIAL") for st in c.present_stages()]
        seq = [u for u in seq if np.isfinite(u)]
        for a, b in zip(seq, seq[1:]):
            if b < a:
                dn += 1
            elif b > a:
                up += 1
    n = dn + up
    p = sign_test(dn, n)
    v = ("untestable here (too few cases)" if n < MIN_CASES else
         "holds (on these cases)" if (dn > up and p < 0.05) else
         "breaks (on these cases)" if (dn < up and p < 0.05) else "no signal")
    out.append(_row("C04", ["V3-POTENTIAL"], "U = 2(1 - E) + 1.5(1 - M) + 3S + vR; systems roll toward low U",
                    "share of stage-to-stage steps (any stage) where U fell",
                    {"n_steps": n, "fell": dn, "rose": up, "p": p}, v))

    # 5. Conservation (V3.4-CONSERVATION): totals over all cases along the common stages
    common = [c for c in cases if all(c.point(st) is not None for st in ("filing", "plea_or_answer", "sentence_or_remedy"))]
    cons = {}
    for key in list(FIVE) + ["V3.4-E", "V3.4-M", "V3.4-P"]:
        totals = []
        for st in ("filing", "plea_or_answer", "sentence_or_remedy"):
            vals = [F[c.case_id][st].get(key) if key in F[c.case_id][st] else c.get(st, key) for c in common]
            totals.append(float(np.nansum(np.asarray(vals, float))))
        mean = np.mean(totals)
        cons[key] = {"totals": totals, "variation": float((max(totals) - min(totals)) / mean) if mean else float("nan")}
    conserved = [k for k, x in cons.items() if x["variation"] < 0.05]
    out.append(_row("C05", ["V3.4-CONSERVATION"], "A quantity is conserved when its total over all beings varies under 5% along a trajectory",
                    "total over the cases scored at filing, plea/answer and sentence/remedy, for each dimension and E, M, P",
                    {"n_cases": len(common), "by_quantity": cons, "conserved": conserved},
                    "untestable here (too few cases)" if len(common) < MIN_CASES else
                    ("holds (on these cases)" if conserved else "breaks (on these cases)"),
                    "Cases are separate beings, not one closed system; conservation was claimed for closed systems."))

    # 6. Coherence law: some combinations cannot exist
    bad = [(c.case_id, st) for c in cases for st in c.present_stages() if F[c.case_id][st].get("V1-COHERENCE") == 0.0]
    npts = sum(1 for c in cases for st in c.present_stages() if "V1-COHERENCE" in F[c.case_id][st])
    out.append(_row("C06", ["V1-COHERENCE"], "Incoherent (cannot exist) if v>0.9 and R>0.9; or S>0.95 and C<0.05; or r>0.9 and v>0.9",
                    "count of real stage points inside the 'impossible' region",
                    {"n_points": npts, "inside": len(bad), "where": bad[:12]},
                    "untestable here (too few cases)" if npts < MIN_CASES else
                    ("breaks (on these cases)" if bad else "holds (on these cases)")))

    # 7. Decay / stability: disorder now, standing falls next
    xs, ys = [], []
    for c in cases:
        st_list = [st for st in c.present_stages() if st != "act"]
        for a, b in zip(st_list, st_list[1:]):
            s, ha, hb = c.get(a, "S"), c.get(a, "H_enjoyment"), c.get(b, "H_enjoyment")
            if None not in (s, ha, hb):
                xs.append(s)
                ys.append(hb - ha)
    out.append(_corr_check("C07", ["V1-DECAY", "V1-STABILITY"], "Disordered phenomena decay; order makes them stable",
                           "entropy S at one stage vs the change in standing H to the next stage", xs, ys, -1))

    # 8-10. Mass, flow, friction, burn
    out.append(_corr_check("C08", ["V1-MASS"], "Mass = R x C: heavy, deep phenomena carry weight (move slowly)",
                           "R x C at entry vs days from filing to sentence/remedy",
                           [f(c, "entry", "V1-MASS") for c in cases], dur, +1))
    out.append(_corr_check("C09", ["V1-FLOW"], "Flow = v^2 / R: fast phenomena with little resistance flow",
                           "flow at entry vs days from filing to sentence/remedy",
                           [f(c, "entry", "V1-FLOW") for c in cases], dur, -1))
    out.append(_corr_check("C10", ["V1-FRICTION", "V2.2-BURN"], "Friction = v x R: fast phenomena against resistance lose energy (burn out)",
                           "v x R at entry vs the fall in standing H from entry to the end",
                           [f(c, "entry", "V1-FRICTION") for c in cases], h_loss, +1))

    # 11. Attraction: resonant sides come together (a chosen ending)
    out.append(_corr_check("C11", ["V1-ATTRACTION"], "Attraction proportional to r^2: resonant phenomena attract",
                           "r^2 at entry vs the case ending without a contest (plea, consent, settlement)",
                           [f(c, "entry", "V1-ATTRACTION") for c in cases], chosen, +1))

    # 12. Fear of loss
    fear_f = [f(c, "filing", "FEAR-LOSS") if c.present("filing") else np.nan for c in cases]
    coop = [c.get("plea_or_answer", "Q15_cooperative") for c in cases]
    coop = [np.nan if x is None else x for x in coop]
    resist = [c.get("plea_or_answer", "R") for c in cases]
    resist = [np.nan if x is None else x for x in resist]
    out.append(_corr_check("C12a", ["FEAR-LOSS", "FEAR-PARTS"], "Fear of Loss = Connection x Possibility x Powerlessness",
                           "fear at filing vs ending without a contest (a frightened accused takes the sure loss)",
                           fear_f, chosen, +1,
                           "Fear itself was never measured in a record; this tests one consequence we read into it, not the formula."))
    out.append(_corr_check("C12b", ["FEAR-LOSS"], "Fear of Loss = Connection x Possibility x Powerlessness",
                           "fear at filing vs resistance R at plea/answer (fear should lower resistance)",
                           fear_f, resist, -1))
    forms = {}
    for key in ("FEAR-LOSS", "fear_sum", "fear_weakest", "fear_strongest", "fear_love_only", "fear_obsession_only"):
        forms[key] = perm_spearman([f(c, "filing", key) for c in cases], chosen)
    out.append(_row("C12c", ["FEAR-LOSS", "G4-ABSORB", "G5-DOMINANCE"],
                    "The parts combine by product (a zero part means no fear)",
                    "each way of combining the fear parts at filing, vs ending without a contest: which form tracks it best",
                    {"forms": forms}, "see forms",
                    "A product beating the sum would support absorption (G4); the strongest part winning would support dominance (G5)."))

    # 13. Interference -> penalty (A2-EMPIRICAL)
    inter = [c.get("act", "interference") for c in cases]
    inter = [np.nan if x is None else x for x in inter]
    out.append(_corr_check("C13a", ["A2-EMPIRICAL", "SINA-A2"], "The penalty grows with how far one party's path crossed another's",
                           "interference of the act vs how badly the case ended for the actor (1 - final H), all cases",
                           inter, sev, +1))
    crim = [i for i, c in enumerate(cases) if months(c) is not None]
    out.append(_corr_check("C13b", ["A2-EMPIRICAL"], "The penalty grows with interference",
                           "interference vs months imposed, cases sentenced in months",
                           [inter[i] for i in crim], [months(cases[i]) for i in crim], +1))

    # 14. Life at the top (A3-LEGAL, SINA-A3)
    d_idx = [i for i, c in enumerate(cases) if has_death(c)]
    o_idx = [i for i, c in enumerate(cases) if not has_death(c)]
    flag = [1.0 if has_death(c) else 0.0 for c in cases]
    stat = perm_spearman(flag, sev)
    stat["mean_severity_death"] = float(np.nanmean([sev[i] for i in d_idx])) if d_idx else float("nan")
    stat["mean_severity_other"] = float(np.nanmean([sev[i] for i in o_idx])) if o_idx else float("nan")
    stat["n_death"] = len(d_idx)
    out.append(_row("C14", ["A3-LEGAL", "SINA-A3"], "Legal systems rank life at or near the top",
                    "cases where a person died vs the rest: how badly the case ended for the actor",
                    stat, verdict(stat, +1),
                    "Many death cases here are negligence (workplace falls, crashes); intent differs, so this mixes two things."))

    # 15. Power explains outcomes (G1-GREENE)
    cap = [c.get("filing", "C") for c in cases]
    cap = [np.nan if x is None else x for x in cap]
    out.append(_corr_check("C15", ["G1-GREENE"], "Power explains outcomes",
                           "the accused side's capacity C at filing vs how badly the case ended for them",
                           cap, sev, -1))

    # 16. Review rulers on appeal stages
    rows = [appeal(c) for c in cases]
    rows = [r for r in rows if r and "moved" in r]
    rres = {"n": len(rows), "moved": int(sum(r["moved"] for r in rows))}
    if rows:
        base = float(np.mean([r["moved"] for r in rows]))
        rres["brier_base_rate"] = float(np.mean([(base - r["moved"]) ** 2 for r in rows]))
        for key in ("R-LOGIT-4", "R-LOGIT-V2", "R-LOGIT-V1", "R1-OMEGA", "A0"):
            rres[key + "_brier"] = float(np.mean([(r[key] - r["moved"]) ** 2 for r in rows]))
        rres["T1_direction"] = perm_spearman([r["T1-barrier"] for r in rows], [r["moved"] for r in rows])
    out.append(_row("C16", ["R-LOGIT-4", "R-LOGIT-V2", "R-LOGIT-V1", "R1-OMEGA", "A0", "T1", "GATES-PRODUCT"],
                    "The V8 review rulers give the chance a decision is moved on review",
                    "predicted chance vs whether the appeal moved the decision (Brier; lower is better than the base rate)",
                    rres, "untestable here (too few cases)" if len(rows) < MIN_CASES else "see Brier scores"))

    # 17. Drift by reading order, now that each stage was re-scored by several scorers
    if reading_order:
        for key, st in (("Q33_motivation_strength", "act"), ("Q16_blame_shifting_defendant", "plea_or_answer"),
                        ("Q24_lenient", "sentence_or_remedy")):
            xs = [reading_order.get(c.case_id, np.nan) for c in cases]
            ys = [c.get(st, key) for c in cases]
            ys = [np.nan if y is None else y for y in ys]
            stat = perm_spearman(xs, ys)
            out.append(_row("C17-" + key, ["GEOMETRY"], "First run: this quality drifted with the order the cases were first read",
                            f"re-scored {key} at {st} vs the original reading order", stat,
                            "drift still there" if (stat["n"] >= MIN_CASES and stat["p"] < 0.05) else
                            ("untestable here (too few cases)" if stat["n"] < MIN_CASES else "drift gone"),
                            "If the drift is gone, it came from the first scoring, not from the cases."))
    return out


def quality_motion(cases: List[StagedCase]) -> Dict[str, dict]:
    """For every quality scored at two or more stages of a case: how much it moved."""
    keys = sorted({k for c in cases for k in c.quality_keys()})
    out = {}
    for k in keys:
        moves, n_cases, by_stage = [], 0, {st: [] for st in STAGES}
        for c in cases:
            seq = [(st, c.get(st, k)) for st in c.present_stages()]
            seq = [(st, x) for st, x in seq if x is not None]
            for st, x in seq:
                by_stage[st].append(x)
            if len(seq) >= 2:
                n_cases += 1
                moves.append(max(x for _, x in seq) - min(x for _, x in seq))
        if n_cases:
            out[k] = {
                "cases_with_2plus_stages": n_cases,
                "mean_range": float(np.mean(moves)),
                "share_that_moved": float(np.mean([m > 0 for m in moves])),
                "mean_by_stage": {st: (float(np.mean(v)) if v else None) for st, v in by_stage.items()},
            }
    return out


def scorer_agreement(calibration: List[StagedCase], everyone: List[StagedCase]) -> dict:
    """Spread of the same case (KIM-2019) across scorers, next to the spread across cases."""
    keys = list(FIVE) + ["fear_connection_love", "fear_connection_obsession", "fear_possibility",
                         "fear_powerlessness", "H_enjoyment", "Q14_remorseful", "Q15_cooperative",
                         "Q33_motivation_strength"]
    res = {"scorers": [c.scorer for c in calibration], "fields": {}}
    within, between = [], []
    for st in STAGES:
        for k in keys:
            xs = [c.get(st, k) for c in calibration if c.present(st)]
            xs = [x for x in xs if x is not None]
            ys = [c.get(st, k) for c in everyone if c.present(st)]
            ys = [y for y in ys if y is not None]
            if len(xs) >= 3 and len(ys) >= MIN_CASES:
                w, b = float(np.std(xs)), float(np.std(ys))
                res["fields"][f"{st}.{k}"] = {"n_scorers": len(xs), "sd_same_case": w, "sd_across_cases": b,
                                              "values": xs}
                within.append(w)
                between.append(b)
    if within:
        res["median_sd_same_case"] = float(np.median(within))
        res["median_sd_across_cases"] = float(np.median(between))
        res["noise_share"] = float(np.median(np.asarray(within) / np.maximum(between, 1e-9)))
    return res


def compare_with_first_reading(cases: List[StagedCase], first: Dict[str, Dict[str, float]]) -> Dict[str, dict]:
    """Original whole-case value vs the new stage values (highest across stages)."""
    out = {}
    keys = sorted({k for row in first.values() for k in row})
    for k in keys:
        xs, ys = [], []
        for c in cases:
            a = first.get(c.case_id, {}).get(k)
            vals = [c.get(st, k) for st in c.present_stages()]
            vals = [v for v in vals if v is not None]
            if a is not None and vals:
                xs.append(a)
                ys.append(max(vals))
        if len(xs) >= MIN_CASES:
            out[k] = {**perm_spearman(xs, ys, n_perm=500),
                      "mean_abs_diff": float(np.mean(np.abs(np.asarray(xs) - np.asarray(ys))))}
    return out
