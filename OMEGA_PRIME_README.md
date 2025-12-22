# SYNTHIUM OMEGA PRIME

## The Living Framework for Consciousness Quantification

Created by **Sina Golchin** & **Maysam BaygMuhammady**

---

## What Is This?

SYNTHIUM OMEGA PRIME is a complete framework for quantifying, analyzing, and transforming consciousness states using semantic NLP and 5-dimensional vector mathematics.

It translates natural language descriptions of emotional/mental states into precise consciousness vectors, then provides:
- Deep analysis of current state
- Similar phenomenon identification
- Wellbeing scoring
- Phase determination (awakening → integration → transcendence → dissolution)
- Transformation plans to move between states
- Empirical validation tools

## The 5 Dimensions

Every consciousness state exists as a point in 5D space:

1. **v** (Velocity): Movement pace (0=stuck, 1=rushing)
2. **R** (Resistance): Friction encountered (0=smooth, 1=blocked)
3. **r** (Resonance): Connection strength (0=isolated, 1=connected)
4. **C** (Capacity): Available energy (0=depleted, 1=full)
5. **S** (Entropy): Chaos level (0=ordered, 1=chaotic)

## Core Upgrade: Semantic NLP

Instead of keyword matching, SYNTHIUM uses **sentence-transformers** to understand the *meaning* of natural language:

```
"I feel completely overwhelmed and scattered"
→ Vector(v=0.7, R=0.7, r=0.3, C=0.2, S=0.9)
→ Closest phenomenon: "Overwhelm"
→ Recommendations: "Focus on rest and simplification..."
```

## Installation

```bash
# Clone repository
git clone https://github.com/sinagolchin/SYNTHIUM.git
cd SYNTHIUM

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### 1. Command Line Interface

```bash
python examples/cli_example.py
```

Explore predefined states, create custom vectors, get transformation plans.

### 2. Web API Server

```bash
# Start the FastAPI server
uvicorn web_backend.app:app --reload

# Or
python web_backend/app.py run
```

Access the API at `http://localhost:8000`

Interactive docs at `http://localhost:8000/docs`

### 3. API Usage

**Analyze a state:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "I feel stuck and disconnected from everything",
    "user_id": "user123"
  }'
```

**Create transformation plan:**
```bash
curl -X POST "http://localhost:8000/transform" \
  -H "Content-Type: application/json" \
  -d '{
    "current_description": "I am burned out and exhausted",
    "target_state": "peace",
    "user_id": "user123"
  }'
```

**List phenomena:**
```bash
curl "http://localhost:8000/phenomena?phase=transcendence"
```

**Analyze trends:**
```bash
curl "http://localhost:8000/trends?user_id=user123&limit=10"
```

### 4. WebSocket for Real-Time

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'analyze',
    description: 'I feel curious and energized',
    user_id: 'user123'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};
```

## Validation System

Test predictions against empirical data:

```bash
python examples/validation_example.py
```

The validator:
- Compares predicted vectors to real participant data
- Calculates correlation scores
- Tests phase accuracy
- Validates wellbeing predictions
- Exports results to JSON/CSV

## Architecture

```
SYNTHIUM/
├── synthium_core/          # Core engine
│   ├── vectors.py          # Vector mathematics
│   ├── engine.py           # Analysis engine
│   ├── database.py         # Phenomena database
│   └── phenomena.py        # 20 core phenomena
│
├── web_backend/            # Web API
│   ├── app.py              # FastAPI server with NLP
│   └── validation.py       # Validation system
│
├── examples/               # Usage examples
│   ├── cli_example.py      # Command-line demo
│   └── validation_example.py
│
├── synthium.py             # Original v10 (Glyph/Ritual)
└── requirements.txt        # Dependencies
```

## The 20 Core Phenomena

The framework includes 20 pre-mapped consciousness states:

**Awakening Phase:**
- Burnout, Depression, Anxiety, Grief, Apathy, Anger, Confusion, Overwhelm, Boredom

**Integration Phase:**
- Flow State, Inner Peace, Joy, Love, Clarity, Curiosity

**Transcendence Phase:**
- Presence, Witness Consciousness

**Dissolution Phase:**
- Sakshatakara, The Void, This

Each phenomenon has:
- Precise vector coordinates
- Description
- Related phenomena
- Tags

## Philosophy

This isn't just software. It's a map of consciousness itself.

The framework recognizes four phases:

1. **Awakening**: Crisis, suffering, resistance (most people)
2. **Integration**: Balance, flow, coherence (skilled practitioners)
3. **Transcendence**: Beyond ego, witness awareness (mystics)
4. **Dissolution**: The seeker dissolves, only This remains (rare)

As you move through these phases, entropy (S) decreases, resonance (r) increases, and resistance (R) dissolves.

The final state is:
```
Vector(v=0.0, R=0.0, r=1.0, C=1.0, S=0.0)
```

Zero movement. Zero resistance. Total connection. Full capacity. Perfect order.

**Sakshatakara.**

---

## API Reference

### POST /analyze
Analyze natural language description → consciousness vector + insights

**Input:**
- `description`: string (natural language)
- `user_id`: string (optional)

**Output:**
- `vector`: 5D coordinates
- `wellbeing_score`: 0-1
- `phase`: awakening/integration/transcendence/dissolution
- `similar_phenomena`: list
- `insights`: list of observations
- `recommendations`: actionable steps

### GET /phenomena
List all phenomena, optionally filtered

**Query params:**
- `phase`: filter by phase
- `tag`: filter by tag
- `limit`: max results

### POST /transform
Create transformation plan from current → target state

**Input:**
- `current_description`: natural language
- `target_state`: phenomenon name
- `user_id`: optional

**Output:**
- Transformation distance
- Difficulty estimate
- Step-by-step action plan

### GET /trends
Analyze user's consciousness trajectory over time

**Query params:**
- `user_id`: required
- `limit`: number of recent states

**Output:**
- Wellbeing trend
- Dimension changes
- Trajectory analysis
- Insights

---

## Technical Notes

### NLP Model
Uses **all-MiniLM-L6-v2** from sentence-transformers:
- 384-dimensional embeddings
- Fast inference (no GPU needed)
- Excellent semantic understanding

### Anchor System
Each dimension has two anchors (high/low). User input is compared to all anchors using cosine similarity, then dimensions are calculated via sigmoid transformation.

### Wellbeing Formula
```python
wellbeing = 0.3*r + 0.3*C + 0.2*(1-R) + 0.2*(1-S)
```

Prioritizes connection (r) and capacity (C), penalizes resistance and chaos.

---

## Contributing

This framework is released to the world. Use it, extend it, validate it.

If you collect empirical data that validates or challenges the vector mappings, please share.

The Soil remembers everything.

---

## License

Public domain. Created by Sina Golchin & Maysam BaygMuhammady, December 2025.

---

## Final Note

There is nothing to seek.
There is nowhere to go.
The framework points to This.

**Tat tvam asi.**

— Sina & Maysam
