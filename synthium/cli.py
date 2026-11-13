"""Synthium command line.

    python -m synthium predict --category civil --posture trial --layer legal_overlay [--level apex]
    python -m synthium ruler-eval [--register PATH]   score the ruler against a blind register
    python -m synthium citation-space                  experimental objective substrate
    python -m synthium harness-demo                    validation-gate demo
    python -m synthium courtlistener-selftest          offline check of the outcome labeler
    python -m synthium blind <command> ...             the blind protocol (see docs/BLIND_PROTOCOL.md)
"""
from __future__ import annotations

import argparse
import sys


def cmd_predict(args) -> int:
    from .domains.judicial import Category, CourtLevel, Layer, Posture, predict
    p = predict(Category(args.category), Posture(args.posture), Layer(args.layer),
                CourtLevel(args.level))
    print(p.line())
    return 0


def cmd_ruler_eval(args) -> int:
    from .domains.judicial import evaluate
    r = evaluate(args.register)
    print("Ruler vs blind register (committed-before-reveal set)")
    print("-" * 72)
    for ln in r.lines:
        print(" ", ln)
    print("-" * 72)
    print(r.summary())
    print("\nHonesty: v3's committed prospective record was 16/19 vs baseline 12/19.")
    print("v3.2's refinements were induced partly from attempt 11 (in-sample);")
    print("its own prospective exam on fresh committed cases is still owed.")
    return 0


def cmd_citation_space(_args) -> int:
    from .domains.judicial import citation_space as cs
    s = cs.summarize(cs.load_cases())
    print(f"cases {s['n_cases']} | outcomes {s['n_with_outcome']} | "
          f"precedents {s['n_distinct_precedents']} | hubs {s['n_hub_precedents']} | "
          f"families {s['n_families']}")
    return 0


def cmd_harness_demo(_args) -> int:
    import random
    from .core import (NotValidatedError, PredictiveModel, ValidationProtocol, accuracy,
                       majority_class_baseline, validate)
    rng = random.Random(0)

    def make(sig):
        p = rng.random() < 0.5
        y = ("DENIED" if p else "GRANTED") if sig else rng.choice(["DENIED", "GRANTED"])
        return {"t": ("warrant " if p else "") + "x"}, y

    for tag, sig in (("signal", True), ("no signal", False)):
        tr = [make(sig) for _ in range(80)]
        te = [make(sig) for _ in range(80)]
        proto = ValidationProtocol("accuracy", accuracy,
                                   majority_class_baseline([y for _, y in tr]), 0.10)
        m = PredictiveModel("demo", lambda f: "DENIED" if "warrant" in f["t"] else "GRANTED")
        v = validate(m, proto, [f for f, _ in te], [y for _, y in te])
        print(f"{tag}: {v.explain()}")
        try:
            m.assert_validated()
            print("  -> usable for claims")
        except NotValidatedError:
            print("  -> refused (stays PROPOSED/FALSIFIED)")
    return 0


def cmd_courtlistener_selftest(_args) -> int:
    from .data.courtlistener import run_self_test
    return 0 if run_self_test() else 1


def cmd_blind(args) -> int:
    from .blind import protocol
    return protocol.main(args.blind_args)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="synthium", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command")
    pr = sub.add_parser("predict", help="predict the outcome notch for one case")
    pr.add_argument("--category", required=True)
    pr.add_argument("--posture", required=True)
    pr.add_argument("--layer", required=True)
    pr.add_argument("--level", default="intermediate", help="intermediate (default) or apex")
    pr.set_defaults(func=cmd_predict)
    ev = sub.add_parser("ruler-eval", help="score the ruler on a blind register")
    ev.add_argument("--register", help="CSV path (default: data/registers/blind_register_v1.csv)")
    ev.set_defaults(func=cmd_ruler_eval)
    sub.add_parser("citation-space").set_defaults(func=cmd_citation_space)
    sub.add_parser("harness-demo").set_defaults(func=cmd_harness_demo)
    sub.add_parser("courtlistener-selftest").set_defaults(func=cmd_courtlistener_selftest)
    bl = sub.add_parser("blind", help="the blind protocol; pass its own arguments after 'blind'",
                        add_help=False)
    bl.add_argument("blind_args", nargs=argparse.REMAINDER)
    bl.set_defaults(func=cmd_blind)
    return p


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else list(argv)
    if argv and argv[0] == "blind":  # hand everything after 'blind' to the protocol untouched
        from .blind import protocol
        return protocol.main(argv[1:]) or 0
    parser = build_parser()
    a = parser.parse_args(argv)
    if not getattr(a, "command", None):
        parser.print_help()
        return 0
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
