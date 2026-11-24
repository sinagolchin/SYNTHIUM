"""Re-evaluate every case stage by stage with every restored formula and tool.

Sina, 2026-11-24: "Because of that now we have to get back to every case we pulled. Re
evaluate them according with all these things." Each case becomes a path through six
stages (act, filing, plea or answer, trial or hearing, sentence or remedy, appeal); every
formula in the under-consideration index that can run on a stage is run, and each one's
claim is set against what happened.

EVERY RESULT IS UNTESTED AND NOT BLIND: the stage scores were made after the endings were
known. Case-level data and results stay out of this public repository.
"""

from .analyses import run_checks, quality_motion, scorer_agreement
from .formulas import STAND_INS, all_for_stage, appeal, fear, five_d
from .stages import FEAR, FIVE, STAGES, StagedCase, case_points, load_staged, stage_points

__all__ = ["run_checks", "quality_motion", "scorer_agreement", "STAND_INS", "all_for_stage", "appeal",
           "fear", "five_d", "FEAR", "FIVE", "STAGES", "StagedCase", "case_points", "load_staged",
           "stage_points"]
