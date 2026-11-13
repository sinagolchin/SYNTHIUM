"""Baselines as frozen *rules*, not numbers.

The discipline this enforces:

    A baseline is a prediction rule frozen BEFORE the test. Its score does not
    exist yet. The score is produced later by running the rule on the same
    held-out cases the model is run on. That is the only honest comparison: the
    baseline earns its number on the future, alongside the model.

This is why ``Baseline`` holds a callable, not a float. A float carried forward
from a previous run is exactly the mistake this module exists to prevent.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Sequence


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class Baseline:
    """A prediction rule frozen before the test. Its SCORE does not exist yet."""

    name: str
    rule: Callable[[Dict[str, Any]], Any]  # features -> predicted label
    declared_at: str = field(default_factory=_now)

    def predict(self, features: Dict[str, Any]) -> Any:
        return self.rule(features)


def majority_class_baseline(train_labels: Sequence[Any]) -> Baseline:
    """The standard floor: always predict the training-majority label.

    The majority is fixed from the TRAINING labels only. Choosing it from the
    test labels would be a leak -- the baseline would be peeking at the answers
    it is supposed to be compared against.
    """
    counts: Dict[Any, int] = {}
    for y in train_labels:
        counts[y] = counts.get(y, 0) + 1
    majority = max(counts, key=counts.get) if counts else None
    return Baseline(
        name=f"always-predict-{majority}",
        rule=lambda _features, _m=majority: _m,
    )


def keyword_baseline(name: str, keyword: str, if_present: Any, if_absent: Any,
                     text_field: str = "text") -> Baseline:
    """A trivial single-keyword rule -- a slightly stronger floor than majority.

    Useful for asking the honest question: does the proposed model beat *just
    looking for one obvious word*? Many elaborate models do not.
    """
    kw = keyword.lower()

    def rule(features: Dict[str, Any]) -> Any:
        return if_present if kw in str(features.get(text_field, "")).lower() else if_absent

    return Baseline(name=name, rule=rule)
