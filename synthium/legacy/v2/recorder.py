import json
import os
from datetime import datetime
from typing import Optional, Dict, Any, List
from .vectors import RealityVector, SynthiumVector

LEXICON_PATH = os.path.join("data", "lexicon.json")
FIELD_DATA_PATH = os.path.join("data", "reality_fields")


class Recorder:
    """Manages both quality lexicon and reality fields."""
    
    def __init__(self):
        self._ensure_directories()
        self._ensure_lexicon_exists()
    
    def _ensure_directories(self):
        """Create necessary directories."""
        os.makedirs("data", exist_ok=True)
        os.makedirs(FIELD_DATA_PATH, exist_ok=True)
    
    def _ensure_lexicon_exists(self):
        """Create lexicon file if it doesn't exist."""
        if not os.path.exists(LEXICON_PATH):
            with open(LEXICON_PATH, "w") as f:
                json.dump({
                    "meta": {"version": "2.0", "created": datetime.now().isoformat()},
                    "qualities": []
                }, f, indent=2)
    
    # --- Quality Lexicon Methods (5D) ---
    
    def save_quality(self, name: str, vector: SynthiumVector, formula: str) -> bool:
        """Save a quality definition to the lexicon."""
        with open(LEXICON_PATH, "r") as f:
            data = json.load(f)
        
        # Check for existing
        for i, entry in enumerate(data["qualities"]):
            if entry["term"].lower() == name.lower():
                data["qualities"][i] = self._create_quality_entry(name, vector, formula)
                action = "UPDATED"
                break
        else:
            data["qualities"].append(self._create_quality_entry(name, vector, formula))
            action = "RECORDED"
        
        # Update metadata
        data["meta"]["last_modified"] = datetime.now().isoformat()
        data["meta"]["total_qualities"] = len(data["qualities"])
        
        with open(LEXICON_PATH, "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"[LEXICON]: {action} quality '{name}'")
        return True
    
    def _create_quality_entry(self, name: str, vector: SynthiumVector, formula: str) -> dict:
        """Create a quality lexicon entry."""
        return {
            "term": name,
            "vector": {"v": vector.v, "R": vector.R, "r": vector.r, "C": vector.C, "S": vector.S},
            "formula": formula,
            "timestamp": datetime.now().isoformat(),
            "category": "Psychological" if vector.S > 0.3 else "Physical"
        }
    
    def find_quality(self, name: str) -> Optional[Dict]:
        """Find a quality in the lexicon."""
        with open(LEXICON_PATH, "r") as f:
            data = json.load(f)
        
        for entry in data["qualities"]:
            if entry["term"].lower() == name.lower():
                return entry
        return None
    
    def get_quality_statistics(self) -> Dict[str, Any]:
        """Get lexicon statistics."""
        with open(LEXICON_PATH, "r") as f:
            data = json.load(f)
        
        qualities = data.get("qualities", [])
        categories = {}
        for entry in qualities:
            cat = entry.get("category", "Unknown")
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total_qualities": len(qualities),
            "by_category": categories,
            "last_modified": data["meta"].get("last_modified", "N/A")
        }
    
    # --- Reality Field Methods (8D) ---
    
    def save_reality_field(self, field_name: str, vectors: List[RealityVector]) -> bool:
        """Save a collection of reality vectors as a field."""
        # Convert to field format
        field_data = {
            "name": field_name,
            "metadata": {
                "created": datetime.now().isoformat(),
                "modified": datetime.now().isoformat(),
                "description": f"Field of {len(vectors)} reality vectors",
                "bounds": self._calculate_bounds(vectors),
                "vector_count": len(vectors)
            },
            "vectors": [vec.to_dict() for vec in vectors]
        }
        
        # Save to file
        filename = f"{field_name.replace(' ', '_')}.json"
        filepath = os.path.join(FIELD_DATA_PATH, filename)
        
        with open(filepath, 'w') as f:
            json.dump(field_data, f, indent=2)
        
        print(f"[FIELD]: Saved '{field_name}' with {len(vectors)} vectors")
        return True
    
    def _calculate_bounds(self, vectors: List[RealityVector]) -> Dict[str, Any]:
        """Calculate spatial bounds of vectors."""
        if not vectors:
            return {"min": [0,0,0], "max": [0,0,0]}
        
        xs = [v.x for v in vectors]
        ys = [v.y for v in vectors]
        zs = [v.z for v in vectors]
        
        return {
            "min": [min(xs), min(ys), min(zs)],
            "max": [max(xs), max(ys), max(zs)],
            "center": [(max(xs)+min(xs))/2, (max(ys)+min(ys))/2, (max(zs)+min(zs))/2]
        }
    
    def load_reality_field(self, field_name: str) -> Optional[List[RealityVector]]:
        """Load a reality field from disk."""
        filename = f"{field_name.replace(' ', '_')}.json"
        filepath = os.path.join(FIELD_DATA_PATH, filename)
        
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                return [RealityVector.from_dict(vec) for vec in data["vectors"]]
        except Exception as e:
            print(f"[FIELD ERROR]: Could not load {field_name}: {e}")
            return None
    
    def list_reality_fields(self) -> List[str]:
        """List all available reality fields."""
        fields = []
        if not os.path.exists(FIELD_DATA_PATH):
            return fields
            
        for filename in os.listdir(FIELD_DATA_PATH):
            if filename.endswith('.json'):
                field_name = filename.replace('.json', '').replace('_', ' ')
                fields.append(field_name)
        return fields
    
    def get_field_statistics(self) -> Dict[str, Any]:
        """Get statistics about all reality fields."""
        fields = self.list_reality_fields()
        total_vectors = 0
        
        for field_name in fields:
            vectors = self.load_reality_field(field_name)
            if vectors:
                total_vectors += len(vectors)
        
        return {
            "total_fields": len(fields),
            "total_vectors": total_vectors,
            "average_vectors_per_field": total_vectors / len(fields) if fields else 0
        }
