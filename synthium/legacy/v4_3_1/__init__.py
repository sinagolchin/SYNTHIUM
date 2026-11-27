__version__ = "4.3.1-deleaked"

try:
    from .confidence import *
except Exception:
    pass
try:
    from .manifold_geometry import RiemannianManifold, learn_metric_from_data
except Exception:
    pass
try:
    from .dimensional_discovery import DimensionalDiscoveryEngine
except Exception:
    pass
try:
    from .domains.judicial import summarize_spec
except Exception:
    summarize_spec = None


def discover_reality_dimensions(observations, method='pca', max_components=None):
    engine = DimensionalDiscoveryEngine()
    return engine.discover(observations, method, max_components)


def create_reality_manifold(data, metric_method='covariance'):
    metric = learn_metric_from_data(data, metric_method)
    n_features = data.shape[1]
    return RiemannianManifold(n_features, metric)


def print_agnosticism_axiom():
    from .confidence import AXIOM_0_AGNOSTICISM
    print(AXIOM_0_AGNOSTICISM)
