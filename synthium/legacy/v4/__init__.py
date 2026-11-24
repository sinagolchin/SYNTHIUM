"""
Synthium v4.0 - Mathematical Framework for Reality
===================================================

N-dimensional differential geometry + tensor calculus + agnostic epistemology

Version: 4.0.0
Philosophy: Reality is an N-dimensional Riemannian manifold (discovered, not assumed)
"""

__version__ = "4.0.0"

# Mathematical Foundation
from .dimensional_discovery import DimensionalDiscoveryEngine, DimensionalAnalysis
from .manifold_geometry import RiemannianManifold, GeodesicPath, learn_metric_from_data
from .tensor_calculus import RealityTensor
from .infinite_calculus import InfiniteDerivativeChain, NDimensionalIntegral, integrate_along_path

# Core Framework
from .confidence import (
    ConfidenceLevel, 
    Confidence, 
    aggregate_confidence, 
    AXIOM_0_AGNOSTICISM, 
    FORMULA_CONFIDENCE
)
from .reality_state import RealityState, map_legacy_to_state, create_default_manifold

# Applications
from .applications import GoldAssistantV4, TradingDecision, CommunicationOptimizer


def discover_reality_dimensions(observations, method='pca', max_components=None):
    """
    Quick dimensional discovery
    
    Example:
        >>> import synthium as syn
        >>> result = syn.discover_reality_dimensions(data)
        >>> print(f"Found {result.intrinsic_dimensions} dimensions")
    """
    engine = DimensionalDiscoveryEngine()
    return engine.discover(observations, method, max_components)


def create_reality_manifold(data, metric_method='covariance'):
    """
    Quick manifold creation from data
    
    Example:
        >>> import synthium as syn
        >>> manifold = syn.create_reality_manifold(data)
        >>> distance = manifold.distance(state1, state2)
    """
    metric = learn_metric_from_data(data, metric_method)
    n_features = data.shape[1]
    return RiemannianManifold(n_features, metric)


def print_agnosticism_axiom():
    """Print Axiom 0 - The Foundation"""
    print(AXIOM_0_AGNOSTICISM)


# Package metadata
__all__ = [
    # Version
    '__version__',
    
    # Mathematical Foundation
    'DimensionalDiscoveryEngine',
    'DimensionalAnalysis',
    'RiemannianManifold',
    'GeodesicPath',
    'learn_metric_from_data',
    'RealityTensor',
    'InfiniteDerivativeChain',
    'NDimensionalIntegral',
    'integrate_along_path',
    
    # Core Framework
    'ConfidenceLevel',
    'Confidence',
    'aggregate_confidence',
    'AXIOM_0_AGNOSTICISM',
    'FORMULA_CONFIDENCE',
    'RealityState',
    'map_legacy_to_state',
    'create_default_manifold',
    
    # Applications
    'GoldAssistantV4',
    'TradingDecision',
    'CommunicationOptimizer',
    
    # Convenience Functions
    'discover_reality_dimensions',
    'create_reality_manifold',
    'print_agnosticism_axiom',
]


# Welcome message
def _print_welcome():
    """Print welcome message on import"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║                     Synthium v4.0 Loaded                       ║
║                                                                ║
║   Reality as N-Dimensional Riemannian Manifold                ║
║   Differential Geometry + Agnostic Epistemology                ║
╚════════════════════════════════════════════════════════════════╝

Quick Start:
  >>> import synthium as syn
  >>> result = syn.discover_reality_dimensions(data)
  >>> syn.print_agnosticism_axiom()

Run Demonstrations:
  $ python -m synthium.main
    """)

# Uncomment to show welcome message on import
# _print_welcome()
