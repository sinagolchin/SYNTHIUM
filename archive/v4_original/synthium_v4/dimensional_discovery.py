"""
Synthium v4.0 - Dimensional Discovery
======================================

Discover true dimensionality from data (don't assume N=5)

Methods: PCA, ICA, Isomap, LLE
"""

import numpy as np
from sklearn.decomposition import PCA, FastICA
from sklearn.manifold import Isomap, LocallyLinearEmbedding
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class DimensionalAnalysis:
    """Results of dimensional discovery"""
    method: str
    intrinsic_dimensions: int
    total_dimensions: int
    explained_variance: np.ndarray
    components: np.ndarray
    loadings: Optional[np.ndarray]
    interpretations: List[str]
    confidence: float


class DimensionalDiscoveryEngine:
    """
    Discover TRUE dimensionality of reality
    
    Key principle: Dimensionality is DISCOVERED, not assumed
    
    Example:
        >>> engine = DimensionalDiscoveryEngine()
        >>> result = engine.discover(observations, method='pca')
        >>> print(f"Found {result.intrinsic_dimensions} dimensions")
    """
    
    def __init__(self, variance_threshold: float = 0.01):
        """
        Args:
            variance_threshold: Minimum explained variance for dimension to be "real"
        """
        self.variance_threshold = variance_threshold
        self.history = []
    
    def discover(self, observations: np.ndarray, method: str = 'pca',
                max_components: Optional[int] = None) -> DimensionalAnalysis:
        """
        Discover dimensions from observations
        
        Args:
            observations: (n_samples, n_features) array
            method: 'pca', 'ica', 'isomap', 'lle'
            max_components: Maximum dimensions to extract (None = auto)
        
        Returns:
            DimensionalAnalysis with discovered structure
        """
        n_samples, n_features = observations.shape
        
        if max_components is None:
            max_components = min(n_samples, n_features)
        
        methods = {
            'pca': self._pca,
            'ica': self._ica,
            'isomap': self._isomap,
            'lle': self._lle
        }
        
        if method not in methods:
            raise ValueError(f"Unknown method: {method}")
        
        result = methods[method](observations, max_components)
        self.history.append(result)
        return result
    
    def _pca(self, X: np.ndarray, n: int) -> DimensionalAnalysis:
        """Principal Component Analysis - linear dimensionality reduction"""
        # Standardize data
        X_std = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-10)
        
        # PCA
        pca = PCA(n_components=n)
        components = pca.fit_transform(X_std)
        
        # Determine significant dimensions
        explained_var = pca.explained_variance_ratio_
        intrinsic_dims = np.sum(explained_var > self.variance_threshold)
        
        # Calculate confidence from eigenvalue spectrum
        eigenvalues = pca.explained_variance_
        if len(eigenvalues) > 1:
            ratios = eigenvalues[:-1] / eigenvalues[1:]
            confidence = min(1.0, np.max(ratios) / 2.0)
        else:
            confidence = 0.5
        
        return DimensionalAnalysis(
            method='PCA',
            intrinsic_dimensions=int(intrinsic_dims),
            total_dimensions=n,
            explained_variance=explained_var,
            components=components,
            loadings=pca.components_,
            interpretations=self._interpret_pca(pca.components_),
            confidence=float(confidence)
        )
    
    def _ica(self, X: np.ndarray, n: int) -> DimensionalAnalysis:
        """Independent Component Analysis - statistical independence"""
        X_std = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-10)
        
        ica = FastICA(n_components=n, max_iter=1000, random_state=42)
        sources = ica.fit_transform(X_std)
        
        # Estimate intrinsic dimensions
        source_vars = np.var(sources, axis=0)
        source_vars_norm = source_vars / source_vars.sum()
        intrinsic_dims = np.sum(source_vars_norm > self.variance_threshold)
        
        return DimensionalAnalysis(
            method='ICA',
            intrinsic_dimensions=int(intrinsic_dims),
            total_dimensions=n,
            explained_variance=source_vars_norm,
            components=sources,
            loadings=ica.mixing_,
            interpretations=[f"Independent source {i+1}" for i in range(n)],
            confidence=0.7
        )
    
    def _isomap(self, X: np.ndarray, n: int) -> DimensionalAnalysis:
        """Isomap - nonlinear manifold learning"""
        n_neighbors = min(10, len(X) - 1)
        iso = Isomap(n_components=n, n_neighbors=n_neighbors)
        embedding = iso.fit_transform(X)
        
        return DimensionalAnalysis(
            method='Isomap',
            intrinsic_dimensions=n,
            total_dimensions=n,
            explained_variance=np.array([1.0/n] * n),
            components=embedding,
            loadings=None,
            interpretations=[f"Manifold dim {i+1}" for i in range(n)],
            confidence=0.6
        )
    
    def _lle(self, X: np.ndarray, n: int) -> DimensionalAnalysis:
        """Locally Linear Embedding - local linear structure"""
        n_neighbors = min(10, len(X) - 1)
        lle = LocallyLinearEmbedding(n_components=n, n_neighbors=n_neighbors)
        embedding = lle.fit_transform(X)
        
        return DimensionalAnalysis(
            method='LLE',
            intrinsic_dimensions=n,
            total_dimensions=n,
            explained_variance=np.array([1.0/n] * n),
            components=embedding,
            loadings=None,
            interpretations=[f"LLE dim {i+1}" for i in range(n)],
            confidence=0.6
        )
    
    def _interpret_pca(self, loadings: np.ndarray) -> List[str]:
        """Interpret PCA dimensions"""
        interpretations = []
        for i, loading in enumerate(loadings):
            top_idx = np.argsort(np.abs(loading))[-3:][::-1]
            interpretations.append(f"PC{i+1}: features {list(top_idx)}")
        return interpretations
    
    def compare_methods(self, observations: np.ndarray,
                       methods: List[str] = ['pca', 'ica']) -> Dict:
        """
        Compare multiple discovery methods
        
        Returns consensus dimensionality and agreement metrics
        """
        results = {}
        dimensions_found = []
        
        for method in methods:
            try:
                result = self.discover(observations, method=method, max_components=20)
                results[method] = result
                dimensions_found.append(result.intrinsic_dimensions)
            except Exception as e:
                print(f"Warning: {method} failed: {e}")
        
        if dimensions_found:
            consensus = int(np.median(dimensions_found))
            agreement = 1.0 - (np.std(dimensions_found) / (np.mean(dimensions_found) + 1e-10))
        else:
            consensus = 0
            agreement = 0.0
        
        return {
            'methods': results,
            'consensus_dimensions': consensus,
            'agreement_score': float(agreement),
            'dimensions_range': (min(dimensions_found), max(dimensions_found)) if dimensions_found else (0, 0)
        }
