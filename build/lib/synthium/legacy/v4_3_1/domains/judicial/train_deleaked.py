"""De-leaked training run for the Synthium Judicial Encoder.

Purpose: report the model's actual outcome-prediction accuracy after removing
the three label leaks present in the original v4.3 training pipeline.

LEAKS FIXED:
    1. Cluster name was being concatenated into the input text (dataset.py).
       Cluster names like "good_faith" and "home_privacy" near-deterministically
       encode the outcome.
    2. Case text contained outcome words ("suppression denied", "granted",
       "affirmed", "reversed", etc.). These are stripped here.
    3. The supervised contrastive loss used cluster labels as positive-pair
       signal. Since clusters near-perfectly determine outcome, this leaks
       the answer into the embedding head. We zero out that loss weight.

In addition:
    - Outcome-stratified train/test split (so the test set is representative).
    - Multiple seeds with mean +/- std reporting.
    - Explicit majority-class baseline for comparison.
    - Confidence interval on test accuracy via Wilson score.

Run from package root:
    PYTHONPATH=. python -m synthium.domains.judicial.train_deleaked --epochs 180 --seeds 5
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from dataclasses import replace
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import torch
from torch.optim import AdamW

from synthium.legacy.v4_3_1.domains.judicial.dataset import (
    JudicialCaseRecord,
    TextVocab,
    build_vocab,
    collate_records,
    DEFAULT_ATLAS_PATH,
)
from synthium.legacy.v4_3_1.domains.judicial.spec import EXTENDED_UNITS, OPERATOR_KEYS, OUTCOME_CLASSES
from synthium.legacy.v4_3_1.neural.encoder import JudicialNeuralEncoder
from synthium.legacy.v4_3_1.neural.losses import LossWeights, total_synthium_loss
from synthium.legacy.v4_3_1.neural.metrics import mae, rmse


# Patterns that directly reveal the suppression outcome.
OUTCOME_LEAK_PATTERNS = [
    re.compile(r"\bsuppression\s+(?:was\s+)?(?:granted|denied|remanded|affirmed|reversed)\b", re.I),
    re.compile(r"\bmotion\s+(?:was\s+)?(?:granted|denied)\b", re.I),
    re.compile(r"\b(?:granted|denied)\s+suppression\b", re.I),
    re.compile(r"\bconviction\s+(?:was\s+)?(?:affirmed|reversed|vacated)\b", re.I),
    re.compile(r"\bsuppression\s+order\b", re.I),
    re.compile(r"\b(?:was\s+)?(?:affirmed|reversed|vacated)\b", re.I),
    re.compile(r"\b(?:was\s+)?(?:granted|denied)\b", re.I),
    re.compile(r"\bviolated\b", re.I),
    re.compile(r"\bno\s+(?:fourth\s+amendment\s+)?violation\b", re.I),
]

OUTCOME_REDACTION = " [REDACTED] "


def redact_outcome_words(text: str) -> str:
    """Replace any phrase that directly reveals the outcome."""
    if not text:
        return ""
    for pat in OUTCOME_LEAK_PATTERNS:
        text = pat.sub(OUTCOME_REDACTION, text)
    return text


def load_records_deleaked(path: Path | None = None) -> List[JudicialCaseRecord]:
    """Load atlas records but build the input text without the cluster leak
    and with outcome-revealing phrases stripped.

    Returns records identical in structure to dataset.load_records, except
    `record.text` no longer contains the cluster name or outcome words.
    """
    path = Path(path or DEFAULT_ATLAS_PATH)
    records: List[JudicialCaseRecord] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            units = np.array(
                [float(row.get(k, 0.0) or 0.0) for k in EXTENDED_UNITS],
                dtype=np.float32,
            )
            ops = np.array(
                [float(row.get(f"op_{k}", 0.0) or 0.0) for k in OPERATOR_KEYS],
                dtype=np.float32,
            )
            outcome = row.get("outcome", "UNKNOWN") or "UNKNOWN"
            if outcome not in OUTCOME_CLASSES:
                outcome = "UNKNOWN"

            # KEY FIX: drop cluster from input text; strip outcome words from the body.
            body = redact_outcome_words(row.get("text", ""))
            # We still keep case_name as a weak identifier (it doesn't reliably
            # encode outcome). If you want to be even stricter, drop it too.
            text = " ".join([row.get("case_name", ""), body]).strip()

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


def stratified_split(
    records: List[JudicialCaseRecord],
    test_fraction: float,
    seed: int,
) -> Tuple[List[JudicialCaseRecord], List[JudicialCaseRecord]]:
    """Stratified split by outcome_index so test set is representative."""
    rng = np.random.default_rng(seed)
    by_class: Dict[int, List[int]] = {}
    for i, r in enumerate(records):
        by_class.setdefault(r.outcome_index, []).append(i)

    test_idx: set[int] = set()
    for cls, idxs in by_class.items():
        idxs_arr = np.array(idxs)
        rng.shuffle(idxs_arr)
        n_test = max(1, int(round(len(idxs_arr) * test_fraction)))
        # If a class has only one example, keep it in train (can't learn from 0).
        if len(idxs_arr) == 1:
            continue
        test_idx.update(int(x) for x in idxs_arr[:n_test])

    train = [r for i, r in enumerate(records) if i not in test_idx]
    test = [r for i, r in enumerate(records) if i in test_idx]
    return train, test


def majority_class_accuracy(test_records: List[JudicialCaseRecord], train_records: List[JudicialCaseRecord]) -> Tuple[float, str]:
    """Predict the training-majority class for every test case."""
    counts: Dict[int, int] = {}
    for r in train_records:
        counts[r.outcome_index] = counts.get(r.outcome_index, 0) + 1
    majority = max(counts, key=counts.get)
    correct = sum(1 for r in test_records if r.outcome_index == majority)
    return correct / max(1, len(test_records)), OUTCOME_CLASSES[majority]


def wilson_ci(k: int, n: int, z: float = 1.96) -> Tuple[float, float]:
    """95% Wilson score interval for a proportion."""
    if n == 0:
        return 0.0, 1.0
    p = k / n
    denom = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def train_once(
    records: List[JudicialCaseRecord],
    epochs: int,
    seed: int,
    drop_contrastive: bool = True,
) -> Dict[str, float]:
    """Train one seed and return test metrics + comparison to baseline."""
    torch.manual_seed(seed)
    np.random.seed(seed)
    try:
        torch.set_num_threads(1)
    except Exception:
        pass

    train_records, test_records = stratified_split(records, test_fraction=0.25, seed=seed)
    vocab = build_vocab(train_records, min_freq=1, max_size=12000)  # build vocab from train only
    model = JudicialNeuralEncoder(
        vocab_size=len(vocab),
        n_units=len(EXTENDED_UNITS),
        n_operators=len(OPERATOR_KEYS),
        n_outcomes=len(OUTCOME_CLASSES),
    )
    opt = AdamW(model.parameters(), lr=2e-3, weight_decay=1e-4)
    unit_index = {name: i for i, name in enumerate(EXTENDED_UNITS)}
    op_index = {name: i for i, name in enumerate(OPERATOR_KEYS)}

    # KEY FIX: zero the contrastive loss so cluster labels can't leak in.
    weights = LossWeights()
    if drop_contrastive:
        weights = replace(weights, metric=0.0)

    train_batch = collate_records(train_records, vocab)
    for epoch in range(1, epochs + 1):
        model.train()
        opt.zero_grad()
        output = model(train_batch["token_ids"], train_batch["mask"])
        # We pass cluster_labels=None so even if the metric weight were nonzero,
        # it would fall back to outcome - which is still a label leak. With
        # metric=0.0, this branch never contributes to the gradient.
        loss, _ = total_synthium_loss(
            output,
            train_batch,
            unit_index,
            op_index,
            weights,
            cluster_labels=None,
        )
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=3.0)
        opt.step()

    # Evaluate
    model.eval()
    test_batch = collate_records(test_records, vocab)
    with torch.no_grad():
        out = model(test_batch["token_ids"], test_batch["mask"])
    pred_units = out.units.cpu().numpy()
    true_units = test_batch["units"].cpu().numpy()
    outcome_pred = out.outcome_logits.argmax(dim=-1).cpu().numpy()
    outcome_true = test_batch["outcome"].cpu().numpy()
    ops_pred = (out.operators.cpu().numpy() >= 0.5).astype(int)
    ops_true = test_batch["operators"].cpu().numpy().astype(int)

    baseline_acc, baseline_label = majority_class_accuracy(test_records, train_records)
    correct = int((outcome_pred == outcome_true).sum())
    n_test = len(test_records)
    test_acc = correct / max(1, n_test)
    ci_lo, ci_hi = wilson_ci(correct, n_test)

    return {
        "seed": seed,
        "n_train": len(train_records),
        "n_test": n_test,
        "test_outcome_accuracy": test_acc,
        "test_outcome_correct": correct,
        "test_outcome_ci95": [ci_lo, ci_hi],
        "majority_baseline_accuracy": baseline_acc,
        "majority_baseline_label": baseline_label,
        "delta_vs_baseline": test_acc - baseline_acc,
        "unit_mae": mae(true_units, pred_units),
        "unit_rmse": rmse(true_units, pred_units),
        "operator_micro_accuracy": float((ops_pred == ops_true).mean()),
    }


def main():
    parser = argparse.ArgumentParser(description="De-leaked judicial encoder run")
    parser.add_argument("--data", type=str, default=None)
    parser.add_argument("--epochs", type=int, default=180)
    parser.add_argument("--seeds", type=int, default=5)
    parser.add_argument("--output-dir", type=str, default="outputs_deleaked")
    args = parser.parse_args()

    records = load_records_deleaked(args.data)
    print(f"Loaded {len(records)} records (cluster name dropped from text; outcome words redacted).")
    print(f"Class distribution: ", end="")
    cls_counts: Dict[str, int] = {}
    for r in records:
        cls_counts[OUTCOME_CLASSES[r.outcome_index]] = cls_counts.get(OUTCOME_CLASSES[r.outcome_index], 0) + 1
    print(cls_counts)

    seed_results = []
    for s in range(args.seeds):
        seed = 42 + s
        result = train_once(records, epochs=args.epochs, seed=seed, drop_contrastive=True)
        seed_results.append(result)
        print(
            f"seed={seed}: n_test={result['n_test']:>2d} "
            f"acc={result['test_outcome_accuracy']:.3f} "
            f"baseline={result['majority_baseline_accuracy']:.3f} "
            f"delta={result['delta_vs_baseline']:+.3f} "
            f"unit_mae={result['unit_mae']:.3f}"
        )

    accs = [r["test_outcome_accuracy"] for r in seed_results]
    baselines = [r["majority_baseline_accuracy"] for r in seed_results]
    deltas = [r["delta_vs_baseline"] for r in seed_results]
    unit_maes = [r["unit_mae"] for r in seed_results]

    summary = {
        "config": {
            "epochs": args.epochs,
            "seeds": args.seeds,
            "drops_contrastive_loss": True,
            "drops_cluster_from_text": True,
            "redacts_outcome_words": True,
            "stratified_split": True,
            "vocab_built_from_train_only": True,
        },
        "per_seed": seed_results,
        "aggregate": {
            "test_outcome_accuracy_mean": float(np.mean(accs)),
            "test_outcome_accuracy_std": float(np.std(accs)),
            "majority_baseline_mean": float(np.mean(baselines)),
            "delta_vs_baseline_mean": float(np.mean(deltas)),
            "delta_vs_baseline_std": float(np.std(deltas)),
            "unit_mae_mean": float(np.mean(unit_maes)),
            "unit_mae_std": float(np.std(unit_maes)),
        },
    }

    print()
    print("=" * 64)
    print("DE-LEAKED RESULTS SUMMARY")
    print("=" * 64)
    print(f"Test accuracy (mean +/- std over {args.seeds} seeds):")
    print(f"  Model:    {summary['aggregate']['test_outcome_accuracy_mean']:.3f} "
          f"+/- {summary['aggregate']['test_outcome_accuracy_std']:.3f}")
    print(f"  Baseline: {summary['aggregate']['majority_baseline_mean']:.3f}  "
          f"(always-predict-majority-class)")
    print(f"  Delta:    {summary['aggregate']['delta_vs_baseline_mean']:+.3f} "
          f"+/- {summary['aggregate']['delta_vs_baseline_std']:.3f}")
    print(f"Unit MAE:   {summary['aggregate']['unit_mae_mean']:.3f} "
          f"+/- {summary['aggregate']['unit_mae_std']:.3f}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "deleaked_training_report.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(f"\nWrote {output_dir / 'deleaked_training_report.json'}")


if __name__ == "__main__":
    main()
