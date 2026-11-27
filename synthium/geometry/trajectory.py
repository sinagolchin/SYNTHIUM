"""A case as a path through the quality space over time (filing to final decision).

Sina's picture: each dimension bends the trajectory of the event. To see that, a case
needs scores at more than one moment (for example at filing, at plea, at sentence).
CASES.csv mostly holds one score per quality per case, so most cases are still a single
point. A few cells already record a change, such as ``"0.2 before verdict / 0.9 after"``;
:func:`staged_cells` finds those.

:class:`CasePath` holds staged scores when they exist and gives the path's length,
its velocity between stages and which dimensions moved.

UNTESTED: there are almost no staged scores yet, so no path has been measured.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

_TWO_NUMBERS = re.compile(
    r"(-?\d+(?:\.\d+)?)[^0-9/]*(?:before|pre)[^/]*/\s*(-?\d+(?:\.\d+)?)[^0-9]*(?:after|post)",
    re.IGNORECASE,
)


@dataclass
class Stage:
    label: str  # e.g. "filing", "plea", "sentence"
    date: Optional[str]  # YYYY-MM-DD
    scores: Dict[str, float]


@dataclass
class CasePath:
    case_id: str
    stages: List[Stage] = field(default_factory=list)

    def dimensions(self) -> List[str]:
        out: List[str] = []
        for s in self.stages:
            for k in s.scores:
                if k not in out:
                    out.append(k)
        return out

    def matrix(self, dims: Optional[Sequence[str]] = None) -> np.ndarray:
        dims = list(dims or self.dimensions())
        return np.array([[s.scores.get(d, np.nan) for d in dims] for s in self.stages])

    def steps(self) -> List[dict]:
        """Change between consecutive stages, over the dimensions scored at both."""
        dims = self.dimensions()
        M = self.matrix(dims)
        out = []
        for i in range(1, len(self.stages)):
            a, b = M[i - 1], M[i]
            ok = ~(np.isnan(a) | np.isnan(b))
            delta = {d: float(b[j] - a[j]) for j, d in enumerate(dims) if ok[j]}
            out.append(
                {
                    "from": self.stages[i - 1].label,
                    "to": self.stages[i].label,
                    "length": float(np.sqrt(sum(v * v for v in delta.values()))),
                    "moved": {d: v for d, v in delta.items() if v != 0},
                }
            )
        return out

    def length(self) -> float:
        return float(sum(s["length"] for s in self.steps()))


def staged_cells(path: str, columns: Sequence[str]) -> List[Tuple[str, str, float, float, str]]:
    """Cells that record a before/after pair: (case_id, column, before, after, raw text)."""
    out = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            for c in columns:
                m = _TWO_NUMBERS.search(row.get(c, "") or "")
                if m:
                    out.append((row.get("case_id", ""), c, float(m.group(1)), float(m.group(2)), row[c]))
    return out


def paths_from_staged_cells(cells) -> List[CasePath]:
    by_case: Dict[str, CasePath] = {}
    for cid, col, before, after, _ in cells:
        p = by_case.setdefault(cid, CasePath(cid, [Stage("before", None, {}), Stage("after", None, {})]))
        p.stages[0].scores[col] = before
        p.stages[1].scores[col] = after
    return list(by_case.values())
