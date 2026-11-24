"""Tests for synthium.phenomena: the catalogue, the index doc, and the structure tests."""

import os

import pytest

np = pytest.importorskip("numpy")

from synthium.geometry.scores import CaseScores  # noqa: E402
from synthium.phenomena import (  # noqa: E402
    FORMS,
    RECORDS,
    UNDER_CONSIDERATION,
    by_id,
    combine,
    computable,
    created_how,
    equilibrium,
    evaluate,
    legacy_profiles,
    phenomena_from_profiles,
    profile_space,
)
from synthium.phenomena.index import in_sync, render  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _cs(cols, X):
    X = np.asarray(X, float)
    return CaseScores(case_ids=[f"c{i}" for i in range(len(X))], columns=list(cols), values=X,
                      tags=[[None] * len(cols) for _ in X], reading_order=np.arange(len(X)),
                      filed=[None] * len(X))


def test_nothing_is_retired():
    assert len(RECORDS) >= 90
    assert all(r.status == UNDER_CONSIDERATION for r in RECORDS)
    ids = [r.id for r in RECORDS]
    assert len(ids) == len(set(ids))
    for r in RECORDS:
        assert "retired" not in r.status.lower()
        assert r.version and r.statement and r.where


def test_every_repo_path_in_the_index_exists():
    for r in RECORDS:
        for p in (x.strip() for x in r.where.split(";")):
            if p.startswith(("synthium/", "archive/", "docs/")):
                assert os.path.exists(os.path.join(ROOT, p)), (r.id, p)


def test_index_doc_is_in_sync():
    assert in_sync(), "run: python -m synthium.phenomena index --write"
    assert "under consideration" in render()


def test_formulas_match_the_restored_code():
    from synthium.legacy.v3_4.combined import AgnosticRealityVector, EthicsDiscovery

    p = dict(v=0.3, R=0.4, r=0.5, C=0.6, S=0.3)
    vals = evaluate(p)
    vec = AgnosticRealityVector(0, 0, 0, **p)
    assert vals["V3.4-E"] == pytest.approx(vec.E)
    assert vals["V3.4-M"] == pytest.approx(vec.M)
    assert vals["V3.4-P"] == pytest.approx(vec.P)
    assert vals["V3.4-COLLAPSE"] == pytest.approx(EthicsDiscovery.predict_collapse_risk(vec)["risk_score"])
    assert vals["V1-MASS"] == pytest.approx(0.24)
    assert vals["V2-FLUX"] == pytest.approx(0.15)
    assert vals["V3-E"] == pytest.approx(0.35 * 0.5 + 0.35 * 0.7 + 0.30 * (1 - 0.12 / 0.61))


def test_old_profiles_come_from_the_restored_code():
    profs = legacy_profiles()
    for name in ("grief", "joy", "anxiety", "love", "fear", "office stress"):
        assert name in profs
    assert set(profs["grief"]) == {"v", "R", "r", "C", "S"}
    phs = phenomena_from_profiles()
    assert all(set(p.formulas()) == {r.id for r in computable()} for p in phs)
    assert profile_space().values.shape == (len(profs), 5)


def test_combine_forms():
    P = np.array([[0.2, 0.8], [0.5, 0.5]])
    assert combine(P, "sum").tolist() == pytest.approx([1.0, 1.0])
    assert combine(P, "weakest part").tolist() == [0.2, 0.5]
    assert combine(P, "strongest part").tolist() == [0.8, 0.5]
    assert combine(P, "product")[1] > combine(P, "product")[0]
    k = combine(np.array([[0.1, 0.9], [0.2, 0.0]]), "strict priority")
    assert k[1] > k[0]  # the first part decides


@pytest.mark.parametrize("form", ["weakest part", "strongest part", "product"])
def test_created_how_finds_the_operation(form):
    rng = np.random.default_rng(1)
    A = rng.uniform(0, 1, (60, 2))
    y = combine(A, form)
    cs = _cs(["a", "b", "y"], np.column_stack([A, y]))
    r = created_how(cs, "y", ["a", "b"], n_perm=50)
    assert r["tested"] and r["best_form"] == form and r["p_best"] < 0.05
    assert set(r["forms"]) == set(FORMS)


def test_created_how_needs_enough_cases():
    cs = _cs(["a", "y"], [[0.1, 0.2], [0.3, 0.4]])
    assert created_how(cs, "y", ["a"])["tested"] is False


def test_equilibrium_finds_a_planted_balance():
    rng = np.random.default_rng(2)
    a, b = rng.uniform(0, 1, 50), rng.uniform(0, 1, 50)
    c = 1.5 - a - b + rng.normal(0, 0.01, 50)  # a + b + c stays near 1.5
    r = equilibrium(_cs(["a", "b", "c"], np.column_stack([a, b, c])), ["a", "b", "c"], n_perm=50)
    assert r["tested"] and r["p_at_least_as_balanced"] < 0.05
    w = r["weights"]
    assert all(np.sign(w[k]) == np.sign(w["a"]) for k in "bc")


def test_equilibrium_on_noise_is_not_balanced():
    rng = np.random.default_rng(3)
    r = equilibrium(_cs(["a", "b", "c"], rng.uniform(0, 1, (50, 3))), ["a", "b", "c"], n_perm=50)
    assert r["p_at_least_as_balanced"] > 0.05


def test_run_writes_a_report(tmp_path):
    from synthium.phenomena.run import run

    rng = np.random.default_rng(4)
    path = tmp_path / "cases.csv"
    a = rng.uniform(0, 1, 30)
    with open(path, "w") as fh:
        fh.write("case_id,filed,Q1_a,Q2_b,Q3_c,Q4_d\n")
        for i in range(30):
            fh.write(f"k{i},2025-01-01,{a[i]:.2f} FOUND,{1 - a[i]:.2f},{rng.uniform():.2f},{rng.uniform():.2f}\n")
    R = run(str(path), str(tmp_path / "out"), n_perm=20)
    assert R["n_cases"] == 30 and "profiles" in R
    text = (tmp_path / "out" / "phenomena_report.md").read_text()
    assert "UNTESTED" in text and "under consideration" in text
    assert by_id()["G9-EQUILIBRIUM"].kind == "axiom"
