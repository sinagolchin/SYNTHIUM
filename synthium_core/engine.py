"""
SynthiumEngine - Core analysis and transformation engine
"""
from typing import Dict, List, Optional, Tuple
import math
from .vectors import SynthiumVector, PREDEFINED_VECTORS
from .phenomena import Phenomenon
from .database import SynthiumDatabase


class SynthiumEngine:
    """Core engine for consciousness analysis and transformation"""

    def __init__(self):
        """Initialize the engine"""
        self.db = SynthiumDatabase()
        print("⚙️ Synthium Core Engine Initialized.")

    def analyze_state(self, vector: SynthiumVector) -> Dict:
        """
        Analyze a consciousness state and provide insights
        """
        # Find similar phenomena
        similar_phenomena = self.db.find_similar_phenomena(vector, limit=5)

        # Calculate wellbeing score
        wellbeing = self.calculate_wellbeing(vector)

        # Determine phase
        phase = self.determine_phase(vector)

        # Calculate stability
        stability = self.calculate_stability(vector)

        # Generate insights
        insights = self.generate_insights(vector)

        # Generate recommendations
        recommendations = self.generate_recommendations(vector)

        return {
            "vector": vector.to_dict(),
            "wellbeing_score": round(wellbeing, 3),
            "phase": phase,
            "stability": round(stability, 3),
            "similar_phenomena": [
                {
                    "phenomenon": p.term,
                    "similarity": round(sim, 3),
                    "description": p.description
                }
                for p, sim in similar_phenomena
            ],
            "insights": insights,
            "recommendations": recommendations
        }

    def calculate_wellbeing(self, vector: SynthiumVector) -> float:
        """
        Calculate overall wellbeing score (0-1)
        Higher resonance (r), capacity (C), lower resistance (R), and entropy (S) = higher wellbeing
        """
        wellbeing = (
            vector.r * 0.3 +           # Resonance/connection (30%)
            vector.C * 0.3 +           # Capacity (30%)
            (1 - vector.R) * 0.2 +     # Low resistance (20%)
            (1 - vector.S) * 0.2       # Low entropy (20%)
        )
        return max(0.0, min(1.0, wellbeing))

    def determine_phase(self, vector: SynthiumVector) -> str:
        """
        Determine the phase of consciousness evolution
        """
        # Dissolution: near-zero velocity and resistance, high resonance
        if vector.v < 0.2 and vector.R < 0.2 and vector.r > 0.8:
            return "dissolution"

        # Transcendence: low entropy, high capacity and resonance
        if vector.S < 0.3 and vector.C > 0.7 and vector.r > 0.7:
            return "transcendence"

        # Integration: balanced, moderate chaos, decent capacity
        if vector.S < 0.5 and vector.C > 0.5 and vector.r > 0.5:
            return "integration"

        # Awakening: high resistance, low capacity, or high chaos
        return "awakening"

    def calculate_stability(self, vector: SynthiumVector) -> float:
        """
        Calculate system stability (0-1)
        Stable systems have low entropy, adequate capacity
        """
        entropy_stability = 1 - vector.S
        capacity_stability = vector.C
        resistance_stability = 1 - vector.R

        stability = (entropy_stability * 0.4 +
                    capacity_stability * 0.4 +
                    resistance_stability * 0.2)

        return max(0.0, min(1.0, stability))

    def generate_insights(self, vector: SynthiumVector) -> List[str]:
        """Generate contextual insights based on vector"""
        insights = []

        # Velocity insights
        if vector.v > 0.8:
            insights.append("High velocity detected - you may be rushing or in urgency mode")
        elif vector.v < 0.2:
            insights.append("Very low velocity - experiencing stuckness or paralysis")

        # Resistance insights
        if vector.R > 0.7:
            insights.append("Significant resistance present - friction or trauma blocking flow")
        elif vector.R < 0.3:
            insights.append("Low resistance - experiencing ease and acceptance")

        # Resonance insights
        if vector.r > 0.7:
            insights.append("Strong resonance - feeling connected and in tune")
        elif vector.r < 0.3:
            insights.append("Low resonance - experiencing disconnection or isolation")

        # Capacity insights
        if vector.C < 0.3:
            insights.append("Depleted capacity - need for rest and restoration")
        elif vector.C > 0.8:
            insights.append("High capacity - energized and ready for action")

        # Entropy insights
        if vector.S > 0.7:
            insights.append("High entropy - experiencing confusion or chaos")
        elif vector.S < 0.3:
            insights.append("Low entropy - clarity and order present")

        return insights

    def generate_recommendations(self, vector: SynthiumVector) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # High velocity + high resistance = need to slow down
        if vector.v > 0.7 and vector.R > 0.6:
            recommendations.append("Consider slowing down - rushing against resistance creates friction")

        # Low capacity + high entropy = need stabilization
        if vector.C < 0.4 and vector.S > 0.6:
            recommendations.append("Focus on rest and simplification to restore capacity")

        # Low resonance = need connection
        if vector.r < 0.4:
            recommendations.append("Seek connection - reach out, share, or practice self-compassion")

        # High entropy = need organization
        if vector.S > 0.7:
            recommendations.append("Create structure - write, organize, or clarify priorities")

        # Low velocity + high capacity = opportunity
        if vector.v < 0.3 and vector.C > 0.7:
            recommendations.append("You have capacity available - consider what you're avoiding")

        # Near transcendence
        if vector.S < 0.3 and vector.C > 0.7 and vector.r > 0.7:
            recommendations.append("You're in a powerful state - this is a moment for deep work or presence")

        if not recommendations:
            recommendations.append("Continue current path - system is balanced")

        return recommendations

    def estimate_phenomenon_vector(self, phenomenon: Phenomenon) -> SynthiumVector:
        """Estimate vector for a phenomenon (used by validation system)"""
        return phenomenon.vector

    def create_transformation_plan(self,
                                  current_vector: SynthiumVector,
                                  target_state: str) -> Dict:
        """
        Create a transformation plan from current state to target state
        """
        # Get target vector
        target_vector = PREDEFINED_VECTORS.get(target_state.lower())
        if not target_vector:
            # Try to find in phenomena
            phenomenon = self.db.get_phenomenon_by_term(target_state)
            if phenomenon:
                target_vector = phenomenon.vector
            else:
                return {"error": f"Unknown target state: {target_state}"}

        # Calculate delta
        delta = {
            "v": target_vector.v - current_vector.v,
            "R": target_vector.R - current_vector.R,
            "r": target_vector.r - current_vector.r,
            "C": target_vector.C - current_vector.C,
            "S": target_vector.S - current_vector.S
        }

        # Calculate distance
        distance = current_vector.distance_to(target_vector)

        # Generate steps
        steps = self._generate_transformation_steps(current_vector, target_vector, delta)

        return {
            "current_state": current_vector.to_dict(),
            "target_state": target_vector.to_dict(),
            "delta": {k: round(v, 3) for k, v in delta.items()},
            "distance": round(distance, 3),
            "estimated_difficulty": self._estimate_difficulty(distance),
            "steps": steps
        }

    def _generate_transformation_steps(self,
                                      current: SynthiumVector,
                                      target: SynthiumVector,
                                      delta: Dict) -> List[Dict]:
        """Generate concrete transformation steps"""
        steps = []

        # Prioritize steps by impact
        priorities = sorted(delta.items(), key=lambda x: abs(x[1]), reverse=True)

        for dimension, change in priorities:
            if abs(change) < 0.1:
                continue  # Skip small changes

            step = self._create_step_for_dimension(dimension, change)
            if step:
                steps.append(step)

        return steps

    def _create_step_for_dimension(self, dimension: str, change: float) -> Optional[Dict]:
        """Create a specific step for changing a dimension"""
        actions = {
            "v": {
                "increase": "Engage in energizing activity, set deadlines, create momentum",
                "decrease": "Practice slowing down, meditation, intentional pauses"
            },
            "R": {
                "increase": "Engage with challenging material, face fears",
                "decrease": "Release resistance through acceptance, breathwork, or somatic practices"
            },
            "r": {
                "increase": "Connect with others, practice empathy, find your tribe",
                "decrease": "Create boundaries, practice solitude, disconnect from draining relationships"
            },
            "C": {
                "increase": "Rest, restore energy, eat well, sleep, reduce commitments",
                "decrease": "Engage capacity through challenge and growth"
            },
            "S": {
                "increase": "Embrace uncertainty, explore chaos, try new things",
                "decrease": "Organize, clarify, create systems, write things down"
            }
        }

        if dimension not in actions:
            return None

        direction = "increase" if change > 0 else "decrease"
        action = actions[dimension][direction]

        return {
            "dimension": dimension,
            "change": round(change, 3),
            "action": action
        }

    def _estimate_difficulty(self, distance: float) -> str:
        """Estimate transformation difficulty"""
        if distance < 0.5:
            return "easy"
        elif distance < 1.0:
            return "moderate"
        elif distance < 1.5:
            return "challenging"
        else:
            return "profound"
