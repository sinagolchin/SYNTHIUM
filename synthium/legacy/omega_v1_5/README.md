# Synthium Omega v1.5

A unified system for quantifying qualitative phenomena.

## Quick Start
```bash
python main.py
```

## Example

1. Select "1. Quantify new phenomenon"
2. Name: "Grief"
3. Describe: "A heavy feeling of loss"
4. View the vector and analysis
5. Save to lexicon

## Philosophy

The lexicon starts empty and grows with discovery. We don't know all phenomena, only how to measure them.

## Vector Components

| Component | Symbol | Description |
|-----------|--------|-------------|
| Velocity  | v      | Rate of change, dynamism |
| Resistance| R      | Inertia, opposition to change |
| Resonance | r      | Connectivity, attraction |
| Capacity  | C      | Depth, potential |
| Entropy   | S      | Disorder, decay |

## Architecture

```
synthium/
├── vectors.py     # SynthiumVector dataclass
├── transducer.py  # Qualitative → Quantitative conversion
├── science.py     # Analysis and formula derivation
└── recorder.py    # Lexicon persistence
```
