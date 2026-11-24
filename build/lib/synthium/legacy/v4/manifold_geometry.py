"""
Synthium v4.0 - Manifold Geometry
==================================

Reality as Riemannian manifold with metric tensor, geodesics, curvature
"""

import numpy as np
from typing import Optional
from dataclasses import dataclass


@dataclass
class GeodesicPath:
    """Geodesic path on manifold"""
    points: np.ndarray
    length: float
    parameterization: np.ndarray


class RiemannianManifold:
    """
    Reality as Riemannian manifold
    
    Metric tensor g_ij defines distance: ds² = g_ij dx^i dx^j
    
    Example:
        >>> manifold = RiemannianManifold(dimension=5, metric=learned_metric)
        >>> distance = manifold.distance(state_A, state_B)
        >>> path = manifold.geodesic(state_A, state_B)
    """
    
    def __init__(self, dimension: int, metric: Optional[np.ndarray] = None):
        """
        Args:
            dimension: Number of dimensions
            metric: Metric tensor g_ij (None = Euclidean)
        """
        self.dim = dimension
        
        if metric is None:
            # Default to Euclidean (flat) metric
            self.metric = np.eye(dimension)
        else:
            assert metric.shape == (dimension, dimension), "Metric must be dim x dim"
            assert np.allclose(metric, metric.T), "Metric must be symmetric"
            self.metric = metric
        
        # Inverse metric g^ij
        self.metric_inv = np.linalg.inv(self.metric)
    
    def distance(self, point1: np.ndarray, point2: np.ndarray) -> float:
        """
        Riemannian distance between two points
        
        d = sqrt((x1-x2)^T · g · (x1-x2))
        """
        diff = point2 - point1
        return np.sqrt(max(0, diff @ self.metric @ diff))
    
    def inner_product(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """
        Inner product of two vectors: <v,w> = g_ij v^i w^j
        """
        return v1 @ self.metric @ v2
    
    def norm(self, vector: np.ndarray) -> float:
        """Vector norm: ||v|| = sqrt(<v,v>)"""
        return np.sqrt(max(0, self.inner_product(vector, vector)))
    
    def geodesic(self, start: np.ndarray, end: np.ndarray,
                num_points: int = 100) -> GeodesicPath:
        """
        Compute geodesic (shortest path) between two points
        
        For flat/constant metric: geodesic = straight line
        For curved metric: would solve geodesic equation (simplified here)
        
        Args:
            start: Starting point
            end: Ending point
            num_points: Number of points along path
        
        Returns:
            GeodesicPath with points and length
        """
        # For constant metric, geodesic is straight line
        t = np.linspace(0, 1, num_points)
        points = np.outer(1-t, start) + np.outer(t, end)
        
        # Total length
        length = self.distance(start, end)
        
        return GeodesicPath(
            points=points,
            length=float(length),
            parameterization=t
        )
    
    def christoffel_symbols(self) -> np.ndarray:
        """
        Christoffel symbols Γ^i_jk
        
        For constant metric: Γ = 0
        For variable metric: Γ^i_jk = (1/2) g^il (∂g_lj/∂x^k + ∂g_lk/∂x^j - ∂g_jk/∂x^l)
        
        Returns:
            Array of shape (dim, dim, dim)
        """
        # For constant metric, all Christoffel symbols are zero
        return np.zeros((self.dim, self.dim, self.dim))
    
    def riemann_curvature(self) -> np.ndarray:
        """
        Riemann curvature tensor R^i_jkl
        
        For flat space: R = 0
        
        Returns:
            Array of shape (dim, dim, dim, dim)
        """
        # For flat space, curvature is zero
        return np.zeros((self.dim, self.dim, self.dim, self.dim))
    
    def scalar_curvature(self) -> float:
        """
        Scalar curvature R = g^ij R_ij
        
        For flat space: R = 0
        """
        return 0.0


def learn_metric_from_data(data: np.ndarray, method: str = 'covariance') -> np.ndarray:
    """
    Learn metric tensor from data
    
    Args:
        data: (n_samples, n_features) array of observations
        method: 'covariance' or 'mahalanobis'
    
    Returns:
        Metric tensor (n_features, n_features)
    
    Example:
        >>> metric = learn_metric_from_data(observations)
        >>> manifold = RiemannianManifold(10, metric)
    """
    n_samples, n_features = data.shape
    
    # Center data
    data_centered = data - data.mean(axis=0)
    
    # Compute covariance
    cov = (data_centered.T @ data_centered) / n_samples
    
    # Regularize to ensure invertibility
    cov += np.eye(n_features) * 1e-6
    
    if method == 'covariance':
        # Use covariance as metric
        return cov
    elif method == 'mahalanobis':
        # Use inverse covariance (precision matrix)
        return np.linalg.inv(cov)
    else:
        raise ValueError(f"Unknown method: {method}")
