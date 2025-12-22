"""
Phenomena - Catalog of consciousness states and experiences
"""
from dataclasses import dataclass
from typing import List, Dict, Optional
from .vectors import SynthiumVector


@dataclass
class Phenomenon:
    """A named consciousness phenomenon with associated vector"""
    id: int
    term: str
    description: str
    vector: SynthiumVector
    phase: str  # "awakening", "integration", "transcendence", "dissolution"
    tags: List[str]
    related_to: List[int]  # IDs of related phenomena

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "term": self.term,
            "description": self.description,
            "vector": self.vector.to_dict(),
            "phase": self.phase,
            "tags": self.tags,
            "related_to": self.related_to
        }


# Core phenomena database
CORE_PHENOMENA = [
    Phenomenon(
        id=1,
        term="Flow State",
        description="Complete absorption in present activity, effortless action",
        vector=SynthiumVector(v=0.7, R=0.2, r=0.8, C=0.9, S=0.1),
        phase="integration",
        tags=["peak_experience", "performance", "presence"],
        related_to=[15, 20]
    ),
    Phenomenon(
        id=2,
        term="Burnout",
        description="Exhaustion from prolonged stress, depleted capacity",
        vector=SynthiumVector(v=0.9, R=0.8, r=0.3, C=0.1, S=0.8),
        phase="awakening",
        tags=["crisis", "depletion", "stress"],
        related_to=[3, 6]
    ),
    Phenomenon(
        id=3,
        term="Depression",
        description="Low energy, disconnection, loss of meaning",
        vector=SynthiumVector(v=0.1, R=0.7, r=0.2, C=0.2, S=0.6),
        phase="awakening",
        tags=["mental_health", "low_energy", "disconnection"],
        related_to=[2, 7]
    ),
    Phenomenon(
        id=4,
        term="Anxiety",
        description="High mental velocity, future-focused worry, chaos",
        vector=SynthiumVector(v=0.8, R=0.6, r=0.4, C=0.5, S=0.8),
        phase="awakening",
        tags=["mental_health", "worry", "chaos"],
        related_to=[2, 11]
    ),
    Phenomenon(
        id=5,
        term="Inner Peace",
        description="Deep calm, low resistance, present-centered awareness",
        vector=SynthiumVector(v=0.3, R=0.1, r=0.7, C=0.8, S=0.1),
        phase="integration",
        tags=["peace", "meditation", "presence"],
        related_to=[1, 16]
    ),
    Phenomenon(
        id=6,
        term="Grief",
        description="Processing loss, high resistance, low capacity",
        vector=SynthiumVector(v=0.2, R=0.8, r=0.3, C=0.3, S=0.7),
        phase="awakening",
        tags=["emotion", "loss", "healing"],
        related_to=[3, 8]
    ),
    Phenomenon(
        id=7,
        term="Apathy",
        description="Emotional numbness, disconnection, low velocity",
        vector=SynthiumVector(v=0.1, R=0.5, r=0.1, C=0.3, S=0.5),
        phase="awakening",
        tags=["disconnection", "numbness"],
        related_to=[3, 6]
    ),
    Phenomenon(
        id=8,
        term="Anger",
        description="High energy directed at resistance, friction",
        vector=SynthiumVector(v=0.8, R=0.9, r=0.4, C=0.6, S=0.7),
        phase="awakening",
        tags=["emotion", "energy", "resistance"],
        related_to=[4, 6]
    ),
    Phenomenon(
        id=9,
        term="Joy",
        description="High resonance, open flow, elevated energy",
        vector=SynthiumVector(v=0.6, R=0.1, r=0.8, C=0.9, S=0.2),
        phase="integration",
        tags=["emotion", "positive", "connection"],
        related_to=[1, 5, 10]
    ),
    Phenomenon(
        id=10,
        term="Love",
        description="Deep resonance, acceptance, connection",
        vector=SynthiumVector(v=0.5, R=0.1, r=0.9, C=0.8, S=0.2),
        phase="integration",
        tags=["emotion", "connection", "transcendence"],
        related_to=[5, 9, 16]
    ),
    Phenomenon(
        id=11,
        term="Confusion",
        description="High entropy, unclear direction, scattered energy",
        vector=SynthiumVector(v=0.5, R=0.5, r=0.4, C=0.5, S=0.9),
        phase="awakening",
        tags=["chaos", "uncertainty"],
        related_to=[4, 12]
    ),
    Phenomenon(
        id=12,
        term="Clarity",
        description="Low entropy, clear seeing, organized thought",
        vector=SynthiumVector(v=0.4, R=0.2, r=0.6, C=0.8, S=0.1),
        phase="integration",
        tags=["insight", "order", "understanding"],
        related_to=[1, 5, 16]
    ),
    Phenomenon(
        id=13,
        term="Overwhelm",
        description="Capacity exceeded, high chaos, system overload",
        vector=SynthiumVector(v=0.7, R=0.7, r=0.3, C=0.2, S=0.9),
        phase="awakening",
        tags=["crisis", "chaos", "depletion"],
        related_to=[2, 4, 11]
    ),
    Phenomenon(
        id=14,
        term="Boredom",
        description="Low velocity, disconnection, excess capacity",
        vector=SynthiumVector(v=0.2, R=0.3, r=0.3, C=0.7, S=0.4),
        phase="awakening",
        tags=["low_energy", "disconnection"],
        related_to=[7, 15]
    ),
    Phenomenon(
        id=15,
        term="Curiosity",
        description="Moderate velocity, openness, seeking resonance",
        vector=SynthiumVector(v=0.6, R=0.3, r=0.6, C=0.7, S=0.3),
        phase="integration",
        tags=["exploration", "growth", "openness"],
        related_to=[1, 9, 12]
    ),
    Phenomenon(
        id=16,
        term="Presence",
        description="Here-now awareness, low resistance, harmony",
        vector=SynthiumVector(v=0.3, R=0.1, r=0.7, C=0.8, S=0.1),
        phase="transcendence",
        tags=["awareness", "meditation", "transcendence"],
        related_to=[5, 10, 12, 17]
    ),
    Phenomenon(
        id=17,
        term="Witness Consciousness",
        description="Pure awareness, observing without attachment",
        vector=SynthiumVector(v=0.1, R=0.0, r=0.8, C=0.9, S=0.0),
        phase="transcendence",
        tags=["awareness", "meditation", "transcendence", "mystical"],
        related_to=[16, 18, 19]
    ),
    Phenomenon(
        id=18,
        term="Sakshatakara",
        description="Direct realization, dissolution of seeker",
        vector=SynthiumVector(v=0.0, R=0.0, r=1.0, C=1.0, S=0.0),
        phase="dissolution",
        tags=["mystical", "enlightenment", "transcendence"],
        related_to=[17, 19, 20]
    ),
    Phenomenon(
        id=19,
        term="The Void",
        description="Emptiness, no-self, pure potential",
        vector=SynthiumVector(v=0.0, R=0.0, r=0.5, C=1.0, S=0.0),
        phase="dissolution",
        tags=["mystical", "emptiness", "transcendence"],
        related_to=[17, 18]
    ),
    Phenomenon(
        id=20,
        term="This",
        description="The eternal present, only what is",
        vector=SynthiumVector(v=0.0, R=0.0, r=1.0, C=1.0, S=0.0),
        phase="dissolution",
        tags=["mystical", "presence", "absolute"],
        related_to=[16, 17, 18]
    ),
]
