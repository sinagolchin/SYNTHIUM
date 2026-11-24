"""Dataset utilities for the Synthium Judicial Module."""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence

import numpy as np

from .spec import EXTENDED_UNITS, OPERATOR_KEYS, OUTCOME_CLASSES

# RESTORED 2026-11-24: path now points at this restored copy's data_files/.
DEFAULT_ATLAS_PATH = Path(__file__).resolve().parents[2] / "data_files" / "judicial_suppression_atlas_v0_2.csv"
DEFAULT_ATLAS_PATH = DEFAULT_ATLAS_PATH.resolve()

TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_'-]*")


@dataclass
class JudicialCaseRecord:
    case_id: str
    case_name: str
    text: str
    units: np.ndarray
    operators: np.ndarray
    outcome_index: int
    cluster: str
    raw: Dict[str, str]


def tokenize(text: str) -> List[str]:
    return [m.group(0).lower() for m in TOKEN_RE.finditer(text or "")]


class TextVocab:
    def __init__(self, token_to_id: Optional[Dict[str, int]] = None, min_freq: int = 1, max_size: int = 20000):
        self.min_freq = int(min_freq)
        self.max_size = int(max_size)
        self.token_to_id = token_to_id or {"<pad>": 0, "<unk>": 1}

    def build(self, texts: Iterable[str]) -> "TextVocab":
        counts: Dict[str, int] = {}
        for text in texts:
            for tok in tokenize(text):
                counts[tok] = counts.get(tok, 0) + 1
        items = sorted(
            [(tok, cnt) for tok, cnt in counts.items() if cnt >= self.min_freq],
            key=lambda x: (-x[1], x[0]),
        )[: max(0, self.max_size - 2)]
        self.token_to_id = {"<pad>": 0, "<unk>": 1}
        for tok, _ in items:
            if tok not in self.token_to_id:
                self.token_to_id[tok] = len(self.token_to_id)
        return self

    def encode(self, text: str, max_len: int = 256) -> List[int]:
        ids = [self.token_to_id.get(tok, 1) for tok in tokenize(text)[:max_len]]
        return ids or [1]

    def __len__(self) -> int:
        return len(self.token_to_id)


def load_records(path: Optional[str | Path] = None) -> List[JudicialCaseRecord]:
    path = Path(path or DEFAULT_ATLAS_PATH)
    records: List[JudicialCaseRecord] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            units = np.array([float(row.get(k, 0.0) or 0.0) for k in EXTENDED_UNITS], dtype=np.float32)
            ops = np.array([float(row.get(f"op_{k}", 0.0) or 0.0) for k in OPERATOR_KEYS], dtype=np.float32)
            outcome = row.get("outcome", "UNKNOWN") or "UNKNOWN"
            if outcome not in OUTCOME_CLASSES:
                outcome = "UNKNOWN"
            text = " ".join([row.get("case_name", ""), row.get("cluster", ""), row.get("text", "")]).strip()
            records.append(
                JudicialCaseRecord(
                    case_id=row.get("case_id", ""),
                    case_name=row.get("case_name", ""),
                    text=text,
                    units=units,
                    operators=ops,
                    outcome_index=OUTCOME_CLASSES.index(outcome),
                    cluster=row.get("cluster", ""),
                    raw=row,
                )
            )
    return records


def build_vocab(records: Sequence[JudicialCaseRecord], min_freq: int = 1, max_size: int = 20000) -> TextVocab:
    return TextVocab(min_freq=min_freq, max_size=max_size).build([r.text for r in records])


def collate_records(records: Sequence[JudicialCaseRecord], vocab: TextVocab, max_len: int = 256) -> Dict[str, object]:
    import torch

    encoded = [vocab.encode(r.text, max_len=max_len) for r in records]
    lengths = torch.tensor([len(x) for x in encoded], dtype=torch.long)
    max_batch_len = int(lengths.max().item()) if len(lengths) else 1
    token_ids = torch.zeros((len(encoded), max_batch_len), dtype=torch.long)
    mask = torch.zeros_like(token_ids, dtype=torch.float32)
    for i, ids in enumerate(encoded):
        token_ids[i, :len(ids)] = torch.tensor(ids, dtype=torch.long)
        mask[i, :len(ids)] = 1.0
    return {
        "token_ids": token_ids,
        "mask": mask,
        "units": torch.tensor(np.stack([r.units for r in records]), dtype=torch.float32),
        "operators": torch.tensor(np.stack([r.operators for r in records]), dtype=torch.float32),
        "outcome": torch.tensor([r.outcome_index for r in records], dtype=torch.long),
        "case_ids": [r.case_id for r in records],
        "case_names": [r.case_name for r in records],
        "clusters": [r.cluster for r in records],
        "texts": [r.text for r in records],
    }


def train_test_split_records(records: Sequence[JudicialCaseRecord], test_fraction: float = 0.25, seed: int = 42):
    rng = np.random.default_rng(seed)
    idx = np.arange(len(records))
    rng.shuffle(idx)
    n_test = max(1, int(round(len(records) * test_fraction)))
    test_idx = set(idx[:n_test].tolist())
    train = [r for i, r in enumerate(records) if i not in test_idx]
    test = [r for i, r in enumerate(records) if i in test_idx]
    return train, test
