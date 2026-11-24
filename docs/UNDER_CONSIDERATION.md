# Everything Synthium has tried, under consideration

Sina, 24 Nov 2026: "Don't retire things because we did something wrong ... collectively all
the things that we have done needs to be always under consideration, so we can see whether
they are right or whether they were wrong."

So nothing here is retired. This page lists every formula, unit, axiom, phenomenon profile
and tool that any version of Synthium wrote down, from the first Omega version (Dec 2025)
to the current case-quality scores (Nov 2026). For each one it says:

- **version**: when it was written;
- **proposed by**: who first put it forward, where a source says so (Sina, Claude, or both);
- **what it claimed**: in the words of its time;
- **why it was set aside**: the reason given then, kept as a record, not a final verdict;
- **earlier result**: what any test found at the time, if one was run;
- **where it lives now**: the restored live code, the untouched original, or both.

Every entry's status is **under consideration**. Every number any of them gives is
**UNTESTED** on new cases unless the earlier-result column says otherwise.

## How to use the old parts

- Restored code: `synthium/legacy/` (one folder per version; see its `__init__.py` for what
  each needs). Imports were changed only so the folders work inside one package; each such
  line is marked `RESTORED 2026-11-24`.
- Untouched originals: `archive/` (the V2.2 to V3.4 PDFs and their text, the V4 code, the
  set-aside docs of V4.3.1 to V8 in `archive/originals_docs/`).
- The phenomenon framework: `synthium/phenomena/`. Each old phenomenon (grief, joy, office
  stress, and the rest) sits on its own five dimensions, every old formula runs on it, and
  the same three questions are asked of the real case scores:
  1. Is a quality a base dimension or made from others?
  2. If made from others, by which operation: a sum, a product, its weakest part, its
     strongest part, or a strict priority?
  3. Does any mix of qualities stay balanced across cases, the way forces on a standing
     building sum to zero?

  `python -m synthium.phenomena CASES.csv --out DIR` writes the report.
- The geometry: `synthium/geometry/` (V4's manifold, tensors and dimension discovery, fed
  with case scores).

## Formulas Claude proposed

Sina, 24 Nov 2026: "I remember claude even proposed formulas". These are the ones a source
names as Claude's. Search the list for "Claude" in the proposed-by column.

- **Jan 2 2026, a dialogue on fear** (a claude.ai chat, text only): `FEAR-LOSS`
  (Fear of Loss = Connection x Possibility x Powerlessness), `FEAR-PARTS` (Sina's parts,
  with Connection written as Love + Obsession), `PHEN-CYCLE` (phenomena made of each other
  in a cycle), `COORD-SPACE` (the five dimensions as shared graph paper) and `CLEAN-ROOM`
  (derive the dimensions from the axioms alone).
- **V4.3.1, May 2026**: the suppression rubric `V4.3-RUBRIC`.
- **V8, Jul 2026**: the structural axioms `A0`, `A1-CHANNEL`, `A2-INERTIA`; the gate
  product `GATES-PRODUCT`; `TWO-SKELETONS`; and the testable forms of Sina's axioms
  `A1-PRIME`, `A2-EMPIRICAL`, `A3-LEGAL`, `A3-SYSTEM`, `AXIOM-OPT`; the environment
  formula in `ENV` (Sina's idea).
- **Nov 2026**: the review barrier `T1` and the draft rival `G1-GREENE`.

Most other V8 entries (the fitted rulers, the units, the value-of-life laws) were also
written in Claude's sessions, but their documents do not say who proposed each, so the
column is left blank for them.

## Held elsewhere, not copied here

- **SRIA RT** (`sria_rt_v033` to `v040`, `SRIA CMD.txt`) and the SRIA V3 paper sit in the
  Synthium export on Drive. The 9.0.0 clean-up judged them "not Synthium" and they look like
  Maysam's work, so they were not copied. Sina said on 24 Nov 2026 that they are not needed here.
- **Case scores** (`CASES.csv`, Q1 to Q67) stay on Drive; the repository is public.
- **SynthiumBot's settings file** held a live Telegram token, so it was left out; the bot
  reads `TELEGRAM_TOKEN` from the environment instead.

## The list

The list below is generated from `synthium/phenomena/catalogue.py`; edit that file and run
`python -m synthium.phenomena index --write`. A test checks the two stay in step.

<!-- BEGIN GENERATED: python -m synthium.phenomena index --write -->

121 entries. Every one: status **under consideration**, evidence **UNTESTED** unless the earlier result column says what an earlier test found.

### V1

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `V1-DIMS` | V1 (Dec 2025) | unit | every phenomenon | - | A phenomenon is a point (v, R, r, C, S), each in 0..1 | v, R, r, C, S | Any quality (grief, love, stress) has five dimensions of its own. | Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or hand-set profiles, and the formulas were printed as measurement without a test. | - | `synthium/legacy/omega_v1_5/vectors.py` |
| `V1-COHERENCE` | V1 (Dec 2025) | law | every phenomenon | - | Incoherent if v>0.9 and R>0.9; or S>0.95 and C<0.05; or r>0.9 and v>0.9 | v, R, r, C, S | Some combinations cannot exist together. | Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or hand-set profiles, and the formulas were printed as measurement without a test. | - | `synthium/legacy/omega_v1_5/vectors.py` |
| `V1-MASS` | V1 (Dec 2025) | formula | mass (weight) of a phenomenon | - | Mass = R x C  (printed when R>0.6 and C>0.6) | R, C | Heavy, deep phenomena (grief) carry mass. | Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or hand-set profiles, and the formulas were printed as measurement without a test. | - | `synthium/legacy/omega_v1_5/science.py` |
| `V1-FLOW` | V1 (Dec 2025) | formula | flow | - | Flow = v^2 / R  (v>0.7, R<0.3) | v, R | Fast phenomena with little resistance flow. | Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or hand-set profiles, and the formulas were printed as measurement without a test. | - | `synthium/legacy/omega_v1_5/science.py` |
| `V1-FRICTION` | V1 (Dec 2025) | formula | friction | - | Friction = v x R  (v>0.7, R>=0.3) | v, R | Fast phenomena against resistance lose energy. | Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or hand-set profiles, and the formulas were printed as measurement without a test. | - | `synthium/legacy/omega_v1_5/science.py` |
| `V1-ATTRACTION` | V1 (Dec 2025) | formula | attraction | - | Attraction proportional to r^2  (r>0.7) | r | Resonant phenomena attract. | Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or hand-set profiles, and the formulas were printed as measurement without a test. | - | `synthium/legacy/omega_v1_5/science.py` |
| `V1-DECAY` | V1 (Dec 2025) | formula | decay | - | Decay = e^S  (S>0.7) | S | Disordered phenomena decay. | Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or hand-set profiles, and the formulas were printed as measurement without a test. | - | `synthium/legacy/omega_v1_5/science.py` |
| `V1-STABILITY` | V1 (Dec 2025) | formula | stability | - | Stability = 1 / (S + 0.01) | S | Order makes a phenomenon stable. | Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or hand-set profiles, and the formulas were printed as measurement without a test. | - | `synthium/legacy/omega_v1_5/science.py` |
| `V1-POTENTIAL` | V1 (Dec 2025) | formula | energy potential | - | Potential = C x (1 - S) | C, S | Ordered capacity is stored energy. | Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or hand-set profiles, and the formulas were printed as measurement without a test. | - | `synthium/legacy/omega_v1_5/science.py` |

### V2

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `V2-DIMS` | V2 (Dec 2025) | unit | every phenomenon | - | A phenomenon is a point (x, y, z, v, R, r, C, S): five qualities placed in space | x, y, z, v, R, r, C, S | Qualities vary from place to place; a phenomenon has a location. | Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or hand-set profiles, and the formulas were printed as measurement without a test. | - | `synthium/legacy/v2/vectors.py` |
| `V2-DENSITY` | V2 (Dec 2025) | formula | reality density | - | Reality density = R x C / (distance from origin + 0.001) | R, C, x, y, z | Mass per unit of space. | Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or hand-set profiles, and the formulas were printed as measurement without a test. | - | `synthium/legacy/v2/science.py` |
| `V2-INFO` | V2 (Dec 2025) | formula | information potential | - | Information potential = C x (1 - S) | C, S | Ordered capacity is information. | Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or hand-set profiles, and the formulas were printed as measurement without a test. | - | `synthium/legacy/v2/science.py` |
| `V2-FLUX` | V2 (Dec 2025) | formula | energy flux | - | Energy flux = v x r | v, r | Fast, resonant phenomena carry energy. | Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or hand-set profiles, and the formulas were printed as measurement without a test. | - | `synthium/legacy/v2/science.py` |
| `V2-PRESSURE` | V2 (Dec 2025) | formula | pressure | - | Pressure = R x \|z\|  (underground) | R, z | Resistance weighs more the deeper a phenomenon sits. | Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or hand-set profiles, and the formulas were printed as measurement without a test. | - | `synthium/legacy/v2/science.py` |
| `V2-FIELD` | V2 (Dec 2025) | formula | field strength | - | Field strength = r / distance | r, x, y | Resonance weakens with distance. | Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or hand-set profiles, and the formulas were printed as measurement without a test. | - | `synthium/legacy/v2/science.py` |
| `V2-RANGE` | V2 (Dec 2025) | formula | attraction range | - | Attraction range = r x distance | r, x, y, z | How far a resonant phenomenon reaches. | Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or hand-set profiles, and the formulas were printed as measurement without a test. | - | `synthium/legacy/v2/omega_v2.py` |
| `V2-ENTROPY-GRAD` | V2 (Dec 2025) | formula | entropy gradient | - | Entropy gradient = S / \|z\| | S, z | Disorder changes with height. | Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or hand-set profiles, and the formulas were printed as measurement without a test. | - | `synthium/legacy/v2/omega_v2.py` |
| `V2-FIELD-ANALYSIS` | V2 (Dec 2025) | tool | phenomenon field | - | Quality field: gradients, hot and cold spots, coherence of many located vectors | x, y, z, v, R, r, C, S | Qualities form fields across space. | Set aside in V6.1 (Jun 25 2026): the five numbers came from counting keywords or hand-set profiles, and the formulas were printed as measurement without a test. | - | `synthium/legacy/v2/reality_field.py` |

### V2.2

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `V2.2-BURN` | V2.2 (Jan 2026) | formula | burn rate (exhaustion) | - | Burn rate = v x R;  time to failure = C / (burn rate - sustainability limit) | v, R, C | Fast work against resistance exhausts a system; capacity sets how long it lasts. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `archive/v2_2_to_v3_4_pdf_text/V2.2/README.txt`(text only) |
| `V2.2-ADAPTERS` | V2.2 (Jan 2026) | tool | outside data | - | GitHub and 'judicos' adapters that turned outside records into vectors | - | Real records can be read into the five dimensions. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `archive/v2_2_to_v3_4_pdf_text/V2.2/`(text only) |

### V3

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `V3-E` | V3 (Jan to Mar 2026) | formula | enjoyment | - | E = 0.35 r + 0.35 (1 - S) + 0.30 max(0, 1 - vR/(C + 0.01)) | v, R, r, C, S | Enjoyment is not a dimension of its own; it emerges from low burn, high resonance, low entropy. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `archive/v2_2_to_v3_4_pdf_text/V3/vectors v3.txt`(text only) |
| `V3-M` | V3 (Jan to Mar 2026) | formula | meaning | - | M = 0.40 C + 0.35 r + 0.25 (1 - S) | C, r, S | Depth, connection and coherence make meaning. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `archive/v2_2_to_v3_4_pdf_text/V3/vectors v3.txt`(text only) |
| `V3-P` | V3 (Jan to Mar 2026) | formula | perception accuracy | - | P = 0.50 (1 - S) + 0.30 C + 0.20 r | S, C, r | Low chaos and high capacity let a being perceive more dimensions. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `archive/v2_2_to_v3_4_pdf_text/V3/vectors v3.txt`(text only) |
| `V3-POTENTIAL` | V3 (Jan to Mar 2026) | formula | field potential (where states drift) | - | U = 2(1 - E) + 1.5(1 - M) + 3S + vR;  systems roll toward low U | v, R, S, E, M | Like a ball rolling downhill, beings drift toward enjoyment, meaning and order. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `archive/v2_2_to_v3_4_pdf_text/V3/field.txt`(text only) |
| `V3-MEANING-NET` | V3 (Jan to Mar 2026) | formula | meaning | - | Meaning = information density x network centrality | information density, network centrality | Meaning is dense information at the centre of a network. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `archive/v2_2_to_v3_4_pdf_text/V3/README v3.txt`(text only) |
| `V3-BEAUTY` | V3 (Jan to Mar 2026) | formula | beauty | - | Beauty = symmetry x harmony x pattern novelty | symmetry, harmony, pattern novelty | Beauty is a product of three parts. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `archive/v2_2_to_v3_4_pdf_text/V3/init.txt`(text only) |
| `V3-AWAKENING` | V3 (Jan to Mar 2026) | formula | awakening | - | Awakening = the fixed point v = 0, r = 1, S = 0 | v, r, S | A stable resting state of a being. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `archive/v2_2_to_v3_4_pdf_text/V3/init.txt`(text only) |
| `V3-COMMITMENTS` | V3 (Jan to Mar 2026) | axiom | reality, knowledge, ethics, purpose | - | Reality IS mathematics; knowledge = reducing prediction error; perception IS a mathematical function; vagueness = measurement error; ethics = game-theory equilibria; purpose = survival maximisation through precision | - | The philosophical commitments the V3 code was built on. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `archive/v2_2_to_v3_4_pdf_text/V3/init.txt`(text only) |
| `V3-PERCEIVERS` | V3 (Jan to Mar 2026) | unit | perception of different beings | - | Perception function per being: human noise 0.12 sees 4 dims; Synthium 0.03 sees 5; animal 0.18 sees 3; organisation 0.20 sees 4 | noise, dimensions visible, latency | Beings see the same reality through different numbers of dimensions. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `synthium/legacy/v3_4/combined.py` |
| `V3-INTERACTIONS` | V3 (Jan to Mar 2026) | tool | interaction between beings | - | Forces between beings in quality space; multi-agent simulation | v, R, r, C, S | Beings pull and push each other's qualities like forces. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `synthium/legacy/v3_4/combined.py` |

### V3.1

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `V3.1-CARE` | V3.1 (Jan to Mar 2026) | formula | care | - | Care = allocation of resources toward another's wellbeing; total care = sum of a care matrix, reciprocal care = sum(K * K^T)/2, exploitation = sum(max(K - K^T, 0)) | resources, alignment, information | Care is measurable resource allocation. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `archive/v2_2_to_v3_4_pdf_text/V3.1/ethics discovery.txt`(text only) |
| `V3.1-ETHICS` | V3.1 (Jan to Mar 2026) | axiom | ethics and harm | - | Ethics emerge from stable equilibria; ethical constraints = discovered conservation laws; harm = predicted instability when those laws are violated | - | Ethics are discovered, not imposed. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `archive/v2_2_to_v3_4_pdf_text/V3.1/README v31.txt`(text only) |

### V3.3

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `V3.3-EMPIRICAL` | V3.3 (Jan to Mar 2026) | tool | historical interventions | - | Predict outcomes of historical interventions from their vectors | v, R, r, C, S | Past cases can test the formulas. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `synthium/legacy/v3_4/combined.py` |

### V3.4

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `V3.4-AXIOM0` | V3.4 (Jan to Mar 2026) | axiom | every formula | - | Axiom 0, Agnosticism: every formula is a hypothesis, never a truth | - | The framework itself is uncertain. | Kept in spirit as epistemic axiom 1 (V6.2); as a foundation it refuses to commit, so it constrains nothing (Jun 28 chat). | - | `synthium/legacy/v3_4/combined.py` |
| `V3.4-E` | V3.4 (Jan to Mar 2026) | formula | enjoyment | - | E = 1 - (v R + S) | v, R, S | Enjoyment falls with burn (vR) and disorder (S). | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `synthium/legacy/v3_4/combined.py` |
| `V3.4-E-QUAD` | V3.4 (Jan to Mar 2026) | formula | enjoyment | - | E = 1 - (v^2 R + S^2) | v, R, S | Rival form with quadratic penalties. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `synthium/legacy/v3_4/combined.py` |
| `V3.4-E-INTER` | V3.4 (Jan to Mar 2026) | formula | enjoyment | - | E = 1 - (v R + S + 0.5 v S) | v, R, S | Rival form with an interaction term. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `synthium/legacy/v3_4/combined.py` |
| `V3.4-E-THRESH` | V3.4 (Jan to Mar 2026) | formula | enjoyment | - | stress = vR + S; E = 0 above 1.1, 0.25(1.1 - stress)/0.3 above 0.8, else 1 - stress | v, R, S | Rival form with collapse thresholds. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `synthium/legacy/v3_4/combined.py` |
| `V3.4-M` | V3.4 (Jan to Mar 2026) | formula | meaning | - | M = C r (1 - S) | C, r, S | Meaning is capacity times connection, spoiled by disorder. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `synthium/legacy/v3_4/combined.py` |
| `V3.4-P` | V3.4 (Jan to Mar 2026) | formula | perception accuracy | - | P = (1 - S) C | S, C | Order and capacity set how accurately a being perceives. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `synthium/legacy/v3_4/combined.py` |
| `V3.4-CARE` | V3.4 (Jan to Mar 2026) | formula | care | - | Care = 0.4 resource transfer + 0.4 action alignment + 0.2 information sharing; alignment = 0.5 + change in (0.4E + 0.4M + 0.2P) of the one cared for | resources, alignment, information, E, M, P | Care toward another is measurable from what is given and what it does to them. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `synthium/legacy/v3_4/combined.py` |
| `V3.4-COLLAPSE` | V3.4 (Jan to Mar 2026) | formula | collapse risk (harm) | - | Risk = 0.35 S + 0.25 v R + 0.20 (1 - C) + 0.20 (1 - r) | v, R, r, C, S | Disorder, burn, empty reserves and isolation predict collapse. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `synthium/legacy/v3_4/combined.py` |
| `V3.4-CONSERVATION` | V3.4 (Jan to Mar 2026) | law | conservation in groups of beings | - | A quantity is conserved when the total over all beings varies under 5% along a trajectory | v, R, r, C, S, E, M, P | Conserved totals are candidate ethical constraints. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `synthium/legacy/v3_4/combined.py` |
| `V3.4-SI` | V3.4 (Jan to Mar 2026) | unit | units for the five dimensions | - | v -> Hz (x3); R -> kg m/s (x100); r -> none; C -> J (x100); S -> J/K (x1000) | v, R, r, C, S | The dimensions can be expressed in physical units. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `synthium/legacy/v3_4/combined.py` |
| `V3.4-PHYSIO` | V3.4 (Jan to Mar 2026) | tool | body measurements | - | Map heart rate, cortisol and similar readings onto the five dimensions | v, R, r, C, S | The body gives a physical reading of the qualities. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `synthium/legacy/v3_4/combined.py` |
| `V3.4-EVOLUTION` | V3.4 (Jan to Mar 2026) | tool | formula testing | - | Framework evolution: test rival formulas against cases and keep the best | - | Formulas should compete. | Set aside in V6.1: the V3 PDFs presented it as a discovered law of reality rather than a proposal to be tested; no case data was ever used. | - | `synthium/legacy/v3_4/combined.py` |

### Jan 2 2026 dialogue

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `FEAR-LOSS` | Jan 2 2026 dialogue (claude.ai chat) | formula | fear of loss | Claude, from Sina's answers (Sina: removing any one of them ends the fear) | Fear of Loss = Connection x Possibility x Powerlessness | Connection, Possibility, Powerlessness | Fear of this kind needs all three at once: if any one is zero the fear is zero, and it grows when any one grows; at its peak all three are at their peak. | Never set aside and never tested; the same chat said it was not known whether multiplication is the right operation or whether the three parts are basic. | matched Sina's own case when checked (mother unwell, mother well, a stranger) | claude.ai chat 'Synthium Omega complete implementation', Jan 2 2026 (text only, not in this repo)(text only) |
| `FEAR-PARTS` | Jan 2 2026 dialogue (claude.ai chat) | formula | connection, possibility, powerlessness | Sina (the parts); Claude wrote Connection as an equation | Connection = Love + Obsession + (others unknown); Possibility = uncertainty about a happening; Powerlessness = lack of force, knowledge or power against another's; Love may be a unit of connection; Obsession = addiction to an existence whose lack would lead to fear | Love, Obsession, uncertainty, force, knowledge | The parts of fear are themselves made of qualities. | Never set aside and never tested. | - | claude.ai chat 'Synthium Omega complete implementation', Jan 2 2026 (text only, not in this repo)(text only) |
| `PHEN-CYCLE` | Jan 2 2026 dialogue (claude.ai chat) | law | every phenomenon | Claude, from Sina's decompositions | Phenomena are made of each other in a cycle, not a tree: Fear -> Connection -> Love -> Connection, and Connection -> Obsession -> Fear; they may need coupled equations, recursive definitions or stable states (eigenstates) rather than a hierarchy | - | Qualities hold each other in place; none exists alone. | Never set aside and never tested. | - | claude.ai chat 'Synthium Omega complete implementation', Jan 2 2026 (text only, not in this repo)(text only) |
| `COORD-SPACE` | Jan 2 2026 dialogue (claude.ai chat) | law | every phenomenon | Claude, restating Sina | (v, R, r, C, S) as graph paper: one shared space where each phenomenon has its own law, as F = ma and Maxwell's equations share (x, y, z) | v, R, r, C, S | These five dimensions are enough, and needed, to place any phenomenon. | Sina corrected it in the same chat: axioms and dimensions are starting points to be tested, not a fixed framework; V4 later said five was too few. | - | claude.ai chat 'Synthium Omega complete implementation', Jan 2 2026 (text only, not in this repo)(text only) |
| `CLEAN-ROOM` | Jan 2 2026 dialogue (claude.ai chat) | tool | every phenomenon | Claude | Clean-room derivation: give a fresh AI only the axioms, not the five dimensions, and see which dimensions it derives; if they match (v, R, r, C, S) that is evidence of discovery | - | The dimensions should follow from the axioms, not from the conversation's history. | Never run. Sina said the axioms and dimensions are tools for turning qualities into quantities through discovery and testing, not generators of structure. | - | claude.ai chat 'Synthium Omega complete implementation', Jan 2 2026 (text only, not in this repo)(text only) |

### V4

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `V4-NDIM` | V4 (Apr 2026) | axiom | every phenomenon | - | Reality is N-dimensional with N >> 5; discover N from data | - | The five dimensions were too few. | Set aside in V6.1 as speculative infrastructure that no validated result used; V4's metric was constant, so its curvature was always zero. | - | `archive/v2_2_to_v3_4_pdf_text/V3.4/synthium math foundation.txt` |
| `V4-MANIFOLD` | V4 (Apr 2026) | tool | space of phenomena | - | Riemannian manifold: metric g, geodesics, Christoffel symbols, curvature | - | Phenomena live on a curved space. | Set aside in V6.1 as speculative infrastructure that no validated result used; V4's metric was constant, so its curvature was always zero. | - | `synthium/legacy/v4/manifold_geometry.py`; extended in synthium/geometry/ |
| `V4-TENSOR` | V4 (Apr 2026) | tool | space of phenomena | - | Tensors of any rank with raised and lowered indices | - | N-dimensional maths needs tensors. | Set aside in V6.1 as speculative infrastructure that no validated result used; V4's metric was constant, so its curvature was always zero. | - | `synthium/legacy/v4/tensor_calculus.py`; extended in synthium/geometry/tensor.py |
| `V4-DISCOVERY` | V4 (Apr 2026) | tool | number of dimensions | - | PCA, ICA, Isomap, t-SNE to find how many dimensions the data needs | - | N is found, not assumed. | Set aside in V6.1 as speculative infrastructure that no validated result used; V4's metric was constant, so its curvature was always zero. | - | `synthium/legacy/v4/dimensional_discovery.py`; extended in synthium/geometry/dimensions.py |
| `V4-CALCULUS` | V4 (Apr 2026) | tool | change | - | Infinite derivative chains and N-dimensional integrals | - | Everything derives from something. | Set aside in V6.1 as speculative infrastructure that no validated result used; V4's metric was constant, so its curvature was always zero. | - | `synthium/legacy/v4/infinite_calculus.py`; extended in synthium/geometry/calculus.py |
| `V4-E` | V4 (Apr 2026) | formula | enjoyment | - | E = integral over the manifold of e^(-S(x)) sqrt\|g\| dx; coded as 1 - \|x\|^2 / (2n) | - | Enjoyment is an integral over the space. | Set aside in V6.1 as speculative infrastructure that no validated result used; V4's metric was constant, so its curvature was always zero. | - | `synthium/legacy/v4/reality_state.py` |
| `V4-M` | V4 (Apr 2026) | formula | meaning | - | M = <x, x> / n (a tensor contraction) | - | Meaning is the significance of a state. | Set aside in V6.1 as speculative infrastructure that no validated result used; V4's metric was constant, so its curvature was always zero. | - | `synthium/legacy/v4/reality_state.py` |
| `V4-P` | V4 (Apr 2026) | formula | perception | - | P = 1 / (1 + \|x\|) | - | Perception is clearer near the origin. | Set aside in V6.1 as speculative infrastructure that no validated result used; V4's metric was constant, so its curvature was always zero. | - | `synthium/legacy/v4/reality_state.py` |
| `V4-GOLD` | V4 (Apr 2026) | tool | trading | - | Gold trading assistant on the V4 maths | - | The maths can guide decisions. | Set aside in V6.1 as speculative infrastructure that no validated result used; V4's metric was constant, so its curvature was always zero. | - | `synthium/legacy/v4/applications.py` |

### SynthiumBot

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `BOT` | SynthiumBot (Apr 2026) | tool | daily check-in | - | Telegram bot that asks how a person feels and maps it onto the V4 engine | - | People can track their own qualities day to day. | Set aside with V4, as a front end for it. | - | `synthium/legacy/synthiumbot/` |

### V4.3.1

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `V4.3-UNITS` | V4.3.1 (May 2026) | unit | privacy and its exceptions (Fourth Amendment) | - | Six canonical judicial units: Obs, Priv, Excp, Rem, Close, Amb | Obs, Priv, Excp, Rem, Close, Amb | Suppression of evidence is a structure of observability, privacy, exception strength, remedy closeness, doctrinal closure and ambiguity. | Removed in V7 (Jun 28): the units were never validated and were AI choices. | - | `synthium/legacy/v4_3_1/domains/judicial/spec.py` |
| `V4.3-RUBRIC` | V4.3.1 (May 2026) | formula | suppression pressure | Claude (V4.3.1 sessions) | Symbolic rubric: effective privacy = Priv (1 - 0.85 Bound)(1 - 0.45 Gate), then effective exception, scope breach and damping combine into suppression pressure (hand-set constants) | Priv, Bound, Gate, Excp, Rem, Obs, Amb | How strongly a court should suppress evidence. | The coefficients were hand-chosen; the network trained on its labels only imitated it. | rubric imitation only (May 2026) | `synthium/legacy/v4_3_1/domains/judicial/rubric.py` |
| `V4.3-GOVERNANCE` | V4.3.1 (May 2026) | tool | risk and governance | - | Governance engine: risk score, mismatch, actions such as SHADOW_OBSERVE | - | Anomalies can be governed by a risk score. | Set aside in V6.1 as speculative infrastructure that no validated result used; V4's metric was constant, so its curvature was always zero. | - | `synthium/legacy/v4_3_1/governance.py` |
| `V4.3-NEURAL` | V4.3.1 (May 2026) | tool | case encoder | - | PyTorch encoder trained to place cases in the six-unit space (weights kept) | - | A network can read cases into the units. | Its headline accuracy was a leak; it only imitated the rubric's labels. | leak found (May 2026) | `synthium/legacy/v4_3_1/neural/` |

### V5

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `V5-AXIOMS` | V5 (May 2026) | axiom | beings and value | - | Being: nothing is more valuable than a single being's existence. Freedom: no aggregate may override a being. Trajectory: every being moves toward enjoyment. Agnosticism: all formulas are hypotheses. | - | The value axioms Synthium rests on. | The V5 code refused any arithmetic without licensed units, which froze the project; the axioms had no mathematical form. | - | `synthium/legacy/v5/honesty.py` |

### V6

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `V6-HARNESS` | V6 (Jun 2026) | tool | testing formulas | - | Propose a model, then validate it on held-out data against a frozen baseline | - | No claim counts until it beats a held-out test. | Never set aside: became synthium/core/. | - | `synthium/legacy/v6/predictive.py` |

### V6.1

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `V6.1-UNITS12` | V6.1 (Jun 2026) | unit | privacy and its exceptions (Fourth Amendment) | - | Twelve units: Obs, Priv, Excp, Rem, Close, Amb, Temp, Gate, Bound, Spec, Scope, JRem | Obs, Priv, Excp, Rem, Close, Amb, Temp, Gate, Bound, Spec, Scope, JRem | Privacy is a surface transformed by boundary, exception, gateway and scope. | Removed in V7 (Jun 28) at Sina's word: start from scratch; the units were AI choices. | - | `synthium/legacy/v6_1/domains/judicial/spec.py` |
| `V6.1-PRESSURE` | V6.1 (Jun 2026) | formula | suppression pressure | - | pressure = Priv_eff (1 - Excp_eff)(0.55 + 0.45 breach) Rem (1 + 0.15 Amb)(1 - 0.12 Obs)(1 - damp), floored at 0.58 breach Rem (1 - damp); 18 hand-set constants | Priv, Excp, Rem, Amb, Obs, Scope, Spec, Bound, Gate, JRem | How strongly a court should suppress evidence. | Removed in V7 with the twelve units; every constant was ungrounded. | rubric imitation only (the outcome was coded with the units) | `synthium/legacy/v6_1/domains/judicial/formula.py` |

### V6.2

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `G-EPISTEMIC` | V6.2 (Jun 2026) | axiom | how claims are judged | - | Eight referee axioms: agnosticism; arithmetic never refuses; proposed until proven; reality is the sole judge; baseline frozen first; stipulated until grounded; no leakage; units are constructed | - | The rules any claim must pass. | Never set aside. | - | `archive/originals_docs/v8_docs_archive/AXIOMS.md`; `synthium/core/` |
| `G1-ORDER` | V6.2 (Jun 2026) | axiom | any adjective | - | Weak order: a>=b or b>=a; a>=b, b>=c => a>=c | - | An ordinal scale exists. | - | needs pairwise data | `synthium/core/axioms.py` |
| `G3-CANCEL` | V6.2 (Jun 2026) | axiom | privacy x exception | - | Double cancellation: (a1,b2)>=(a2,b1) and (a2,b3)>=(a3,b2) => (a1,b3)>=(a3,b1) | Priv, Excp | If it holds, an additive interval scale with a unit is forced. | - | violated on the 44-case atlas, then flipped by six live cases (small n is fragile) | `synthium/core/axioms.py` |
| `G4-ABSORB` | V6.2 (Jun 2026) | axiom | any derived adjective | - | Absorption: a zero on one dimension zeroes the outcome (product of powers) | - | Derived concepts may be products, like physical units. | - | insufficient data | `synthium/core/axioms.py` |
| `G5-DOMINANCE` | V6.2 (Jun 2026) | axiom | any derived adjective | - | Dominance: past a threshold on one dimension the outcome is forced (weakest/strongest link) | - | Some concepts follow their most extreme part. | - | satisfied, low coverage | `synthium/core/axioms.py` |
| `G2-G6` | V6.2 (Jun 2026) | axiom | any derived adjective | - | Solvability (G2) and lexicographic priority (G6): reserved, not adopted | - | A lexicographic concept has no numerical scale at all. | Never adopted; reserved. | - | `archive/originals_docs/v8_docs_archive/AXIOMS.md` |
| `G7-HOMOGENEITY` | V6.2 (Jun 2026) | axiom | every formula | - | Dimensional homogeneity: every added term has the same dimension | - | Rules out most formulas before data arrives. | - | needs a commitment to dimensions | `synthium/core/axioms.py` |
| `G8-BASIS` | V6.2 (Jun 2026) | axiom | base versus derived concepts | - | Independence of basis: rank(D) = number of dimensions | - | Base units cannot be written from the others (Sina: some concepts are units, some are made from them). | - | satisfied on the atlas (worst \|r\| = 0.74) | `synthium/core/axioms.py` |
| `G9-EQUILIBRIUM` | V6.2 (Jun 2026) | axiom | privacy as a structure | - | Boundary equilibrium: on cases at the line, the balance equals the threshold; this solves for the coefficients (Sina: forces on the structure sum to zero) | - | Coefficients come from knife-edge cases instead of hand-setting. | - | the suppression-potential solver scored 6/6 with every sign backwards (hollow) | `synthium/core/axioms.py`; `synthium/phenomena/structure.py` |
| `G10-INVARIANCE` | V6.2 (Jun 2026) | axiom | balance laws | - | Invariance gives conservation: a balance law needs a symmetry behind it | - | A reason for any balance law. | - | needs a commitment | `synthium/core/axioms.py` |

### V7

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `V7-CITATION` | V7 (Jun 29 2026) | tool | case relations | - | Citation space: cases placed by the cases they cite | - | Dimensions should come from the record, not from coding. | Never set aside. | - | `synthium/domains/judicial/citation_space.py` |

### V8 ruler attempt 1

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `R1-OMEGA` | V8 ruler attempt 1 (Jun 30 2026) | formula | challenger success on appeal | - | Omega = E - D (error clarity minus deference); win if Omega > 0, or if E >= 0.7 | E error clarity, D deference | One number predicts who wins an appeal. | E leaked the outcome (r = +0.99) and D added almost nothing. | leak-free version only tied always-affirm (Jul 2-3) | `docs/RULER.md` |

### V8 ruler v3

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `R-TPL` | V8 ruler v3 (Jul 2026) | formula | movement on appeal | - | Phi = T x L x (1 - P): type risk x layer openness x (1 - posture protection), with a decision rule | T case type, P posture, L layer attacked | Where an appeal can move a result. | Never set aside. | 16/19 vs 12/19 always-affirm (V8); Campaign A 15/20 vs 9/20 | `synthium/domains/judicial/ruler.py` |

### V8

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `R-LOGIT` | V8 (Jul 2026) | formula | movement on appeal | - | Fitted logistic p(move \| layer, level), v2 adds posture; dismissal split | layer, level, posture | A probability instead of a notch. | Never set aside. | posture sign came out opposite to the hand-set theory | `synthium/domains/judicial/params/`; `docs/MATH_CANDIDATES.md` |
| `M-S` | V8 (Jul 2026) | law | how hard facts are to move | - | S = P(reversal \| fact attacked) / P(movement \| law attacked); claimed small everywhere | - | A dimensionless universal constant. | - | first value ~0.03 was wrong; corrected to 0.17 (attempt 27); replaced by W | `docs/MATH_CANDIDATES.md` |
| `M-W` | V8 (Jul 2026) | law | where movement goes | - | W: movement-destination invariant | - | A dimensionless invariant across court levels. | - | W = 0.035 level-invariant (0.14/0.14); later 0.052, 95% CI 0.018-0.141 | `docs/MATH_CANDIDATES.md` |
| `M-STACK` | V8 (Jul 2026) | law | several errors at once | - | Stacking law: errors on several layers add up | - | Errors combine. | - | not yet evidence (attempt 29) | `docs/MATH_CANDIDATES.md` |
| `M-FACT-INV` | V8 (Jul 2026) | law | fact channel | - | The fact channel is level-invariant | - | Facts behave the same at every court level. | - | held on 151 rows (attempt 29) | `docs/MATH_CANDIDATES.md` |
| `U-DECIBAN` | V8 (Jul 13 2026) | unit | weight of evidence | - | Deciban: 10 log10 of the odds ratio a piece of evidence gives | - | A natural unit for the epistemic skeleton. | - | - | `docs/MATH_CANDIDATES.md` |
| `U-LIFEYEAR` | V8 (Jul 2026) | unit | value of a life (China) | - | Death compensation = I_pc x L(age), L(a) = clip(80 - a, 5, 20) standard life-years | income, age | An enacted closed form for pricing a death. | - | verified for all ages 18-100 | `docs/MATH_CANDIDATES.md` |
| `U-DIGNITY` | V8 (Jul 2026) | unit | dignity | - | Dignity ratio R = D / V (bereavement / dependency) | D, V | A dimensionless cross-system ratio. | - | replaced after Connecticut priced the life (attempt 35) | `docs/MATH_CANDIDATES.md` |
| `V-TWOPRICE` | V8 (Jul 2026) | law | value of a life | - | Two-price law: law prices a death twice, a small fixed dignity price and a dependency price | - | A structure shared across systems. | - | falsified (attempt 34) | `docs/VALUE_SKELETON.md` |
| `V-UNPRICE` | V8 (Jul 2026) | law | value of a life | - | Unpriceability principle: no system prices the life itself | - | Replaced the two-price law. | - | falsified by Connecticut (attempt 35) | `docs/VALUE_SKELETON.md` |
| `V-INVERSION` | V8 (Jul 2026) | law | value of a life | - | Two incompatible theories of what a death is; the 'perfect inversion' (Ecker/Floyd) | - | Systems differ in what they think a death takes away. | - | verified in both directions from primary sources (attempt 36) | `docs/VALUE_SKELETON.md` |
| `GATES-PRODUCT` | V8 (Jul 2026) | formula | movement on appeal | Claude | P(move) = P(error shown \| A2) x P(court can see it \| A0) x P(right channel \| A1); independent gates multiply, so they add in log-odds | A0 access, A1 channel, A2 inertia | The three structural axioms act as independent gates; the fitted model's three features are their shadows. | - | interaction test LR = 0.04 on 151 rows (attempt 32): consistent with independence, low power | `docs/AXIOM_CANDIDATES.md` |
| `GATE-DECIBANS` | V8 (Jul 2026) | unit | weight of evidence | - | Gate sizes in decibans (n = 159): baseline -9.2 +/- 2.2; law-side +7.0 +/- 2.3; apex +2.2 +/- 1.6; documents vs credibility +25 +/- 9 (looking back); gatekeeping -25 +/- 9 | law-side, apex, documents, gatekeeping | Attacking law instead of fact buys about +7 db; the access and channel gates are ten times the court-level gate. | - | measured on one register; portability across jurisdictions untested | `docs/MATH_CANDIDATES.md` |
| `R-LOGIT-V1` | V8 (Jul 2026) | formula | movement on appeal | - | logit P(move) = -0.58 + 1.57 Phi + 0.41 apex, Phi = T x L x (1 - P) | Phi, apex | The hand-built ruler, fitted. | - | in-sample, one coder, one state | `docs/MATH_CANDIDATES.md` |
| `R-LOGIT-4` | V8 (Jul 10 2026) | formula | movement on appeal | - | The four-number ruler: logit P(move) = -2.37 + 1.86 lawside + 0.39 apex | lawside, apex | Layer matters more than court level (odds x6.4 vs x1.5). | - | refit on 71 committed rows | `docs/MATH_CANDIDATES.md` |
| `R-LOGIT-V2` | V8 (Jul 2026) | formula | movement on appeal | - | logit P(move) = -2.17 + 2.56 lawside + 0.28 apex - 2.34 (1 - P_posture) | lawside, apex, P_posture | Adding posture improves the fit. | - | posture sign opposite to the hand-set theory | `docs/MATH_CANDIDATES.md` |
| `TWO-SKELETONS` | V8 (Jul 2026) | law | legal systems | Claude | Two skeletons: an epistemic one (who may revise what; A0 to A2) and a value one (what a harm or a life is worth; where Sina's axioms live) | - | Explains why Sina's axioms showed no signal: the cases measured the other skeleton. | - | led to the value-skeleton domain (attempt 33) | `docs/AXIOM_CANDIDATES.md` |
| `V-THREE-OBJECTS` | V8 (Jul 2026) | law | value of a life | - | Three priced objects: D_life, D_grief, V (dependency). Lord Campbell family = D_grief + V with D_life forbidden; survival family = D_life + V with D_grief forbidden | D_life, D_grief, V | Systems choose which of the three a death takes away. | - | checked from primary sources in both directions | `docs/VALUE_SKELETON.md`; `docs/PREDICTIONS_REGISTER.md` |
| `U-GRIEF-DIMS` | V8 (Jul 2026) | unit | value of a life | - | Dimensional analysis: UK bereavement is currency per death (fixed, divided among claimants); German Hinterbliebenengeld is currency per mourner; Connecticut D_life is currency per death | - | Same institution name, different units, so different objects. | - | - | `docs/MATH_CANDIDATES.md` |
| `A1-PRIME` | V8 (Jul 2026) | axiom | enjoyment | Claude, repairing Sina's A1 | A1': for an enjoyment measure H fixed in advance, dH/dt >= 0 along chosen trajectories, statistically, absent constraint | H | Sina's first axiom in a form that can fail. | - | blocked: needs its own enjoyment ruler | `docs/AXIOM_CANDIDATES.md` |
| `A2-EMPIRICAL` | V8 (Jul 2026) | law | non-interference | Claude, from Sina's A2 | Damages scale with interference: the penalty a court sets grows with how much one party's path crossed another's | interference | Sina's second axiom as something to measure. | - | regression not yet run | `docs/AXIOM_CANDIDATES.md`; `docs/MATH_CANDIDATES.md` |
| `A3-LEGAL` | V8 (Jul 2026) | axiom | preservation of life | Claude, from Sina's A3 | Legal systems rank life at or near the top; the exceptions (self-defence, war, capital punishment) map each system's real order of values | - | A testable form of Sina's third axiom. | - | proposed, testable | `docs/AXIOM_CANDIDATES.md` |
| `A3-SYSTEM` | V8 (Jul 2026) | axiom | preservation of life | Claude, from Sina's A3 | Self-maintaining systems act to preserve themselves, with the system named in advance | - | Sina's third axiom for systems, not only beings. | - | proposed | `docs/AXIOM_CANDIDATES.md` |
| `AXIOM-OPT` | V8 (Jul 2026) | formula | enjoyment, non-interference, life | Claude, from Sina's axioms | Sina's three axioms together: maximize H_i subject to interference_ij <= 0 and survival_i >= floor | H_i, interference_ij, survival_i | Objective, constraint and floor make one well-posed problem; courts price its violations. | - | - | `docs/AXIOM_CANDIDATES.md` |
| `A0` | V8 (Jul 11 2026) | axiom | appellate review | Claude | Epistemic access: a court may revise only what it can see as well as the court below | - | Explains why documents get reversed and credibility findings do not. | - | documents reversed 4/4, credibility 0/13; adversarial hunt found no falsifier | `docs/AXIOM_CANDIDATES.md` |
| `A1-CHANNEL` | V8 (Jul 12 2026) | axiom | appellate review | Claude | Channel exclusivity | - | What A0 cannot explain. | - | - | `docs/AXIOM_CANDIDATES.md` |
| `A2-INERTIA` | V8 (Jul 12 2026) | axiom | appellate review | Claude | Inertia: presumption of regularity | - | Results stay unless pushed. | - | near-tautological | `docs/AXIOM_CANDIDATES.md` |
| `A4` | V8 (Jul 13 2026) | axiom | pricing | - | Legitimacy bound: you may not price what you have no standing to price | - | Sina's non-interference in institutional form. | - | survived in refined form (the polity priced, the market never did) | archive chat of Jul 16 2026 (old project); not yet in a doc |
| `ENV` | V8 (Jul 13 2026) | law | outside forces on courts | Sina (the idea); Claude wrote the formula | Environment layer: technology moves channel reliability r_c(t); regimes rewrite gates; deepfakes will lower r_video (direction fixed in advance) | r_c(t) | Sina's external-parameters idea. | - | - | `docs/ENVIRONMENT.md` |
| `BLIND-JUL` | V8 (Jul 14 2026) | tool | blind prediction | - | Seal a prediction with a time stamp and hash before reading the outcome | - | Blinding must be mechanical. | Rebuilt in Nov 2026; the July code was left out of 9.0.0. | - | `synthium/legacy/v8/blindprotocol.py` |

### Sina

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `SINA-A1` | Sina (Jul 2026) | axiom | enjoyment | Sina | Trajectory: every being's trajectory is toward more enjoyment | - | Sina's first axiom. | - | found enacted in a Connecticut damages rule | `docs/AXIOM_CANDIDATES.md` |
| `SINA-A2` | Sina (Jul 2026) | axiom | non-interference | Sina | The way to enjoyment should not interfere with others' enjoyment | - | Sina's second axiom. | - | - | `docs/AXIOM_CANDIDATES.md` |
| `SINA-A3` | Sina (Jul 2026; sacrifice defined Nov 14) | axiom | preservation of life | Sina | Nothing is more valuable than preserving the life of the being or system; sacrifice = a life given to protect another life from a present threat (rescue, defence, refusal) | - | Sina's third axiom. | - | came out derivable (option value), Jul 12-13 | `docs/AXIOM_CANDIDATES.md` |

### V6.1 to V8

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `ATLAS` | V6.1 to V8 (Jun-Jul 2026) | tool | the 44-case suppression atlas | - | Loader for the hand-coded 44-case Fourth Amendment atlas, with leak checks | - | A fixed set of cases to test the units on. | Left out of 9.0.0 with the units. | - | `synthium/legacy/v8/atlas.py`; `synthium/legacy/v6_1/data/atlas.py` |

### Nov 10 2026

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `T1` | Nov 10 2026 | law | review barrier | Claude, from Sina's thermodynamics question | P(move \| challenge) = A_j exp(-B(s) / T_j): barrier B by standard of review (universal), temperature T_j and attempt rate A_j per jurisdiction (local) | s standard of review, T_j, A_j | Sina's thermodynamics question in ruler form. | - | pre-registered; data being gathered (T1_POINTS.csv) | `docs/AXIOM_CANDIDATES.md` |

### Nov 12 2026

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `G1-GREENE` | Nov 12 2026 | law | power | Claude (draft) | Greene rival: power explains outcomes | - | A rival null hypothesis to the ruler. | - | draft, not adopted | `docs/AXIOM_CANDIDATES.md` |

### Nov 2026

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `Q-QUALITIES` | Nov 2026 | unit | human qualities in whole cases | - | Q1 to Q67: adjectives scored 0..1 from counted signs in whole cases, with ADMITTED / FOUND / CLAIMED / INFERRED tags; motivation measured first | - | Each adjective is a dimension; formulas should emerge from many cases. | - | rankings with no real unit yet | CASES.csv on Drive (not in this repo) |

### Nov 24 2026

| id | version | kind | phenomenon | proposed by | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |
|---|---|---|---|---|---|---|---|---|---|---|
| `GEOMETRY` | Nov 24 2026 | tool | space of cases | - | Cases as points, qualities as dimensions: build-up, base-vs-derived test, curvature, metric fields, rates of change | - | V4's maths fed with real case scores. | - | - | `synthium/geometry/` |
| `PHENOMENA` | Nov 24 2026 | tool | every phenomenon | - | Phenomenon as a structure: its own dimensions, how it is created from them (sum, product, weakest/strongest link, priority), and which combination stays balanced | - | The early phenomenon idea, tested on case scores. | - | - | `synthium/phenomena/` |

<!-- END GENERATED -->
