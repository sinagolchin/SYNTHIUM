"""Tests for synthium.geometry: the maths is checked on cases with known answers."""

import csv
import math

import pytest

np = pytest.importorskip("numpy")

from synthium.geometry import (  # noqa: E402
    MetricField,
    RealityTensor,
    RiemannianManifold,
    build_up,
    curvature_index_vs_shuffled,
    derivative,
    integrate_1d,
    integrate_along_path,
    integrate_nd,
    is_new_dimension,
    learn_metric_from_data,
    load_cases,
    pairwise_distances_missing,
    parallel_analysis,
    parse_score,
    rate_along,
    sphere_metric,
)
from synthium.geometry.dimensions import compare_domains, estimate_dimensions  # noqa: E402
from synthium.geometry.trajectory import (  # noqa: E402
    CasePath,
    Stage,
    paths_from_staged_cells,
    staged_cells,
)


# ---------- reading scores ----------

@pytest.mark.parametrize(
    "text,value,tag",
    [
        ("0.75 FOUND (disclosure)", 0.75, "FOUND"),
        ("1.0(claimed)", 1.0, "CLAIMED"),
        ("0.5 CLAIMED-P (one admission)", 0.5, "CLAIMED"),
        ("1 of 2 (respondent imputed control)", 0.5, None),
        ("3 ADMITTED", 3.0, "ADMITTED"),
        ("0 FOUND-JURY (CLAIMED-P high)", 0.0, "FOUND"),
        ("present-contested (drug use)", None, None),
        ("", None, None),
    ],
)
def test_parse_score(text, value, tag):
    v, t = parse_score(text)
    assert v == value
    if value is not None:
        assert t == tag


def _write_cases(path, rows, extra=("filed",)):
    cols = ["case_id", *extra] + sorted({k for r in rows for k in r if k.startswith("Q")})
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


def _synthetic(path, n=40, seed=1):
    """Q1, Q2 independent; Q3 = Q1 + Q2 (a combination); Q4 noise; Q9 sparse."""
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n):
        a, b = rng.normal(), rng.normal()
        rows.append(
            {
                "case_id": f"C{i}",
                "filed": f"20{10 + i % 10}-0{1 + i % 9}-15",
                "Q1_a": f"{a:.4f} FOUND",
                "Q2_b": f"{b:.4f}",
                "Q3_sum": f"{a + b + 0.05 * rng.normal():.4f} INFERRED",
                "Q4_noise": f"{rng.normal():.4f}",
                "Q9_sparse": f"{rng.normal():.3f}" if i < 3 else "",
                "Q33_motivation_kind": "GAIN",
            }
        )
    _write_cases(path, rows)


def test_load_cases_matrix(tmp_path):
    p = tmp_path / "c.csv"
    _synthetic(p)
    cs = load_cases(str(p))
    assert cs.n_cases == 40
    assert "Q33_motivation_kind" not in cs.columns
    assert cs.coverage()["Q9_sparse"] == 3
    assert cs.active_dimensions()["C0"][:2] == ["Q1_a", "Q2_b"]
    assert cs.tags[0][cs.columns.index("Q1_a")] == "FOUND"
    assert not np.isnan(cs.filed_as_years()).any()


def test_load_cases_other_domain(tmp_path):
    p = tmp_path / "m.csv"
    with open(p, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["market_id", "opened", "M_hype", "M_herding", "note"])
        w.writerow(["m1", "2025-01-01", "0.5", "0.2", "x"])
        w.writerow(["m2", "2025-02-01", "0.7", "", "y"])
    cs = load_cases(str(p), domain="markets", quality_pattern=r"^M_", id_column="market_id",
                    date_column="opened")
    assert cs.columns == ["M_hype", "M_herding"]
    assert cs.case_ids == ["m1", "m2"]
    assert cs.domain == "markets"


# ---------- manifold ----------

def test_constant_metric_is_flat_and_v4_compatible():
    M = RiemannianManifold(3, np.diag([1.0, 4.0, 9.0]))
    assert M.distance(np.zeros(3), np.array([1.0, 1.0, 1.0])) == pytest.approx(math.sqrt(14))
    assert M.scalar_curvature() == 0.0
    path = M.geodesic(np.zeros(3), np.ones(3), 11)
    assert path.points.shape == (11, 3)


def test_mahalanobis_discounts_correlated_qualities():
    rng = np.random.default_rng(0)
    a = rng.normal(size=500)
    X = np.column_stack([a, a + 0.1 * rng.normal(size=500)])  # nearly the same quality twice
    g = learn_metric_from_data(X, "mahalanobis", shrinkage=0.0)
    M = RiemannianManifold(2, g)
    along = M.distance(np.zeros(2), np.array([1.0, 1.0]))  # the usual direction
    across = M.distance(np.zeros(2), np.array([1.0, -1.0]))  # a rare direction
    assert across > 5 * along


def test_pairwise_missing_uses_shared_dims_only():
    Z = np.array([[0.0, 0.0, np.nan], [3.0, 4.0, 1.0], [np.nan, np.nan, 5.0]])
    D, shared = pairwise_distances_missing(Z, min_shared=2)
    assert D[0, 1] == pytest.approx(math.sqrt((9 + 16) / 2))
    assert shared[0, 1] == 2
    assert np.isnan(D[0, 2])


def test_curvature_index_sees_a_circle():
    t = np.linspace(0, 2 * np.pi, 60, endpoint=False)
    X = np.column_stack([np.cos(t), np.sin(t)])
    res = curvature_index_vs_shuffled(X, k=6, n_perm=50)
    assert res["observed"] > res["shuffled_mean"]
    assert res["p_at_least_as_folded"] < 0.05
    flat = np.random.default_rng(2).uniform(size=(60, 2))
    assert curvature_index_vs_shuffled(flat, k=6, n_perm=50)["p_at_least_as_folded"] > 0.05


# ---------- curvature and geodesics ----------

@pytest.mark.parametrize("r", [1.0, 2.0])
def test_sphere_scalar_curvature(r):
    S = sphere_metric(r)
    assert S.scalar_curvature(np.array([1.0, 0.3])) == pytest.approx(2 / r**2, rel=1e-3)


def test_flat_space_has_zero_curvature():
    F = MetricField(lambda x: np.diag([1.0, 2.0, 3.0]), 3)
    assert np.allclose(F.riemann(np.array([0.1, 0.2, 0.3])), 0, atol=1e-6)


def test_sphere_christoffel_known_values():
    G = sphere_metric(1.0).christoffel(np.array([1.0, 0.0]))
    # Gamma^theta_phiphi = -sin cos ; Gamma^phi_thetaphi = cot
    assert G[0, 1, 1] == pytest.approx(-math.sin(1) * math.cos(1), rel=1e-5)
    assert G[1, 0, 1] == pytest.approx(math.cos(1) / math.sin(1), rel=1e-5)


def test_sphere_geodesic_is_great_circle():
    S = sphere_metric(1.0)
    path = S.geodesic([math.pi / 2, 0.0], [0.0, 1.0], t_end=math.pi / 2, steps=200)
    assert np.allclose(path[:, 0], math.pi / 2, atol=1e-6)  # stays on the equator
    assert S.path_length(path) == pytest.approx(math.pi / 2, rel=1e-3)


# ---------- tensors ----------

def test_tensor_raise_lower_roundtrip_and_rank2():
    g = np.array([[2.0, 0.5], [0.5, 1.0]])
    v = RealityTensor([1.0, 2.0], "u")
    assert v.index_type == "contravariant"
    back = v.lower_index(g).raise_index(np.linalg.inv(g))
    assert np.allclose(back.components, v.components)
    assert v.inner_product(v, g) == pytest.approx(np.array([1, 2]) @ g @ np.array([1, 2]))
    T = v.tensor_product(RealityTensor([3.0, 4.0], "d"))
    assert T.indices == "ud"
    assert float(T.contract(0, 1)) == pytest.approx(1 * 3 + 2 * 4)
    Td = T.lower_index(g, axis=0)
    assert Td.indices == "dd"


# ---------- dimensions ----------

def test_parallel_analysis_finds_two_planted_dimensions():
    rng = np.random.default_rng(3)
    f = rng.normal(size=(200, 2))
    W = rng.normal(size=(2, 6))
    X = f @ W + 0.2 * rng.normal(size=(200, 6))
    assert parallel_analysis(X, n_perm=100)["dimensions_beating_chance"] == 2


def test_build_up_dot_line_area_volume(tmp_path):
    p = tmp_path / "c.csv"
    _synthetic(p)
    cs = load_cases(str(p))
    bu = build_up(cs, order=["Q1_a", "Q2_b", "Q3_sum", "Q4_noise"], n_perm=50)
    names = [s.name for s in bu.steps]
    assert names == ["dot", "line", "area", "volume", "4-volume"]
    by = {s.added: s for s in bu.steps}
    assert by["Q2_b"].new_share > 0.8  # independent: a new direction
    assert by["Q3_sum"].new_share < 0.05  # the sum adds no new direction
    assert by["Q4_noise"].new_share > 0.8
    assert by["Q3_sum"].volume < 0.1 * by["Q3_sum"].volume_shuffled


def test_build_up_stops_when_cases_run_out(tmp_path):
    p = tmp_path / "c.csv"
    _synthetic(p)
    cs = load_cases(str(p))
    bu = build_up(cs, order=["Q1_a", "Q9_sparse"], n_perm=10)
    assert [s.name for s in bu.steps] == ["dot", "line"]


def test_new_dimension_test_spots_the_combination(tmp_path):
    p = tmp_path / "c.csv"
    _synthetic(p)
    cs = load_cases(str(p))
    r = is_new_dimension(cs, "Q3_sum", n_perm=50)
    assert r["verdict"] == "combination of others"
    assert set(r["best_predictors"]) == {"Q1_a", "Q2_b"}
    assert is_new_dimension(cs, "Q4_noise", n_perm=50)["verdict"].startswith("new")
    est = estimate_dimensions(cs, n_perm=30)
    assert "Q4_noise" in est["new_dimensions"]
    assert "Q9_sparse" in est["untested"]


def test_compare_domains_matches_by_name(tmp_path):
    p = tmp_path / "c.csv"
    _synthetic(p)
    a = load_cases(str(p), domain="courts")
    b = load_cases(str(p), domain="markets")
    out = compare_domains(a, b)
    assert "noise" in out["new_dimension_in_both"]


# ---------- calculus ----------

def test_derivatives_of_known_functions():
    assert derivative(math.sin, 0.3, 1) == pytest.approx(math.cos(0.3), rel=1e-4)
    assert derivative(math.exp, 0.5, 3) == pytest.approx(math.exp(0.5), rel=1e-2)
    assert derivative(lambda x: x**4, 1.0, 4) == pytest.approx(24, rel=1e-2)


def test_integrals():
    assert integrate_1d(lambda x: x**2, 0, 1) == pytest.approx(1 / 3, rel=1e-4)
    line = np.column_stack([np.linspace(0, 3, 50), np.linspace(0, 4, 50)])
    assert integrate_along_path(lambda p: 1.0, line) == pytest.approx(5.0)
    assert integrate_nd(lambda p: 1.0, [(0, 2), (0, 3), (0, 1)]) == pytest.approx(6.0)


def test_rate_along_trend_and_no_trend():
    t = np.arange(60)
    y = 0.05 * t + np.random.default_rng(0).normal(scale=0.2, size=60)
    up = rate_along(t, y, n_perm=200)
    assert up["slope"] == pytest.approx(0.05, abs=0.01) and up["p_slope"] < 0.01
    flat = rate_along(t, np.random.default_rng(1).normal(size=60), n_perm=200)
    assert flat["p_slope"] > 0.01


# ---------- trajectories ----------

def test_case_path_and_staged_cells(tmp_path):
    p = tmp_path / "c.csv"
    _write_cases(p, [{"case_id": "A", "Q15_cooperative": "0.2 before verdict / 0.9 after (CODER)"},
                     {"case_id": "B", "Q15_cooperative": "0.5"}])
    cells = staged_cells(str(p), ["Q15_cooperative"])
    assert cells[0][:4] == ("A", "Q15_cooperative", 0.2, 0.9)
    path = paths_from_staged_cells(cells)[0]
    assert path.length() == pytest.approx(0.7)
    cp = CasePath("X", [Stage("filing", "2020-01-01", {"Q1": 0.0, "Q2": 0.0}),
                        Stage("sentence", "2021-01-01", {"Q1": 0.3, "Q2": 0.4})])
    assert cp.length() == pytest.approx(0.5)
