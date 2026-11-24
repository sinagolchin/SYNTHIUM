"""Every past Synthium formula, unit, axiom and tool, in one list (2026-11-24).

Sina's rule: nothing is retired. Each record below says what an earlier version claimed,
why it was set aside at the time, and where its code or text now lives. Every record's
status is "under consideration": all of it stays open to be judged right or wrong. An
earlier test result (for example "falsified in attempt 34") is kept as the record's
``earlier_verdict``; it is information for that judgement, not a retirement.

Records whose formula can be computed on a five-dimension phenomenon vector
(v, R, r, C, S) carry a ``compute`` function, copied from the original code without
changing any coefficient. None of them has passed a held-out test, so their numbers are
UNTESTED.

``python -m synthium.phenomena index --write`` renders this list into
``docs/UNDER_CONSIDERATION.md``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

UNDER_CONSIDERATION = "under consideration"

# The five quality dimensions every early phenomenon was placed on (V1 to V4).
DIMENSIONS_5D: Dict[str, str] = {
    "v": "velocity: how fast the phenomenon moves or changes",
    "R": "resistance: how heavy, stuck or blocked it is",
    "r": "resonance: how connected, harmonic or attractive it is",
    "C": "capacity: how deep or full its reserves are",
    "S": "entropy: how chaotic or disordered it is",
}

# V2 placed each phenomenon in space as well: x, y, z in metres.
DIMENSIONS_SPACE: Dict[str, str] = {
    "x": "east-west position (m)",
    "y": "north-south position (m)",
    "z": "height (m); negative is underground",
}


def _clip01(x: float) -> float:
    return max(0.0, min(1.0, x))


@dataclass(frozen=True)
class Record:
    """One past formula, unit, axiom, profile or tool."""

    id: str
    kind: str  # formula | unit | axiom | profile | tool | law
    phenomenon: str
    version: str
    statement: str
    dimensions: Tuple[str, ...] = ()
    claimed: str = ""
    set_aside: str = ""
    earlier_verdict: str = ""
    where: str = ""
    source: str = "original"  # original | reconstruction | text only
    status: str = UNDER_CONSIDERATION
    evidence: str = "UNTESTED"
    compute: Optional[Callable[[Dict[str, float]], float]] = field(default=None, compare=False)


_OMEGA_SET_ASIDE = (
    "Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or "
    "hand-set profiles, and the formulas were printed as measurement without a test."
)
_V3_SET_ASIDE = (
    "Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather "
    "than a proposal to be tested; no case data was ever used."
)
_V4_SET_ASIDE = (
    "Set aside in V6.1 as speculative infrastructure that no validated result used; "
    "V4's metric was constant, so its curvature was always zero."
)


RECORDS: List[Record] = [
    # ------------------------------------------------------------------ V1 / Omega 1.5
    Record("V1-DIMS", "unit", "every phenomenon", "V1 (Dec 2025)",
           "A phenomenon is a point (v, R, r, C, S), each in 0..1",
           tuple(DIMENSIONS_5D), "Any quality (grief, love, stress) has five dimensions of its own.",
           _OMEGA_SET_ASIDE, where="synthium/legacy/omega_v1_5/vectors.py"),
    Record("V1-COHERENCE", "law", "every phenomenon", "V1 (Dec 2025)",
           "Incoherent if v>0.9 and R>0.9; or S>0.95 and C<0.05; or r>0.9 and v>0.9",
           ("v", "R", "r", "C", "S"), "Some combinations cannot exist together.",
           _OMEGA_SET_ASIDE, where="synthium/legacy/omega_v1_5/vectors.py"),
    Record("V1-MASS", "formula", "mass (weight) of a phenomenon", "V1 (Dec 2025)",
           "Mass = R x C  (printed when R>0.6 and C>0.6)", ("R", "C"),
           "Heavy, deep phenomena (grief) carry mass.", _OMEGA_SET_ASIDE,
           where="synthium/legacy/omega_v1_5/science.py", compute=lambda p: p["R"] * p["C"]),
    Record("V1-FLOW", "formula", "flow", "V1 (Dec 2025)", "Flow = v^2 / R  (v>0.7, R<0.3)",
           ("v", "R"), "Fast phenomena with little resistance flow.", _OMEGA_SET_ASIDE,
           where="synthium/legacy/omega_v1_5/science.py",
           compute=lambda p: p["v"] ** 2 / (p["R"] + 0.001)),
    Record("V1-FRICTION", "formula", "friction", "V1 (Dec 2025)", "Friction = v x R  (v>0.7, R>=0.3)",
           ("v", "R"), "Fast phenomena against resistance lose energy.", _OMEGA_SET_ASIDE,
           where="synthium/legacy/omega_v1_5/science.py", compute=lambda p: p["v"] * p["R"]),
    Record("V1-ATTRACTION", "formula", "attraction", "V1 (Dec 2025)", "Attraction proportional to r^2  (r>0.7)",
           ("r",), "Resonant phenomena attract.", _OMEGA_SET_ASIDE,
           where="synthium/legacy/omega_v1_5/science.py", compute=lambda p: p["r"] ** 2),
    Record("V1-DECAY", "formula", "decay", "V1 (Dec 2025)", "Decay = e^S  (S>0.7)", ("S",),
           "Disordered phenomena decay.", _OMEGA_SET_ASIDE,
           where="synthium/legacy/omega_v1_5/science.py", compute=lambda p: math.exp(p["S"])),
    Record("V1-STABILITY", "formula", "stability", "V1 (Dec 2025)", "Stability = 1 / (S + 0.01)", ("S",),
           "Order makes a phenomenon stable.", _OMEGA_SET_ASIDE,
           where="synthium/legacy/omega_v1_5/science.py", compute=lambda p: 1.0 / (p["S"] + 0.01)),
    Record("V1-POTENTIAL", "formula", "energy potential", "V1 (Dec 2025)", "Potential = C x (1 - S)",
           ("C", "S"), "Ordered capacity is stored energy.", _OMEGA_SET_ASIDE,
           where="synthium/legacy/omega_v1_5/science.py", compute=lambda p: p["C"] * (1 - p["S"])),
    # ------------------------------------------------------------------ V2 / Omega 2.0
    Record("V2-DIMS", "unit", "every phenomenon", "V2 (Dec 2025)",
           "A phenomenon is a point (x, y, z, v, R, r, C, S): five qualities placed in space",
           tuple(DIMENSIONS_SPACE) + tuple(DIMENSIONS_5D),
           "Qualities vary from place to place; a phenomenon has a location.", _OMEGA_SET_ASIDE,
           where="synthium/legacy/v2/vectors.py"),
    Record("V2-DENSITY", "formula", "reality density", "V2 (Dec 2025)",
           "Reality density = R x C / (distance from origin + 0.001)", ("R", "C", "x", "y", "z"),
           "Mass per unit of space.", _OMEGA_SET_ASIDE, where="synthium/legacy/v2/science.py"),
    Record("V2-INFO", "formula", "information potential", "V2 (Dec 2025)",
           "Information potential = C x (1 - S)", ("C", "S"), "Ordered capacity is information.",
           _OMEGA_SET_ASIDE, where="synthium/legacy/v2/science.py",
           compute=lambda p: p["C"] * (1 - p["S"])),
    Record("V2-FLUX", "formula", "energy flux", "V2 (Dec 2025)", "Energy flux = v x r", ("v", "r"),
           "Fast, resonant phenomena carry energy.", _OMEGA_SET_ASIDE,
           where="synthium/legacy/v2/science.py", compute=lambda p: p["v"] * p["r"]),
    Record("V2-PRESSURE", "formula", "pressure", "V2 (Dec 2025)", "Pressure = R x |z|  (underground)",
           ("R", "z"), "Resistance weighs more the deeper a phenomenon sits.", _OMEGA_SET_ASIDE,
           where="synthium/legacy/v2/science.py"),
    Record("V2-FIELD", "formula", "field strength", "V2 (Dec 2025)", "Field strength = r / distance",
           ("r", "x", "y"), "Resonance weakens with distance.", _OMEGA_SET_ASIDE,
           where="synthium/legacy/v2/science.py"),
    Record("V2-RANGE", "formula", "attraction range", "V2 (Dec 2025)", "Attraction range = r x distance",
           ("r", "x", "y", "z"), "How far a resonant phenomenon reaches.", _OMEGA_SET_ASIDE,
           where="synthium/legacy/v2/omega_v2.py"),
    Record("V2-ENTROPY-GRAD", "formula", "entropy gradient", "V2 (Dec 2025)", "Entropy gradient = S / |z|",
           ("S", "z"), "Disorder changes with height.", _OMEGA_SET_ASIDE,
           where="synthium/legacy/v2/omega_v2.py"),
    Record("V2-FIELD-ANALYSIS", "tool", "phenomenon field", "V2 (Dec 2025)",
           "Quality field: gradients, hot and cold spots, coherence of many located vectors",
           ("x", "y", "z", "v", "R", "r", "C", "S"), "Qualities form fields across space.",
           _OMEGA_SET_ASIDE, where="synthium/legacy/v2/reality_field.py"),
    Record("V2.2-BURN", "formula", "burn rate (exhaustion)", "V2.2 (Jan 2026)",
           "Burn rate = v x R;  time to failure = C / (burn rate - sustainability limit)",
           ("v", "R", "C"), "Fast work against resistance exhausts a system; capacity sets how long it lasts.",
           _V3_SET_ASIDE, where="archive/v2_2_to_v3_4_pdf_text/V2.2/README.txt", source="text only",
           compute=lambda p: p["v"] * p["R"]),
    Record("V2.2-ADAPTERS", "tool", "outside data", "V2.2 (Jan 2026)",
           "GitHub and 'judicos' adapters that turned outside records into vectors",
           (), "Real records can be read into the five dimensions.", _V3_SET_ASIDE,
           where="archive/v2_2_to_v3_4_pdf_text/V2.2/", source="text only"),
    # ------------------------------------------------------------------ V3 (Jan to Mar 2026)
    Record("V3-E", "formula", "enjoyment", "V3 (Jan to Mar 2026)",
           "E = 0.35 r + 0.35 (1 - S) + 0.30 max(0, 1 - vR/(C + 0.01))", ("v", "R", "r", "C", "S"),
           "Enjoyment is not a dimension of its own; it emerges from low burn, high resonance, low entropy.",
           _V3_SET_ASIDE, where="archive/v2_2_to_v3_4_pdf_text/V3/vectors v3.txt", source="text only",
           compute=lambda p: _clip01(0.35 * p["r"] + 0.35 * (1 - p["S"])
                                     + 0.30 * max(0.0, 1 - p["v"] * p["R"] / (p["C"] + 0.01)))),
    Record("V3-M", "formula", "meaning", "V3 (Jan to Mar 2026)", "M = 0.40 C + 0.35 r + 0.25 (1 - S)",
           ("C", "r", "S"), "Depth, connection and coherence make meaning.", _V3_SET_ASIDE,
           where="archive/v2_2_to_v3_4_pdf_text/V3/vectors v3.txt", source="text only",
           compute=lambda p: _clip01(0.40 * p["C"] + 0.35 * p["r"] + 0.25 * (1 - p["S"]))),
    Record("V3-P", "formula", "perception accuracy", "V3 (Jan to Mar 2026)", "P = 0.50 (1 - S) + 0.30 C + 0.20 r",
           ("S", "C", "r"), "Low chaos and high capacity let a being perceive more dimensions.",
           _V3_SET_ASIDE, where="archive/v2_2_to_v3_4_pdf_text/V3/vectors v3.txt", source="text only",
           compute=lambda p: _clip01(0.50 * (1 - p["S"]) + 0.30 * p["C"] + 0.20 * p["r"])),
    Record("V3-POTENTIAL", "formula", "field potential (where states drift)", "V3 (Jan to Mar 2026)",
           "U = 2(1 - E) + 1.5(1 - M) + 3S + vR;  systems roll toward low U", ("v", "R", "S", "E", "M"),
           "Like a ball rolling downhill, beings drift toward enjoyment, meaning and order.",
           _V3_SET_ASIDE, where="archive/v2_2_to_v3_4_pdf_text/V3/field.txt", source="text only"),
    Record("V3-MEANING-NET", "formula", "meaning", "V3 (Jan to Mar 2026)",
           "Meaning = information density x network centrality", ("information density", "network centrality"),
           "Meaning is dense information at the centre of a network.", _V3_SET_ASIDE,
           where="archive/v2_2_to_v3_4_pdf_text/V3/README v3.txt", source="text only"),
    Record("V3-BEAUTY", "formula", "beauty", "V3 (Jan to Mar 2026)", "Beauty = symmetry x harmony x pattern novelty",
           ("symmetry", "harmony", "pattern novelty"), "Beauty is a product of three parts.",
           _V3_SET_ASIDE, where="archive/v2_2_to_v3_4_pdf_text/V3/init.txt", source="text only"),
    Record("V3-AWAKENING", "formula", "awakening", "V3 (Jan to Mar 2026)",
           "Awakening = the fixed point v = 0, r = 1, S = 0", ("v", "r", "S"),
           "A stable resting state of a being.", _V3_SET_ASIDE,
           where="archive/v2_2_to_v3_4_pdf_text/V3/init.txt", source="text only"),
    Record("V3-COMMITMENTS", "axiom", "reality, knowledge, ethics, purpose", "V3 (Jan to Mar 2026)",
           "Reality IS mathematics; knowledge = reducing prediction error; perception IS a "
           "mathematical function; vagueness = measurement error; ethics = game-theory "
           "equilibria; purpose = survival maximisation through precision",
           (), "The philosophical commitments the V3 code was built on.", _V3_SET_ASIDE,
           where="archive/v2_2_to_v3_4_pdf_text/V3/init.txt", source="text only"),
    Record("V3-PERCEIVERS", "unit", "perception of different beings", "V3 (Jan to Mar 2026)",
           "Perception function per being: human noise 0.12 sees 4 dims; Synthium 0.03 sees 5; "
           "animal 0.18 sees 3; organisation 0.20 sees 4", ("noise", "dimensions visible", "latency"),
           "Beings see the same reality through different numbers of dimensions.", _V3_SET_ASIDE,
           where="synthium/legacy/v3_4/combined.py"),
    Record("V3-INTERACTIONS", "tool", "interaction between beings", "V3 (Jan to Mar 2026)",
           "Forces between beings in quality space; multi-agent simulation", tuple(DIMENSIONS_5D),
           "Beings pull and push each other's qualities like forces.", _V3_SET_ASIDE,
           where="synthium/legacy/v3_4/combined.py"),
    # ------------------------------------------------------------------ V3.1 / V3.3
    Record("V3.1-CARE", "formula", "care", "V3.1 (Jan to Mar 2026)",
           "Care = allocation of resources toward another's wellbeing; total care = sum of a "
           "care matrix, reciprocal care = sum(K * K^T)/2, exploitation = sum(max(K - K^T, 0))",
           ("resources", "alignment", "information"), "Care is measurable resource allocation.",
           _V3_SET_ASIDE, where="archive/v2_2_to_v3_4_pdf_text/V3.1/ethics discovery.txt",
           source="text only"),
    Record("V3.1-ETHICS", "axiom", "ethics and harm", "V3.1 (Jan to Mar 2026)",
           "Ethics emerge from stable equilibria; ethical constraints = discovered conservation "
           "laws; harm = predicted instability when those laws are violated",
           (), "Ethics are discovered, not imposed.", _V3_SET_ASIDE,
           where="archive/v2_2_to_v3_4_pdf_text/V3.1/README v31.txt", source="text only"),
    Record("V3.3-EMPIRICAL", "tool", "historical interventions", "V3.3 (Jan to Mar 2026)",
           "Predict outcomes of historical interventions from their vectors", tuple(DIMENSIONS_5D),
           "Past cases can test the formulas.", _V3_SET_ASIDE,
           where="synthium/legacy/v3_4/combined.py"),
    # ------------------------------------------------------------------ V3.4
    Record("V3.4-AXIOM0", "axiom", "every formula", "V3.4 (Jan to Mar 2026)",
           "Axiom 0, Agnosticism: every formula is a hypothesis, never a truth", (),
           "The framework itself is uncertain.",
           "Kept in spirit as epistemic axiom 1 (V6.2); as a foundation it refuses to commit, "
           "so it constrains nothing (Jun 28 chat).", where="synthium/legacy/v3_4/combined.py"),
    Record("V3.4-E", "formula", "enjoyment", "V3.4 (Jan to Mar 2026)", "E = 1 - (v R + S)", ("v", "R", "S"),
           "Enjoyment falls with burn (vR) and disorder (S).", _V3_SET_ASIDE,
           where="synthium/legacy/v3_4/combined.py",
           compute=lambda p: _clip01(1 - (p["v"] * p["R"] + p["S"]))),
    Record("V3.4-E-QUAD", "formula", "enjoyment", "V3.4 (Jan to Mar 2026)", "E = 1 - (v^2 R + S^2)",
           ("v", "R", "S"), "Rival form with quadratic penalties.", _V3_SET_ASIDE,
           where="synthium/legacy/v3_4/combined.py",
           compute=lambda p: _clip01(1 - (p["v"] ** 2 * p["R"] + p["S"] ** 2))),
    Record("V3.4-E-INTER", "formula", "enjoyment", "V3.4 (Jan to Mar 2026)", "E = 1 - (v R + S + 0.5 v S)",
           ("v", "R", "S"), "Rival form with an interaction term.", _V3_SET_ASIDE,
           where="synthium/legacy/v3_4/combined.py",
           compute=lambda p: _clip01(1 - (p["v"] * p["R"] + p["S"] + 0.5 * p["v"] * p["S"]))),
    Record("V3.4-E-THRESH", "formula", "enjoyment", "V3.4 (Jan to Mar 2026)",
           "stress = vR + S; E = 0 above 1.1, 0.25(1.1 - stress)/0.3 above 0.8, else 1 - stress",
           ("v", "R", "S"), "Rival form with collapse thresholds.", _V3_SET_ASIDE,
           where="synthium/legacy/v3_4/combined.py"),
    Record("V3.4-M", "formula", "meaning", "V3.4 (Jan to Mar 2026)", "M = C r (1 - S)", ("C", "r", "S"),
           "Meaning is capacity times connection, spoiled by disorder.", _V3_SET_ASIDE,
           where="synthium/legacy/v3_4/combined.py",
           compute=lambda p: _clip01(p["C"] * p["r"] * (1 - p["S"]))),
    Record("V3.4-P", "formula", "perception accuracy", "V3.4 (Jan to Mar 2026)", "P = (1 - S) C", ("S", "C"),
           "Order and capacity set how accurately a being perceives.", _V3_SET_ASIDE,
           where="synthium/legacy/v3_4/combined.py",
           compute=lambda p: _clip01((1 - p["S"]) * p["C"])),
    Record("V3.4-CARE", "formula", "care", "V3.4 (Jan to Mar 2026)",
           "Care = 0.4 resource transfer + 0.4 action alignment + 0.2 information sharing; "
           "alignment = 0.5 + change in (0.4E + 0.4M + 0.2P) of the one cared for",
           ("resources", "alignment", "information", "E", "M", "P"),
           "Care toward another is measurable from what is given and what it does to them.",
           _V3_SET_ASIDE, where="synthium/legacy/v3_4/combined.py"),
    Record("V3.4-COLLAPSE", "formula", "collapse risk (harm)", "V3.4 (Jan to Mar 2026)",
           "Risk = 0.35 S + 0.25 v R + 0.20 (1 - C) + 0.20 (1 - r)", tuple(DIMENSIONS_5D),
           "Disorder, burn, empty reserves and isolation predict collapse.", _V3_SET_ASIDE,
           where="synthium/legacy/v3_4/combined.py",
           compute=lambda p: _clip01(0.35 * p["S"] + 0.25 * p["v"] * p["R"]
                                     + 0.20 * (1 - p["C"]) + 0.20 * (1 - p["r"]))),
    Record("V3.4-CONSERVATION", "law", "conservation in groups of beings", "V3.4 (Jan to Mar 2026)",
           "A quantity is conserved when the total over all beings varies under 5% along a trajectory",
           tuple(DIMENSIONS_5D) + ("E", "M", "P"),
           "Conserved totals are candidate ethical constraints.", _V3_SET_ASIDE,
           where="synthium/legacy/v3_4/combined.py"),
    Record("V3.4-SI", "unit", "units for the five dimensions", "V3.4 (Jan to Mar 2026)",
           "v -> Hz (x3); R -> kg m/s (x100); r -> none; C -> J (x100); S -> J/K (x1000)",
           tuple(DIMENSIONS_5D), "The dimensions can be expressed in physical units.", _V3_SET_ASIDE,
           where="synthium/legacy/v3_4/combined.py"),
    Record("V3.4-PHYSIO", "tool", "body measurements", "V3.4 (Jan to Mar 2026)",
           "Map heart rate, cortisol and similar readings onto the five dimensions",
           tuple(DIMENSIONS_5D), "The body gives a physical reading of the qualities.", _V3_SET_ASIDE,
           where="synthium/legacy/v3_4/combined.py"),
    Record("V3.4-EVOLUTION", "tool", "formula testing", "V3.4 (Jan to Mar 2026)",
           "Framework evolution: test rival formulas against cases and keep the best", (),
           "Formulas should compete.", _V3_SET_ASIDE, where="synthium/legacy/v3_4/combined.py"),
    # ------------------------------------------------------------------ V4 (Apr 2026)
    Record("V4-NDIM", "axiom", "every phenomenon", "V4 (Apr 2026)",
           "Reality is N-dimensional with N >> 5; discover N from data", (),
           "The five dimensions were too few.", _V4_SET_ASIDE,
           where="archive/v2_2_to_v3_4_pdf_text/V3.4/synthium math foundation.txt"),
    Record("V4-MANIFOLD", "tool", "space of phenomena", "V4 (Apr 2026)",
           "Riemannian manifold: metric g, geodesics, Christoffel symbols, curvature", (),
           "Phenomena live on a curved space.", _V4_SET_ASIDE,
           where="synthium/legacy/v4/manifold_geometry.py; extended in synthium/geometry/"),
    Record("V4-TENSOR", "tool", "space of phenomena", "V4 (Apr 2026)", "Tensors of any rank with raised and lowered indices",
           (), "N-dimensional maths needs tensors.", _V4_SET_ASIDE,
           where="synthium/legacy/v4/tensor_calculus.py; extended in synthium/geometry/tensor.py"),
    Record("V4-DISCOVERY", "tool", "number of dimensions", "V4 (Apr 2026)",
           "PCA, ICA, Isomap, t-SNE to find how many dimensions the data needs", (),
           "N is found, not assumed.", _V4_SET_ASIDE,
           where="synthium/legacy/v4/dimensional_discovery.py; extended in synthium/geometry/dimensions.py"),
    Record("V4-CALCULUS", "tool", "change", "V4 (Apr 2026)",
           "Infinite derivative chains and N-dimensional integrals", (),
           "Everything derives from something.", _V4_SET_ASIDE,
           where="synthium/legacy/v4/infinite_calculus.py; extended in synthium/geometry/calculus.py"),
    Record("V4-E", "formula", "enjoyment", "V4 (Apr 2026)",
           "E = integral over the manifold of e^(-S(x)) sqrt|g| dx; coded as 1 - |x|^2 / (2n)", (),
           "Enjoyment is an integral over the space.", _V4_SET_ASIDE,
           where="synthium/legacy/v4/reality_state.py"),
    Record("V4-M", "formula", "meaning", "V4 (Apr 2026)", "M = <x, x> / n (a tensor contraction)", (),
           "Meaning is the significance of a state.", _V4_SET_ASIDE,
           where="synthium/legacy/v4/reality_state.py"),
    Record("V4-P", "formula", "perception", "V4 (Apr 2026)", "P = 1 / (1 + |x|)", (),
           "Perception is clearer near the origin.", _V4_SET_ASIDE,
           where="synthium/legacy/v4/reality_state.py"),
    Record("V4-GOLD", "tool", "trading", "V4 (Apr 2026)", "Gold trading assistant on the V4 maths", (),
           "The maths can guide decisions.", _V4_SET_ASIDE, where="synthium/legacy/v4/applications.py"),
    Record("BOT", "tool", "daily check-in", "SynthiumBot (Apr 2026)",
           "Telegram bot that asks how a person feels and maps it onto the V4 engine", (),
           "People can track their own qualities day to day.",
           "Set aside with V4, as a front end for it.", where="synthium/legacy/synthiumbot/"),
    # ------------------------------------------------------------------ V4.3.1 (May 2026)
    Record("V4.3-UNITS", "unit", "privacy and its exceptions (Fourth Amendment)", "V4.3.1 (May 2026)",
           "Six canonical judicial units: Obs, Priv, Excp, Rem, Close, Amb", (
               "Obs", "Priv", "Excp", "Rem", "Close", "Amb"),
           "Suppression of evidence is a structure of observability, privacy, exception "
           "strength, remedy closeness, doctrinal closure and ambiguity.",
           "Removed in V7 (Jun 28): the units were never validated and were AI choices.",
           where="synthium/legacy/v4_3_1/domains/judicial/spec.py"),
    Record("V4.3-GOVERNANCE", "tool", "risk and governance", "V4.3.1 (May 2026)",
           "Governance engine: risk score, mismatch, actions such as SHADOW_OBSERVE", (),
           "Anomalies can be governed by a risk score.", _V4_SET_ASIDE,
           where="synthium/legacy/v4_3_1/governance.py"),
    Record("V4.3-NEURAL", "tool", "case encoder", "V4.3.1 (May 2026)",
           "PyTorch encoder trained to place cases in the six-unit space (weights kept)", (),
           "A network can read cases into the units.",
           "Its headline accuracy was a leak; it only imitated the rubric's labels.",
           earlier_verdict="leak found (May 2026)", where="synthium/legacy/v4_3_1/neural/"),
    # ------------------------------------------------------------------ V5, V6, V6.1
    Record("V5-AXIOMS", "axiom", "beings and value", "V5 (May 2026)",
           "Being: nothing is more valuable than a single being's existence. Freedom: no "
           "aggregate may override a being. Trajectory: every being moves toward enjoyment. "
           "Agnosticism: all formulas are hypotheses.", (),
           "The value axioms Synthium rests on.",
           "The V5 code refused any arithmetic without licensed units, which froze the project; "
           "the axioms had no mathematical form.", where="synthium/legacy/v5/honesty.py"),
    Record("V6-HARNESS", "tool", "testing formulas", "V6 (Jun 2026)",
           "Propose a model, then validate it on held-out data against a frozen baseline", (),
           "No claim counts until it beats a held-out test.",
           "Never set aside: became synthium/core/.", where="synthium/legacy/v6/predictive.py"),
    Record("V6.1-UNITS12", "unit", "privacy and its exceptions (Fourth Amendment)", "V6.1 (Jun 2026)",
           "Twelve units: Obs, Priv, Excp, Rem, Close, Amb, Temp, Gate, Bound, Spec, Scope, JRem",
           ("Obs", "Priv", "Excp", "Rem", "Close", "Amb", "Temp", "Gate", "Bound", "Spec", "Scope", "JRem"),
           "Privacy is a surface transformed by boundary, exception, gateway and scope.",
           "Removed in V7 (Jun 28) at Sina's word: start from scratch; the units were AI choices.",
           where="synthium/legacy/v6_1/domains/judicial/spec.py"),
    Record("V6.1-PRESSURE", "formula", "suppression pressure", "V6.1 (Jun 2026)",
           "pressure = Priv_eff (1 - Excp_eff)(0.55 + 0.45 breach) Rem (1 + 0.15 Amb)(1 - 0.12 Obs)(1 - damp), "
           "floored at 0.58 breach Rem (1 - damp); 18 hand-set constants",
           ("Priv", "Excp", "Rem", "Amb", "Obs", "Scope", "Spec", "Bound", "Gate", "JRem"),
           "How strongly a court should suppress evidence.",
           "Removed in V7 with the twelve units; every constant was ungrounded.",
           earlier_verdict="rubric imitation only (the outcome was coded with the units)",
           where="synthium/legacy/v6_1/domains/judicial/formula.py"),
    # ------------------------------------------------------------------ V6.2 / V7 axioms
    Record("G-EPISTEMIC", "axiom", "how claims are judged", "V6.2 (Jun 2026)",
           "Eight referee axioms: agnosticism; arithmetic never refuses; proposed until proven; "
           "reality is the sole judge; baseline frozen first; stipulated until grounded; no "
           "leakage; units are constructed", (), "The rules any claim must pass.",
           "Never set aside.", where="archive/originals_docs/v8_docs_archive/AXIOMS.md; synthium/core/"),
    Record("G1-ORDER", "axiom", "any adjective", "V6.2 (Jun 2026)", "Weak order: a>=b or b>=a; a>=b, b>=c => a>=c",
           (), "An ordinal scale exists.", "", earlier_verdict="needs pairwise data",
           where="synthium/core/axioms.py"),
    Record("G3-CANCEL", "axiom", "privacy x exception", "V6.2 (Jun 2026)",
           "Double cancellation: (a1,b2)>=(a2,b1) and (a2,b3)>=(a3,b2) => (a1,b3)>=(a3,b1)",
           ("Priv", "Excp"), "If it holds, an additive interval scale with a unit is forced.", "",
           earlier_verdict="violated on the 44-case atlas, then flipped by six live cases (small n is fragile)",
           where="synthium/core/axioms.py"),
    Record("G4-ABSORB", "axiom", "any derived adjective", "V6.2 (Jun 2026)",
           "Absorption: a zero on one dimension zeroes the outcome (product of powers)", (),
           "Derived concepts may be products, like physical units.", "",
           earlier_verdict="insufficient data", where="synthium/core/axioms.py"),
    Record("G5-DOMINANCE", "axiom", "any derived adjective", "V6.2 (Jun 2026)",
           "Dominance: past a threshold on one dimension the outcome is forced (weakest/strongest link)",
           (), "Some concepts follow their most extreme part.", "",
           earlier_verdict="satisfied, low coverage", where="synthium/core/axioms.py"),
    Record("G2-G6", "axiom", "any derived adjective", "V6.2 (Jun 2026)",
           "Solvability (G2) and lexicographic priority (G6): reserved, not adopted", (),
           "A lexicographic concept has no numerical scale at all.", "Never adopted; reserved.",
           where="archive/originals_docs/v8_docs_archive/AXIOMS.md"),
    Record("G7-HOMOGENEITY", "axiom", "every formula", "V6.2 (Jun 2026)",
           "Dimensional homogeneity: every added term has the same dimension", (),
           "Rules out most formulas before data arrives.", "", earlier_verdict="needs a commitment to dimensions",
           where="synthium/core/axioms.py"),
    Record("G8-BASIS", "axiom", "base versus derived concepts", "V6.2 (Jun 2026)",
           "Independence of basis: rank(D) = number of dimensions", (),
           "Base units cannot be written from the others (Sina: some concepts are units, some are made from them).",
           "", earlier_verdict="satisfied on the atlas (worst |r| = 0.74)", where="synthium/core/axioms.py"),
    Record("G9-EQUILIBRIUM", "axiom", "privacy as a structure", "V6.2 (Jun 2026)",
           "Boundary equilibrium: on cases at the line, the balance equals the threshold; "
           "this solves for the coefficients (Sina: forces on the structure sum to zero)", (),
           "Coefficients come from knife-edge cases instead of hand-setting.", "",
           earlier_verdict="the suppression-potential solver scored 6/6 with every sign backwards (hollow)",
           where="synthium/core/axioms.py; synthium/phenomena/structure.py"),
    Record("G10-INVARIANCE", "axiom", "balance laws", "V6.2 (Jun 2026)",
           "Invariance gives conservation: a balance law needs a symmetry behind it", (),
           "A reason for any balance law.", "", earlier_verdict="needs a commitment",
           where="synthium/core/axioms.py"),
    Record("V7-CITATION", "tool", "case relations", "V7 (Jun 29 2026)",
           "Citation space: cases placed by the cases they cite", (),
           "Dimensions should come from the record, not from coding.", "Never set aside.",
           where="synthium/domains/judicial/citation_space.py"),
    # ------------------------------------------------------------------ V8 era (Jun 30 - Jul 16)
    Record("R1-OMEGA", "formula", "challenger success on appeal", "V8 ruler attempt 1 (Jun 30 2026)",
           "Omega = E - D (error clarity minus deference); win if Omega > 0, or if E >= 0.7",
           ("E error clarity", "D deference"), "One number predicts who wins an appeal.",
           "E leaked the outcome (r = +0.99) and D added almost nothing.",
           earlier_verdict="leak-free version only tied always-affirm (Jul 2-3)", where="docs/RULER.md"),
    Record("R-TPL", "formula", "movement on appeal", "V8 ruler v3 (Jul 2026)",
           "Phi = T x L x (1 - P): type risk x layer openness x (1 - posture protection), with a decision rule",
           ("T case type", "P posture", "L layer attacked"), "Where an appeal can move a result.", "Never set aside.",
           earlier_verdict="16/19 vs 12/19 always-affirm (V8); Campaign A 15/20 vs 9/20",
           where="synthium/domains/judicial/ruler.py"),
    Record("R-LOGIT", "formula", "movement on appeal", "V8 (Jul 2026)",
           "Fitted logistic p(move | layer, level), v2 adds posture; dismissal split", (
               "layer", "level", "posture"), "A probability instead of a notch.", "Never set aside.",
           earlier_verdict="posture sign came out opposite to the hand-set theory",
           where="synthium/domains/judicial/params/; docs/MATH_CANDIDATES.md"),
    Record("M-S", "law", "how hard facts are to move", "V8 (Jul 2026)",
           "S = P(reversal | fact attacked) / P(movement | law attacked); claimed small everywhere",
           (), "A dimensionless universal constant.", "",
           earlier_verdict="first value ~0.03 was wrong; corrected to 0.17 (attempt 27); replaced by W",
           where="docs/MATH_CANDIDATES.md"),
    Record("M-W", "law", "where movement goes", "V8 (Jul 2026)", "W: movement-destination invariant",
           (), "A dimensionless invariant across court levels.", "",
           earlier_verdict="W = 0.035 level-invariant (0.14/0.14); later 0.052, 95% CI 0.018-0.141",
           where="docs/MATH_CANDIDATES.md"),
    Record("M-STACK", "law", "several errors at once", "V8 (Jul 2026)",
           "Stacking law: errors on several layers add up", (), "Errors combine.", "",
           earlier_verdict="not yet evidence (attempt 29)", where="docs/MATH_CANDIDATES.md"),
    Record("M-FACT-INV", "law", "fact channel", "V8 (Jul 2026)",
           "The fact channel is level-invariant", (), "Facts behave the same at every court level.", "",
           earlier_verdict="held on 151 rows (attempt 29)", where="docs/MATH_CANDIDATES.md"),
    Record("U-DECIBAN", "unit", "weight of evidence", "V8 (Jul 13 2026)",
           "Deciban: 10 log10 of the odds ratio a piece of evidence gives", (),
           "A natural unit for the epistemic skeleton.", "", where="docs/MATH_CANDIDATES.md"),
    Record("U-LIFEYEAR", "unit", "value of a life (China)", "V8 (Jul 2026)",
           "Death compensation = I_pc x L(age), L(a) = clip(80 - a, 5, 20) standard life-years", (
               "income", "age"), "An enacted closed form for pricing a death.", "",
           earlier_verdict="verified for all ages 18-100", where="docs/MATH_CANDIDATES.md"),
    Record("U-DIGNITY", "unit", "dignity", "V8 (Jul 2026)", "Dignity ratio R = D / V (bereavement / dependency)",
           ("D", "V"), "A dimensionless cross-system ratio.", "",
           earlier_verdict="replaced after Connecticut priced the life (attempt 35)", where="docs/MATH_CANDIDATES.md"),
    Record("V-TWOPRICE", "law", "value of a life", "V8 (Jul 2026)",
           "Two-price law: law prices a death twice, a small fixed dignity price and a dependency price",
           (), "A structure shared across systems.", "", earlier_verdict="falsified (attempt 34)",
           where="docs/VALUE_SKELETON.md"),
    Record("V-UNPRICE", "law", "value of a life", "V8 (Jul 2026)",
           "Unpriceability principle: no system prices the life itself", (), "Replaced the two-price law.", "",
           earlier_verdict="falsified by Connecticut (attempt 35)", where="docs/VALUE_SKELETON.md"),
    Record("V-INVERSION", "law", "value of a life", "V8 (Jul 2026)",
           "Two incompatible theories of what a death is; the 'perfect inversion' (Ecker/Floyd)",
           (), "Systems differ in what they think a death takes away.", "",
           earlier_verdict="verified in both directions from primary sources (attempt 36)",
           where="docs/VALUE_SKELETON.md"),
    Record("A0", "axiom", "appellate review", "V8 (Jul 11 2026)",
           "Epistemic access: a court may revise only what it can see as well as the court below",
           (), "Explains why documents get reversed and credibility findings do not.", "",
           earlier_verdict="documents reversed 4/4, credibility 0/13; adversarial hunt found no falsifier",
           where="docs/AXIOM_CANDIDATES.md"),
    Record("A1-CHANNEL", "axiom", "appellate review", "V8 (Jul 12 2026)", "Channel exclusivity", (),
           "What A0 cannot explain.", "", where="docs/AXIOM_CANDIDATES.md"),
    Record("A2-INERTIA", "axiom", "appellate review", "V8 (Jul 12 2026)", "Inertia: presumption of regularity", (),
           "Results stay unless pushed.", "", earlier_verdict="near-tautological", where="docs/AXIOM_CANDIDATES.md"),
    Record("SINA-A1", "axiom", "enjoyment", "Sina (Jul 2026)",
           "Trajectory: every being's trajectory is toward more enjoyment", (), "Sina's first axiom.", "",
           earlier_verdict="found enacted in a Connecticut damages rule", where="docs/AXIOM_CANDIDATES.md"),
    Record("SINA-A2", "axiom", "non-interference", "Sina (Jul 2026)",
           "The way to enjoyment should not interfere with others' enjoyment", (), "Sina's second axiom.", "",
           where="docs/AXIOM_CANDIDATES.md"),
    Record("SINA-A3", "axiom", "preservation of life", "Sina (Jul 2026; sacrifice defined Nov 14)",
           "Nothing is more valuable than preserving the life of the being or system; sacrifice = a "
           "life given to protect another life from a present threat (rescue, defence, refusal)",
           (), "Sina's third axiom.", "", earlier_verdict="came out derivable (option value), Jul 12-13",
           where="docs/AXIOM_CANDIDATES.md"),
    Record("A4", "axiom", "pricing", "V8 (Jul 13 2026)",
           "Legitimacy bound: you may not price what you have no standing to price", (),
           "Sina's non-interference in institutional form.", "",
           earlier_verdict="survived in refined form (the polity priced, the market never did)",
           where="archive chat of Jul 16 2026 (old project); not yet in a doc"),
    Record("ENV", "law", "outside forces on courts", "V8 (Jul 13 2026)",
           "Environment layer: technology moves channel reliability r_c(t); regimes rewrite gates; "
           "deepfakes will lower r_video (direction fixed in advance)", ("r_c(t)",),
           "Sina's external-parameters idea.", "", where="docs/ENVIRONMENT.md"),
    Record("BLIND-JUL", "tool", "blind prediction", "V8 (Jul 14 2026)",
           "Seal a prediction with a time stamp and hash before reading the outcome", (),
           "Blinding must be mechanical.", "Rebuilt in Nov 2026; the July code was left out of 9.0.0.",
           where="synthium/legacy/v8/blindprotocol.py"),
    Record("ATLAS", "tool", "the 44-case suppression atlas", "V6.1 to V8 (Jun-Jul 2026)",
           "Loader for the hand-coded 44-case Fourth Amendment atlas, with leak checks", (),
           "A fixed set of cases to test the units on.", "Left out of 9.0.0 with the units.",
           where="synthium/legacy/v8/atlas.py; synthium/legacy/v6_1/data/atlas.py"),
    # ------------------------------------------------------------------ Nov 2026
    Record("T1", "law", "review barrier", "Nov 10 2026",
           "P(move | challenge) = A_j exp(-B(s) / T_j): barrier B by standard of review "
           "(universal), temperature T_j and attempt rate A_j per jurisdiction (local)",
           ("s standard of review", "T_j", "A_j"), "Sina's thermodynamics question in ruler form.", "",
           earlier_verdict="pre-registered; data being gathered (T1_POINTS.csv)", where="docs/AXIOM_CANDIDATES.md"),
    Record("G1-GREENE", "law", "power", "Nov 12 2026", "Greene rival: power explains outcomes", (),
           "A rival null hypothesis to the ruler.", "", earlier_verdict="draft, not adopted",
           where="docs/AXIOM_CANDIDATES.md"),
    Record("Q-QUALITIES", "unit", "human qualities in whole cases", "Nov 2026",
           "Q1 to Q67: adjectives scored 0..1 from counted signs in whole cases, with "
           "ADMITTED / FOUND / CLAIMED / INFERRED tags; motivation measured first", (),
           "Each adjective is a dimension; formulas should emerge from many cases.", "",
           earlier_verdict="rankings with no real unit yet", where="CASES.csv on Drive (not in this repo)"),
    Record("GEOMETRY", "tool", "space of cases", "Nov 24 2026",
           "Cases as points, qualities as dimensions: build-up, base-vs-derived test, curvature, "
           "metric fields, rates of change", (), "V4's maths fed with real case scores.", "",
           where="synthium/geometry/"),
    Record("PHENOMENA", "tool", "every phenomenon", "Nov 24 2026",
           "Phenomenon as a structure: its own dimensions, how it is created from them "
           "(sum, product, weakest/strongest link, priority), and which combination stays balanced",
           (), "The early phenomenon idea, tested on case scores.", "", where="synthium/phenomena/"),
]


def by_id() -> Dict[str, Record]:
    return {r.id: r for r in RECORDS}


def computable() -> List[Record]:
    """Records whose formula runs on a five-dimension phenomenon vector."""
    return [r for r in RECORDS if r.compute is not None]


def legacy_profiles() -> Dict[str, Dict[str, float]]:
    """The phenomenon profiles the early versions held, read from the restored code.

    V2's fourteen emotional profiles, plus the phenomena saved in the V1 and V2
    lexicons. Each is a point (v, R, r, C, S). These were hand-set, not measured.
    """
    import json
    import os

    from synthium.legacy.v2.omega_v2 import Transducer

    out: Dict[str, Dict[str, float]] = {k: dict(v) for k, v in Transducer.EMOTIONAL_PROFILES.items()}
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for rel, key in (("legacy/omega_v1_5/data/lexicon.json", "discovered_units"),
                     ("legacy/v2/data/lexicon_v2.json", "qualities")):
        with open(os.path.join(here, rel), encoding="utf-8") as fh:
            for item in json.load(fh).get(key, []):
                out.setdefault(item["term"].lower(), dict(item["vector"]))
    return out


def evaluate(point: Dict[str, float]) -> Dict[str, float]:
    """Run every computable past formula on one phenomenon point (v, R, r, C, S)."""
    return {r.id: float(r.compute(point)) for r in computable()}
