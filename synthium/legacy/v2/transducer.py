import re
from .vectors import RealityVector, SynthiumVector

class Transducer:
    """Converts descriptions to 8D RealityVectors."""
    
    # Keyword mappings
    QUALITY_KEYWORDS = {
        'v': ['fast', 'quick', 'speed', 'velocity', 'dynamic', 'moving'],
        'R': ['heavy', 'resistant', 'dense', 'solid', 'stuck', 'blocked'],
        'r': ['vibrant', 'resonant', 'connected', 'harmonic', 'attractive'],
        'C': ['deep', 'capacity', 'large', 'full', 'potential', 'room'],
        'S': ['chaotic', 'random', 'entropy', 'decay', 'disorder', 'noise']
    }
    
    # Spatial context keywords
    SPATIAL_CONTEXT = {
        'high': {'z': 10.0}, 'low': {'z': -5.0}, 'center': {'x': 0, 'y': 0},
        'north': {'y': 10.0}, 'south': {'y': -10.0}, 'east': {'x': 10.0}, 'west': {'x': -10.0},
        'underground': {'z': -10.0}, 'above': {'z': 20.0}, 'surface': {'z': 0}
    }
    
    def quantify(self, description: str, 
                 location: tuple = (0.0, 0.0, 0.0)) -> RealityVector:
        """
        Convert description to 8D RealityVector at given location.
        
        Args:
            description: Text describing the phenomenon
            location: (x, y, z) coordinates in meters
        """
        x, y, z = location
        desc_lower = description.lower()
        
        # Analyze spatial context from description
        x, y, z = self._extract_spatial_context(desc_lower, x, y, z)
        
        # Analyze qualities
        qualities = self._analyze_qualities(desc_lower)
        
        return RealityVector(x, y, z, **qualities)
    
    def quantify_quality_only(self, description: str) -> SynthiumVector:
        """Legacy: Convert description to 5D quality vector only."""
        qualities = self._analyze_qualities(description.lower())
        return SynthiumVector(**qualities)
    
    def _extract_spatial_context(self, text: str, 
                                default_x: float, 
                                default_y: float, 
                                default_z: float) -> tuple:
        """Extract spatial coordinates from text descriptions."""
        x, y, z = default_x, default_y, default_z
        
        for keyword, offsets in self.SPATIAL_CONTEXT.items():
            if keyword in text:
                x += offsets.get('x', 0)
                y += offsets.get('y', 0)
                z += offsets.get('z', 0)
        
        # Extract numeric coordinates if mentioned
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
    
    def _analyze_qualities(self, text: str) -> dict:
        """Analyze text to extract 5D quality scores."""
        # Predefined emotional profiles
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
            'hope': {'v': 0.5, 'R': 0.2, 'r': 0.7, 'C': 0.9, 'S': 0.2}
        }
        
        # Check for known emotions
        for emotion, profile in EMOTIONAL_PROFILES.items():
            if emotion in text:
                return profile.copy()
        
        # Default keyword analysis
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
