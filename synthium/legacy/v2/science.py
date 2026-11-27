import math
from .vectors import RealityVector

class HolisticScience:
    """Unified physics engine for 8D reality space."""
    
    def analyze_spatial_quality_field(self, vectors: list) -> dict:
        """Analyze how qualities vary across space."""
        if not vectors:
            return {"error": "No vectors provided"}
        
        # Calculate spatial gradients
        gradients = self._calculate_gradients(vectors)
        
        # Find quality hot/cold spots
        hotspots = self._find_extrema(vectors)
        
        # Calculate field coherence
        coherence = self._field_coherence(vectors)
        
        return {
            "spatial_gradients": gradients,
            "quality_hotspots": hotspots,
            "field_coherence": coherence,
            "total_points": len(vectors),
            "spatial_bounds": self._spatial_bounds(vectors),
            "quality_variance": self._quality_variance(vectors)
        }
    
    def analyze_reality_vector(self, vector: RealityVector) -> dict:
        """Comprehensive analysis of an 8D reality vector."""
        # Physical properties
        spatial_magnitude = math.sqrt(vector.x**2 + vector.y**2 + vector.z**2)
        quality_magnitude = math.sqrt(vector.v**2 + vector.R**2 + vector.r**2 + 
                                     vector.C**2 + vector.S**2)
        
        # Derived metrics
        reality_density = (vector.R * vector.C) / (spatial_magnitude + 0.001)
        information_potential = vector.C * (1 - vector.S)
        energy_flux = vector.v * vector.r
        
        # Coherence check
        coherent, violations = vector.is_coherent()
        
        # Spatial-contextual formulas
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
    
    def _derive_spatial_formulas(self, vector: RealityVector) -> list:
        """Derive formulas that include spatial context."""
        formulas = []
        
        # Spatial-dependent formulas
        if vector.z < 0:  # Underground
            formulas.append(f"Pressure = R × |z| = {vector.R * abs(vector.z):.1f} Pa")
        
        if math.sqrt(vector.x**2 + vector.y**2) > 10:  # Far from origin
            formulas.append(f"Field_strength = r / distance = {vector.r / (math.sqrt(vector.x**2 + vector.y**2) + 0.001):.3f}")
        
        # Quality formulas
        if vector.R > 0.6 and vector.C > 0.6:
            formulas.append("Mass_density = R × C")
        
        if vector.v > 0.7:
            if vector.R < 0.3:
                formulas.append("Flow_potential = v²/R")
            else:
                formulas.append("Friction_loss = v × R")
        
        if vector.r > 0.7:
            formulas.append(f"Attraction_range = r × √(x²+y²+z²) = {vector.r * math.sqrt(vector.x**2 + vector.y**2 + vector.z**2):.1f} m")
        
        if vector.S > 0.7:
            formulas.append(f"Entropy_gradient = S/|z| = {vector.S/(abs(vector.z)+0.001):.3f}")
        
        return formulas if formulas else ["Complex_8D_relation = f(x,y,z,v,R,r,C,S)"]
    
    def _calculate_gradients(self, vectors: list) -> dict:
        """Calculate how qualities change with position."""
        if len(vectors) < 2:
            return {"insufficient_data": "Need at least 2 points"}
        
        # Simple gradient calculation
        gradients = {}
        for dim in ['v', 'R', 'r', 'C', 'S']:
            # Find max and min for this quality dimension
            values = [(getattr(v, dim), (v.x, v.y, v.z)) for v in vectors]
            max_val, max_pos = max(values, key=lambda x: x[0])
            min_val, min_pos = min(values, key=lambda x: x[0])
            
            # Calculate distance between extremes
            dist = math.sqrt((max_pos[0]-min_pos[0])**2 + 
                           (max_pos[1]-min_pos[1])**2 + 
                           (max_pos[2]-min_pos[2])**2)
            
            if dist > 0:
                gradient = (max_val - min_val) / dist
                gradients[dim] = f"{gradient:.3f} per meter"
            else:
                gradients[dim] = "uniform"
        
        return gradients
    
    def _classify_spatial_zone(self, vector: RealityVector) -> str:
        """Classify the spatial location."""
        radius = math.sqrt(vector.x**2 + vector.y**2 + vector.z**2)
        
        if vector.z < -10:
            return "Deep Underground"
        elif vector.z < 0:
            return "Subsurface"
        elif vector.z < 10:
            return "Surface Level"
        elif vector.z < 100:
            return "Elevated"
        elif radius > 1000:
            return "Distant"
        else:
            return "Local"
    
    def _classify_quality(self, vector: RealityVector) -> str:
        """Classify the quality pattern."""
        if vector.S > 0.8:
            return "Chaotic Field"
        elif vector.r > 0.8:
            return "Resonance Field"
        elif vector.R > 0.8:
            return "Resistance Field"
        elif vector.v > 0.8:
            return "Velocity Field"
        elif vector.C > 0.8:
            return "Capacity Field"
        else:
            return "Mixed Quality Field"
    
    def _find_extrema(self, vectors: list) -> dict:
        """Find locations of maximum quality values."""
        if not vectors:
            return {}
        
        extrema = {}
        for dim in ['v', 'R', 'r', 'C', 'S']:
            # Find maximum
            max_vector = max(vectors, key=lambda v: getattr(v, dim))
            extrema[f"max_{dim}"] = {
                "value": getattr(max_vector, dim),
                "location": (max_vector.x, max_vector.y, max_vector.z)
            }
        
        return extrema
    
    def _field_coherence(self, vectors: list) -> float:
        """Calculate how coherent the field is (0-1)."""
        if len(vectors) < 2:
            return 1.0
        
        # Calculate average pairwise coherence
        coherent_count = 0
        total_pairs = 0
        
        for i in range(len(vectors)):
            for j in range(i+1, len(vectors)):
                if vectors[i].is_coherent()[0] and vectors[j].is_coherent()[0]:
                    coherent_count += 1
                total_pairs += 1
        
        return coherent_count / total_pairs if total_pairs > 0 else 1.0
    
    def _spatial_bounds(self, vectors: list) -> dict:
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
    
    def _quality_variance(self, vectors: list) -> dict:
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
