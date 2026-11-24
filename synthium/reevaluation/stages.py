"""Read stage-by-stage case scores (one JSON file per case) made with RUBRIC.md.

Each case is a path through six stages: act, filing, plea_or_answer, trial_or_hearing,
sentence_or_remedy, appeal. At each stage the accused side's position is a point on the
five early dimensions (v, R, r, C, S), plus the Fear of Loss parts, an enjoyment level H
and the qualities (Q columns) as they were visible at that stage.

UNTESTED and NOT BLIND: the stage scores were made after every ending was known.
"""

from __future__ import annotations

import glob
import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

import numpy as np

from ..geometry.scores import CaseScores
from ..geometry.trajectory import CasePath, Stage

STAGES = ("act", "filing", "plea_or_answer", "trial_or_hearing", "sentence_or_remedy", "appeal")
FIVE = ("v", "R", "r", "C", "S")
FEAR = ("fear_connection_love", "fear_connection_obsession", "fear_possibility", "fear_powerlessness")
EXTRA = ("H_enjoyment", "interference")


def val(x) -> Optional[float]:
    """A scored cell is ``{"v": 0.5, "tag": ..., "why": ...}``, a bare number, or null."""
    if x is None:
        return None
    if isinstance(x, dict):
        x = x.get("v", x.get("value"))
    if isinstance(x, bool):
        return None
    if isinstance(x, (int, float)) and np.isfinite(x):
        return float(x)
    if isinstance(x, str):
        try:
            return float(x.split()[0])
        except (ValueError, IndexError):
            return None
    return None


def tag(x) -> Optional[str]:
    return x.get("tag") if isinstance(x, dict) else None


@dataclass
class StagedCase:
    case_id: str
    case_type: str
    scorer: str
    stages: Dict[str, dict] = field(default_factory=dict)  # stage name -> stage object
    missing: List[str] = field(default_factory=list)
    notes: str = ""
    raw: dict = field(default_factory=dict)

    def present(self, stage: str) -> bool:
        s = self.stages.get(stage)
        return bool(s) and str(s.get("present", "")).lower() in ("yes", "true", "pending")

    def present_stages(self) -> List[str]:
        return [s for s in STAGES if self.present(s)]

    def get(self, stage: str, key: str) -> Optional[float]:
        s = self.stages.get(stage) or {}
        if key in s:
            return val(s[key])
        q = s.get("Q") or {}
        if key in q:
            return val(q[key])
        return None

    def point(self, stage: str, keys: Sequence[str] = FIVE) -> Optional[Dict[str, float]]:
        """The stage as a point on ``keys``; None if any is missing."""
        out = {}
        for k in keys:
            x = self.get(stage, k)
            if x is None:
                return None
            out[k] = x
        return out

    def path(self, keys: Sequence[str]) -> CasePath:
        out = CasePath(self.case_id)
        for st in self.present_stages():
            sc = {k: self.get(st, k) for k in keys}
            sc = {k: v for k, v in sc.items() if v is not None}
            out.stages.append(Stage(st, (self.stages[st] or {}).get("date"), sc))
        return out

    def quality_keys(self) -> List[str]:
        keys: List[str] = []
        for s in self.stages.values():
            for k in (s or {}).get("Q", {}) or {}:
                if k not in keys:
                    keys.append(k)
        return keys


def _stage_map(obj: dict) -> Dict[str, dict]:
    st = obj.get("stages", [])
    if isinstance(st, dict):
        return {k: v for k, v in st.items() if k in STAGES}
    out = {}
    for s in st:
        name = (s or {}).get("stage")
        if name in STAGES:
            out[name] = s
    return out


def load_staged(directory: str, include_calibration: bool = False) -> List[StagedCase]:
    """Every ``<case_id>.json`` in ``directory`` (calibration copies are kept apart)."""
    files = sorted(glob.glob(os.path.join(directory, "*.json")))
    if include_calibration:
        files += sorted(glob.glob(os.path.join(directory, "calibration", "*.json")))
    out = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            obj = json.load(fh)
        out.append(
            StagedCase(
                case_id=obj.get("case_id") or os.path.basename(f)[:-5],
                case_type=str(obj.get("case_type", "")),
                scorer=str(obj.get("scorer", "")),
                stages=_stage_map(obj),
                missing=list(obj.get("missing", []) or []),
                notes=str(obj.get("notes", "")),
                raw=obj,
            )
        )
    return out


def stage_points(cases: Sequence[StagedCase], keys: Sequence[str], stages: Sequence[str] = STAGES,
                 domain: str = "courts-stages") -> CaseScores:
    """Every (case, stage) as one point, so the geometry tools can run on them."""
    ids, rows, order, filed = [], [], [], []
    for i, c in enumerate(cases):
        for j, st in enumerate(stages):
            if not c.present(st):
                continue
            ids.append(f"{c.case_id}@{st}")
            rows.append([c.get(st, k) if c.get(st, k) is not None else np.nan for k in keys])
            order.append(i * 10 + j)
            filed.append(None)
    values = np.array(rows, float) if rows else np.zeros((0, len(keys)))
    return CaseScores(ids, list(keys), values, [[None] * len(keys) for _ in rows],
                      np.array(order), filed, domain)


def case_points(cases: Sequence[StagedCase], stage: str, keys: Sequence[str],
                domain: str = "courts-one-stage") -> CaseScores:
    """One point per case, taken at a single stage."""
    rows = [[c.get(stage, k) if c.get(stage, k) is not None else np.nan for k in keys] for c in cases]
    values = np.array(rows, float) if rows else np.zeros((0, len(keys)))
    return CaseScores([c.case_id for c in cases], list(keys), values,
                      [[None] * len(keys) for _ in rows], np.arange(len(cases)),
                      [None] * len(cases), domain)


def median_of(copies: Sequence[StagedCase]) -> StagedCase:
    """One case scored by several scorers, combined cell by cell: the median of the numbers,
    the most common value for anything else. Used for the calibration case so that no single
    scorer's reading of it stands in for the rest."""
    from collections import Counter

    def combine(values):
        nums = [val(v) for v in values if val(v) is not None]
        if nums and all(isinstance(v, (int, float, dict, type(None))) and not isinstance(v, bool)
                        for v in values):
            return {"v": float(np.median(nums)), "tag": "MEDIAN", "why": f"median of {len(nums)} scorers"}
        plain = [json.dumps(v, sort_keys=True) for v in values if v is not None]
        return json.loads(Counter(plain).most_common(1)[0][0]) if plain else None

    stages: Dict[str, dict] = {}
    for st in STAGES:
        objs = [c.stages.get(st) for c in copies if c.stages.get(st)]
        if not objs:
            continue
        out: dict = {}
        for k in {k for o in objs for k in o if k != "Q"}:
            out[k] = combine([o.get(k) for o in objs])
        qkeys = {k for o in objs for k in (o.get("Q") or {})}
        out["Q"] = {k: combine([(o.get("Q") or {}).get(k) for o in objs]) for k in qkeys}
        stages[st] = out
    first = copies[0]
    return StagedCase(first.case_id, first.case_type, "median-of-" + str(len(copies)), stages,
                      sorted({m for c in copies for m in c.missing}), "", {})
