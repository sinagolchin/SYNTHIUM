"""
Database layer for Synthium - handles persistence and retrieval
"""
from typing import List, Optional, Dict
from .phenomena import Phenomenon, CORE_PHENOMENA
from .vectors import SynthiumVector
import json


class SynthiumDatabase:
    """In-memory database for phenomena and user states"""

    def __init__(self):
        """Initialize with core phenomena"""
        self.phenomena: Dict[int, Phenomenon] = {}
        self.user_states: Dict[str, List[Dict]] = {}  # user_id -> list of states
        self._load_core_phenomena()

    def _load_core_phenomena(self):
        """Load core phenomena into database"""
        for phenomenon in CORE_PHENOMENA:
            self.phenomena[phenomenon.id] = phenomenon

    def get_phenomenon(self, phenomenon_id: int) -> Optional[Phenomenon]:
        """Get a phenomenon by ID"""
        return self.phenomena.get(phenomenon_id)

    def get_phenomenon_by_term(self, term: str) -> Optional[Phenomenon]:
        """Get a phenomenon by term name"""
        for phenomenon in self.phenomena.values():
            if phenomenon.term.lower() == term.lower():
                return phenomenon
        return None

    def get_all_phenomena(self) -> List[Phenomenon]:
        """Get all phenomena"""
        return list(self.phenomena.values())

    def get_phenomena_by_phase(self, phase: str) -> List[Phenomenon]:
        """Get all phenomena in a specific phase"""
        return [p for p in self.phenomena.values() if p.phase == phase]

    def get_phenomena_by_tag(self, tag: str) -> List[Phenomenon]:
        """Get all phenomena with a specific tag"""
        return [p for p in self.phenomena.values() if tag in p.tags]

    def find_similar_phenomena(self, vector: SynthiumVector, limit: int = 5) -> List[tuple]:
        """Find phenomena most similar to given vector"""
        similarities = []
        for phenomenon in self.phenomena.values():
            similarity = vector.similarity_to(phenomenon.vector)
            similarities.append((phenomenon, similarity))

        # Sort by similarity (descending) and return top N
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:limit]

    def add_user_state(self, user_id: str, state: Dict):
        """Record a user state"""
        if user_id not in self.user_states:
            self.user_states[user_id] = []
        self.user_states[user_id].append(state)

    def get_user_history(self, user_id: str) -> List[Dict]:
        """Get all recorded states for a user"""
        return self.user_states.get(user_id, [])

    def get_user_trajectory(self, user_id: str) -> List[SynthiumVector]:
        """Get the vector trajectory for a user"""
        history = self.get_user_history(user_id)
        vectors = []
        for state in history:
            if "vector" in state:
                vectors.append(SynthiumVector.from_dict(state["vector"]))
        return vectors

    def export_to_json(self, filepath: str):
        """Export database to JSON file"""
        data = {
            "phenomena": [p.to_dict() for p in self.phenomena.values()],
            "user_states": self.user_states
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def import_from_json(self, filepath: str):
        """Import database from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Import phenomena
        for p_data in data.get("phenomena", []):
            phenomenon = Phenomenon(
                id=p_data["id"],
                term=p_data["term"],
                description=p_data["description"],
                vector=SynthiumVector.from_dict(p_data["vector"]),
                phase=p_data["phase"],
                tags=p_data["tags"],
                related_to=p_data["related_to"]
            )
            self.phenomena[phenomenon.id] = phenomenon

        # Import user states
        self.user_states = data.get("user_states", {})
