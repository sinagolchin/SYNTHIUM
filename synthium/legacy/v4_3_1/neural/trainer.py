"""Training helpers for neural Synthium models."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence

import numpy as np
import torch
from torch.optim import AdamW

from synthium.legacy.v4_3_1.domains.judicial.dataset import JudicialCaseRecord, TextVocab, build_vocab, collate_records
from synthium.legacy.v4_3_1.domains.judicial.spec import EXTENDED_UNITS, OPERATOR_KEYS, OUTCOME_CLASSES
from .encoder import JudicialNeuralEncoder
from .losses import LossWeights, total_synthium_loss


@dataclass
class TrainingResult:
    model: JudicialNeuralEncoder
    vocab: TextVocab
    history: List[Dict[str, float]]


def _limit_threads():
    try:
        torch.set_num_threads(1)
    except Exception:
        pass


def train_judicial_encoder(
    records: Sequence[JudicialCaseRecord],
    epochs: int = 180,
    lr: float = 2e-3,
    seed: int = 42,
    verbose: bool = False,
) -> TrainingResult:
    _limit_threads()
    torch.manual_seed(seed)
    np.random.seed(seed)
    vocab = build_vocab(records, min_freq=1, max_size=12000)
    model = JudicialNeuralEncoder(
        vocab_size=len(vocab),
        n_units=len(EXTENDED_UNITS),
        n_operators=len(OPERATOR_KEYS),
        n_outcomes=len(OUTCOME_CLASSES),
    )
    opt = AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    unit_index = {name: i for i, name in enumerate(EXTENDED_UNITS)}
    op_index = {name: i for i, name in enumerate(OPERATOR_KEYS)}
    weights = LossWeights()
    batch = collate_records(records, vocab)
    history: List[Dict[str, float]] = []
    for epoch in range(1, epochs + 1):
        model.train()
        opt.zero_grad()
        output = model(batch["token_ids"], batch["mask"])
        loss, parts = total_synthium_loss(output, batch, unit_index, op_index, weights, cluster_labels=batch["clusters"])
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=3.0)
        opt.step()
        if epoch == 1 or epoch == epochs or epoch % max(1, epochs // 5) == 0:
            history.append({"epoch": epoch, **parts})
            if verbose:
                print(f"epoch={epoch:04d} loss={parts['total']:.4f} units={parts['units']:.4f} ops={parts['operators']:.4f} outcome={parts['outcome']:.4f}")
    return TrainingResult(model=model, vocab=vocab, history=history)


def evaluate_judicial_encoder(model: JudicialNeuralEncoder, vocab: TextVocab, records: Sequence[JudicialCaseRecord]) -> Dict[str, float]:
    from .metrics import mae, rmse

    batch = collate_records(records, vocab)
    model.eval()
    with torch.no_grad():
        out = model(batch["token_ids"], batch["mask"])
    pred_units = out.units.cpu().numpy()
    true_units = batch["units"].cpu().numpy()
    outcome_pred = out.outcome_logits.argmax(dim=-1).cpu().numpy()
    outcome_true = batch["outcome"].cpu().numpy()
    ops_pred = (out.operators.cpu().numpy() >= 0.5).astype(int)
    ops_true = batch["operators"].cpu().numpy().astype(int)
    return {
        "unit_mae": mae(true_units, pred_units),
        "unit_rmse": rmse(true_units, pred_units),
        "outcome_accuracy": float((outcome_pred == outcome_true).mean()),
        "operator_micro_accuracy": float((ops_pred == ops_true).mean()),
    }
