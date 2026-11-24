"""CLI demo for training the Neural Judicial Encoder."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch

from synthium.legacy.v4_3_1.domains.judicial.dataset import load_records, train_test_split_records, collate_records
from synthium.legacy.v4_3_1.domains.judicial.rubric import suppression_pressure
from synthium.legacy.v4_3_1.domains.judicial.spec import EXTENDED_UNITS, OPERATOR_KEYS, OUTCOME_CLASSES
from synthium.legacy.v4_3_1.neural.encoder import predict_dict
from synthium.legacy.v4_3_1.neural.trainer import train_judicial_encoder, evaluate_judicial_encoder
from synthium.legacy.v4_3_1.neural.metrics import nearest_neighbors, cluster_centroids, nearest_centroid


def main():
    parser = argparse.ArgumentParser(description="Train Synthium Neural Judicial Encoder v0.1")
    parser.add_argument("--data", type=str, default=None, help="Path to judicial atlas CSV")
    parser.add_argument("--epochs", type=int, default=180)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", type=str, default="outputs_neural_judicial")
    args = parser.parse_args()

    records = load_records(args.data)
    train_records, test_records = train_test_split_records(records, test_fraction=0.25, seed=args.seed)
    result = train_judicial_encoder(train_records, epochs=args.epochs, seed=args.seed, verbose=True)
    train_metrics = evaluate_judicial_encoder(result.model, result.vocab, train_records)
    test_metrics = evaluate_judicial_encoder(result.model, result.vocab, test_records)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    torch.save({
        "model_state_dict": result.model.state_dict(),
        "vocab": result.vocab.token_to_id,
        "unit_names": list(EXTENDED_UNITS),
        "operator_names": list(OPERATOR_KEYS),
        "outcome_names": list(OUTCOME_CLASSES),
    }, output_dir / "judicial_neural_encoder.pt")

    # Build nearest-neighbor map from true atlas coordinates.
    import numpy as np
    X = np.stack([r.units for r in records])
    names = [r.case_name for r in records]
    nn = nearest_neighbors(X[:, :6], names, k=3)
    centroids = cluster_centroids(X[:, :6], [r.cluster for r in records])

    batch = collate_records(test_records[:1], result.vocab)
    result.model.eval()
    with torch.no_grad():
        out = result.model(batch["token_ids"], batch["mask"])
    pred = predict_dict(out, EXTENDED_UNITS, OPERATOR_KEYS, OUTCOME_CLASSES)
    pressure = suppression_pressure(pred["units"], pred["operators"])
    pred["suppression_pressure"] = pressure
    cluster, dist = nearest_centroid(np.array([pred["units"][u] for u in EXTENDED_UNITS[:6]], dtype=float), centroids)
    pred["nearest_centroid"] = {"cluster": cluster, "distance": float(dist)}

    report = {
        "num_records": len(records),
        "num_train": len(train_records),
        "num_test": len(test_records),
        "history": result.history,
        "train_metrics": train_metrics,
        "test_metrics": test_metrics,
        "sample_prediction_case": test_records[0].case_name if test_records else None,
        "sample_prediction": pred,
        "nearest_neighbors_true_space_sample": {k: nn[k] for k in list(nn)[:5]},
    }
    (output_dir / "training_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
