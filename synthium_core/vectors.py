"""
SynthiumVector - The fundamental unit of consciousness quantification
Represents a point in 5D consciousness space
"""
from dataclasses import dataclass
from typing import Dict, Tuple
import math


@dataclass
class SynthiumVector:
    """
    A point in 5-dimensional consciousness space.

    Dimensions:
    - v: Velocity of movement (0=stuck, 1=rushing)
    - R: Resistance encountered (0=smooth, 1=blocked)
    - r: Resonance/connection (0=isolated, 1=connected)
    - C: Capacity to act (0=depleted, 1=full)
    - S: Entropy/chaos (0=ordered, 1=chaotic)
    """
    v: float  # Velocity
    R: float  # Resistance
    r: float  # Resonance
    C: float  # Capacity
    S: float  # Entropy

    def __post_init__(self):
        """Validate and clamp values to [0, 1] range"""
        self.v = max(0.0, min(1.0, self.v))
        self.R = max(0.0, min(1.0, self.R))
        self.r = max(0.0, min(1.0, self.r))
        self.C = max(0.0, min(1.0, self.C))
        self.S = max(0.0, min(1.0, self.S))

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary"""
        return {
            "v": round(self.v, 3),
            "R": round(self.R, 3),
            "r": round(self.r, 3),
            "C": round(self.C, 3),
            "S": round(self.S, 3)
        }

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'SynthiumVector':
        """Create from dictionary"""
        return cls(
            v=data.get("v", 0.5),
            R=data.get("R", 0.5),
            r=data.get("r", 0.5),
            C=data.get("C", 0.5),
            S=data.get("S", 0.5)
        )

    def distance_to(self, other: 'SynthiumVector') -> float:
        """Calculate Euclidean distance to another vector"""
        return math.sqrt(
            (self.v - other.v)**2 +
            (self.R - other.R)**2 +
            (self.r - other.r)**2 +
            (self.C - other.C)**2 +
            (self.S - other.S)**2
        )

    def similarity_to(self, other: 'SynthiumVector') -> float:
        """Calculate similarity (inverse of normalized distance)"""
        max_distance = math.sqrt(5)  # Maximum possible distance in 5D unit hypercube
        distance = self.distance_to(other)
        return 1.0 - (distance / max_distance)

    def magnitude(self) -> float:
        """Calculate vector magnitude"""
        return math.sqrt(self.v**2 + self.R**2 + self.r**2 + self.C**2 + self.S**2)

    def __repr__(self) -> str:
        return f"SynthiumVector(v={self.v:.2f}, R={self.R:.2f}, r={self.r:.2f}, C={self.C:.2f}, S={self.S:.2f})"

    def __str__(self) -> str:
        return f"[v:{self.v:.2f} R:{self.R:.2f} r:{self.r:.2f} C:{self.C:.2f} S:{self.S:.2f}]"


# Predefined states for common phenomena
PREDEFINED_VECTORS = {
    "flow": SynthiumVector(v=0.7, R=0.2, r=0.8, C=0.9, S=0.1),
    "burnout": SynthiumVector(v=0.9, R=0.8, r=0.3, C=0.1, S=0.8),
    "depression": SynthiumVector(v=0.1, R=0.7, r=0.2, C=0.2, S=0.6),
    "anxiety": SynthiumVector(v=0.8, R=0.6, r=0.4, C=0.5, S=0.8),
    "peace": SynthiumVector(v=0.3, R=0.1, r=0.7, C=0.8, S=0.1),
    "love": SynthiumVector(v=0.5, R=0.1, r=0.9, C=0.8, S=0.2),
    "grief": SynthiumVector(v=0.2, R=0.8, r=0.3, C=0.3, S=0.7),
    "joy": SynthiumVector(v=0.6, R=0.1, r=0.8, C=0.9, S=0.2),
    "confusion": SynthiumVector(v=0.5, R=0.5, r=0.4, C=0.5, S=0.9),
    "clarity": SynthiumVector(v=0.4, R=0.2, r=0.6, C=0.8, S=0.1),
}
