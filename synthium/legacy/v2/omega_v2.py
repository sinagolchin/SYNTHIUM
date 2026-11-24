#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         SYNTHIUM OMEGA v2.0                                   ║
║                    UNIFIED 8D REALITY COMPILER                                ║
║                 "Mapping the Geometry of Existence"                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Dimensions: 3D Space (x,y,z) + 5D Qualities (v,R,r,C,S) = 8D Reality        ║
║                                                                               ║
║  v = Velocity      R = Resistance     r = Resonance                          ║
║  C = Capacity      S = Entropy                                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

Usage:
    python synthium_omega_v2.py

Author: Sina
License: Open Source
"""

import math
import json
import os
import re
import sys
import random
from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, List, Dict, Any, Optional


# =============================================================================
# VECTORS MODULE
# =============================================================================

@dataclass
class RealityVector:
    """
    Unified 8D Reality Vector
    3D Spatial + 5D Qualitative = Complete reality description
    """
    # Spatial dimensions (meters from origin)
    x: float
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
        
        if self.z < 0 and self.v > 0.8:
            violations.append("High velocity underground")
        
        if abs(self.x) > 1000 or abs(self.y) > 1000 or abs(self.z) > 1000:
            if self.r > 0.9:
                violations.append("High resonance at extreme distance")
        
        if self.v > 0.9 and self.R > 0.9:
            violations.append("Energy paradox: v + R > 1.8")
        
        if self.S > 0.95 and self.C < 0.05:
            violations.append("Total decay without substrate")
        
        return (len(violations) == 0, violations)
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary for storage."""
        return {
            'x': self.x, 'y': self.y, 'z': self.z,
            'v': self.v, 'R': self.R, 'r': self.r, 'C': self.C, 'S': self.S
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'RealityVector':
        """Create from dictionary."""
        return cls(
            x=data['x'], y=data['y'], z=data['z'],
            v=data['v'], R=data['R'], r=data['r'], 
            C=data['C'], S=data['S']
        )
    
    def __str__(self):
        return f"RealityVector(Space:({self.x:.1f},{self.y:.1f},{self.z:.1f}) | Quality:(v={self.v:.2f},R={self.R:.2f},r={self.r:.2f},C={self.C:.2f},S={self.S:.2f}))"


@dataclass
class SynthiumVector:
    """Legacy 5D quality vector (for backward compatibility)."""
    v: float
    R: float
    r: float
    C: float
    S: float
    
    def __post_init__(self):
        for name, value in self.__dict__.items():
            if not (0.0 <= value <= 1.0):
                raise ValueError(f"Component '{name}' must be 0-1. Got {value}")
    
    def to_reality_vector(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> RealityVector:
        """Convert to full 8D vector at given location."""
        return RealityVector(x, y, z, self.v, self.R, self.r, self.C, self.S)
    
    def magnitude(self) -> float:
        """Calculate 5D magnitude."""
        return math.sqrt(self.v**2 + self.R**2 + self.r**2 + self.C**2 + self.S**2)
    
    def __str__(self):
        return f"SynthiumVector(v={self.v:.2f}, R={self.R:.2f}, r={self.r:.2f}, C={self.C:.2f}, S={self.S:.2f})"


# =============================================================================
# TRANSDUCER MODULE
# =============================================================================

class Transducer:
    """Converts descriptions to 8D RealityVectors."""
    
    QUALITY_KEYWORDS = {
        'v': ['fast', 'quick', 'speed', 'velocity', 'dynamic', 'moving', 'rapid'],
        'R': ['heavy', 'resistant', 'dense', 'solid', 'stuck', 'blocked', 'slow'],
        'r': ['vibrant', 'resonant', 'connected', 'harmonic', 'attractive', 'magnetic'],
        'C': ['deep', 'capacity', 'large', 'full', 'potential', 'room', 'vast'],
        'S': ['chaotic', 'random', 'entropy', 'decay', 'disorder', 'noise', 'turbulent']
    }
    
    SPATIAL_CONTEXT = {
        'high': {'z': 10.0}, 'low': {'z': -5.0}, 'center': {'x': 0, 'y': 0},
        'north': {'y': 10.0}, 'south': {'y': -10.0}, 
        'east': {'x': 10.0}, 'west': {'x': -10.0},
        'underground': {'z': -10.0}, 'above': {'z': 20.0}, 'surface': {'z': 0}
    }
    
    EMOTIONAL_PROFILES = {
        'grief': {'v': 0.1, 'R': 0.9, 'r': 0.2, 'C': 0.8, 'S': 0.4},
        'joy': {'v': 0.7, 'R': 0.1, 'r': 0.8, 'C': 0.6, 'S': 0.1},
        'anxiety': {'v': 0.8, 'R': 0.6, 'r': 0.2, 'C': 0.3, 'S': 0.7},
        'anger': {'v': 0.9, 'R': 0.7, 'r': 0.1, 'C': 0.4, 'S': 0.6},
        'love': {'v': 0.3, 'R': 0.1, 'r': 0.95, 'C': 0.8, 'S': 0.1},
        'frustration': {'v': 0.3, 'R': 0.85, 'r': 0.2, 'C': 0.5, 'S': 0.7},
        'embarrassment': {'v': 0.45, 'R': 0.75, 'r': 0.55, 'C': 0.35, 'S': 0.85},
        'calm': {'v': 0.2, 'R': 0.3, 'r': 0.6, 'C': 0.7, 'S': 0.1},
        'fear': {'v': 0.7, 'R': 0.8, 'r': 0.1, 'C': 0.2, 'S': 0.8},
        'hope': {'v': 0.5, 'R': 0.2, 'r': 0.7, 'C': 0.9, 'S': 0.2},
        'despair': {'v': 0.05, 'R': 0.95, 'r': 0.1, 'C': 0.9, 'S': 0.6},
        'excitement': {'v': 0.9, 'R': 0.2, 'r': 0.7, 'C': 0.5, 'S': 0.4},
        'peace': {'v': 0.1, 'R': 0.2, 'r': 0.8, 'C': 0.7, 'S': 0.05},
        'confusion': {'v': 0.6, 'R': 0.5, 'r': 0.3, 'C': 0.4, 'S': 0.9}
    }
    
    def quantify(self, description: str, 
                 location: Tuple[float, float, float] = (0.0, 0.0, 0.0)) -> RealityVector:
        """Convert description to 8D RealityVector at given location."""
        x, y, z = location
        desc_lower = description.lower()
        
        x, y, z = self._extract_spatial_context(desc_lower, x, y, z)
        qualities = self._analyze_qualities(desc_lower)
        
        return RealityVector(x, y, z, **qualities)
    
    def quantify_quality_only(self, description: str) -> SynthiumVector:
        """Legacy: Convert description to 5D quality vector only."""
        qualities = self._analyze_qualities(description.lower())
        return SynthiumVector(**qualities)
    
    def _extract_spatial_context(self, text: str, 
                                default_x: float, 
                                default_y: float, 
                                default_z: float) -> Tuple[float, float, float]:
        """Extract spatial coordinates from text descriptions."""
        x, y, z = default_x, default_y, default_z
        
        for keyword, offsets in self.SPATIAL_CONTEXT.items():
            if keyword in text:
                x += offsets.get('x', 0)
                y += offsets.get('y', 0)
                z += offsets.get('z', 0)
        
        coord_pattern = r'(\d+(?:\.\d+)?) meters? (north|south|east|west|up|down)'
        matches = re.findall(coord_pattern, text)
        
        for dist_str, direction in matches:
            dist = float(dist_str)
            if direction == 'north': y += dist
            elif direction == 'south': y -= dist
            elif direction == 'east': x += dist
            elif direction == 'west': x -= dist
            elif direction == 'up': z += dist
            elif direction == 'down': z -= dist
        
        return (x, y, z)
    
    def _analyze_qualities(self, text: str) -> Dict[str, float]:
        """Analyze text to extract 5D quality scores."""
        for emotion, profile in self.EMOTIONAL_PROFILES.items():
            if emotion in text:
                return profile.copy()
        
        scores = {'v': 0.5, 'R': 0.5, 'r': 0.5, 'C': 0.5, 'S': 0.5}
        
        for dim, keywords in self.QUALITY_KEYWORDS.items():
            dim_score = 0
            matches = 0
            for keyword in keywords:
                if keyword in text:
                    dim_score += 2
                    matches += 1
            if matches > 0:
                scores[dim] = min(1.0, dim_score / (matches * 2))
        
        return scores


# =============================================================================
# HOLISTIC SCIENCE MODULE
# =============================================================================

class HolisticScience:
    """Unified physics engine for 8D reality space."""
    
    def analyze_reality_vector(self, vector: RealityVector) -> Dict[str, Any]:
        """Comprehensive analysis of an 8D reality vector."""
        spatial_magnitude = math.sqrt(vector.x**2 + vector.y**2 + vector.z**2)
        quality_magnitude = math.sqrt(vector.v**2 + vector.R**2 + vector.r**2 + 
                                     vector.C**2 + vector.S**2)
        
        reality_density = (vector.R * vector.C) / (spatial_magnitude + 0.001)
        information_potential = vector.C * (1 - vector.S)
        energy_flux = vector.v * vector.r
        
        coherent, violations = vector.is_coherent()
        formulas = self._derive_spatial_formulas(vector)
        
        return {
            "spatial_magnitude": f"{spatial_magnitude:.2f} m from origin",
            "quality_magnitude": f"{quality_magnitude:.2f} (intensity)",
            "reality_density": f"{reality_density:.3f} kg/m³ equivalent",
            "information_potential": f"{information_potential:.3f} bits",
            "energy_flux": f"{energy_flux:.3f} J/s·m² equivalent",
            "coherent": coherent,
            "violations": violations,
            "derived_formulas": formulas,
            "spatial_zone": self._classify_spatial_zone(vector),
            "quality_type": self._classify_quality(vector)
        }
    
    def analyze_spatial_quality_field(self, vectors: List[RealityVector]) -> Dict[str, Any]:
        """Analyze how qualities vary across space."""
        if not vectors:
            return {"error": "No vectors provided"}
        
        return {
            "spatial_gradients": self._calculate_gradients(vectors),
            "quality_hotspots": self._find_extrema(vectors),
            "field_coherence": self._field_coherence(vectors),
            "total_points": len(vectors),
            "spatial_bounds": self._spatial_bounds(vectors),
            "quality_variance": self._quality_variance(vectors)
        }
    
    def _derive_spatial_formulas(self, vector: RealityVector) -> List[str]:
        """Derive formulas that include spatial context."""
        formulas = []
        
        if vector.z < 0:
            formulas.append(f"Pressure = R × |z| = {vector.R * abs(vector.z):.1f} Pa")
        
        horizontal_dist = math.sqrt(vector.x**2 + vector.y**2)
        if horizontal_dist > 10:
            formulas.append(f"Field_strength = r / distance = {vector.r / (horizontal_dist + 0.001):.3f}")
        
        if vector.R > 0.6 and vector.C > 0.6:
            formulas.append(f"Mass_density = R × C = {vector.R * vector.C:.3f}")
        
        if vector.v > 0.7:
            if vector.R < 0.3:
                formulas.append(f"Flow_potential = v²/R = {(vector.v**2) / (vector.R + 0.001):.3f}")
            else:
                formulas.append(f"Friction_loss = v × R = {vector.v * vector.R:.3f}")
        
        if vector.r > 0.7:
            total_dist = math.sqrt(vector.x**2 + vector.y**2 + vector.z**2)
            formulas.append(f"Attraction_range = r × d = {vector.r * total_dist:.1f} m")
        
        if vector.S > 0.7:
            formulas.append(f"Entropy_gradient = S/|z| = {vector.S / (abs(vector.z) + 0.001):.3f}")
        
        return formulas if formulas else ["Complex_8D = f(x,y,z,v,R,r,C,S)"]
    
    def _calculate_gradients(self, vectors: List[RealityVector]) -> Dict[str, str]:
        """Calculate how qualities change with position."""
        if len(vectors) < 2:
            return {"insufficient_data": "Need at least 2 points"}
        
        gradients = {}
        for dim in ['v', 'R', 'r', 'C', 'S']:
            values = [(getattr(v, dim), (v.x, v.y, v.z)) for v in vectors]
            max_val, max_pos = max(values, key=lambda x: x[0])
            min_val, min_pos = min(values, key=lambda x: x[0])
            
            dist = math.sqrt((max_pos[0]-min_pos[0])**2 + 
                           (max_pos[1]-min_pos[1])**2 + 
                           (max_pos[2]-min_pos[2])**2)
            
            if dist > 0:
                gradient = (max_val - min_val) / dist
                gradients[dim] = f"{gradient:.4f} per meter"
            else:
                gradients[dim] = "uniform"
        
        return gradients
    
    def _classify_spatial_zone(self, vector: RealityVector) -> str:
        """Classify the spatial location."""
        radius = math.sqrt(vector.x**2 + vector.y**2 + vector.z**2)
        
        if vector.z < -10: return "Deep Underground"
        elif vector.z < 0: return "Subsurface"
        elif vector.z < 10: return "Surface Level"
        elif vector.z < 100: return "Elevated"
        elif radius > 1000: return "Distant"
        else: return "Local"
    
    def _classify_quality(self, vector: RealityVector) -> str:
        """Classify the quality pattern."""
        if vector.S > 0.8: return "Chaotic Field"
        elif vector.r > 0.8: return "Resonance Field"
        elif vector.R > 0.8: return "Resistance Field"
        elif vector.v > 0.8: return "Velocity Field"
        elif vector.C > 0.8: return "Capacity Field"
        else: return "Mixed Quality Field"
    
    def _find_extrema(self, vectors: List[RealityVector]) -> Dict[str, Any]:
        """Find locations of maximum quality values."""
        if not vectors:
            return {}
        
        extrema = {}
        for dim in ['v', 'R', 'r', 'C', 'S']:
            max_vector = max(vectors, key=lambda v: getattr(v, dim))
            extrema[f"max_{dim}"] = {
                "value": round(getattr(max_vector, dim), 3),
                "location": (round(max_vector.x, 1), round(max_vector.y, 1), round(max_vector.z, 1))
            }
        return extrema
    
    def _field_coherence(self, vectors: List[RealityVector]) -> float:
        """Calculate how coherent the field is (0-1)."""
        if len(vectors) < 2:
            return 1.0
        
        coherent_count = sum(1 for v in vectors if v.is_coherent()[0])
        return round(coherent_count / len(vectors), 3)
    
    def _spatial_bounds(self, vectors: List[RealityVector]) -> Dict[str, Any]:
        """Calculate spatial bounds of the field."""
        if not vectors:
            return {"min": (0,0,0), "max": (0,0,0)}
        
        xs = [v.x for v in vectors]
        ys = [v.y for v in vectors]
        zs = [v.z for v in vectors]
        
        return {
            "min": (min(xs), min(ys), min(zs)),
            "max": (max(xs), max(ys), max(zs)),
            "center": ((max(xs)+min(xs))/2, (max(ys)+min(ys))/2, (max(zs)+min(zs))/2)
        }
    
    def _quality_variance(self, vectors: List[RealityVector]) -> Dict[str, str]:
        """Calculate variance of each quality dimension."""
        if len(vectors) < 2:
            return {}
        
        variances = {}
        for dim in ['v', 'R', 'r', 'C', 'S']:
            values = [getattr(v, dim) for v in vectors]
            mean = sum(values) / len(values)
            variance = sum((x - mean) ** 2 for x in values) / len(values)
            variances[dim] = f"{variance:.4f}"
        return variances


# =============================================================================
# REALITY FIELD MODULE
# =============================================================================

class RealityField:
    """Represents a quality field across space."""
    
    def __init__(self, name: str):
        self.name = name
        self.vectors: List[RealityVector] = []
        self.metadata = {
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat(),
            "description": "",
            "bounds": {"min": (0,0,0), "max": (0,0,0)},
            "quality_types": set()
        }
    
    def add_vector(self, vector: RealityVector):
        """Add a reality vector to the field."""
        self.vectors.append(vector)
        self.metadata["modified"] = datetime.now().isoformat()
        
        if len(self.vectors) == 1:
            self.metadata["bounds"]["min"] = (vector.x, vector.y, vector.z)
            self.metadata["bounds"]["max"] = (vector.x, vector.y, vector.z)
        else:
            min_b = self.metadata["bounds"]["min"]
            max_b = self.metadata["bounds"]["max"]
            self.metadata["bounds"]["min"] = (min(min_b[0], vector.x), min(min_b[1], vector.y), min(min_b[2], vector.z))
            self.metadata["bounds"]["max"] = (max(max_b[0], vector.x), max(max_b[1], vector.y), max(max_b[2], vector.z))
        
        if vector.S > 0.5: self.metadata["quality_types"].add("chaotic")
        if vector.r > 0.5: self.metadata["quality_types"].add("resonant")
        if vector.R > 0.5: self.metadata["quality_types"].add("resistant")
    
    def get_vectors_near(self, x: float, y: float, z: float, radius: float = 1.0) -> List[RealityVector]:
        """Get vectors within radius of a point."""
        return [v for v in self.vectors 
                if math.sqrt((v.x-x)**2 + (v.y-y)**2 + (v.z-z)**2) <= radius]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert field to dictionary for storage."""
        meta = self.metadata.copy()
        meta["quality_types"] = list(self.metadata["quality_types"])
        return {"name": self.name, "metadata": meta, "vectors": [v.to_dict() for v in self.vectors]}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RealityField':
        """Create field from dictionary."""
        field = cls(data["name"])
        field.metadata = data["metadata"]
        if isinstance(field.metadata.get("quality_types"), list):
            field.metadata["quality_types"] = set(field.metadata["quality_types"])
        field.vectors = [RealityVector.from_dict(v) for v in data["vectors"]]
        return field


# =============================================================================
# RECORDER MODULE
# =============================================================================

class Recorder:
    """Manages quality lexicon and reality fields persistence."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.lexicon_path = os.path.join(data_dir, "lexicon.json")
        self.fields_path = os.path.join(data_dir, "reality_fields")
        self._ensure_directories()
        self._ensure_lexicon_exists()
    
    def _ensure_directories(self):
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.fields_path, exist_ok=True)
    
    def _ensure_lexicon_exists(self):
        if not os.path.exists(self.lexicon_path):
            with open(self.lexicon_path, "w") as f:
                json.dump({
                    "meta": {"version": "2.0", "created": datetime.now().isoformat()},
                    "qualities": []
                }, f, indent=2)
    
    # --- Quality Lexicon (5D) ---
    
    def save_quality(self, name: str, vector: SynthiumVector, formula: str) -> str:
        """Save a quality definition to the lexicon."""
        with open(self.lexicon_path, "r") as f:
            data = json.load(f)
        
        entry = {
            "term": name,
            "vector": {"v": vector.v, "R": vector.R, "r": vector.r, "C": vector.C, "S": vector.S},
            "formula": formula,
            "timestamp": datetime.now().isoformat(),
            "category": "Psychological" if vector.S > 0.3 else "Physical"
        }
        
        for i, existing in enumerate(data["qualities"]):
            if existing["term"].lower() == name.lower():
                data["qualities"][i] = entry
                action = "UPDATED"
                break
        else:
            data["qualities"].append(entry)
            action = "RECORDED"
        
        data["meta"]["last_modified"] = datetime.now().isoformat()
        
        with open(self.lexicon_path, "w") as f:
            json.dump(data, f, indent=2)
        
        return action
    
    def find_quality(self, name: str) -> Optional[Dict]:
        """Find a quality in the lexicon."""
        with open(self.lexicon_path, "r") as f:
            data = json.load(f)
        
        for entry in data["qualities"]:
            if entry["term"].lower() == name.lower():
                return entry
        return None
    
    def list_qualities(self) -> List[str]:
        """List all quality names."""
        with open(self.lexicon_path, "r") as f:
            data = json.load(f)
        return [e["term"] for e in data["qualities"]]
    
    def get_quality_statistics(self) -> Dict[str, Any]:
        """Get lexicon statistics."""
        with open(self.lexicon_path, "r") as f:
            data = json.load(f)
        
        qualities = data.get("qualities", [])
        categories = {}
        for e in qualities:
            cat = e.get("category", "Unknown")
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total_qualities": len(qualities),
            "by_category": categories,
            "last_modified": data["meta"].get("last_modified", "N/A")
        }
    
    # --- Reality Fields (8D) ---
    
    def save_field(self, field: RealityField) -> str:
        """Save a reality field to disk."""
        filename = f"{field.name.replace(' ', '_')}.json"
        filepath = os.path.join(self.fields_path, filename)
        
        with open(filepath, 'w') as f:
            json.dump(field.to_dict(), f, indent=2)
        
        return f"Saved '{field.name}' with {len(field.vectors)} vectors"
    
    def load_field(self, name: str) -> Optional[RealityField]:
        """Load a reality field from disk."""
        filename = f"{name.replace(' ', '_')}.json"
        filepath = os.path.join(self.fields_path, filename)
        
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r') as f:
            return RealityField.from_dict(json.load(f))
    
    def list_fields(self) -> List[str]:
        """List all available fields."""
        if not os.path.exists(self.fields_path):
            return []
        return [f.replace('.json', '').replace('_', ' ') 
                for f in os.listdir(self.fields_path) if f.endswith('.json')]
    
    def get_field_statistics(self) -> Dict[str, Any]:
        """Get statistics about all reality fields."""
        fields = self.list_fields()
        total_vectors = sum(len(self.load_field(f).vectors) for f in fields if self.load_field(f))
        
        return {
            "total_fields": len(fields),
            "total_vectors": total_vectors,
            "avg_vectors_per_field": round(total_vectors / len(fields), 1) if fields else 0
        }


# =============================================================================
# CLI INTERFACE
# =============================================================================

def print_banner():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                 SYNTHIUM OMEGA v2.0                       ║
    ║            UNIFIED 8D REALITY COMPILER                    ║
    ║        "Mapping the Geometry of Existence"                ║
    ╚══════════════════════════════════════════════════════════╝
    
    Dimensions: 3D Space (x,y,z) + 5D Qualities (v,R,r,C,S)
    """)


def quantify_mode(tool: Transducer, lab: HolisticScience, scribe: Recorder):
    """Quantify a phenomenon at a specific location."""
    print("\n" + "="*60)
    print("🎯 8D REALITY QUANTIFICATION")
    print("="*60)
    
    name = input("\nPhenomenon name: ").strip()
    if not name:
        print("Cancelled.")
        return
    
    desc = input(f"Describe '{name}': ").strip()
    
    print("\n📍 Enter location (meters from origin, Enter for 0):")
    try:
        x = float(input("  x (east-west): ") or "0")
        y = float(input("  y (north-south): ") or "0")
        z = float(input("  z (up-down): ") or "0")
    except ValueError:
        x, y, z = 0.0, 0.0, 0.0
    
    try:
        vector = tool.quantify(desc, location=(x, y, z))
        print(f"\n[8D REALITY VECTOR]:\n  {vector}")
        
        analysis = lab.analyze_reality_vector(vector)
        print("\n[ANALYSIS]:")
        for key, value in analysis.items():
            if key == "violations" and not value:
                continue
            if key == "derived_formulas":
                print(f"  • formulas: {', '.join(value)}")
            else:
                print(f"  • {key}: {value}")
        
        print("\n💾 Save options: [1] Lexicon (5D)  [2] Field (8D)  [3] Both  [4] Skip")
        choice = input("Select: ").strip()
        
        if choice in ["1", "3"]:
            sv = SynthiumVector(vector.v, vector.R, vector.r, vector.C, vector.S)
            formula = analysis["derived_formulas"][0] if analysis["derived_formulas"] else "Complex"
            action = scribe.save_quality(name, sv, formula)
            print(f"[LEXICON]: {action} '{name}'")
        
        if choice in ["2", "3"]:
            field_name = input("Field name (Enter for default): ").strip() or f"{name}_field"
            field = RealityField(field_name)
            field.add_vector(vector)
            msg = scribe.save_field(field)
            print(f"[FIELD]: {msg}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def map_field_mode(tool: Transducer, lab: HolisticScience, scribe: Recorder):
    """Map a quality field across multiple spatial points."""
    print("\n" + "="*60)
    print("📍 QUALITY FIELD MAPPING")
    print("="*60)
    
    field_name = input("\nField name: ").strip()
    if not field_name:
        print("Cancelled.")
        return
    
    quality_desc = input("Quality to map: ").strip()
    
    print("\n📐 Define mapping area:")
    try:
        cx = float(input("  Center x: ") or "0")
        cy = float(input("  Center y: ") or "0")
        cz = float(input("  Center z: ") or "0")
        radius = float(input("  Radius (m): ") or "10")
        points = int(input("  Sample points: ") or "9")
    except ValueError:
        cx, cy, cz, radius, points = 0, 0, 0, 10, 9
    
    field = RealityField(field_name)
    print(f"\nGenerating {points} sample points...")
    
    for i in range(points):
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)
        r = random.uniform(0, radius)
        
        x = cx + r * math.sin(phi) * math.cos(theta)
        y = cy + r * math.sin(phi) * math.sin(theta)
        z = cz + r * math.cos(phi)
        
        vector = tool.quantify(quality_desc, location=(x, y, z))
        field.add_vector(vector)
        print(f"  Point {i+1}: ({x:.1f}, {y:.1f}, {z:.1f})")
    
    analysis = lab.analyze_spatial_quality_field(field.vectors)
    print("\n📊 FIELD ANALYSIS:")
    for key, value in analysis.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {key}: {value}")
    
    if input("\nSave field? (y/n): ").lower() == 'y':
        msg = scribe.save_field(field)
        print(f"✅ {msg}")


def search_mode(scribe: Recorder):
    """Search the quality lexicon."""
    print("\n" + "="*60)
    print("🔍 QUALITY LEXICON SEARCH")
    print("="*60)
    
    qualities = scribe.list_qualities()
    if qualities:
        print(f"\nKnown qualities: {', '.join(qualities)}")
    
    term = input("\nSearch term: ").strip()
    entry = scribe.find_quality(term)
    
    if entry:
        v = entry['vector']
        print(f"\n✅ FOUND: {entry['term']}")
        print(f"   Category: {entry.get('category', 'N/A')}")
        print(f"   Formula: {entry.get('formula', 'N/A')}")
        print(f"   Vector: v={v['v']:.2f}, R={v['R']:.2f}, r={v['r']:.2f}, C={v['C']:.2f}, S={v['S']:.2f}")
    else:
        print(f"\n❌ '{term}' not found.")


def explore_fields_mode(scribe: Recorder, lab: HolisticScience):
    """Explore existing reality fields."""
    print("\n" + "="*60)
    print("🗺️  REALITY FIELD EXPLORER")
    print("="*60)
    
    fields = scribe.list_fields()
    if not fields:
        print("\nNo fields found. Create one first.")
        return
    
    print(f"\nAvailable fields ({len(fields)}):")
    for i, name in enumerate(fields, 1):
        print(f"  {i}. {name}")
    
    try:
        choice = int(input("\nSelect (number): ").strip())
        if 1 <= choice <= len(fields):
            field = scribe.load_field(fields[choice-1])
            if field:
                print(f"\n📋 FIELD: {field.name}")
                print(f"   Vectors: {len(field.vectors)}")
                print(f"   Bounds: {field.metadata['bounds']}")
                print(f"   Types: {field.metadata['quality_types']}")
                
                if field.vectors:
                    analysis = lab.analyze_spatial_quality_field(field.vectors)
                    print("\n📊 ANALYSIS:")
                    for key, value in analysis.items():
                        if isinstance(value, dict):
                            print(f"  {key}:")
                            for k, v in value.items():
                                print(f"    {k}: {v}")
                        else:
                            print(f"  {key}: {value}")
    except (ValueError, IndexError):
        print("Invalid selection.")


def show_statistics(scribe: Recorder):
    """Display system statistics."""
    print("\n" + "="*60)
    print("📊 SYNTHIUM OMEGA v2.0 STATISTICS")
    print("="*60)
    
    qs = scribe.get_quality_statistics()
    print(f"\n📚 QUALITY LEXICON:")
    print(f"   Total: {qs['total_qualities']}")
    print(f"   Categories: {qs['by_category']}")
    print(f"   Modified: {qs['last_modified']}")
    
    fs = scribe.get_field_statistics()
    print(f"\n🗺️  REALITY FIELDS:")
    print(f"   Fields: {fs['total_fields']}")
    print(f"   Vectors: {fs['total_vectors']}")
    print(f"   Avg/field: {fs['avg_vectors_per_field']}")


def main():
    print_banner()
    
    tool = Transducer()
    lab = HolisticScience()
    scribe = Recorder()
    
    while True:
        print("\n" + "="*60)
        print("📋 MAIN MENU")
        print("="*60)
        print("1. 🎯 Quantify phenomenon (8D)")
        print("2. 📍 Map quality field")
        print("3. 🔍 Search lexicon")
        print("4. 🗺️  Explore fields")
        print("5. 📊 Statistics")
        print("6. 🚪 Exit")
        
        choice = input("\nSelect (1-6): ").strip()
        
        if choice == "1":
            quantify_mode(tool, lab, scribe)
        elif choice == "2":
            map_field_mode(tool, lab, scribe)
        elif choice == "3":
            search_mode(scribe)
        elif choice == "4":
            explore_fields_mode(scribe, lab)
        elif choice == "5":
            show_statistics(scribe)
        elif choice == "6":
            print("\n👋 Goodbye!\n")
            break
        else:
            print("Invalid choice.")


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
