"""Synthium phenomena: every phenomenon as a structure with its own dimensions.

Restored 2026-11-24 at Sina's word ("every phenomenon has its own dimensions ... bring
that back"). Holds the catalogue of every past formula, unit, axiom and tool
(:mod:`.catalogue`, status "under consideration"), the structure tests run on case scores
(:mod:`.structure`), and the generator for ``docs/UNDER_CONSIDERATION.md`` (:mod:`.index`).

EVERY RESULT IS UNTESTED. Needs numpy (``pip install synthium[geometry]``); the old
profiles also need the restored V2 code in ``synthium.legacy``.
"""

from .catalogue import (
    DIMENSIONS_5D,
    DIMENSIONS_SPACE,
    RECORDS,
    UNDER_CONSIDERATION,
    Record,
    by_id,
    computable,
    evaluate,
    legacy_profiles,
)
from .structure import (
    FORMS,
    Phenomenon,
    base_or_derived,
    combine,
    created_how,
    equilibrium,
    phenomena_from_profiles,
    profile_space,
    spearman,
)

__all__ = [
    "DIMENSIONS_5D", "DIMENSIONS_SPACE", "RECORDS", "UNDER_CONSIDERATION", "Record", "by_id",
    "computable", "evaluate", "legacy_profiles", "FORMS", "Phenomenon", "base_or_derived",
    "combine", "created_how", "equilibrium", "phenomena_from_profiles", "profile_space", "spearman",
]
