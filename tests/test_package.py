"""Package-level checks: data paths, bundled data, frozen parameters, and the CLI."""
from __future__ import annotations

import csv
import io
import json
from contextlib import redirect_stdout

from synthium import cli, data_dir, data_path
from synthium.blind import classify_cn
from synthium.domains.judicial import fitted_params


def run_cli(*argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = cli.main(list(argv))
    return rc, buf.getvalue()


# -- paths and bundled data ---------------------------------------------------

def test_data_dir_defaults_to_repo_data():
    assert data_dir().name == "data" and data_path("citation_seed.json").exists()


def test_data_dir_env_override(monkeypatch, tmp_path):
    monkeypatch.setenv("SYNTHIUM_DATA", str(tmp_path))
    assert data_dir() == tmp_path


def test_verified_ledger_is_present_and_readable():
    with open(data_path("VERIFIED_LEDGER.csv"), newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows and {"case", "status"} <= set(rows[0])
    assert len(rows) >= 15  # 15 rows as of 2026-11-10; the ledger only grows


def test_registers_present():
    regs = sorted(p.name for p in data_path("registers").glob("blind_register_*.csv"))
    assert "blind_register_v1.csv" in regs and len(regs) >= 13


def test_frozen_params_load():
    for name in ("fitted_params", "fitted_params_v2", "fitted_params_v3_dismissal"):
        assert isinstance(fitted_params(name), dict)
    assert fitted_params("fitted_params")["n"] == 71


# -- Chinese tenor classifier ------------------------------------------------

def test_classify_cn_fullwidth_comma():
    assert classify_cn("……裁定如下：驳回上诉，维持原判。")[0] == "CLEAN_AFFIRM"


# -- CLI -------------------------------------------------------------------------

def test_cli_predict():
    rc, out = run_cli("predict", "--category", "civil", "--posture", "trial", "--layer", "legal_overlay")
    assert rc == 0 and out.startswith("MODIFIED") and "R3" in out


def test_cli_predict_apex_flags_leaky_type_armor():
    rc, out = run_cli("predict", "--category", "criminal", "--posture", "trial",
                      "--layer", "legal_overlay", "--level", "apex")
    assert rc == 0 and "HIGH-VARIANCE" in out


def test_cli_ruler_eval_reproduces_record():
    rc, out = run_cli("ruler-eval")
    assert rc == 0 and "ruler exact-notch 16/19" in out and "baseline 12/19" in out


def test_cli_citation_space_and_selftest():
    assert run_cli("citation-space")[0] == 0
    assert run_cli("courtlistener-selftest")[0] == 0


def test_cli_blind_passthrough(tmp_path):
    rc, _ = run_cli("blind", "--home", str(tmp_path), "verify")
    assert rc == 0


def test_cli_no_command_prints_help():
    rc, out = run_cli()
    assert rc == 0 and "ruler-eval" in out


def test_params_are_plain_json():
    for p in data_path().parent.joinpath("synthium", "domains", "judicial", "params").glob("*.json"):
        json.loads(p.read_text(encoding="utf-8"))
