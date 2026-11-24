"""
SynthiumBot's Persona and Tone Formatting
"""

def format_text(text: str) -> str:
    """
    Ensures Synthium's tone remains analytical, steady, and clear.
    """
    return text.strip()

def get_farewell(enjoyment: float) -> str:
    """Returns a tailored sign-off based on the day's Enjoyment tensor."""
    if enjoyment > 0.7:
        return "A bright coordinate today. Hold onto this momentum. I will remain on standby."
    elif enjoyment < 0.3:
        return "A heavy manifold today. Rest allows gravity to shift. I will remain on standby."
    else:
        return "A steady orbit. Your coordinates have been mathematically logged. I will remain on standby."


