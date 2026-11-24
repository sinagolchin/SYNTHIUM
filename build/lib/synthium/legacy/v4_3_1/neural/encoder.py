"""Trainable neural encoders for Synthium."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import torch
from torch import nn


@dataclass
class EncoderOutput:
    unit_logits: torch.Tensor
    operator_logits: torch.Tensor
    outcome_logits: torch.Tensor
    embedding: torch.Tensor
    log_variance: torch.Tensor

    @property
    def units(self) -> torch.Tensor:
        return torch.sigmoid(self.unit_logits)

    @property
    def operators(self) -> torch.Tensor:
        return torch.sigmoid(self.operator_logits)


class JudicialNeuralEncoder(nn.Module):
    """Small trainable text encoder for the judicial module.

    This is intentionally lightweight: an embedding layer plus masked mean pooling
    and multi-head outputs. It is a true trainable neural model with backprop, but
    it does not require external pretrained weights.
    """

    def __init__(
        self,
        vocab_size: int,
        n_units: int,
        n_operators: int,
        n_outcomes: int,
        embed_dim: int = 96,
        hidden_dim: int = 128,
        manifold_dim: int = 32,
        dropout: float = 0.10,
    ):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.encoder = nn.Sequential(
            nn.Linear(embed_dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
        )
        self.unit_head = nn.Linear(hidden_dim, n_units)
        self.operator_head = nn.Linear(hidden_dim, n_operators)
        self.outcome_head = nn.Linear(hidden_dim, n_outcomes)
        self.embedding_head = nn.Linear(hidden_dim, manifold_dim)
        self.logvar_head = nn.Linear(hidden_dim, n_units)

    def forward(self, token_ids: torch.Tensor, mask: torch.Tensor) -> EncoderOutput:
        x = self.embedding(token_ids)
        mask3 = mask.unsqueeze(-1)
        pooled = (x * mask3).sum(dim=1) / mask3.sum(dim=1).clamp_min(1.0)
        h = self.encoder(pooled)
        emb = torch.nn.functional.normalize(self.embedding_head(h), dim=-1)
        return EncoderOutput(
            unit_logits=self.unit_head(h),
            operator_logits=self.operator_head(h),
            outcome_logits=self.outcome_head(h),
            embedding=emb,
            log_variance=self.logvar_head(h).clamp(min=-7.0, max=4.0),
        )


def predict_dict(output: EncoderOutput, unit_names, operator_names, outcome_names) -> Dict[str, object]:
    units = output.units.detach().cpu()[0].numpy().tolist()
    ops = output.operators.detach().cpu()[0].numpy().tolist()
    outcome_probs = torch.softmax(output.outcome_logits, dim=-1).detach().cpu()[0].numpy().tolist()
    outcome_idx = int(max(range(len(outcome_probs)), key=lambda i: outcome_probs[i]))
    return {
        "units": {k: float(v) for k, v in zip(unit_names, units)},
        "operators": {k: float(v) for k, v in zip(operator_names, ops)},
        "outcome": outcome_names[outcome_idx],
        "outcome_probabilities": {k: float(v) for k, v in zip(outcome_names, outcome_probs)},
    }
