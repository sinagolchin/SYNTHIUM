"""Every restored earlier version still imports and its own checks still run (UNTESTED results)."""

import importlib

import pytest

np = pytest.importorskip("numpy")

PLAIN = [
    "synthium.legacy",
    "synthium.legacy.omega_v1_5.science",
    "synthium.legacy.v2.omega_v2",
    "synthium.legacy.v2.reality_field",
    "synthium.legacy.v3_4.combined",
    "synthium.legacy.v5.honesty",
    "synthium.legacy.v6.predictive",
    "synthium.legacy.v6.courtlistener",
    "synthium.legacy.v6_1",
    "synthium.legacy.v6_1.domains.judicial.formula",
    "synthium.legacy.v8.atlas",
    "synthium.legacy.v8.blindprotocol",
    "synthium.legacy.synthiumbot.tone",
    "synthium.legacy.synthiumbot.memory",
    "synthium.legacy.synthiumbot.config",
]


@pytest.mark.parametrize("mod", PLAIN)
def test_imports(mod):
    importlib.import_module(mod)


@pytest.mark.parametrize("mod", ["synthium.legacy.v4", "synthium.legacy.v4_3_1",
                                 "synthium.legacy.synthiumbot.synthium_v4"])
def test_imports_with_scipy(mod):
    pytest.importorskip("scipy")
    pytest.importorskip("sklearn")
    importlib.import_module(mod)


def test_neural_encoder_with_torch():
    pytest.importorskip("torch")
    importlib.import_module("synthium.legacy.v4_3_1.neural")


def test_bot_token_is_not_in_the_repo():
    import re

    from synthium.legacy.synthiumbot import config

    src = open(config.__file__).read()
    assert "os.environ.get(\"TELEGRAM_TOKEN\"" in src
    assert not re.search(r"\d{6,}:[A-Za-z0-9_-]{30,}", src)


def test_v1_mass_formula():
    from synthium.legacy.omega_v1_5.science import HolisticScience
    from synthium.legacy.omega_v1_5.vectors import SynthiumVector

    v = SynthiumVector(v=0.1, R=0.9, r=0.2, C=0.8, S=0.4)
    assert "Mass = R × C" in HolisticScience().derive_formula(v)


def test_v6_1_lists_its_ungrounded_constants():
    from synthium.legacy.v6_1.domains.judicial.formula import ungrounded_coefficients

    assert len(ungrounded_coefficients()) == 18


def test_v8_atlas_loads_44_cases():
    from synthium.legacy.v8.atlas import load_atlas

    assert len(load_atlas()) == 44


def test_v6_courtlistener_self_test():
    from synthium.legacy.v6 import courtlistener

    assert courtlistener.run_self_test() is True
