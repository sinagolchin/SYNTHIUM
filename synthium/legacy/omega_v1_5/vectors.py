import math
from dataclasses import dataclass

@dataclass
class SynthiumVector:
    v: float  # Velocity
    R: float  # Resistance
    r: float  # Resonance
    C: float  # Capacity
    S: float  # Entropy

    def __post_init__(self):
        for name, value in self.__dict__.items():
            if not (0.0 <= value <= 1.0):
                raise ValueError(f"Component '{name}' must be 0-1. Got {value}")

    def magnitude(self) -> float:
        return math.sqrt(self.v**2 + self.R**2 + self.r**2 + self.C**2 + self.S**2)

    def distance_to(self, other: 'SynthiumVector') -> float:
        return math.sqrt(
            (self.v - other.v)**2 + (self.R - other.R)**2 +
            (self.r - other.r)**2 + (self.C - other.C)**2 +
            (self.S - other.S)**2
        )

    def is_coherent(self) -> bool:
        if self.v > 0.9 and self.R > 0.9:
            return False
        if self.S > 0.95 and self.C < 0.05:
            return False
        if self.r > 0.9 and self.v > 0.9:
            return False
        return True

    def __str__(self):
        return f"Vector(v={self.v:.2f}, R={self.R:.2f}, r={self.r:.2f}, C={self.C:.2f}, S={self.S:.2f})"
