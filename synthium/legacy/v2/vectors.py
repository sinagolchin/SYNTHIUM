import math
from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class RealityVector:
    """
    Unified 8D Reality Vector
    3D Spatial + 5D Qualitative = Complete reality description
    """
    # Spatial dimensions (meters from origin)
    x: float  # Position in space
    y: float
    z: float
    
    # Qualitative dimensions (normalized 0-1)
    v: float  # Velocity
    R: float  # Resistance
    r: float  # Resonance
    C: float  # Capacity
    S: float  # Entropy
    
    def __post_init__(self):
        """Validate all dimensions."""
        # Spatial: any real number allowed
        # Qualitative: must be 0-1
        for dim in ['v', 'R', 'r', 'C', 'S']:
            value = getattr(self, dim)
            if not (0.0 <= value <= 1.0):
                raise ValueError(f"Qualitative dimension '{dim}' must be 0-1. Got {value}")

    def spatial_part(self) -> Tuple[float, float, float]:
        """Get just the spatial coordinates."""
        return (self.x, self.y, self.z)
    
    def qualitative_part(self) -> Tuple[float, float, float, float, float]:
        """Get just the qualitative dimensions."""
        return (self.v, self.R, self.r, self.C, self.S)
    
    def distance_to(self, other: 'RealityVector') -> float:
        """Calculate 8D Euclidean distance."""
        spatial_dist = (self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2
        qual_dist = (self.v - other.v)**2 + (self.R - other.R)**2 + (self.r - other.r)**2 + \
                   (self.C - other.C)**2 + (self.S - other.S)**2
        return math.sqrt(spatial_dist + qual_dist)
    
    def spatial_distance(self, other: 'RealityVector') -> float:
        """Calculate only physical distance."""
        return math.sqrt((self.x - other.x)**2 + 
                        (self.y - other.y)**2 + 
                        (self.z - other.z)**2)
    
    def quality_distance(self, other: 'RealityVector') -> float:
        """Calculate only quality difference."""
        return math.sqrt((self.v - other.v)**2 + 
                        (self.R - other.R)**2 + 
                        (self.r - other.r)**2 +
                        (self.C - other.C)**2 + 
                        (self.S - other.S)**2)
    
    def is_coherent(self) -> Tuple[bool, List[str]]:
        """Check if vector represents a physically plausible reality state."""
        violations = []
        
        # Spatial-qualitative coherence checks
        if self.z < 0 and self.v > 0.8:  # Underground but fast-moving
            violations.append("High velocity underground")
        
        if abs(self.x) > 1000 or abs(self.y) > 1000 or abs(self.z) > 1000:
            if self.r > 0.9:  # Extreme distance but high resonance
                violations.append("High resonance at extreme distance")
        
        # Qualitative coherence
        if self.v > 0.9 and self.R > 0.9:
            violations.append("Energy paradox: v + R > 1.8")
        
        if self.S > 0.95 and self.C < 0.05:
            violations.append("Total decay without substrate")
        
        return (len(violations) == 0, violations)
    
    def to_dict(self):
        """Convert to dictionary for storage."""
        return {
            'x': self.x, 'y': self.y, 'z': self.z,
            'v': self.v, 'R': self.R, 'r': self.r, 'C': self.C, 'S': self.S
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary."""
        return cls(
            x=data['x'], y=data['y'], z=data['z'],
            v=data['v'], R=data['R'], r=data['r'], 
            C=data['C'], S=data['S']
        )
    
    def __str__(self):
        return f"RealityVector(Space:({self.x:.1f},{self.y:.1f},{self.z:.1f}) | Qualities:(v={self.v:.2f},R={self.R:.2f},r={self.r:.2f},C={self.C:.2f},S={self.S:.2f}))"


# For backward compatibility
@dataclass
class SynthiumVector:
    """Legacy 5D quality vector (for existing systems)."""
    v: float
    R: float
    r: float
    C: float
    S: float
    
    def __post_init__(self):
        for name, value in self.__dict__.items():
            if not (0.0 <= value <= 1.0):
                raise ValueError(f"Component '{name}' must be 0-1. Got {value}")
    
    def to_reality_vector(self, x=0.0, y=0.0, z=0.0) -> RealityVector:
        """Convert to full 8D vector at given location."""
        return RealityVector(x, y, z, self.v, self.R, self.r, self.C, self.S)
    
    def __str__(self):
        return f"SynthiumVector(v={self.v:.2f}, R={self.R:.2f}, r={self.r:.2f}, C={self.C:.2f}, S={self.S:.2f})"
