"""
Spatiotemporal quality field mapping.
Tracks how qualities vary across space and time.
"""

import json
import os
import math
from datetime import datetime
from typing import List, Dict, Any, Optional
from .vectors import RealityVector

FIELD_DATA_PATH = os.path.join("data", "reality_fields")


class RealityField:
    """Represents a quality field across space."""
    
    def __init__(self, name: str):
        self.name = name
        self.vectors: List[RealityVector] = []
        self.metadata = {
            "created": datetime.now().isoformat(),
            "modified": datetime.now().isoformat(),
            "description": "",
            "resolution_m": 1.0,  # Spatial resolution in meters
            "bounds": {"min": (0,0,0), "max": (0,0,0)},
            "quality_types": set()
        }
    
    def add_vector(self, vector: RealityVector):
        """Add a reality vector to the field."""
        self.vectors.append(vector)
        self.metadata["modified"] = datetime.now().isoformat()
        
        # Update bounds
        if len(self.vectors) == 1:
            self.metadata["bounds"]["min"] = (vector.x, vector.y, vector.z)
            self.metadata["bounds"]["max"] = (vector.x, vector.y, vector.z)
        else:
            min_bounds = self.metadata["bounds"]["min"]
            max_bounds = self.metadata["bounds"]["max"]
            self.metadata["bounds"]["min"] = (
                min(min_bounds[0], vector.x),
                min(min_bounds[1], vector.y),
                min(min_bounds[2], vector.z)
            )
            self.metadata["bounds"]["max"] = (
                max(max_bounds[0], vector.x),
                max(max_bounds[1], vector.y),
                max(max_bounds[2], vector.z)
            )
        
        # Track quality types
        if vector.S > 0.5:
            self.metadata["quality_types"].add("chaotic")
        if vector.r > 0.5:
            self.metadata["quality_types"].add("resonant")
        if vector.R > 0.5:
            self.metadata["quality_types"].add("resistant")
    
    def get_vector_at(self, x: float, y: float, z: float, 
                     radius: float = 1.0) -> List[RealityVector]:
        """Get vectors within radius of a point."""
        result = []
        for vec in self.vectors:
            dist = math.sqrt((vec.x - x)**2 + (vec.y - y)**2 + (vec.z - z)**2)
            if dist <= radius:
                result.append(vec)
        return result
    
    def get_quality_slice(self, dimension: str, 
                         value_range: tuple = (0, 1)) -> List[RealityVector]:
        """Get vectors where a specific quality is in range."""
        result = []
        for vec in self.vectors:
            quality_value = getattr(vec, dimension)
            if value_range[0] <= quality_value <= value_range[1]:
                result.append(vec)
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert field to dictionary for storage."""
        # Convert set to list for JSON serialization
        metadata_copy = self.metadata.copy()
        metadata_copy["quality_types"] = list(self.metadata["quality_types"])
        
        return {
            "name": self.name,
            "metadata": metadata_copy,
            "vectors": [vec.to_dict() for vec in self.vectors]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RealityField':
        """Create field from dictionary."""
        field = cls(data["name"])
        field.metadata = data["metadata"]
        # Convert quality_types back to set
        if isinstance(field.metadata.get("quality_types"), list):
            field.metadata["quality_types"] = set(field.metadata["quality_types"])
        field.vectors = [RealityVector.from_dict(vec) for vec in data["vectors"]]
        return field


class FieldManager:
    """Manages multiple reality fields."""
    
    def __init__(self):
        self._ensure_directory()
        self.fields: Dict[str, RealityField] = {}
        self._load_fields()
    
    def _ensure_directory(self):
        """Create data directory if it doesn't exist."""
        if not os.path.exists(FIELD_DATA_PATH):
            os.makedirs(FIELD_DATA_PATH, exist_ok=True)
    
    def _load_fields(self):
        """Load all fields from disk."""
        if not os.path.exists(FIELD_DATA_PATH):
            return
            
        for filename in os.listdir(FIELD_DATA_PATH):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(FIELD_DATA_PATH, filename), 'r') as f:
                        data = json.load(f)
                        field = RealityField.from_dict(data)
                        self.fields[field.name] = field
                except Exception as e:
                    print(f"Warning: Could not load field {filename}: {e}")
    
    def create_field(self, name: str, description: str = "") -> RealityField:
        """Create a new reality field."""
        if name in self.fields:
            raise ValueError(f"Field '{name}' already exists")
        
        field = RealityField(name)
        field.metadata["description"] = description
        self.fields[name] = field
        return field
    
    def save_field(self, field: RealityField):
        """Save a field to disk."""
        filename = f"{field.name.replace(' ', '_')}.json"
        filepath = os.path.join(FIELD_DATA_PATH, filename)
        
        with open(filepath, 'w') as f:
            json.dump(field.to_dict(), f, indent=2)
    
    def get_field(self, name: str) -> Optional[RealityField]:
        """Get a field by name."""
        return self.fields.get(name)
    
    def list_fields(self) -> List[str]:
        """List all available fields."""
        return list(self.fields.keys())
    
    def get_field_statistics(self) -> Dict[str, Any]:
        """Get statistics across all fields."""
        stats = {
            "total_fields": len(self.fields),
            "total_vectors": 0,
            "spatial_coverage": {"min": (0,0,0), "max": (0,0,0)},
            "field_types": {}
        }
        
        if not self.fields:
            return stats
        
        # Calculate aggregate statistics
        all_vectors = []
        for field in self.fields.values():
            stats["total_vectors"] += len(field.vectors)
            all_vectors.extend(field.vectors)
            
            # Track field types
            quality_types = field.metadata.get("quality_types", set())
            if isinstance(quality_types, set):
                field_type = "_".join(sorted(quality_types)) if quality_types else "empty"
            else:
                field_type = "_".join(sorted(quality_types)) if quality_types else "empty"
            stats["field_types"][field_type] = stats["field_types"].get(field_type, 0) + 1
        
        if all_vectors:
            # Calculate overall spatial bounds
            xs = [v.x for v in all_vectors]
            ys = [v.y for v in all_vectors]
            zs = [v.z for v in all_vectors]
            stats["spatial_coverage"]["min"] = (min(xs), min(ys), min(zs))
            stats["spatial_coverage"]["max"] = (max(xs), max(ys), max(zs))
        
        return stats
