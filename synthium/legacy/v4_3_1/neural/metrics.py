"""Evaluation and distance utilities."""
from __future__ import annotations

from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.mean(np.abs(y_true - y_pred)))


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def euclidean_distance_matrix(X: np.ndarray) -> np.ndarray:
    diff = X[:, None, :] - X[None, :, :]
    return np.sqrt(np.sum(diff * diff, axis=-1))


def nearest_neighbors(X: np.ndarray, names: Sequence[str], k: int = 3) -> Dict[str, List[Tuple[str, float]]]:
    D = euclidean_distance_matrix(X)
    out: Dict[str, List[Tuple[str, float]]] = {}
    for i, name in enumerate(names):
        order = np.argsort(D[i])
        out[name] = [(names[j], float(D[i, j])) for j in order if j != i][:k]
    return out


def cluster_centroids(X: np.ndarray, clusters: Sequence[str]) -> Dict[str, np.ndarray]:
    clusters_arr = np.array(clusters)
    centroids = {}
    for c in sorted(set(clusters)):
        mask = clusters_arr == c
        centroids[c] = X[mask].mean(axis=0)
    return centroids


def nearest_centroid(x: np.ndarray, centroids: Dict[str, np.ndarray]) -> Tuple[str, float]:
    best_name = None
    best_dist = float("inf")
    for name, center in centroids.items():
        d = float(np.sqrt(np.sum((x - center) ** 2)))
        if d < best_dist:
            best_name, best_dist = name, d
    return str(best_name), best_dist
