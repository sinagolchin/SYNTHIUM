# Retired Lineages

What the v6.1 consolidation dropped, and why. Kept as institutional memory so
abandoned approaches are not silently revived.

## The "Omega" keyword-quantifier

**Files:** `main.py`, `transducer.py`, `science.py`, `recorder.py`, `vectors*`,
`reality_field.py`, `lexicon*.json`, and the `__init__` that exported them.

**What it did:** scored free text on five dimensions by counting keywords
(`['fast','quick','speed',...] -> v`), then printed "formulas" like `Mass = R × C`
when thresholds were crossed.

**Why retired:** this is the project's central failure mode in pure form —
unjustified numbers dressed as measurement, and pseudo-physics labels dressed as
discovery. It cannot be validated and should not be built on. The legitimate
descendant of "turn text into structured features" is the rubric-coded atlas
plus the courtlistener labeler, both of which keep features and independent
targets separate.

## The v4.3.1 monolith

**File:** `synthium_v4_3_1.py` (2,045 lines).

**What it did:** everything — confidence system, Riemannian manifold,
`RealityState`, calculus, dimensional discovery, governance engine, CourtListener
client, judicial spec, formulas, dataset loading, metrics, a PyTorch encoder,
losses, and training — in one file.

**Why retired as a unit:** unmaintainable and impossible to reason about in
isolation. The genuinely useful parts (judicial spec, formulas, atlas handling,
the propose/validate idea) were carried into focused modules. The speculative
infrastructure (manifold geometry, governance engine, dimensional discovery) was
left out of the core because none of it is exercised by a validated result; it
can return as a clearly-marked optional module if and when a real experiment
needs it.

## The neural layer

**Files:** `encoder.py`, `losses.py`, `trainer.py`, `train_deleaked.py`,
`metrics.py`, and the neural sections of the monolith.

**Why left out of the v6.1 core:** the encoder's only demonstrated behavior is
imitating rubric labels, and its headline accuracy was a leakage artifact
(`EMPIRICAL_STATUS.md`). Reintroducing it before there is a rubric-independent
target to train against would re-invite the exact confound that was just removed.
It belongs in an optional `synthium.neural` extra, gated behind a real
court-derived dataset — not in the dependency-light core.

## The SRIA / LANL cyber workstream

**Files:** `sria_rt_v0*.py`, `SRIA_*.md`, `SRIA_CMD.txt`,
`sria_rt_v041_baseline_eval_clean.pdf`, the v2 omega files, `synthium_omega_v2.py`.

**Why retired:** descoped. It was previously the most promising candidate for a
first predictive-validity claim (LANL provides rubric-independent ground truth),
but it is out of scope for the consolidated judicial-focused package. Preserved
here as a note in case it is revived as its own subject core later.

## The v3.x "discovery" PDF corpus

**Files:** the ~80 PDFs (`manifold_geometry.pdf`, `tensor_calculus.pdf`,
`ethics_discovery.pdf`, `empirical_discovery.pdf`, the `*_v3*`/`*_v34` series,
`Sria_V3_0_Current_Paper_3.pdf`, etc.).

**Why retired:** they narrate Synthium as a *discovered* theory of qualitative
reality, the framing `PROJECT_INSTRUCTIONS.md` explicitly walks back. Their
mathematical content (Riemannian metrics, dimensional discovery) is not wrong in
itself, but it is presented as established structure rather than proposed
instrument. The current docs supersede them.
