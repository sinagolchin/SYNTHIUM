"""Synthium command line.

    python -m synthium spec                  show the judicial spec (PROPOSED)
    python -m synthium atlas                 atlas stats + cluster->outcome leakage
    python -m synthium coefficients          list every ungrounded formula constant
    python -m synthium atlas-validate        run the rubric-imitation smoke test
    python -m synthium requirements          what predictive validity would require
    python -m synthium harness-demo          VALIDATED vs FALSIFIED on synthetic data
    python -m synthium courtlistener-selftest  offline extractor self-test
    python -m synthium build-dataset --max N --out cases.jsonl   (needs token)
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import List


def _rule(title: str) -> None:
    print("=" * 70)
    print(f" {title}")
    print("=" * 70)


def cmd_spec(_args) -> int:
    from .domains.judicial import summarize_spec, UNIT_DEFINITIONS
    _rule("Judicial Module v0.2 -- PROPOSED")
    spec = summarize_spec()
    print(f"status        : {spec['status']}")
    print(f"units         : {spec['n_units']} ({', '.join(spec['extended_units'])})")
    print(f"operators     : {spec['n_operators']}")
    print("\nformula hierarchy:")
    for line in spec["formulas"]:
        print(f"  {line}")
    print("\nNB: 'coder_confidence' tags below are qualitative coder notes, NOT")
    print("    evidence of predictive validity.")
    for key in spec["extended_units"]:
        u = UNIT_DEFINITIONS[key]
        print(f"  {u.key:6s} {u.name:34s} [{u.coder_confidence}]")
    return 0


def cmd_atlas(_args) -> int:
    from .data.atlas import load_atlas, outcome_distribution, cluster_outcome_leakage
    _rule("Atlas -- 44 rubric-coded case studies (NOT a statistical sample)")
    cases = load_atlas()
    print(f"cases: {len(cases)}")
    print(f"outcome distribution: {outcome_distribution(cases)}")
    print("\ncluster -> outcome leakage (why cluster must stay out of features):")
    leak = cluster_outcome_leakage(cases)
    deterministic = [(c, d) for c, d in leak.items() if len(d) == 1 and sum(d.values()) > 1]
    for cluster, dist in sorted(deterministic, key=lambda kv: -sum(kv[1].values())):
        only = next(iter(dist))
        print(f"  {cluster:28s} {sum(dist.values()):2d} cases -> {only} (100%)")
    print(f"\n{len(leak)} distinct clusters across {len(cases)} cases; knowing the")
    print("cluster essentially tells you the outcome. That is leakage, not signal.")
    return 0


def cmd_coefficients(_args) -> int:
    from .domains.judicial import ungrounded_coefficients
    _rule("Ungrounded coefficients in the suppression formula")
    coeffs = ungrounded_coefficients()
    print(f"{len(coeffs)} hand-chosen constants, none fit or derived:\n")
    for c in coeffs:
        print(f"  {c.name:20s} = {c.value:<5} grounded={c.grounded}  ({c.note})")
    print("\nEvery one is a hypothesis. Promoting any requires estimating it from")
    print("data with a confidence interval, then flipping its grounded flag.")
    return 0


def cmd_atlas_validate(_args) -> int:
    from .domains.judicial import validate_against_atlas
    _rule("Rubric-imitation smoke test (atlas outcome as target)")
    verdict, caveat = validate_against_atlas(threshold=0.5)
    print(verdict.explain())
    print("\n" + caveat)
    return 0


def cmd_requirements(_args) -> int:
    from .domains.judicial import predictive_validity_requirements
    _rule("What predictive validity would actually require")
    for i, req in enumerate(predictive_validity_requirements(), 1):
        print(f"  {i}. {req}")
    return 0


def cmd_harness_demo(_args) -> int:
    import random
    from .core import (PredictiveModel, ValidationProtocol, accuracy,
                       majority_class_baseline, validate, NotValidatedError)
    _rule("Predictive harness demo -- reality judges, the framework reports")
    rng = random.Random(0)

    def make(has_signal: bool):
        present = rng.random() < 0.5
        text = ("warrant " if present else "") + " ".join(
            rng.choice(["search", "home", "vehicle", "phone", "consent"]) for _ in range(5))
        if has_signal:
            label = "DENIED" if present else "GRANTED"
        else:
            label = rng.choice(["DENIED", "GRANTED"])
        return {"text": text}, label

    def split(has_signal, n):
        d = [make(has_signal) for _ in range(n)]
        return [x[0] for x in d], [x[1] for x in d]

    def model_fn(f):
        return "DENIED" if "warrant" in f["text"] else "GRANTED"

    for tag, has_signal in (("real signal present", True), ("no signal", False)):
        tr_f, tr_y = split(has_signal, 80)
        te_f, te_y = split(has_signal, 80)
        proto = ValidationProtocol("accuracy", accuracy,
                                   majority_class_baseline(tr_y), required_margin=0.10)
        m = PredictiveModel("warrant-reader", model_fn)
        v = validate(m, proto, te_f, te_y)
        print(f"\n{tag}:")
        print("  " + v.explain())
        try:
            m.assert_validated()
            print("  assert_validated(): passed -- usable for claims.")
        except NotValidatedError:
            print("  assert_validated(): refused -- model stays PROPOSED/FALSIFIED.")
    return 0


def cmd_courtlistener_selftest(_args) -> int:
    from .data.courtlistener import run_self_test
    return 0 if run_self_test() else 1


def cmd_build_dataset(args) -> int:
    from .data.courtlistener import (CourtListenerV4Client, SUPPRESSION_QUERIES,
                                     build_dataset, write_jsonl, label_distribution)
    client = CourtListenerV4Client()
    cases = build_dataset(client, SUPPRESSION_QUERIES, max_per_query=args.max,
                          fetch_full_text=not args.no_full_text)
    write_jsonl(cases, args.out)
    confident = sum(1 for c in cases if c.extractor_confident)
    print(f"Wrote {len(cases)} cases -> {args.out}")
    print(f"Label distribution: {label_distribution(cases)}")
    print(f"Extractor confident on {confident}/{len(cases)}.")
    print("\nReminder: these labels are a FIRST-PASS read of the court record. "
          "Hand-check a sample before treating them as ground truth.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="synthium", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command")
    sub.add_parser("spec").set_defaults(func=cmd_spec)
    sub.add_parser("atlas").set_defaults(func=cmd_atlas)
    sub.add_parser("coefficients").set_defaults(func=cmd_coefficients)
    sub.add_parser("atlas-validate").set_defaults(func=cmd_atlas_validate)
    sub.add_parser("requirements").set_defaults(func=cmd_requirements)
    sub.add_parser("harness-demo").set_defaults(func=cmd_harness_demo)
    sub.add_parser("courtlistener-selftest").set_defaults(func=cmd_courtlistener_selftest)
    b = sub.add_parser("build-dataset")
    b.add_argument("--max", type=int, default=20)
    b.add_argument("--out", type=str, default="synthium_cases.jsonl")
    b.add_argument("--no-full-text", action="store_true")
    b.set_defaults(func=cmd_build_dataset)
    return p


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
