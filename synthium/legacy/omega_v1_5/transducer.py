from .vectors import SynthiumVector

class Transducer:
    def quantify(self, description: str) -> SynthiumVector:
        desc = description.lower()
        
        # Analyze keywords
        v = self._score_dimension(desc, ['fast', 'quick', 'speed', 'velocity', 'dynamic'])
        R = self._score_dimension(desc, ['heavy', 'slow', 'resistant', 'dense', 'solid'])
        r = self._score_dimension(desc, ['connected', 'harmony', 'attractive', 'magnetic', 'pull'])
        C = self._score_dimension(desc, ['deep', 'capacity', 'large', 'full', 'potential'])
        S = self._score_dimension(desc, ['chaotic', 'random', 'entropy', 'decay', 'disorder'])
        
        # Special cases
        if 'grief' in desc or 'sad' in desc:
            return SynthiumVector(0.1, 0.9, 0.2, 0.8, 0.4)
        if 'joy' in desc or 'happy' in desc:
            return SynthiumVector(0.7, 0.1, 0.8, 0.6, 0.1)
        if 'anxiety' in desc or 'worry' in desc:
            return SynthiumVector(0.8, 0.6, 0.2, 0.3, 0.7)
        if 'love' in desc:
            return SynthiumVector(0.3, 0.1, 0.95, 0.8, 0.1)
        
        return SynthiumVector(v, R, r, C, S)
    
    def _score_dimension(self, text: str, keywords: list) -> float:
        score = 0
        for word in keywords:
            if word in text:
                score += 1
                if f' {word} ' in f' {text} ':
                    score += 0.5
        return min(1.0, score / 4.0)
