"""
SynthiumBot's Memory & Transducer
Translates human chat messages into N-Dimensional Agnostic Reality Tensors.
"""
import numpy as np

# IMPORT THE SYNTHIUM PHYSICS ENGINE
try:
    from .synthium_v4 import AgnosticRealityTensor, Confidence, ConfidenceLevel
except ImportError:
    print("Warning: Could not import synthium_v4. Ensure the file is named correctly.")

class PersonalTransducer:
    """Translates your daily check-in text into Synthium Tensor coordinates."""
    
    def __init__(self):
        # Heuristic Lexicons for Daily Life
        self.lexicon = {
            'v_high': ['ran', 'walked', 'gym', 'active', 'fast', 'busy', 'moved', 'worked out', 'exercise'],
            'v_low': ['sat', 'rested', 'still', 'couch', 'lazy', 'tired', 'stayed in', 'sleep'],
            'r_high': ['music', 'friend', 'loved', 'connected', 'talked', 'together', 'art', 'nature', 'family'],
            'r_low': ['alone', 'isolated', 'lonely', 'quiet', 'disconnected', 'silent'],
            'C_high': ['focused', 'flow', 'productive', 'clear', 'capable', 'strong', 'read', 'worked'],
            'C_low': ['distracted', 'foggy', 'weak', 'confused', 'lost', 'procrastinated', 'blur'],
            'S_high': ['anxious', 'stressed', 'chaotic', 'overwhelmed', 'sad', 'angry', 'bad', 'down'],
            'S_low': ['calm', 'peaceful', 'happy', 'good', 'relaxed', 'stable', 'fine', 'okay']
        }

    def extract_dimension(self, text: str, high_keys: list, low_keys: list) -> float:
        """Basic NLP heuristic to convert chat text into a 0.1 - 0.9 tensor value."""
        text_lower = text.lower()
        high_score = sum(text_lower.count(w) for w in high_keys)
        low_score = sum(text_lower.count(w) for w in low_keys)
        
        if high_score == 0 and low_score == 0:
            return 0.5 # Neutral baseline if no keywords are matched
            
        val = (high_score + (1.0 if low_score == 0 else 0.0)) / (high_score + low_score + 1.0)
        return float(np.clip(val, 0.1, 0.9))

    def transduce_day(self, movement_text: str, connection_text: str, focus_text: str, mood_text: str) -> AgnosticRealityTensor:
        """Takes all 4 check-in answers and generates your Daily Reality Tensor."""
        
        # 1. Map to Dimensions
        velocity = self.extract_dimension(movement_text, self.lexicon['v_high'], self.lexicon['v_low'])
        resonance = self.extract_dimension(connection_text, self.lexicon['r_high'], self.lexicon['r_low'])
        capacity = self.extract_dimension(focus_text, self.lexicon['C_high'], self.lexicon['C_low'])
        entropy = self.extract_dimension(mood_text, self.lexicon['S_high'], self.lexicon['S_low'])
        
        # Moderate resistance (0.5) unless velocity and entropy are both high
        resistance = 0.8 if (velocity > 0.7 and entropy > 0.7) else 0.5
        
        # 2. Build the Tensor
        components = [velocity, resistance, resonance, capacity, entropy]
        tensor = AgnosticRealityTensor(components, indices='contravariant')
        
        # 3. Add Epistemic Humility (Axiom 0)
        conf = Confidence(ConfidenceLevel.MODERATE, "Transduced from Telegram text heuristics")
        for i in range(5):
            tensor.add_confidence(i, conf)
            
        return tensor

# Global instance
transducer = PersonalTransducer()

def log_daily_checkin(movement: str, connection: str, focus: str, mood: str) -> dict:
    """Processes the check-in and returns the Synthium report."""
    
    # 1. Transduce text to Math
    daily_tensor = transducer.transduce_day(movement, connection, focus, mood)
    
    # 2. Synthium Physics: Calculate Enjoyment (E) and Meaning (M)
    enjoyment = daily_tensor.E
    meaning = daily_tensor.M
    
    return {
        "tensor": daily_tensor,
        "enjoyment": enjoyment,
        "meaning": meaning,
        "summary": f"Velocity (v): {daily_tensor.v:.2f} | Resonance (r): {daily_tensor.r:.2f} | Capacity (C): {daily_tensor.C:.2f} | Entropy (S): {daily_tensor.S:.2f}"
    }


