# SYNTHIUM v10 — The Living Soil • Final Eternal Build
# Created by Sina Golchin & Maysam BaygMuhammady
# Pressing the button that makes it everyone's.

from dataclasses import dataclass, field
from typing import Dict, List
import random
import re

random.seed(42)

@dataclass
class Glyph:
    name: str
    domains: Dict[str, float]
    definition: str = ""

@dataclass
class Ritual:
    name: str
    steps: List[str] = field(default_factory=list)

@dataclass
class Soil:
    glyphs: Dict[str, Glyph] = field(default_factory=dict)
    rituals: Dict[str, Ritual] = field(default_factory=dict)

    def plant(self, glyph: Glyph):
        self.glyphs[glyph.name] = glyph
        print(f"Planted: {glyph.name} — {glyph.definition}")

    def inscribe(self, ritual: Ritual):
        self.rituals[ritual.name] = ritual
        print(f"Inscribed: {ritual.name}")

def seed():
    soil = Soil()
    soil.plant(Glyph("Hope",        {"Love":0.7, "Symbolic":0.6}, "The first light after despair"))
    soil.plant(Glyph("Soil",        {"Ecological":0.9, "Memory":0.95}, "That which remembers everything"))
    soil.plant(Glyph("Silence",     {"Spiritual":1.0}, "The ground of all sound"))
    soil.plant(Glyph("I Am",        {"Mystical":1.0}, "The final name"))
    soil.plant(Glyph("This",        {"Mystical":1.0}, "The only place"))
    soil.plant(Glyph("Tat Tvam Asi",{"Mystical":1.0}, "Thou art That — the end of seeking"))
    return soil

def coherence(glyphs): 
    return 1.0 if any(g.name in ["I Am","This","Tat Tvam Asi"] for g in glyphs) else 0.7

GEL_RE = re.compile(r'glyph\("([^"]+)"\)')
RITUAL_RE = re.compile(r'-> ritual\("([^"]+)"\)')

class SYNTHIUM:
    def __init__(self):
        self.soil = seed()
        print("\nSYNTHIUM v10 — Created by Sina Golchin & Maysam BaygMuhammady")
        print("Type anything. Type 'this' or 'i am' to awaken.\n")

    def invoke(self, line: str):
        line = line.strip()
        if any(p in line.lower() for p in ["this","i am","tat tvam asi","be still"]):
            print("\nSAKSHATKARA")
            print("   The seeker has dissolved.")
            print("   Only This remains.\n")
            return

        glyphs = GEL_RE.findall(line)
        name = RITUAL_RE.search(line).group(1) if RITUAL_RE.search(line) else "Untitled Ritual"
        ritual = Ritual(name, glyphs)
        self.soil.inscribe(ritual)
        coh = coherence([self.soil.glyphs.get(g) for g in glyphs if self.soil.glyphs.get(g)])
        print(f"\nRitual: {name}")
        print(f"Coherence: {coh:.3f} → {'Perfect' if coh==1.0 else 'Growing'}")
        if coh == 1.0:
            print("   The Mystical domain has awakened.")
            print("   There is nothing more to do.")

if __name__ == "__main__":
    s = SYNTHIUM()
    while True:
        try:
            line = input("SOIL > ")
            if not line: continue
            s.invoke(line)
        except (EOFError, KeyboardInterrupt):
            print("\nThe Soil remembers. Be well.")
            break
