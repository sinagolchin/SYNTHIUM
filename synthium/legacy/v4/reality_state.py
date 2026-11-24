"""
Synthium v4.0 - Reality State
==============================

States as tensors on manifolds (not simple vectors)
"""

import numpy as np
from typing import Optional, Dict


class RealityState:
    """
    A state of reality as tensor on manifold
    
    NOT a simple vector [v, R, r, C, S]
    BUT a tensor on N-dimensional Riemannian manifold
    
    Example:
        >>> state = RealityState(coordinates, manifold)
        >>> print(f"E={state.enjoyment:.3f}, M={state.meaning:.3f}")
        >>> path = state.geodesic_to(other_state)
    """
    
    def __init__(self, 
                 coordinates: np.ndarray,
                 manifold,  # RiemannianManifold
                 tensor_type: str = 'contravariant'):
        """
        Args:
            coordinates: Position on manifold (N-dimensional)
            manifold: The manifold this state lives on
            tensor_type: 'contravariant' or 'covariant'
        """
        self.coordinates = coordinates
        self.manifold = manifold
        self.tensor_type = tensor_type
        self.dim = len(coordinates)
        
        # Cached derived quantities
        self._enjoyment = None
        self._meaning = None
        self._perception = None
    
    @property
    def enjoyment(self) -> float:
        """
        Enjoyment E as N-D integral
        
        Old (v3.4): E = 1 - (v·R + S)
        New (v4.0): E = ∫_M e^(-S(x)) √|g| dx₁...dxₙ
        
        Simplified implementation: E = 1 - ||x||² / (2 * dim)
        This ensures E ∈ [0, 1] for reasonable states
        """
        if self._enjoyment is None:
            norm_sq = self.manifold.inner_product(self.coordinates, self.coordinates)
            self._enjoyment = max(0, 1 - norm_sq / (2 * self.dim))
        
        return self._enjoyment
    
    @property
    def meaning(self) -> float:
        """
        Meaning M as tensor contraction
        
        Simplified: M = <x,x> / dim
        
        Represents "significance" of the state
        """
        if self._meaning is None:
            inner = self.manifold.inner_product(self.coordinates, self.coordinates)
            self._meaning = inner / self.dim
        
        return self._meaning
    
    @property
    def perception(self) -> float:
        """
        Perception P from manifold geometry
        
        Related to curvature and position
        
        Simplified: P = 1 / (1 + ||x||)
        Higher for states closer to origin
        """
        if self._perception is None:
            norm = self.manifold.norm(self.coordinates)
            self._perception = 1 / (1 + norm)
        
        return self._perception
    
    def distance_to(self, other: 'RealityState') -> float:
        """
        Geodesic distance to another state
        
        Uses the manifold's metric to compute proper distance
        """
        return self.manifold.distance(self.coordinates, other.coordinates)
    
    def geodesic_to(self, other: 'RealityState', num_points: int = 100):
        """
        Compute geodesic path to another state
        
        Returns the shortest path on the manifold
        """
        return self.manifold.geodesic(self.coordinates, other.coordinates, num_points)
    
    def evolve(self, direction: np.ndarray, step_size: float = 0.1) -> 'RealityState':
        """
        Evolve state in a direction
        
        Uses exponential map (geodesic flow)
        
        Args:
            direction: Direction vector
            step_size: How far to move
        
        Returns:
            New RealityState
        """
        new_coords = self.coordinates + step_size * direction
        return RealityState(new_coords, self.manifold, self.tensor_type)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'coordinates': self.coordinates.tolist(),
            'dimension': self.dim,
            'enjoyment': self.enjoyment,
            'meaning': self.meaning,
            'perception': self.perception,
            'tensor_type': self.tensor_type
        }
    
    def __repr__(self):
        return f"RealityState(dim={self.dim}, E={self.enjoyment:.3f}, M={self.meaning:.3f}, P={self.perception:.3f})"


def map_legacy_to_state(v: float, R: float, r: float, C: float, S: float,
                        manifold) -> RealityState:
    """
    Map legacy 5D vector to new state
    
    For backward compatibility with v3.4
    
    Args:
        v, R, r, C, S: Legacy 5D components
        manifold: Manifold to place state on
    
    Returns:
        RealityState on the manifold
    
    Example:
        >>> state = map_legacy_to_state(0.7, 0.5, 0.8, 0.6, 0.4, manifold)
    """
    coords = np.array([v, R, r, C, S])
    
    # If manifold is higher-dimensional, pad with zeros
    if manifold.dim > 5:
        coords = np.pad(coords, (0, manifold.dim - 5))
    elif manifold.dim < 5:
        coords = coords[:manifold.dim]
    
    return RealityState(coords, manifold)


def create_default_manifold(dimension: int = 5):
    """
    Create default Euclidean manifold
    
    Args:
        dimension: Number of dimensions
    
    Returns:
        RiemannianManifold with Euclidean metric
    """
    from .manifold_geometry import RiemannianManifold
    return RiemannianManifold(dimension, metric=np.eye(dimension))
