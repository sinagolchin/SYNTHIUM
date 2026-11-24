"""Neural Synthium losses.

The core idea is multi-objective training: learn units, operators, outcomes,
metric embeddings, uncertainty, and symbolic formula consistency together.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import torch
import torch.nn.functional as F


@dataclass
class LossWeights:
    units: float = 1.0
    operators: float = 0.7
    outcome: float = 0.8
    metric: float = 0.2
    confidence: float = 0.1
    consistency: float = 0.4


def supervised_contrastive_loss(embeddings: torch.Tensor, labels, temperature: float = 0.2) -> torch.Tensor:
    device = embeddings.device
    if not isinstance(labels, torch.Tensor):
        # Convert arbitrary strings/labels to integer ids.
        mapping = {}
        ids = []
        for x in labels:
            if x not in mapping:
                mapping[x] = len(mapping)
            ids.append(mapping[x])
        labels = torch.tensor(ids, device=device, dtype=torch.long)
    labels = labels.to(device)
    n = embeddings.shape[0]
    if n < 2:
        return torch.zeros((), device=device)
    sim = embeddings @ embeddings.T / temperature
    eye = torch.eye(n, device=device, dtype=torch.bool)
    sim = sim.masked_fill(eye, -1e9)
    positive = labels.unsqueeze(0) == labels.unsqueeze(1)
    positive = positive & (~eye)
    if positive.sum() == 0:
        return torch.zeros((), device=device)
    log_prob = sim - torch.logsumexp(sim, dim=1, keepdim=True)
    loss = -(log_prob * positive.float()).sum(dim=1) / positive.float().sum(dim=1).clamp_min(1.0)
    valid = positive.any(dim=1)
    return loss[valid].mean()


def formula_consistency_loss(pred_units: torch.Tensor, target_ops: torch.Tensor, unit_index: Dict[str, int], op_index: Dict[str, int]) -> torch.Tensor:
    """Penalty for violating discovered Synthium operator rules.

    These are soft constraints. They do not replace data, but they reduce
    incoherent predictions.
    """
    losses = []
    priv = pred_units[:, unit_index["Priv"]]
    excp = pred_units[:, unit_index["Excp"]]
    rem = pred_units[:, unit_index["Rem"]]
    scope = pred_units[:, unit_index.get("Scope", unit_index["Rem"])]
    jrem = pred_units[:, unit_index.get("JRem", unit_index["Rem"])]

    def op(name: str) -> torch.Tensor:
        if name not in op_index:
            return torch.zeros_like(priv)
        return target_ops[:, op_index[name]]

    abandonment = op("abandonment")
    good_faith = op("good_faith")
    exigency = op("exigency")
    scope_breach = op("scope_breach")
    home_core = op("home_core")

    # Abandonment should pull effective privacy low.
    losses.append(abandonment * F.relu(priv - 0.45).pow(2))
    # Good faith in an available regime should reduce remedial proximity.
    losses.append(good_faith * jrem * F.relu(rem - 0.58).pow(2))
    # Exigency should raise exception strength.
    losses.append(exigency * F.relu(0.68 - excp).pow(2))
    # Scope breach should imply low scope fidelity and high remedial proximity.
    losses.append(scope_breach * F.relu(scope - 0.45).pow(2))
    losses.append(scope_breach * F.relu(0.70 - rem).pow(2))
    # Home core with weak exception should not have low privacy.
    losses.append(home_core * F.relu(0.80 - priv).pow(2))

    stacked = torch.stack(losses, dim=0)
    return stacked.mean()


def heteroscedastic_unit_loss(unit_logits: torch.Tensor, log_variance: torch.Tensor, target_units: torch.Tensor) -> torch.Tensor:
    pred = torch.sigmoid(unit_logits)
    inv_var = torch.exp(-log_variance)
    return (0.5 * inv_var * (pred - target_units).pow(2) + 0.5 * log_variance).mean()


def total_synthium_loss(output, batch: Dict[str, torch.Tensor], unit_index: Dict[str, int], op_index: Dict[str, int], weights: LossWeights, cluster_labels=None):
    units_target = batch["units"]
    ops_target = batch["operators"]
    outcome_target = batch["outcome"]

    l_units = F.mse_loss(output.units, units_target)
    l_conf = heteroscedastic_unit_loss(output.unit_logits, output.log_variance, units_target)
    l_ops = F.binary_cross_entropy_with_logits(output.operator_logits, ops_target)
    l_out = F.cross_entropy(output.outcome_logits, outcome_target)
    l_metric = supervised_contrastive_loss(output.embedding, cluster_labels if cluster_labels is not None else outcome_target)
    l_cons = formula_consistency_loss(output.units, ops_target, unit_index, op_index)

    total = (
        weights.units * l_units
        + weights.operators * l_ops
        + weights.outcome * l_out
        + weights.metric * l_metric
        + weights.confidence * l_conf
        + weights.consistency * l_cons
    )
    return total, {
        "total": float(total.detach().cpu()),
        "units": float(l_units.detach().cpu()),
        "operators": float(l_ops.detach().cpu()),
        "outcome": float(l_out.detach().cpu()),
        "metric": float(l_metric.detach().cpu()),
        "confidence": float(l_conf.detach().cpu()),
        "consistency": float(l_cons.detach().cpu()),
    }
