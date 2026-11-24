"""
Synthium v4.0 - Tensor Calculus
================================

Proper tensor operations (contravariant/covariant)
"""

import numpy as np
from typing import Literal


class RealityTensor:
    """
    Reality state as tensor
    
    Contravariant (upper index): v^i - like velocity, transforms like dx
    Covariant (lower index): v_i - like gradient, transforms like ∂/∂x
    
    Example:
        >>> tensor = RealityTensor(components, 'contravariant')
        >>> tensor_lower = tensor.lower_index(metric)
    """
    
    def __init__(self, components: np.ndarray, 
                 index_type: Literal['contravariant', 'covariant'] = 'contravariant'):
        """
        Args:
            components: Tensor components
            index_type: 'contravariant' (upper ^) or 'covariant' (lower _)
        """
        self.components = components
        self.index_type = index_type
        self.rank = len(components.shape)
    
    def raise_index(self, metric_inv: np.ndarray) -> 'RealityTensor':
        """
        Raise index: v_i → v^i = g^ij v_j
        
        Convert covariant to contravariant
        
        Args:
            metric_inv: Inverse metric tensor g^ij
        
        Returns:
            New tensor with raised index
        """
        if self.index_type == 'contravariant':
            # Already contravariant
            return self
        
        if self.rank == 1:
            new_components = metric_inv @ self.components
        else:
            raise NotImplementedError("Only rank-1 tensors supported")
        
        return RealityTensor(new_components, 'contravariant')
    
    def lower_index(self, metric: np.ndarray) -> 'RealityTensor':
        """
        Lower index: v^i → v_i = g_ij v^j
        
        Convert contravariant to covariant
        
        Args:
            metric: Metric tensor g_ij
        
        Returns:
            New tensor with lowered index
        """
        if self.index_type == 'covariant':
            # Already covariant
            return self
        
        if self.rank == 1:
            new_components = metric @ self.components
        else:
            raise NotImplementedError("Only rank-1 tensors supported")
        
        return RealityTensor(new_components, 'covariant')
    
    def inner_product(self, other: 'RealityTensor', metric: np.ndarray) -> float:
        """
        Inner product: v^i w_i
        
        Requires one upper and one lower index (contract properly)
        
        Args:
            other: Another tensor
            metric: Metric tensor
        
        Returns:
            Scalar result
        """
        # Ensure we have one upper and one lower
        v_upper = self.raise_index(np.linalg.inv(metric)) if self.index_type == 'covariant' else self
        w_lower = other.lower_index(metric) if other.index_type == 'contravariant' else other
        
        return float(np.sum(v_upper.components * w_lower.components))
    
    def contract(self, other: 'RealityTensor') -> float:
        """
        Contract two tensors (simple dot product)
        
        For rank-1 tensors: Σ v^i w^i
        """
        if self.rank == 1 and other.rank == 1:
            return float(np.dot(self.components, other.components))
        else:
            raise NotImplementedError("Only rank-1 contraction supported")
    
    def tensor_product(self, other: 'RealityTensor') -> 'RealityTensor':
        """
        Tensor product (outer product): v ⊗ w
        
        Creates a rank-2 tensor
        """
        new_components = np.outer(self.components, other.components)
        return RealityTensor(new_components, self.index_type)
    
    def __repr__(self):
        index_symbol = '^' if self.index_type == 'contravariant' else '_'
        return f"Tensor{index_symbol}i (rank={self.rank}, shape={self.components.shape})"
