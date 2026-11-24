"""Position, rate and acceleration of each quality across the stages of a case.

Sina, Nov 24: "Calculating speed is different than acceleration. But they are related.
Acceleration is referring to speed changes ... It's like we are trying to find math behind
the thing that exists. Just like Newton did."

So, for every quality (and every dimension) scored at a stage of a case:

- position      x at the stage
- rate          d = x(next stage) - x(this stage), per stage step
- acceleration  a = d(next step) - d(this step)

Questions asked of all cases together:

1. Rate: across cases, does a quality move the same way on the same step (e.g. remorse
   rising from plea to sentence)? Sign test per step, corrected for the number of tests.
2. Acceleration: on the same pair of steps, does the rate itself change the same way?
3. Momentum: once a quality moves, does it keep moving the same way on the next step,
   or turn back? Compared against the same case's values put in shuffled stage order,
   because pure noise alone makes a step up tend to be followed by a step down.
4. What goes with the rate of standing H (the "force" question): which positions at the
   start of a step go with H rising or falling over it. Exploratory: steps of one case are
   not independent.

Rates are per stage step, not per day: stages are unevenly spaced in time. Untested and not
blind: the stage scores were made after every ending was known.
"""

from __future__ import annotations

from typing import Dict, List, Sequence

import numpy as np

from .analyses import perm_spearman
from .stages import FEAR, FIVE, STAGES, StagedCase

MIN_CASES = 8


def _sign_p(k: int, n: int) -> float:
    from math import comb

    if n == 0:
        return float("nan")
    k = min(k, n - k)
    return float(min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n))


def bh(ps: Sequence[float]) -> List[float]:
    """Benjamini-Hochberg q-values (share of false finds expected among those kept)."""
    ps = np.asarray(ps, float)
    n = len(ps)
    if n == 0:
        return []
    order = np.argsort(ps)
    q = np.empty(n)
    run = 1.0
    for rank, i in reversed(list(enumerate(order, start=1))):
        run = min(run, ps[i] * n / rank)
        q[i] = run
    return [float(x) for x in q]


def _sequence(c: StagedCase, key: str):
    seq = [(st, c.get(st, key)) for st in c.present_stages()]
    return [(st, x) for st, x in seq if x is not None]


def _momentum(cases: Sequence[StagedCase], key: str, n_perm: int, rng) -> dict:
    """Correlation of one step's rate with the next step's, real stage order vs shuffled."""
    seqs = [np.array([x for _, x in _sequence(c, key)]) for c in cases]
    seqs = [s for s in seqs if len(s) >= 3]

    def pairs(ss):
        a, b = [], []
        for s in ss:
            d = np.diff(s)
            a.extend(d[:-1])
            b.extend(d[1:])
        return np.array(a), np.array(b)

    d1, d2 = pairs(seqs)
    moving = (d1 != 0) & (d2 != 0)
    if len(seqs) < MIN_CASES or moving.sum() < MIN_CASES:
        return {"tested": False, "n_cases": len(seqs), "n_moving_pairs": int(moving.sum())}
    same_real = float(np.mean(np.sign(d1[moving]) == np.sign(d2[moving])))
    null = []
    for _ in range(n_perm):
        a, b = pairs([rng.permutation(s) for s in seqs])
        m = (a != 0) & (b != 0)
        if m.sum():
            null.append(np.mean(np.sign(a[m]) == np.sign(b[m])))
    null = np.array(null)
    p = float((np.sum(np.abs(null - null.mean()) >= abs(same_real - null.mean())) + 1) / (len(null) + 1))
    return {
        "tested": True,
        "n_cases": len(seqs),
        "n_moving_pairs": int(moving.sum()),
        "share_keep_direction": same_real,
        "share_keep_direction_shuffled": float(null.mean()),
        "p": p,
        "reading": ("keeps moving the same way (momentum)" if same_real > null.mean() else
                    "turns back more than shuffled order (pull back)"),
    }


def motion(cases: Sequence[StagedCase], keys: Sequence[str] = None, n_perm: int = 300, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    if keys is None:
        qk = sorted({k for c in cases for k in c.quality_keys()})
        keys = list(FIVE) + list(FEAR) + ["H_enjoyment", "interference"] + qk

    rate_tests, acc_tests, per_key = [], [], {}
    for key in keys:
        steps: Dict[str, List[float]] = {}
        triples: Dict[str, List[float]] = {}
        all_rates = []
        for c in cases:
            seq = _sequence(c, key)
            for (s1, x1), (s2, x2) in zip(seq, seq[1:]):
                steps.setdefault(f"{s1} -> {s2}", []).append(x2 - x1)
                all_rates.append(x2 - x1)
            for (s1, x1), (s2, x2), (s3, x3) in zip(seq, seq[1:], seq[2:]):
                triples.setdefault(f"{s1} -> {s2} -> {s3}", []).append((x3 - x2) - (x2 - x1))
        if not all_rates:
            continue
        for name, ds in steps.items():
            up, down = sum(d > 0 for d in ds), sum(d < 0 for d in ds)
            if up + down >= MIN_CASES:
                rate_tests.append({"key": key, "step": name, "n_cases": len(ds), "up": up, "down": down,
                                   "flat": len(ds) - up - down, "mean_rate": float(np.mean(ds)),
                                   "p": _sign_p(up, up + down)})
        for name, accs in triples.items():
            up, down = sum(a > 0 for a in accs), sum(a < 0 for a in accs)
            if up + down >= MIN_CASES:
                acc_tests.append({"key": key, "steps": name, "n_cases": len(accs), "speeding_up": up,
                                  "slowing_down": down, "mean_acceleration": float(np.mean(accs)),
                                  "p": _sign_p(up, up + down)})
        per_key[key] = {
            "n_steps": len(all_rates),
            "share_steps_moving": float(np.mean([d != 0 for d in all_rates])),
            "mean_abs_rate": float(np.mean(np.abs(all_rates))),
            "momentum": _momentum(cases, key, n_perm, rng),
        }

    for tests in (rate_tests, acc_tests):
        for t, q in zip(tests, bh([t["p"] for t in tests])):
            t["q"] = q
        tests.sort(key=lambda t: t["p"])
    mom = [(k, v["momentum"]) for k, v in per_key.items() if v["momentum"].get("tested")]
    for (k, m), q in zip(mom, bh([m["p"] for _, m in mom])):
        m["q"] = q

    return {
        "rate_tests": rate_tests,
        "acceleration_tests": acc_tests,
        "per_key": per_key,
        "force_on_H": force_on(cases, "H_enjoyment", keys),
        "n_rate_tests": len(rate_tests),
        "n_acceleration_tests": len(acc_tests),
    }


def force_on(cases: Sequence[StagedCase], target: str, keys: Sequence[str], min_steps: int = 15) -> List[dict]:
    """Rate of ``target`` over a step vs each key's position at the start of that step.
    Exploratory: steps of the same case are not independent, so p is only a guide."""
    out = []
    for key in keys:
        if key == target:
            continue
        xs, ds = [], []
        for c in cases:
            seq = [st for st in c.present_stages()]
            for s1, s2 in zip(seq, seq[1:]):
                h1, h2, x = c.get(s1, target), c.get(s2, target), c.get(s1, key)
                if None not in (h1, h2, x):
                    xs.append(x)
                    ds.append(h2 - h1)
        if len(xs) >= min_steps and np.std(xs) > 0 and np.std(ds) > 0:
            st = perm_spearman(xs, ds, n_perm=500)
            out.append({"key": key, "n_steps": len(xs), "rho": st["rho"], "p_naive": st["p"]})
    for t, q in zip(out, bh([t["p_naive"] for t in out])):
        t["q_naive"] = q
    out.sort(key=lambda t: t["p_naive"])
    return out
