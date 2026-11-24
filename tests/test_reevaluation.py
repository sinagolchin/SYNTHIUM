"""Stage-by-stage re-evaluation: loading, formulas and checks on a synthetic fixture."""

import json
import os

import numpy as np

from synthium.reevaluation import load_staged, run_checks, all_for_stage, appeal, fear
from synthium.reevaluation.analyses import entry_stage, chosen_ending, duration_days, final_H
from synthium.reevaluation.geometry_on_stages import path_order_test


def _cell(v):
    return {"v": v, "tag": "FOUND", "why": "synthetic"}


def _case(i, rng):
    stages = []
    names = ["act", "filing", "plea_or_answer", "trial_or_hearing", "sentence_or_remedy", "appeal"]
    for j, st in enumerate(names):
        present = "yes"
        if st == "trial_or_hearing":
            present = "no" if i % 2 else "yes"
        if st == "appeal":
            present = "yes" if i % 3 == 0 else "no"
        s = {"stage": st, "present": present, "date": f"2020-0{1 + j}-1{j}"}
        for k in ("v", "R", "r", "C", "S"):
            s[k] = _cell(float(rng.uniform(0.05, 0.95)))
        if st == "filing" and i % 4 == 0:
            s["R"] = {"v": None, "why": "not yet responded"}
        for k in ("fear_connection_love", "fear_connection_obsession", "fear_possibility",
                  "fear_powerlessness", "H_enjoyment", "interference"):
            s[k] = _cell(float(rng.uniform(0, 1)))
        s["Q"] = {"Q33_motivation_strength": _cell(float(rng.uniform(0, 1)))}
        if st == "appeal":
            s.update({"moved": bool(i % 2), "apex": False,
                      "lawside_error": _cell(0.6), "posture_protection": _cell(0.4)})
        stages.append(s)
    return {"case_id": f"T{i:02d}", "case_type": "criminal", "scorer": "test", "stages": stages,
            "missing": [], "notes": ""}


def _fixture(tmp_path, n=20):
    rng = np.random.default_rng(1)
    for i in range(n):
        with open(os.path.join(tmp_path, f"T{i:02d}.json"), "w") as fh:
            json.dump(_case(i, rng), fh)
    return load_staged(str(tmp_path))


def test_load_and_entry_stage(tmp_path):
    cases = _fixture(tmp_path)
    assert len(cases) == 20
    c0 = cases[0]
    assert c0.point("filing") is None            # R unscored at filing
    assert entry_stage(c0) == "plea_or_answer"   # falls back to the first response
    assert entry_stage(cases[1]) == "filing"
    assert chosen_ending(cases[1]) == 1.0 and chosen_ending(cases[0]) == 0.0
    assert duration_days(c0) is not None and final_H(c0) is not None


def test_formulas_compute(tmp_path):
    cases = _fixture(tmp_path)
    vals = all_for_stage(cases[1], "filing")
    for k in ("V3-E", "V4-E", "V3-POTENTIAL", "V1-COHERENCE", "FEAR-LOSS"):
        assert k in vals and np.isfinite(vals[k])
    f = fear(cases[1], "filing")
    assert abs(f["FEAR-LOSS"] - f["connection"] * cases[1].get("filing", "fear_possibility")
               * cases[1].get("filing", "fear_powerlessness")) < 1e-9
    a = appeal(cases[0])
    assert a is not None and 0 < a["R-LOGIT-4"] < 1


def test_checks_run_and_label(tmp_path):
    cases = _fixture(tmp_path)
    checks = run_checks(cases, {c.case_id: i for i, c in enumerate(cases)})
    ids = {c["id"] for c in checks}
    assert {"C01", "C06", "C08", "C12a"} <= ids
    for c in checks:
        assert c["verdict"] in ("holds (on these cases)", "breaks (on these cases)", "no signal",
                                "untestable here (too few cases)", "see forms",
                                "drift still there", "drift gone")


def test_path_order(tmp_path):
    cases = _fixture(tmp_path)
    out = path_order_test(cases, n_perm=50)
    assert out["tested"] and out["n_cases"] == 20
