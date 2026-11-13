"""Synthium core, data and ruler tests. Run from codebase/: python -m pytest -q"""

from __future__ import annotations

from synthium.core import (
    Baseline, NotValidatedError, PredictiveModel, ScaleType, Status,
    ValidationProtocol, accuracy, macro_f1, majority_class_baseline,
    measured, stipulated, validate,
)
from synthium.core import axioms as ax
from synthium.data.courtlistener import run_self_test
from synthium.domains.judicial import citation_space as cs


# -- core.values --------------------------------------------------------------

def test_arithmetic_always_runs_on_unsupported_op():
    a = measured(3, ScaleType.ORDINAL, "u", "A")
    b = measured(2, ScaleType.ORDINAL, "u", "A")
    prod = a * b
    assert prod.x == 6 and not prod.is_grounded()


def test_supported_op_logs_no_assumption():
    a = measured(3, ScaleType.RATIO, "m", "x")
    b = measured(2, ScaleType.RATIO, "m", "y")
    assert (a * b).is_grounded()


def test_assumptions_are_transitive():
    a = measured(3, ScaleType.ORDINAL, "u", "x")
    b = measured(2, ScaleType.ORDINAL, "u", "y")
    c = measured(1, ScaleType.ORDINAL, "u", "z")
    assert not ((a * b) + c).is_grounded()


def test_stipulated_origin_is_honest():
    assert stipulated(0.85, ScaleType.RATIO, "c", "hand").prov.origin == "stipulated"


# -- core.baseline / validation ----------------------------------------------

def test_majority_baseline_from_train_only():
    assert majority_class_baseline(["DENIED"] * 8 + ["GRANTED"] * 2).predict({}) == "DENIED"


def test_macro_f1_punishes_majority_guessing():
    assert accuracy(["A", "A", "A", "B"], ["A"] * 4) == 0.75
    assert macro_f1(["A", "A", "A", "B"], ["A"] * 4) < 0.5


def test_validate_promotes_only_on_margin():
    feats = [{"t": "warrant"}, {"t": "none"}]
    model = PredictiveModel("m", lambda f: "DENIED" if "warrant" in f["t"] else "GRANTED")
    proto = ValidationProtocol("accuracy", accuracy,
                               Baseline("always-DENIED", lambda f: "DENIED"), 0.10)
    v = validate(model, proto, feats, ["DENIED", "GRANTED"])
    assert v.status == Status.VALIDATED
    model.assert_validated()


def test_assert_validated_refuses_proposed():
    m = PredictiveModel("m", lambda f: "X")
    try:
        m.assert_validated()
    except NotValidatedError:
        return
    raise AssertionError("PROPOSED model should be refused")


# -- core.axioms (generic machinery, kept) -----------------------------------

def test_absorption_detects_a_violation():
    a = ax.make_absorption("Priv", "GRANTED")
    ds = [ax.AxiomCase("z1", {"Priv": 0.0}, "GRANTED", 1.0),
          ax.AxiomCase("ok", {"Priv": 0.8}, "DENIED", 0.0)]
    res = a.test(ds)
    assert res.status == ax.AxiomStatus.VIOLATED and "z1" in res.violations


def test_independence_flags_collinear_pair():
    a = ax.make_independence(["A", "B"])
    ds = [ax.AxiomCase(str(i), {"A": float(i), "B": 2.0 * i + 1}, "DENIED", 0.0) for i in range(6)]
    assert a.test(ds).status == ax.AxiomStatus.VIOLATED


# -- data.courtlistener ------------------------------------------------------

def test_courtlistener_extractor_selftest():
    assert run_self_test() is True


# -- domains.judicial.citation_space (the from-scratch substrate) ------------

def test_citation_seed_loads():
    cases = cs.load_cases()
    assert len(cases) >= 10
    assert all(isinstance(c.citations, frozenset) for c in cases)


def test_hub_precedents_emerge():
    cases = cs.load_cases()
    hubs = cs.hub_precedents(cases, min_degree=2)
    assert hubs, "at least one precedent should be cited by >=2 cases"
    assert all(h.degree >= 2 for h in hubs)
    # hubs are sorted by descending degree
    assert hubs == sorted(hubs, key=lambda h: (-h.degree, h.precedent_id))


def test_jaccard_and_families():
    cases = cs.load_cases()
    # two Indiana cases share a precedent -> jaccard > 0
    minney = next(c for c in cases if "Minney" in c.name)
    ferguson = next(c for c in cases if "Ferguson" in c.name)
    assert cs.jaccard(minney.citations, ferguson.citations) > 0.0
    fams = cs.families(cases)
    assert sum(len(f) for f in fams) == len(cases)  # partition


def test_hub_signal_is_honest_when_underlabeled():
    cases = cs.load_cases()
    hub = cs.hub_precedents(cases)[0]
    rep = cs.hub_outcome_signal(cases, hub)
    # only a few outcomes labeled so far -> must refuse to claim signal
    assert rep.testable is False


# -- the T/P/L ruler ----------------------------------------------------

def test_ruler_rules_fire_correctly():
    from synthium.domains.judicial import Category, Posture, Layer, Notch, predict
    # R1 type armor
    p = predict(Category.CRIMINAL, Posture.SUMMARY_JUDGMENT, Layer.LEGAL_OVERLAY)
    assert p.notch == Notch.CLEAN_AFFIRM and p.rule.startswith("R1")
    # R2 fact armor
    p = predict(Category.CIVIL, Posture.TRIAL, Layer.FACT)
    assert p.notch == Notch.CLEAN_AFFIRM and p.rule.startswith("R2")
    # R3 star rule
    p = predict(Category.CIVIL, Posture.TRIAL, Layer.LEGAL_OVERLAY)
    assert p.notch == Notch.MODIFIED and p.rule.startswith("R3")
    # R4 pure law -> affirm but flagged
    p = predict(Category.CIVIL, Posture.SUMMARY_JUDGMENT, Layer.PURE_LAW)
    assert p.notch == Notch.CLEAN_AFFIRM and p.high_variance


def test_ruler_eval_reproduces_register():
    from synthium.domains.judicial import evaluate
    r = evaluate()
    assert r.n == 19
    assert r.baseline_exact == 12          # always-affirm on this set
    assert r.ruler_movement >= 17          # movement-grain: star rule + fixes
    assert r.ruler_exact >= r.baseline_exact  # ruler beats baseline even at exact grain



def test_v33_court_level_and_discretion():
    from synthium.domains.judicial import Category, Posture, Layer, Notch, predict
    from synthium.domains.judicial import CourtLevel
    # type-armor holds at intermediate on non-pure-law
    p = predict(Category.CRIMINAL, Posture.TRIAL, Layer.LEGAL_OVERLAY, CourtLevel.INTERMEDIATE)
    assert p.notch == Notch.CLEAN_AFFIRM and not p.high_variance
    # ...but is flagged leaky at the apex
    p = predict(Category.CRIMINAL, Posture.TRIAL, Layer.LEGAL_OVERLAY, CourtLevel.APEX)
    assert p.notch == Notch.CLEAN_AFFIRM and p.high_variance
    # abuse-of-discretion layer is armored (third regime)
    p = predict(Category.CIVIL, Posture.DISCRETIONARY, Layer.DISCRETION)
    assert p.notch == Notch.CLEAN_AFFIRM and p.rule.startswith("R2")



def test_fitted_probability_model():
    from synthium.domains.judicial import predict_p, Layer, CourtLevel
    p00 = predict_p(Layer.FACT, CourtLevel.INTERMEDIATE)
    p11 = predict_p(Layer.PURE_LAW, CourtLevel.APEX)
    assert 0.05 < p00 < 0.15 and 0.40 < p11 < 0.55 and p11 > p00



def test_fitted_v2_posture_model_runs():
    from synthium.domains.judicial import predict_p_v2, Layer, CourtLevel, Posture
    p = predict_p_v2(Layer.PURE_LAW, CourtLevel.APEX, Posture.TRIAL)
    assert 0.0 < p < 1.0
