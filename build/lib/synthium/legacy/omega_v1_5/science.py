from .vectors import SynthiumVector

class HolisticScience:
    def derive_formula(self, vector: SynthiumVector) -> str:
        formulas = []
        
        if vector.R > 0.6 and vector.C > 0.6:
            formulas.append("Mass = R × C")
        if vector.v > 0.7:
            if vector.R < 0.3:
                formulas.append("Flow = v²/R")
            else:
                formulas.append("Friction = v × R")
        if vector.r > 0.7:
            formulas.append("Attraction ∝ r²")
        if vector.S > 0.7:
            formulas.append("Decay = e^(S)")
        
        return " + ".join(formulas) if formulas else "Complex = f(v,R,r,C,S)"

    def analyze(self, vector: SynthiumVector) -> dict:
        mass = vector.R * vector.C
        stability = 1.0 / (vector.S + 0.01)
        potential = vector.C * (1 - vector.S)
        
        return {
            "mass_index": f"{mass:.3f}",
            "stability_score": f"{stability:.3f}",
            "energy_potential": f"{potential:.3f}",
            "derived_formula": self.derive_formula(vector),
            "coherent": vector.is_coherent()
        }
