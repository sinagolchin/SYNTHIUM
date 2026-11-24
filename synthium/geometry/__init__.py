"""Synthium geometry: the V4 manifold, tensor and calculus ideas, fed with case scores.

Each case is a point. Each quality is a dimension. The number of dimensions is not
fixed in advance: the tools estimate how many the cases need.

EVERY RESULT IS UNTESTED. The scores are rankings from counted signs with no real unit
yet, and no number here has been checked on new cases.

Needs numpy (``pip install synthium[geometry]``). The original V4 code is archived,
unchanged, in ``archive/v4_original/``.
"""

from .calculus import (
    InfiniteDerivativeChain,
    derivative,
    derivative_chain,
    integrate_1d,
    integrate_along_path,
    integrate_nd,
    rate_along,
)
from .confidence import (
    AXIOM_0_AGNOSTICISM,
    FORMULA_CONFIDENCE,
    Confidence,
    ConfidenceLevel,
    aggregate_confidence,
)
from .dimensions import (
    BuildUp,
    build_up,
    choose_order,
    compare_domains,
    estimate_dimensions,
    is_new_dimension,
    parallel_analysis,
    participation_ratio,
    pca,
)
from .manifold import (
    GeodesicPath,
    RiemannianManifold,
    curvature_index,
    curvature_index_vs_shuffled,
    data_geodesics,
    learn_metric_from_data,
    pairwise_distances_missing,
)
from .metric_field import MetricField, metric_field_from_cases, sphere_metric
from .scores import CaseScores, load_cases, parse_score, standardise
from .tensor import RealityTensor
from .trajectory import CasePath, Stage, paths_from_staged_cells, staged_cells

__all__ = [n for n in dir() if not n.startswith("_")]
