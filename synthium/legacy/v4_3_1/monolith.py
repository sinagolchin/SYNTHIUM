#!/usr/bin/env python3
"""SYNTHIUM v4.3.1 — SINGLE-FILE PROJECT BUNDLE.

A structural framework for CONSTRUCTING measurement rulers for abstract concepts.

Synthium is NOT a discovered theory of qualitative reality.
Synthium IS infrastructure for building, testing, and revising rulers that
attempt to measure qualitative phenomena (privacy, exception strength,
suppression pressure, correlation quality, semantic coherence, etc.).

Each unit is a PROPOSED measurement dimension, not an assumed coordinate.
Each formula is a FALSIFIABLE HYPOTHESIS, not a law.
Discovery claims, if they ever come, must be earned through reproducible
predictive success across independent data — not through architectural elegance.

----------------------------------------------------------------------------
CONTENTS
----------------------------------------------------------------------------
Synthium Core (universal layer):
    Confidence system with decay and aggregation
    Tensor calculus (rank-1 raise/lower)
    Riemannian manifold (constant or position-dependent metric)
    Reality state (semantic vs behavioral fusion)
    Robust derivatives + n-dimensional integration
    Dimensional discovery (PCA, ICA, Isomap, LLE) with bootstrap stability
    Governance engine with hysteresis and persistence escalation
    Anomaly governance monitor (baseline-driven application)

Domain layer:
    CourtListener API client
    Judicial subject core spec v0.2
    Judicial rubric (symbolic suppression pressure)
    Judicial atlas loader, tokenizer, vocab, collation

Optional neural layer (requires torch):
    Trainable text encoder with multi-head outputs
    Multi-objective Synthium loss (units, ops, outcome, metric, confidence, consistency)
    Training and evaluation utilities
    Original (leaky) training entry point — preserved for reproduction
    De-leaked training entry point — v4.3.1 canonical, see EMPIRICAL_STATUS.md

----------------------------------------------------------------------------
EMPIRICAL STATUS (v4.3.1)
----------------------------------------------------------------------------
The neural judicial encoder's original 0.727 test outcome accuracy was driven
by three data leaks: cluster name concatenated into the input text, outcome
words present in case summaries, and cluster labels used as positive-pair
signal in the contrastive loss. After removing these leaks, the same
architecture achieves 0.527 +/- 0.176 across 5 seeds, BELOW the 0.727
majority-class baseline. The framework currently has no validated outcome-
prediction claims at the available data scale. See run_deleaked() below.

----------------------------------------------------------------------------
QUICK START
----------------------------------------------------------------------------
    # Core demo (no torch needed):
    python synthium_v4_3_1.py --demo-core

    # Original (leaky) training run — reproduces v4.3 published number:
    python synthium_v4_3_1.py --train-original --epochs 180

    # De-leaked training run — v4.3.1 canonical, multi-seed:
    python synthium_v4_3_1.py --train-deleaked --epochs 180 --seeds 5

    # Where to put the atlas:
    #   ./data/judicial_suppression_atlas_v0_2.csv
    # (Override with --data /path/to/atlas.csv)
"""

# Stdlib imports (hoisted from all modules)
from __future__ import annotations
from dataclasses import dataclass, field, replace
from enum import Enum, IntEnum
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple
import argparse
import csv
import json
import math
import re
import time
import urllib.parse
import urllib.request

# Third-party imports (hoisted from all modules)
from scipy.integrate import trapezoid
from sklearn.decomposition import PCA, FastICA
from sklearn.manifold import Isomap, LocallyLinearEmbedding
import numpy as np

# Optional neural layer dependencies
try:
    import torch
    import torch.nn.functional as F
    from torch import nn
    from torch.optim import AdamW
    TORCH_AVAILABLE = True
except Exception:
    torch = None
    F = None
    nn = None
    AdamW = None
    TORCH_AVAILABLE = False

SYNTHIUM_VERSION = "4.3.1-deleaked"

# ==============================================================================
# 1. CONFIDENCE — Axiom 0, confidence levels, aggregation, formula registry
# ==============================================================================

class ConfidenceLevel(Enum):
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"
    SPECULATIVE = "SPECULATIVE"

@dataclass
class Confidence:
    level: ConfidenceLevel
    source: str
    limitations: List[str] = field(default_factory=list)
    numeric_score: Optional[float] = None
    source_type: str = "unspecified"
    age_steps: int = 0

    def decayed_score(self, decay_per_step: float = 0.02) -> float:
        base = self.numeric_score if self.numeric_score is not None else {
            ConfidenceLevel.HIGH: 0.9,
            ConfidenceLevel.MODERATE: 0.65,
            ConfidenceLevel.LOW: 0.35,
            ConfidenceLevel.SPECULATIVE: 0.15,
        }[self.level]
        return max(0.0, base * ((1.0 - decay_per_step) ** max(0, self.age_steps)))

AXIOM_0_AGNOSTICISM = """
AXIOM 0: AGNOSTICISM
ALL FORMULAS ARE HYPOTHESES, NOT TRUTHS.
Nothing in Synthium is absolute truth. We remain epistemically humble.
"""

def aggregate_confidence(confidences: List[Confidence]) -> Confidence:
    if not confidences:
        return Confidence(ConfidenceLevel.SPECULATIVE, "No data", ["No measurements available"], numeric_score=0.1)

    level_order = {
        ConfidenceLevel.HIGH: 3,
        ConfidenceLevel.MODERATE: 2,
        ConfidenceLevel.LOW: 1,
        ConfidenceLevel.SPECULATIVE: 0,
    }
    overall_level = min(confidences, key=lambda c: level_order[c.level]).level
    numeric = min(c.decayed_score() for c in confidences)
    sources = ", ".join(sorted(set(c.source for c in confidences)))
    limitations = sorted(set(item for c in confidences for item in c.limitations))
    return Confidence(
        level=overall_level,
        source=f"Aggregated from: {sources}",
        limitations=limitations,
        numeric_score=numeric,
        source_type="aggregated",
    )

class FormulaConfidenceRegistry:
    def __init__(self):
        self.registry = {}

    def register(self, formula_name: str, confidence: Confidence):
        self.registry[formula_name] = confidence

    def get(self, formula_name: str) -> Optional[Confidence]:
        return self.registry.get(formula_name)

FORMULA_CONFIDENCE = FormulaConfidenceRegistry()

# ==============================================================================
# 2. TENSOR CALCULUS — rank-1 tensor with metric raise/lower
# ==============================================================================

class RealityTensor:
    def __init__(self, data: np.ndarray, tensor_type: str = "contravariant"):
        arr = np.asarray(data, dtype=float)
        if arr.ndim != 1:
            raise ValueError("RealityTensor currently expects a rank-1 tensor (vector/covector).")
        self.data = arr
        self.tensor_type = tensor_type

    def raise_index(self, metric_inv: np.ndarray):
        if self.tensor_type == "covariant":
            self.data = np.asarray(metric_inv, dtype=float) @ self.data
            self.tensor_type = "contravariant"

    def lower_index(self, metric: np.ndarray):
        if self.tensor_type == "contravariant":
            self.data = np.asarray(metric, dtype=float) @ self.data
            self.tensor_type = "covariant"

# ==============================================================================
# 3. MANIFOLD GEOMETRY — Riemannian manifold with optional metric_field
# ==============================================================================

@dataclass
class GeodesicPath:
    points: np.ndarray
    length: float
    parameterization: np.ndarray
    local_lengths: np.ndarray

class RiemannianManifold:
    def __init__(self, dimension: int, metric: Optional[np.ndarray] = None, metric_field: Optional[Callable[[np.ndarray], np.ndarray]] = None):
        self.dim = dimension
        self.metric = np.eye(dimension) if metric is None else np.asarray(metric, dtype=float)
        self.metric_field = metric_field
        self.metric_inv = np.linalg.inv(self.metric)

    def metric_at(self, point: Optional[np.ndarray] = None) -> np.ndarray:
        if self.metric_field is not None and point is not None:
            g = np.asarray(self.metric_field(np.asarray(point, dtype=float)), dtype=float)
            return 0.5 * (g + g.T) + np.eye(self.dim) * 1e-8
        return self.metric

    def distance(self, point1: np.ndarray, point2: np.ndarray, num_points: int = 64) -> float:
        if self.metric_field is None:
            diff = np.asarray(point2) - np.asarray(point1)
            return float(np.sqrt(max(0.0, diff @ self.metric @ diff)))
        path = self.approximate_geodesic(np.asarray(point1), np.asarray(point2), num_points=num_points)
        return path.length

    def inner_product(self, v1: np.ndarray, v2: np.ndarray, point: Optional[np.ndarray] = None) -> float:
        g = self.metric_at(point)
        return float(np.asarray(v1) @ g @ np.asarray(v2))

    def norm(self, vector: np.ndarray, point: Optional[np.ndarray] = None) -> float:
        return float(np.sqrt(max(0.0, self.inner_product(vector, vector, point))))

    def approximate_geodesic(self, start: np.ndarray, end: np.ndarray, num_points: int = 100) -> GeodesicPath:
        t = np.linspace(0.0, 1.0, num_points)
        points = np.outer(1.0 - t, start) + np.outer(t, end)
        local_lengths = []
        for i in range(len(points) - 1):
            mid = 0.5 * (points[i] + points[i + 1])
            diff = points[i + 1] - points[i]
            g = self.metric_at(mid)
            local_lengths.append(np.sqrt(max(0.0, diff @ g @ diff)))
        ll = np.asarray(local_lengths, dtype=float)
        return GeodesicPath(points=points, length=float(ll.sum()), parameterization=t, local_lengths=ll)

    def geodesic(self, start: np.ndarray, end: np.ndarray, num_points: int = 100) -> GeodesicPath:
        return self.approximate_geodesic(start, end, num_points=num_points)

    def local_curvature_proxy(self, point: np.ndarray, eps: float = 1e-3) -> float:
        if self.metric_field is None:
            return 0.0
        point = np.asarray(point, dtype=float)
        g0 = self.metric_at(point)
        diffs = []
        for k in range(self.dim):
            p_plus = point.copy(); p_plus[k] += eps
            p_minus = point.copy(); p_minus[k] -= eps
            gp = self.metric_at(p_plus)
            gm = self.metric_at(p_minus)
            diffs.append(np.linalg.norm((gp - gm) / (2.0 * eps)))
        return float(np.mean(diffs) / (np.linalg.norm(g0) + 1e-12))

def learn_metric_from_data(data: np.ndarray, method: str = "covariance") -> np.ndarray:
    X = np.asarray(data, dtype=float)
    n_samples, _ = X.shape
    Xc = X - X.mean(axis=0)
    cov = (Xc.T @ Xc) / max(1, n_samples)
    cov = 0.5 * (cov + cov.T) + np.eye(cov.shape[0]) * 1e-6
    if method == "covariance":
        return cov
    if method == "mahalanobis":
        return np.linalg.inv(cov)
    raise ValueError(f"Unknown method: {method}")

# ==============================================================================
# 4. REALITY STATE — coordinates + fusion breakdown (semantic vs behavioral)
# ==============================================================================

@dataclass
class FusionBreakdown:
    semantic_integrity: float
    behavioral_integrity: float
    mismatch_penalty: float
    interaction_term: float
    fusion_score: float
    coordinate_contributions: Dict[str, list]

class RealityState:
    def __init__(self, coordinates: np.ndarray, manifold: RiemannianManifold, behavioral_coordinates: Optional[np.ndarray] = None, tensor_type: str = "contravariant", weights=(0.35, 0.35, 0.15, 0.15)):
        self.coordinates = np.asarray(coordinates, dtype=float)
        self.manifold = manifold
        self.tensor_type = tensor_type
        self.dim = len(self.coordinates)
        self.behavioral_coordinates = np.asarray(behavioral_coordinates, dtype=float) if behavioral_coordinates is not None else self.coordinates.copy()
        self.weights = weights
        self._breakdown: Optional[FusionBreakdown] = None

    @property
    def semantic_integrity(self) -> float:
        norm_sq = self.manifold.inner_product(self.coordinates, self.coordinates, self.coordinates)
        return float(max(0.0, 1.0 - (norm_sq / (2.0 * self.dim))))

    @property
    def behavioral_integrity(self) -> float:
        norm_sq = self.manifold.inner_product(self.behavioral_coordinates, self.behavioral_coordinates, self.behavioral_coordinates)
        return float(max(0.0, 1.0 - (norm_sq / (2.0 * self.dim))))

    @property
    def mismatch_score(self) -> float:
        diff = self.coordinates - self.behavioral_coordinates
        return float(min(1.0, self.manifold.norm(diff, 0.5 * (self.coordinates + self.behavioral_coordinates)) / (np.sqrt(self.dim) + 1e-9)))

    def fusion_breakdown(self) -> FusionBreakdown:
        if self._breakdown is None:
            w_sem, w_beh, w_inter, w_mis = self.weights
            s_sem = self.semantic_integrity
            s_beh = self.behavioral_integrity
            mismatch = self.mismatch_score
            interaction = min(s_sem, s_beh)
            fusion = max(0.0, min(1.0, (w_sem * s_sem) + (w_beh * s_beh) + (w_inter * interaction) - (w_mis * mismatch)))
            coord_delta = (self.coordinates - self.behavioral_coordinates).tolist()
            coord_energy = ((self.coordinates ** 2) - (self.behavioral_coordinates ** 2)).tolist()
            self._breakdown = FusionBreakdown(
                semantic_integrity=s_sem,
                behavioral_integrity=s_beh,
                mismatch_penalty=mismatch,
                interaction_term=interaction,
                fusion_score=fusion,
                coordinate_contributions={
                    "semantic_minus_behavioral": coord_delta,
                    "energy_difference": coord_energy,
                },
            )
        return self._breakdown

    @property
    def fusion_score(self) -> float:
        return self.fusion_breakdown().fusion_score

    def to_dict(self) -> Dict:
        br = self.fusion_breakdown()
        return {
            "coordinates": self.coordinates.tolist(),
            "behavioral_coordinates": self.behavioral_coordinates.tolist(),
            "dimension": self.dim,
            "semantic_integrity": br.semantic_integrity,
            "behavioral_integrity": br.behavioral_integrity,
            "mismatch_score": br.mismatch_penalty,
            "interaction_term": br.interaction_term,
            "fusion_score": br.fusion_score,
            "coordinate_contributions": br.coordinate_contributions,
        }

def map_legacy_to_state(v: float, R: float, r: float, C: float, S: float, manifold: RiemannianManifold) -> RealityState:
    coords = np.array([v, R, r, C, S], dtype=float)
    if manifold.dim > 5:
        coords = np.pad(coords, (0, manifold.dim - 5))
    elif manifold.dim < 5:
        coords = coords[: manifold.dim]
    return RealityState(coords, manifold)

def create_default_manifold(dimension: int = 5) -> RiemannianManifold:
    return RiemannianManifold(dimension, metric=np.eye(dimension))

# ==============================================================================
# 5. INFINITE CALCULUS — robust derivative chain, n-d integration
# ==============================================================================

@dataclass
class DerivativeEstimate:
    value: float
    uncertainty: float
    stable: bool

class RobustDerivativeChain:
    def __init__(self, base_function: Callable[[float], float], dt_candidates: Tuple[float, ...] = (1e-2, 5e-3, 1e-3)):
        self.base_function = base_function
        self.dt_candidates = dt_candidates
        self.estimates: Dict[int, DerivativeEstimate] = {}

    def compute(self, t: float, max_order: int = 6) -> Dict[int, DerivativeEstimate]:
        funcs: List[Callable[[float], float]] = [self.base_function]
        self.estimates = {0: DerivativeEstimate(float(self.base_function(t)), 0.0, True)}
        for order in range(1, max_order + 1):
            prev_f = funcs[-1]
            est = self._robust_derivative(prev_f, t)
            self.estimates[order] = est
            funcs.append(lambda x, f=prev_f: self._robust_derivative(f, x).value)
        return self.estimates

    def _robust_derivative(self, f: Callable[[float], float], x: float) -> DerivativeEstimate:
        vals = []
        for dt in self.dt_candidates:
            try:
                val = (f(x + dt) - f(x - dt)) / (2.0 * dt)
                if np.isfinite(val):
                    vals.append(float(val))
            except Exception:
                continue
        if not vals:
            return DerivativeEstimate(0.0, float("inf"), False)
        arr = np.asarray(vals)
        med = float(np.median(arr))
        mad = float(np.median(np.abs(arr - med)))
        stable = mad <= max(1e-6, 0.15 * (abs(med) + 1e-9))
        return DerivativeEstimate(med, mad, stable)

    def flatten_values(self) -> Dict[int, float]:
        return {k: v.value for k, v in self.estimates.items()}

    def chaos_score(self, order: int = 6) -> float:
        est = self.estimates.get(order)
        if est is None:
            return 0.0
        penalty = 2.0 if not est.stable else 1.0
        return abs(est.value) * penalty

class NDimensionalIntegral:
    @staticmethod
    def integrate_1d(f: Callable[[float], float], a: float, b: float, n_points: int = 1000) -> float:
        x = np.linspace(a, b, n_points)
        y = np.array([f(xi) for xi in x], dtype=float)
        return float(trapezoid(y, x))

    @staticmethod
    def integrate_nd(f: Callable[[np.ndarray], float], ranges: List[Tuple[float, float]], n_samples: int = 100000) -> float:
        samples = np.random.uniform(
            low=[r[0] for r in ranges],
            high=[r[1] for r in ranges],
            size=(n_samples, len(ranges)),
        )
        values = np.array([f(sample) for sample in samples], dtype=float)
        box_volume = np.prod([r[1] - r[0] for r in ranges])
        return float(box_volume * np.mean(values))

def integrate_along_path(f: Callable[[np.ndarray], float], path: np.ndarray) -> float:
    values = np.array([f(point) for point in path], dtype=float)
    segments = np.linalg.norm(np.diff(path, axis=0), axis=1)
    return float(np.sum((values[:-1] + values[1:]) * 0.5 * segments))

# ==============================================================================
# 6. DIMENSIONAL DISCOVERY — PCA, ICA, Isomap, LLE with stability scoring
# ==============================================================================

@dataclass
class DimensionalAnalysis:
    method: str
    intrinsic_dimensions: int
    total_dimensions: int
    explained_variance: np.ndarray
    components: np.ndarray
    loadings: Optional[np.ndarray]
    interpretations: List[str] = field(default_factory=list)
    confidence: float = 0.5
    stability_score: float = 0.0
    reconstruction_errors: Optional[np.ndarray] = None

class DimensionalDiscoveryEngine:
    def __init__(self, variance_threshold: float = 0.01, random_state: int = 42):
        self.variance_threshold = variance_threshold
        self.random_state = random_state
        self.history: List[DimensionalAnalysis] = []

    def discover(self, observations: np.ndarray, method: str = "pca", max_components: Optional[int] = None) -> DimensionalAnalysis:
        X = np.asarray(observations, dtype=float)
        n_samples, n_features = X.shape
        if max_components is None:
            max_components = min(n_samples, n_features)
        max_components = max(1, min(max_components, n_samples, n_features))
        methods = {
            "pca": self._pca,
            "ica": self._ica,
            "isomap": self._isomap,
            "lle": self._lle,
        }
        result = methods[method](X, max_components)
        self.history.append(result)
        return result

    def _standardize(self, X: np.ndarray) -> np.ndarray:
        return (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-10)

    def _elbow_dim(self, explained: np.ndarray) -> int:
        if len(explained) == 1:
            return 1
        drops = explained[:-1] - explained[1:]
        idx = int(np.argmax(drops)) + 1
        thresh_idx = int(np.sum(explained > self.variance_threshold))
        return max(1, min(max(idx, thresh_idx), len(explained)))

    def _bootstrap_pca_stability(self, X: np.ndarray, n: int, trials: int = 5) -> float:
        n_samples = len(X)
        dims = []
        for _ in range(trials):
            idx = np.random.randint(0, n_samples, size=n_samples)
            Xb = self._standardize(X[idx])
            pca = PCA(n_components=n, random_state=self.random_state)
            ev = pca.fit(Xb).explained_variance_ratio_
            dims.append(self._elbow_dim(ev))
        return 1.0 / (1.0 + np.std(dims))

    def _interpret_loadings(self, loadings: np.ndarray, top_k: int = 3) -> List[str]:
        out: List[str] = []
        for i, row in enumerate(loadings[: min(len(loadings), 5)]):
            top = np.argsort(np.abs(row))[-top_k:][::-1]
            out.append(f"Component {i+1}: strongest features {top.tolist()}")
        return out

    def _pca(self, X: np.ndarray, n: int) -> DimensionalAnalysis:
        Xs = self._standardize(X)
        pca = PCA(n_components=n, random_state=self.random_state)
        components = pca.fit_transform(Xs)
        explained = pca.explained_variance_ratio_
        intrinsic = self._elbow_dim(explained)
        stability = self._bootstrap_pca_stability(X, intrinsic)
        return DimensionalAnalysis(
            method="PCA",
            intrinsic_dimensions=intrinsic,
            total_dimensions=n,
            explained_variance=explained,
            components=components,
            loadings=pca.components_,
            interpretations=self._interpret_loadings(pca.components_),
            confidence=0.8,
            stability_score=float(stability),
        )

    def _ica(self, X: np.ndarray, n: int) -> DimensionalAnalysis:
        Xs = self._standardize(X)
        ica = FastICA(n_components=n, max_iter=1000, random_state=self.random_state)
        sources = ica.fit_transform(Xs)
        source_vars = np.var(sources, axis=0)
        explained = source_vars / (source_vars.sum() + 1e-12)
        intrinsic = self._elbow_dim(np.sort(explained)[::-1])
        return DimensionalAnalysis(
            method="ICA",
            intrinsic_dimensions=intrinsic,
            total_dimensions=n,
            explained_variance=explained,
            components=sources,
            loadings=ica.mixing_,
            interpretations=self._interpret_loadings(ica.mixing_.T if ica.mixing_ is not None else np.eye(n)),
            confidence=0.7,
            stability_score=0.6,
        )

    def _nonlinear_dim_scan(self, X: np.ndarray, method: str, n: int) -> tuple[int, np.ndarray, np.ndarray]:
        errors = []
        embeddings = []
        max_n = min(n, X.shape[1], max(2, len(X) - 1))
        for k in range(1, max_n + 1):
            if method == "isomap":
                model = Isomap(n_components=k, n_neighbors=min(10, len(X) - 1))
                emb = model.fit_transform(X)
                err = float(model.reconstruction_error())
            else:
                model = LocallyLinearEmbedding(n_components=k, n_neighbors=min(10, len(X) - 1), random_state=self.random_state)
                emb = model.fit_transform(X)
                err = float(np.mean((X - X.mean(axis=0)) ** 2)) if k == 1 else float(np.var(emb))
            errors.append(err)
            embeddings.append(emb)
        errors_arr = np.array(errors)
        improvement = np.r_[errors_arr[0] - errors_arr[1:], [0.0]] if len(errors_arr) > 1 else np.array([0.0])
        if method == "isomap":
            intrinsic = int(np.argmin(errors_arr)) + 1
        else:
            intrinsic = int(np.argmax(improvement[:-1]) + 1) if len(improvement) > 1 else 1
        intrinsic = max(1, min(intrinsic, len(embeddings)))
        return intrinsic, embeddings[intrinsic - 1], errors_arr

    def _isomap(self, X: np.ndarray, n: int) -> DimensionalAnalysis:
        intrinsic, emb, errors = self._nonlinear_dim_scan(X, "isomap", n)
        explained = np.ones(intrinsic) / intrinsic
        return DimensionalAnalysis(
            method="Isomap",
            intrinsic_dimensions=intrinsic,
            total_dimensions=n,
            explained_variance=explained,
            components=emb,
            loadings=None,
            interpretations=[f"Chosen dimension {intrinsic} from reconstruction error scan"],
            confidence=0.65,
            stability_score=0.55,
            reconstruction_errors=errors,
        )

    def _lle(self, X: np.ndarray, n: int) -> DimensionalAnalysis:
        intrinsic, emb, errors = self._nonlinear_dim_scan(X, "lle", n)
        explained = np.ones(intrinsic) / intrinsic
        return DimensionalAnalysis(
            method="LLE",
            intrinsic_dimensions=intrinsic,
            total_dimensions=n,
            explained_variance=explained,
            components=emb,
            loadings=None,
            interpretations=[f"Chosen dimension {intrinsic} from local reconstruction scan"],
            confidence=0.6,
            stability_score=0.5,
            reconstruction_errors=errors,
        )

# ==============================================================================
# 7. GOVERNANCE — risk scoring, hysteresis, action escalation
# ==============================================================================

class ActionLevel(IntEnum):
    ALLOW = 1
    WATCH = 2
    SHADOW_OBSERVE = 3
    COLLECT_EVIDENCE = 4
    STEP_UP_AUTH = 5
    SESSION_REVERIFY = 6
    QUEUE_REVIEW = 7
    HUMAN_REVIEW = 8
    BLOCK = 9
    PRIVILEGE_FREEZE = 10
    RMA_CONTAINMENT = 11

@dataclass
class GovernanceDecision:
    action: ActionLevel
    applied_friction_coefficient: float
    justification: str
    risk_score: float
    recommended_review_window: int = 0

@dataclass
class GovernanceState:
    last_action: ActionLevel = ActionLevel.ALLOW
    consecutive_high_risk: int = 0
    history: List[float] = field(default_factory=list)

class GovernanceEngine:
    def __init__(self, chaos_threshold: float = 1e6, hysteresis_margin: float = 0.15, history_window: int = 5):
        self.chaos_threshold = chaos_threshold
        self.hysteresis_margin = hysteresis_margin
        self.history_window = history_window
        self.state = GovernanceState()

    def evaluate_trajectory(self, derivatives: Dict[int, float], fusion_score: float, derivative_uncertainty: Optional[Dict[int, float]] = None, confidence: Optional[Confidence] = None) -> GovernanceDecision:
        derivative_uncertainty = derivative_uncertainty or {}
        pop = abs(derivatives.get(6, 0.0))
        velocity = abs(derivatives.get(1, 0.0))
        uncertainty_penalty = min(1.0, derivative_uncertainty.get(6, 0.0) / (abs(pop) + 1e-9)) if pop != 0 else 0.0
        conf_penalty = 0.0 if confidence is None else (1.0 - confidence.decayed_score())
        trend_term = self._update_history(pop)
        incoherence = 1.0 - max(0.0, min(1.0, fusion_score))

        risk_score = (
            0.45 * min(1.0, pop / self.chaos_threshold)
            + 0.15 * min(1.0, velocity / 10.0)
            + 0.20 * incoherence
            + 0.10 * uncertainty_penalty
            + 0.10 * conf_penalty
        )
        risk_score = min(1.0, risk_score + 0.1 * trend_term)

        proposed = self._risk_to_action(risk_score)
        action = self._apply_hysteresis(proposed, risk_score)
        if risk_score >= 0.75:
            self.state.consecutive_high_risk += 1
        else:
            self.state.consecutive_high_risk = 0
        action = self._escalate_for_persistence(action)
        self.state.last_action = action

        friction = min(1.0, (action.value - 1) / 10.0)
        review_window = max(1, int(10 * (1.0 - risk_score))) if action.value >= ActionLevel.COLLECT_EVIDENCE else 0
        justification = (
            f"risk={risk_score:.3f}, pop={pop:.2e}, velocity={velocity:.2f}, "
            f"fusion={fusion_score:.3f}, uncertainty_penalty={uncertainty_penalty:.3f}, "
            f"confidence_penalty={conf_penalty:.3f}, trend={trend_term:.3f}"
        )
        return GovernanceDecision(action, friction, justification, risk_score, review_window)

    def _update_history(self, pop: float) -> float:
        norm_pop = min(1.0, abs(pop) / self.chaos_threshold)
        self.state.history.append(norm_pop)
        self.state.history = self.state.history[-self.history_window :]
        if len(self.state.history) < 2:
            return norm_pop
        diffs = np.diff(self.state.history)
        upward = np.mean(np.maximum(diffs, 0.0))
        return float(min(1.0, upward + np.mean(self.state.history)))

    def _risk_to_action(self, risk: float) -> ActionLevel:
        if risk >= 0.98:
            return ActionLevel.RMA_CONTAINMENT
        if risk >= 0.90:
            return ActionLevel.PRIVILEGE_FREEZE
        if risk >= 0.82:
            return ActionLevel.BLOCK
        if risk >= 0.72:
            return ActionLevel.HUMAN_REVIEW
        if risk >= 0.62:
            return ActionLevel.QUEUE_REVIEW
        if risk >= 0.52:
            return ActionLevel.SESSION_REVERIFY
        if risk >= 0.42:
            return ActionLevel.STEP_UP_AUTH
        if risk >= 0.32:
            return ActionLevel.COLLECT_EVIDENCE
        if risk >= 0.22:
            return ActionLevel.SHADOW_OBSERVE
        if risk >= 0.12:
            return ActionLevel.WATCH
        return ActionLevel.ALLOW

    def _apply_hysteresis(self, proposed: ActionLevel, risk: float) -> ActionLevel:
        last = self.state.last_action
        if proposed.value < last.value and risk > max(0.0, (last.value - 1) / 10.0 - self.hysteresis_margin):
            return last
        return proposed

    def _escalate_for_persistence(self, action: ActionLevel) -> ActionLevel:
        if self.state.consecutive_high_risk >= 3 and action.value < ActionLevel.HUMAN_REVIEW:
            return ActionLevel.HUMAN_REVIEW
        if self.state.consecutive_high_risk >= 5 and action.value < ActionLevel.BLOCK:
            return ActionLevel.BLOCK
        return action

# ==============================================================================
# 8. APPLICATIONS — anomaly governance monitor (baseline-driven)
# ==============================================================================

@dataclass
class MonitoringDecision:
    decision: GovernanceDecision
    state_summary: Dict
    derivative_summary: Dict[int, float]
    uncertainty_summary: Dict[int, float]

class AnomalyGovernanceMonitor:
    def __init__(self, baseline_observations: np.ndarray, chaos_threshold: float = 1e4):
        metric = learn_metric_from_data(baseline_observations, method="mahalanobis")
        self.manifold = RiemannianManifold(baseline_observations.shape[1], metric=metric)
        self.governor = GovernanceEngine(chaos_threshold=chaos_threshold)
        self.confidence = Confidence(ConfidenceLevel.MODERATE, "Baseline-observation monitor", ["Thresholds heuristic"], numeric_score=0.65, source_type="empirical")

    def evaluate(self, semantic_coords: np.ndarray, behavioral_coords: np.ndarray, trajectory_fn: Callable[[float], float], t: float = 0.0) -> MonitoringDecision:
        state = RealityState(semantic_coords, self.manifold, behavioral_coords)
        chain = RobustDerivativeChain(trajectory_fn)
        estimates = chain.compute(t=t, max_order=6)
        derivs = {k: v.value for k, v in estimates.items()}
        uncert = {k: v.uncertainty for k, v in estimates.items()}
        decision = self.governor.evaluate_trajectory(derivs, state.fusion_score, derivative_uncertainty=uncert, confidence=self.confidence)
        return MonitoringDecision(decision, state.to_dict(), derivs, uncert)

# ==============================================================================
# 9. COURTLISTENER CLIENT — search-API helpers, urllib-based
# ==============================================================================

"""CourtListener API helpers.

This module is intentionally lightweight and uses urllib so the package has no
hard dependency on requests. It is designed for environments with network access.
"""


@dataclass
class CourtListenerSearchResult:
    case_name: str
    court: str
    date_filed: str
    docket_number: str
    absolute_url: str
    citation: str
    snippet: str
    raw: Dict


class CourtListenerClient:
    def __init__(self, api_token: Optional[str] = None, base_url: str = "https://www.courtlistener.com/api/rest/v4/search/"):
        self.api_token = api_token
        self.base_url = base_url

    def search(self, query: str, type_: str = "o", page_size: int = 10, **params) -> List[CourtListenerSearchResult]:
        q = {"q": query, "type": type_, "page_size": page_size}
        q.update({k: v for k, v in params.items() if v is not None})
        url = self.base_url + "?" + urllib.parse.urlencode(q)
        headers = {"User-Agent": "Synthium/4.3 neural research prototype"}
        if self.api_token:
            headers["Authorization"] = f"Token {self.api_token}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        results = data.get("results", data if isinstance(data, list) else [])
        return [self._parse_result(r) for r in results]

    def _parse_result(self, r: Dict) -> CourtListenerSearchResult:
        opinions = r.get("opinions") or []
        snippet = ""
        citation = ""
        if opinions and isinstance(opinions, list):
            snippet = opinions[0].get("snippet", "") or opinions[0].get("plain_text", "")[:500]
        citations = r.get("citation") or r.get("citations") or []
        if isinstance(citations, list):
            citation = "; ".join(str(x) for x in citations[:3])
        else:
            citation = str(citations)
        return CourtListenerSearchResult(
            case_name=r.get("caseName") or r.get("case_name") or "",
            court=r.get("court") or "",
            date_filed=r.get("dateFiled") or r.get("date_filed") or "",
            docket_number=r.get("docketNumber") or r.get("docket_number") or "",
            absolute_url=r.get("absolute_url") or r.get("absoluteUrl") or "",
            citation=citation,
            snippet=snippet,
            raw=r,
        )


def suppression_queries() -> List[str]:
    return [
        '"Fourth Amendment" "motion to suppress" "good faith"',
        '"Fourth Amendment" "exigent circumstances" "cell phone"',
        '"Fourth Amendment" curtilage suppression',
        '"Fourth Amendment" "geofence warrant"',
        '"Fourth Amendment" "private search"',
        '"Fourth Amendment" abandonment suppression',
        '"Fourth Amendment" "scope" "warrant" "cell phone"',
    ]

# ==============================================================================
# 10. JUDICIAL SPEC — units, operators, formula hierarchy, outcome classes
# ==============================================================================

"""Synthium Judicial Module Spec v0.2.

Domain instantiation for Fourth Amendment suppression doctrine.
This module does not replace Synthium Core. It supplies field-specific
units, operators, formula hierarchy, and confidence tags for one legal slice.
"""


class DiscoveryConfidence(str, Enum):
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    MODERATE_LOW = "MODERATE_LOW"
    LOW = "LOW"
    SPECULATIVE = "SPECULATIVE"


@dataclass(frozen=True)
class JudicialUnit:
    symbol: str
    name: str
    definition: str
    confidence: DiscoveryConfidence
    canonical: bool = True


@dataclass(frozen=True)
class JudicialOperator:
    key: str
    name: str
    definition: str
    formula: str
    confidence: DiscoveryConfidence


CANONICAL_UNITS: Tuple[str, ...] = (
    "Obs", "Priv", "Excp", "Rem", "Close", "Amb"
)

EXTENDED_UNITS: Tuple[str, ...] = (
    "Obs", "Priv", "Excp", "Rem", "Close", "Amb",
    "Temp", "Gate", "Bound", "Spec", "Scope", "JRem"
)

UNIT_DEFINITIONS: Dict[str, JudicialUnit] = {
    "Obs": JudicialUnit(
        "Obs", "Observability",
        "Direct lawful perceptual grounding behind state action.",
        DiscoveryConfidence.MODERATE,
    ),
    "Priv": JudicialUnit(
        "Priv", "Privacy legitimacy",
        "Baseline legal weight of the privacy interest before exceptions.",
        DiscoveryConfidence.HIGH,
    ),
    "Excp": JudicialUnit(
        "Excp", "Exception strength",
        "Force of a doctrine that transforms or overrides baseline privacy.",
        DiscoveryConfidence.HIGH,
    ),
    "Rem": JudicialUnit(
        "Rem", "Remedial proximity",
        "Closeness between possible violation and evidence sought to be excluded.",
        DiscoveryConfidence.HIGH,
    ),
    "Close": JudicialUnit(
        "Close", "Doctrinal closure",
        "Compression of judicial movement by precedent, statute, or settled doctrine.",
        DiscoveryConfidence.MODERATE,
    ),
    "Amb": JudicialUnit(
        "Amb", "Factual ambiguity",
        "Instability or contestability of key threshold facts.",
        DiscoveryConfidence.MODERATE,
    ),
    "Temp": JudicialUnit(
        "Temp", "Temporal admissibility distance",
        "Procedural-time distance between original act and later evidentiary use.",
        DiscoveryConfidence.MODERATE_LOW,
        canonical=False,
    ),
    "Gate": JudicialUnit(
        "Gate", "State-action gateway weight",
        "Degree to which Fourth Amendment scrutiny narrows because action is private.",
        DiscoveryConfidence.MODERATE_LOW,
        canonical=False,
    ),
    "Bound": JudicialUnit(
        "Bound", "Boundary reclassification weight",
        "Degree to which privacy status collapses after protected-zone reclassification.",
        DiscoveryConfidence.MODERATE,
        canonical=False,
    ),
    "Spec": JudicialUnit(
        "Spec", "Warrant specificity",
        "Particularity and data-scope precision of a warrant or authorization.",
        DiscoveryConfidence.MODERATE_LOW,
        canonical=False,
    ),
    "Scope": JudicialUnit(
        "Scope", "Authorization-scope fidelity",
        "Match between legal authorization granted and action actually taken.",
        DiscoveryConfidence.MODERATE,
        canonical=False,
    ),
    "JRem": JudicialUnit(
        "JRem", "Jurisdictional remedial regime",
        "Availability of local remedy dampers such as good faith.",
        DiscoveryConfidence.MODERATE_LOW,
        canonical=False,
    ),
}

OPERATOR_KEYS: Tuple[str, ...] = (
    "abandonment", "consent", "exigency", "good_faith", "attenuation",
    "private_search", "scope_breach", "curtilage", "emergency_aid",
    "public_exposure", "automobile_exception", "protective_sweep",
    "probation_waiver", "search_incident", "boundary_reclassification",
    "digital_privacy", "home_core", "warrant_particularity",
)

OPERATOR_DEFINITIONS: Dict[str, JudicialOperator] = {
    "exigency": JudicialOperator(
        "exigency", "Exigency dominance",
        "Urgency can dominate locally and raise effective exception strength.",
        "Excp_eff = max(Excp_base, Exigency_strength)",
        DiscoveryConfidence.HIGH,
    ),
    "good_faith": JudicialOperator(
        "good_faith", "Good-faith damping",
        "Reasonable reliance can reduce suppression pressure in jurisdictions permitting it.",
        "Damping_eff += GF_avail * GoodFaith",
        DiscoveryConfidence.HIGH,
    ),
    "abandonment": JudicialOperator(
        "abandonment", "Abandonment collapse",
        "Abandonment can collapse effective privacy sharply.",
        "Priv_eff = Priv_base * (1 - A)",
        DiscoveryConfidence.HIGH,
    ),
    "boundary_reclassification": JudicialOperator(
        "boundary_reclassification", "Boundary reclassification",
        "Place or object is classified outside the protected zone.",
        "Priv_eff = Priv_base * B",
        DiscoveryConfidence.HIGH,
    ),
    "private_search": JudicialOperator(
        "private_search", "Private-search gateway",
        "Private non-state search narrows the Fourth Amendment gateway.",
        "GatewayTransform = f(state_action_boundary)",
        DiscoveryConfidence.MODERATE,
    ),
    "scope_breach": JudicialOperator(
        "scope_breach", "Scope authorization breach",
        "State action exceeds the actual authorization granted.",
        "ScopeBreach = max(0, ActionDepth - AuthorizedDepth)",
        DiscoveryConfidence.MODERATE,
    ),
    "emergency_aid": JudicialOperator(
        "emergency_aid", "Emergency-aid scope limit",
        "Emergency aid may justify entry but not unrelated exploratory search.",
        "Excp_valid = EmergencyAid_strength * ScopeFit",
        DiscoveryConfidence.MODERATE,
    ),
    "public_exposure": JudicialOperator(
        "public_exposure", "Public exposure visibility",
        "Exposure to ordinary public view can reduce effective privacy.",
        "Priv_eff = Priv_base * ExposureShield",
        DiscoveryConfidence.MODERATE_LOW,
    ),
}

FORMULA_HIERARCHY: Tuple[str, ...] = (
    "J_case = [Obs, Priv, Excp, Rem, Close, Amb]",
    "J_case_ext = [Obs, Priv, Excp, Rem, Close, Amb, Temp, Gate, Bound, Spec, Scope, JRem]",
    "P0 = PrivacySurface(J_case_ext, t)",
    "P1 = BoundaryTransform(P0, Bound)",
    "P2 = ExceptionTransform(P1, Excp)",
    "P3 = GatewayTransform(P2, Gate)",
    "P4 = ScopeTransform(P3, Scope, Spec)",
    "Outcome ~= RemedyFilter(P4, Rem, JRem)",
)

OUTCOME_CLASSES: Tuple[str, ...] = (
    "DENIED", "GRANTED", "MIXED_REMAND", "PROCEDURAL", "UNKNOWN", "GRANTED_OR_REVERSED"
)


def summarize_spec() -> Dict[str, object]:
    return {
        "canonical_units": list(CANONICAL_UNITS),
        "extended_units": list(EXTENDED_UNITS),
        "operators": list(OPERATOR_KEYS),
        "formulas": list(FORMULA_HIERARCHY),
        "unit_confidence": {k: v.confidence.value for k, v in UNIT_DEFINITIONS.items()},
    }

# ==============================================================================
# 11. JUDICIAL RUBRIC — symbolic suppression-pressure formula
# ==============================================================================

"""Rubric and symbolic formulas for the Synthium judicial module."""


@dataclass(frozen=True)
class Band:
    low: float
    high: float
    label: str
    meaning: str


SCORING_BANDS = (
    Band(0.00, 0.19, "nearly_absent", "Nearly absent"),
    Band(0.20, 0.39, "weak", "Present but weak"),
    Band(0.40, 0.59, "moderate", "Moderate or mixed"),
    Band(0.60, 0.79, "strong", "Strong"),
    Band(0.80, 1.00, "dominant", "Very strong or dominant"),
)


def band_for(value: float) -> Band:
    value = max(0.0, min(1.0, float(value)))
    for band in SCORING_BANDS:
        if band.low <= value <= band.high:
            return band
    return SCORING_BANDS[-1]


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def effective_privacy(units: Mapping[str, float]) -> float:
    """Boundary-adjusted privacy value."""
    priv = float(units.get("Priv", 0.0))
    bound = float(units.get("Bound", 0.0))
    gate = float(units.get("Gate", 0.0))
    # Bound collapses privacy. Gate does not erase privacy, but narrows constitutional entry.
    return clamp01(priv * (1.0 - 0.85 * bound) * (1.0 - 0.45 * gate))


def effective_exception(units: Mapping[str, float], operators: Mapping[str, float]) -> float:
    excp = float(units.get("Excp", 0.0))
    if operators.get("exigency", 0.0) > 0.5:
        excp = max(excp, 0.82)
    if operators.get("consent", 0.0) > 0.5:
        excp = max(excp, 0.88)
    if operators.get("abandonment", 0.0) > 0.5:
        excp = max(excp, 0.92)
    if operators.get("search_incident", 0.0) > 0.5:
        excp = max(excp, 0.84)
    if operators.get("automobile_exception", 0.0) > 0.5:
        excp = max(excp, 0.75)
    return clamp01(excp)


def scope_breach(units: Mapping[str, float], operators: Mapping[str, float]) -> float:
    scope_fit = float(units.get("Scope", 0.75))
    spec = float(units.get("Spec", 0.70))
    breach = max(0.0, 1.0 - min(scope_fit, spec))
    if operators.get("scope_breach", 0.0) > 0.5:
        breach = max(breach, 0.75)
    return clamp01(breach)


def damping(units: Mapping[str, float], operators: Mapping[str, float]) -> float:
    gf_avail = float(units.get("JRem", 1.0))
    d = 0.0
    d += gf_avail * 0.72 * float(operators.get("good_faith", 0.0))
    d += 0.58 * float(operators.get("attenuation", 0.0))
    d += 0.35 * float(operators.get("private_search", 0.0))
    return clamp01(d)


def suppression_pressure(units: Mapping[str, float], operators: Mapping[str, float]) -> float:
    """Current symbolic Synthium formula for suppression pressure.

    This is a provisional hypothesis, not a validated legal estimator.
    """
    priv_eff = effective_privacy(units)
    excp_eff = effective_exception(units, operators)
    rem = float(units.get("Rem", 0.0))
    obs = float(units.get("Obs", 0.0))
    amb = float(units.get("Amb", 0.0))
    breach = scope_breach(units, operators)
    damp = damping(units, operators)

    violation_pressure = priv_eff * (1.0 - excp_eff) * (0.55 + 0.45 * breach)
    ambiguity_boost = 1.0 + 0.15 * amb
    observation_stabilizer = 1.0 - 0.12 * obs
    pressure = violation_pressure * rem * ambiguity_boost * observation_stabilizer * (1.0 - damp)
    # Scope breach can independently revive suppression pressure.
    pressure = max(pressure, 0.58 * breach * rem * (1.0 - damp))
    return clamp01(pressure)


def units_from_record(record: Mapping[str, object], unit_names: Iterable[str] = EXTENDED_UNITS) -> Dict[str, float]:
    return {name: float(record.get(name, 0.0)) for name in unit_names}


def operators_from_record(record: Mapping[str, object]) -> Dict[str, float]:
    return {k[3:]: float(v) for k, v in record.items() if k.startswith("op_")}

# ==============================================================================
# 12. JUDICIAL DATASET — atlas loader, tokenizer, vocab, collation
# ==============================================================================

"""Dataset utilities for the Synthium Judicial Module."""


def _resolve_default_atlas_path():
    here = Path(__file__).resolve().parent
    for candidate in (
        here / "data" / "judicial_suppression_atlas_v0_2.csv",
        here / "judicial_suppression_atlas_v0_2.csv",
        Path.cwd() / "data" / "judicial_suppression_atlas_v0_2.csv",
        Path.cwd() / "judicial_suppression_atlas_v0_2.csv",
    ):
        if candidate.exists():
            return candidate.resolve()
    return (here / "data" / "judicial_suppression_atlas_v0_2.csv").resolve()


DEFAULT_ATLAS_PATH = _resolve_default_atlas_path()

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

# ==============================================================================
# 13. NEURAL METRICS — MAE, RMSE, distance matrix, nearest neighbors
# ==============================================================================

"""Evaluation and distance utilities."""


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

# ==============================================================================
# 14. NEURAL ENCODER — JudicialNeuralEncoder + predict_dict (requires torch)
# ==============================================================================

"""Trainable neural encoders for Synthium."""


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

# ==============================================================================
# 15. NEURAL LOSSES — multi-objective Synthium loss (requires torch)
# ==============================================================================

"""Neural Synthium losses.

The core idea is multi-objective training: learn units, operators, outcomes,
metric embeddings, uncertainty, and symbolic formula consistency together.
"""


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

# ==============================================================================
# 16. NEURAL TRAINER — original training entry point (requires torch)
# ==============================================================================

"""Training helpers for neural Synthium models."""


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

# ==============================================================================
# 17. JUDICIAL TRAINING (ORIGINAL, with leaks — preserved for reproduction)
# ==============================================================================

"""CLI demo for training the Neural Judicial Encoder."""

# ==============================================================================
# 18. JUDICIAL TRAINING (DE-LEAKED, v4.3.1 canonical entry point)
# ==============================================================================

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

# ==============================================================================
# 19. UNIFIED CLI — pick a demo or a training run
# ==============================================================================


def _demo_core():
    """Run a small Core-only demo (no torch, no neural)."""
    print("=" * 70)
    print(f" SYNTHIUM {SYNTHIUM_VERSION} — Core demo")
    print("=" * 70)

    np.random.seed(42)
    baseline = np.random.randn(250, 5)
    engine = DimensionalDiscoveryEngine()
    analysis = engine.discover(baseline, method="pca", max_components=5)
    print(f"Discovered dimensions: {analysis.intrinsic_dimensions} via {analysis.method}")
    print(f"Stability score: {analysis.stability_score:.3f}")

    monitor = AnomalyGovernanceMonitor(baseline, chaos_threshold=5e2)
    semantic = np.array([0.4, 0.2, 0.1, 0.3, 0.2])
    behavioral = np.array([0.9, 0.2, 0.1, 0.8, 0.2])

    def trajectory(t):
        return np.sin(t) * np.exp(t / 3.0)

    report = monitor.evaluate(semantic, behavioral, trajectory, t=10.0)
    print(f"Fusion score: {report.state_summary['fusion_score']:.3f}")
    print(f"Mismatch score: {report.state_summary['mismatch_score']:.3f}")
    print(f"Governance action: {report.decision.action.name}")
    print(f"Risk score: {report.decision.risk_score:.3f}")


def _demo_judicial_spec():
    """Print the judicial subject-core specification."""
    print("=" * 70)
    print(f" SYNTHIUM {SYNTHIUM_VERSION} — Judicial subject core")
    print("=" * 70)
    print(json.dumps(summarize_spec(), indent=2))


def _print_axiom():
    print(AXIOM_0_AGNOSTICISM)
    print()
    print("v4.3.1 reframe:")
    print("Synthium is a ruler-building structure, not a discovered theory.")
    print("All units are constructed instruments. All formulas are testable hypotheses.")


def _cli():
    parser = argparse.ArgumentParser(
        description=f"Synthium {SYNTHIUM_VERSION} — single-file project bundle"
    )
    parser.add_argument("--axiom", action="store_true",
                        help="Print Axiom 0 and the v4.3.1 reframe.")
    parser.add_argument("--demo-core", action="store_true",
                        help="Run a Core-only demo (no torch needed).")
    parser.add_argument("--demo-judicial-spec", action="store_true",
                        help="Print the judicial subject-core specification.")
    parser.add_argument("--train-original", action="store_true",
                        help="Run the ORIGINAL (with leaks) judicial training. "
                             "Reproduces the v4.3 published number for comparison.")
    parser.add_argument("--train-deleaked", action="store_true",
                        help="Run the DE-LEAKED judicial training. "
                             "This is the v4.3.1 canonical entry point.")
    parser.add_argument("--data", type=str, default=None,
                        help="Path to judicial atlas CSV.")
    parser.add_argument("--epochs", type=int, default=180)
    parser.add_argument("--seeds", type=int, default=5)
    parser.add_argument("--output-dir", type=str, default="outputs_deleaked")
    args = parser.parse_args()

    if args.axiom:
        _print_axiom()
        return
    if args.demo_core:
        _demo_core()
        return
    if args.demo_judicial_spec:
        _demo_judicial_spec()
        return
    if args.train_original:
        if not TORCH_AVAILABLE:
            print("PyTorch is required for training. Install with: pip install torch")
            return
        # Use the original train.main() via a direct call
        _original_train_main(args)
        return
    if args.train_deleaked:
        if not TORCH_AVAILABLE:
            print("PyTorch is required for training. Install with: pip install torch")
            return
        _deleaked_train_main(args)
        return

    # No flag given — print help summary
    print(f"Synthium {SYNTHIUM_VERSION}")
    print()
    print("Synthium is a ruler-building structure for abstract concepts.")
    print("All formulas are testable hypotheses, not discovered laws.")
    print()
    print("Choose one of:")
    print("  --axiom                Print Axiom 0 and v4.3.1 reframe")
    print("  --demo-core            Core demo (no torch needed)")
    print("  --demo-judicial-spec   Print judicial subject-core spec")
    print("  --train-original       Reproduce v4.3 (with leaks) training")
    print("  --train-deleaked       Run v4.3.1 de-leaked training")
    print()
    print("See EMPIRICAL_STATUS.md for honest current empirical state.")


def _original_train_main(args):
    """Wrapper around the original training pipeline."""
    records = load_records(args.data)
    train_records, test_records = train_test_split_records(records, test_fraction=0.25, seed=42)
    result = train_judicial_encoder(train_records, epochs=args.epochs, seed=42, verbose=True)
    train_metrics = evaluate_judicial_encoder(result.model, result.vocab, train_records)
    test_metrics = evaluate_judicial_encoder(result.model, result.vocab, test_records)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "num_records": len(records),
        "num_train": len(train_records),
        "num_test": len(test_records),
        "train_metrics": train_metrics,
        "test_metrics": test_metrics,
        "warning": "This run preserves the v4.3 data leaks for reproduction. "
                   "See EMPIRICAL_STATUS.md and use --train-deleaked for the honest baseline.",
    }
    (output_dir / "original_training_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


def _deleaked_train_main(args):
    """Wrapper around the de-leaked training pipeline (v4.3.1 canonical)."""
    records = load_records_deleaked(args.data)
    print(f"Loaded {len(records)} records (cluster name dropped; outcome words redacted).")
    cls_counts = {}
    for r in records:
        cls_counts[OUTCOME_CLASSES[r.outcome_index]] = cls_counts.get(OUTCOME_CLASSES[r.outcome_index], 0) + 1
    print(f"Class distribution: {cls_counts}")

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
    _cli()
