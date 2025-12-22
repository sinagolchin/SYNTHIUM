"""
Synthium Core - Consciousness Quantification Framework
Created by Sina Golchin & Maysam BaygMuhammady
"""

from .vectors import SynthiumVector
from .engine import SynthiumEngine
from .database import SynthiumDatabase
from .phenomena import Phenomenon, CORE_PHENOMENA

__version__ = "2.1.0"
__all__ = [
    "SynthiumVector",
    "SynthiumEngine",
    "SynthiumDatabase",
    "Phenomenon",
    "CORE_PHENOMENA"
]
