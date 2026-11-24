from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
import numpy as np
from sklearn.decomposition import PCA, FastICA
from sklearn.manifold import Isomap, LocallyLinearEmbedding

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
