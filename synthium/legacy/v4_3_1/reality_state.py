from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional
import numpy as np
from .manifold_geometry import RiemannianManifold

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
