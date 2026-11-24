"""Read the case quality scores (CASES.csv) into a matrix.

Each case is a point. Each quality column (``Q1_...`` to ``Q67_...``) is a dimension.
Most cases carry only some qualities, so the matrix holds NaN where a quality was
not scored. Nothing here invents a value for a missing score.

A cell such as ``"0.75 FOUND (disclosure)"`` becomes the number 0.75 and the tag
``FOUND``. The first number in the cell is taken; a cell such as ``"1 of 2"`` becomes
0.5. Text that holds no leading number (``"present-contested ..."``) is left missing.

UNTESTED: these numbers are rankings from counted signs, with no real unit yet.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

import numpy as np

# Columns that start with Q but hold text or counts, not a 0..1 quality score.
NON_SCORE_Q_COLUMNS = frozenset(
    {
        "Q33_motivation_kind",
        "Q33_motivation_tag",
        "Q21_imputed_motive_count_adopted",
    }
)

# Known scale exceptions: these columns use 0..3 for some cases. Analyses that mix
# dimensions standardise each column first, so the scale does not decide the result.
WIDE_SCALE_COLUMNS = frozenset({"Q3_hostile", "Q6_fair_court"})

_QUALITY_RE = re.compile(r"^Q\d+[a-z]?_")
_NUMBER_RE = re.compile(r"^\s*(-?\d+(?:\.\d+)?)")
_OF_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s+of\s+(\d+(?:\.\d+)?)")
_TAG_RE = re.compile(
    r"\b(ADMITTED|FOUND(?:-JURY|-J)?|CLAIMED(?:-[PDGV])?|INFERRED|STIPULATED)\b"
    r"|\((claimed|proposed|inferred)\b",
    re.IGNORECASE,
)


def parse_score(text: str):
    """Return ``(value, tag)`` for one cell; ``(None, None)`` when there is no number."""
    if text is None:
        return None, None
    s = str(text).strip()
    if not s:
        return None, None
    m = _OF_RE.match(s)
    if m and float(m.group(2)) > 0:
        value = float(m.group(1)) / float(m.group(2))
    else:
        m = _NUMBER_RE.match(s)
        if not m:
            return None, _find_tag(s)
        value = float(m.group(1))
    return value, _find_tag(s)


def _find_tag(s: str) -> Optional[str]:
    m = _TAG_RE.search(s)
    if not m:
        return None
    tag = (m.group(1) or m.group(2)).upper()
    if tag.startswith("FOUND"):
        return "FOUND"
    if tag.startswith("CLAIMED"):
        return "CLAIMED"
    return tag


def quality_columns(header: Sequence[str], pattern: Optional[str] = None,
                    exclude: Sequence[str] = NON_SCORE_Q_COLUMNS) -> List[str]:
    """Columns that hold quality scores. ``pattern`` (a regex) lets another domain, such
    as prediction markets, name its own quality columns."""
    rx = re.compile(pattern) if pattern else _QUALITY_RE
    return [c for c in header if rx.match(c) and c not in set(exclude)]


@dataclass
class CaseScores:
    """Cases as points, qualities as dimensions, NaN where a quality was not scored."""

    case_ids: List[str]
    columns: List[str]
    values: np.ndarray  # shape (n_cases, n_qualities), NaN = not scored
    tags: List[List[Optional[str]]]  # same shape as values
    reading_order: np.ndarray  # 0..n-1 in the order the cases were studied
    filed: List[Optional[str]] = field(default_factory=list)  # YYYY-MM-DD or None
    domain: str = "courts"

    def active_dimensions(self) -> Dict[str, List[str]]:
        """For each case, the qualities scored for it (its active dimensions)."""
        present = ~np.isnan(self.values)
        return {
            cid: [c for c, p in zip(self.columns, row) if p]
            for cid, row in zip(self.case_ids, present)
        }

    @property
    def n_cases(self) -> int:
        return len(self.case_ids)

    def coverage(self) -> Dict[str, int]:
        """How many cases carry each quality."""
        counts = (~np.isnan(self.values)).sum(axis=0)
        return {c: int(n) for c, n in zip(self.columns, counts)}

    def select(self, columns: Sequence[str]) -> np.ndarray:
        idx = [self.columns.index(c) for c in columns]
        return self.values[:, idx]

    def complete_rows(self, columns: Sequence[str]) -> np.ndarray:
        """Indices of the cases that carry every quality in ``columns``."""
        sub = self.select(columns)
        return np.where(~np.isnan(sub).any(axis=1))[0]

    def filed_as_years(self) -> np.ndarray:
        """Filing date as a decimal year (NaN when missing)."""
        out = np.full(self.n_cases, np.nan)
        for i, f in enumerate(self.filed):
            if f:
                y, m, d = (int(x) for x in f.split("-"))
                out[i] = y + (m - 1) / 12.0 + (d - 1) / 365.25
        return out


def load_cases(
    path: str,
    domain: str = "courts",
    quality_pattern: Optional[str] = None,
    exclude: Sequence[str] = NON_SCORE_Q_COLUMNS,
    id_column: str = "case_id",
    date_column: str = "filed",
) -> CaseScores:
    """Load any domain's case table. Defaults fit the courts CASES.csv; another domain
    passes its own ``quality_pattern`` (regex for its score columns) and column names."""
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise ValueError(f"no rows in {path}")
    columns = quality_columns(list(rows[0].keys()), quality_pattern, exclude)
    values = np.full((len(rows), len(columns)), np.nan)
    tags: List[List[Optional[str]]] = []
    filed: List[Optional[str]] = []
    date_re = re.compile(r"(\d{4}-\d{2}-\d{2})")
    for i, row in enumerate(rows):
        row_tags: List[Optional[str]] = []
        for j, c in enumerate(columns):
            v, t = parse_score(row.get(c, ""))
            if v is not None:
                values[i, j] = v
            row_tags.append(t if v is not None else None)
        tags.append(row_tags)
        m = date_re.search(row.get(date_column, "") or "")
        filed.append(m.group(1) if m else None)
    return CaseScores(
        case_ids=[r.get(id_column) or f"row{i}" for i, r in enumerate(rows)],
        columns=columns,
        values=values,
        tags=tags,
        reading_order=np.arange(len(rows)),
        filed=filed,
        domain=domain,
    )


def standardise(X: np.ndarray) -> np.ndarray:
    """Column z-scores, ignoring NaN. A column with no spread becomes all zeros."""
    mu = np.nanmean(X, axis=0)
    sd = np.nanstd(X, axis=0)
    sd = np.where(sd > 0, sd, 1.0)
    return (X - mu) / sd
