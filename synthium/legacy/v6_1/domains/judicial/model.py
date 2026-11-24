"""Turn the PROPOSED judicial formula into a testable model -- and be honest
about what testing it on the atlas can and cannot show.

There are two different experiments, and conflating them is the original sin
``PROJECT_INSTRUCTIONS.md`` warns against:

  RUBRIC IMITATION  -- can the formula reproduce the atlas's own outcome column?
                       The atlas outcome was coded alongside the units by the
                       same hand, so this measures internal consistency, not
                       predictive power. ``validate_against_atlas`` runs this and
                       labels the verdict accordingly.

  PREDICTIVE VALIDITY -- can the formula forecast outcomes read straight from the
                       court record, for cases it was not fit on? That needs
                       rubric-coded units AND a courtlistener outcome for the
                       same cases. We do not have that join yet, so this cannot
                       be run today. ``predictive_validity_requirements`` says so
                       plainly rather than faking a number.

The decision threshold is itself an ungrounded constant. So it is a declared
parameter of the experiment, not a value baked into the framework.
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

from ...core import (
    Baseline,
    PredictiveModel,
    Status,
    ValidationProtocol,
    Verdict,
    accuracy,
    macro_f1,
    majority_class_baseline,
    validate,
)
from ...data.atlas import Case, stratified_split
from .formula import suppression_pressure

# Binary outcomes the court actually decides; everything else is atlas-only
# bookkeeping and is excluded from a grant/deny test.
BINARY_OUTCOMES = ("GRANTED", "DENIED")


def build_formula_model(threshold: float, name: str = "suppression-formula") -> PredictiveModel:
    """A model mapping the symbolic pressure to GRANTED/DENIED at ``threshold``.

    High suppression pressure -> the motion to suppress is GRANTED. The
    threshold is supplied by the experimenter; the framework does not invent it.
    """

    def predict(features: Dict[str, object]) -> str:
        units = {k: float(v) for k, v in features.items() if isinstance(v, (int, float))}
        ops = units  # operators live in the same flat feature dict
        pressure, _coeffs = suppression_pressure(units, ops)
        return "GRANTED" if pressure >= threshold else "DENIED"

    return PredictiveModel(name, predict)


def _binary_cases(cases: Sequence[Case]) -> List[Case]:
    return [c for c in cases if c.outcome in BINARY_OUTCOMES]


def validate_against_atlas(threshold: float = 0.5, *, seed: int = 42,
                           required_margin: float = 0.0) -> Tuple[Verdict, str]:
    """Run the RUBRIC-IMITATION experiment on the atlas. Returns (verdict, caveat).

    The verdict uses the real harness -- frozen majority baseline, held-out
    split -- so the machinery is honest. The caveat states, in the returned
    string, that beating the baseline here would still NOT establish predictive
    validity, because the target came from the same rubric as the features.
    """
    from ...data.atlas import load_atlas

    cases = _binary_cases(load_atlas())
    train, test = stratified_split(cases, test_fraction=0.25, seed=seed)

    model = build_formula_model(threshold)
    protocol = ValidationProtocol(
        metric_name="macro_f1",
        metric=macro_f1,
        baseline=majority_class_baseline([c.outcome for c in train]),
        required_margin=required_margin,
    )
    test_features = [c.features(redact=True) for c in test]
    test_labels = [c.outcome for c in test]
    verdict = validate(model, protocol, test_features, test_labels)

    caveat = (
        "RUBRIC IMITATION ONLY. The target (atlas 'outcome') was coded alongside "
        "the unit values by the same rubric, so this verdict measures internal "
        "consistency, not predictive validity. A VALIDATED status here would NOT "
        "license any claim that the formula predicts real court outcomes. "
        "n is tiny (binary atlas subset); treat as a smoke test, not evidence."
    )
    return verdict, caveat


def predictive_validity_requirements() -> List[str]:
    """What it would actually take to run the predictive-validity experiment.

    Stated as a checklist because the honest answer to 'is the formula valid?'
    today is 'we have not built the conditions to find out yet.'
    """
    return [
        "A set of cases with BOTH rubric-coded units/operators AND an outcome "
        "read independently from the court record (synthium.data.courtlistener).",
        "A pre-declared baseline (majority class and/or a single-keyword rule).",
        "A pre-declared required margin and metric, frozen before test outcomes "
        "are seen.",
        "A held-out split the formula was never tuned on.",
        "Enough cases that the margin is distinguishable from noise -- 37 binary "
        "atlas cases are not enough; target hundreds with court-derived labels.",
        "Inter-rater reliability on the unit coding, so the features themselves "
        "are reproducible across coders before their predictive value is judged.",
    ]
