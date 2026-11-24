# Neural Synthium Upgrade Spec v0.1

## Purpose

Add trainable neural tissue to Synthium without replacing the symbolic-geometric core.

## Layer model

```text
Raw reality data
  -> domain transducer
  -> neural encoder
  -> Synthium units
  -> manifold placement
  -> operator layer
  -> formula hierarchy
  -> outcome / pressure / explanation
  -> confidence + governance
```

## Components added

### 1. Trainable weights

Implemented in `synthium/neural/encoder.py` using PyTorch modules:

- embedding layer;
- MLP encoder;
- unit head;
- operator head;
- outcome head;
- embedding head;
- uncertainty head.

### 2. Backpropagation

Implemented in `synthium/neural/trainer.py` with AdamW and PyTorch autograd.

### 3. Learned embeddings

The `embedding_head` produces normalized manifold embeddings for retrieval and metric learning.

### 4. Gradient-trained encoders

`JudicialNeuralEncoder` maps case text to Synthium judicial coordinates.

### 5. Neural loss function

Implemented in `synthium/neural/losses.py`:

```text
L_total =
  lambda_units * L_units
+ lambda_ops * L_operators
+ lambda_outcome * L_outcome
+ lambda_metric * L_metric
+ lambda_confidence * L_confidence
+ lambda_consistency * L_consistency
```

### 6. Optimizer

AdamW in `trainer.py`.

### 7. Formal dataset

`data/judicial_suppression_atlas_v0_2.csv` is the first labeled training set.

### 8. Evaluation

`evaluate_judicial_encoder()` reports:

- unit MAE;
- unit RMSE;
- outcome accuracy;
- operator micro-accuracy.

## Domain separation

The judicial domain lives under:

```text
synthium/domains/judicial/
```

Synthium Core remains universal. Future domains should follow the same structure:

```text
synthium/domains/medical/
synthium/domains/sociology/
synthium/domains/physics/
```

