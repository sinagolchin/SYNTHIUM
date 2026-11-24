"""Judicial domain.

The project's core result as software: the T/P/L ruler (ruler.py), earned from the
blind register and structurally confirmed across 11 legal systems, plus the frozen
fitted movement-probability models. citation_space.py is an experimental
objective-substrate layer.
"""
from .ruler import (Category, CourtLevel, EvalResult, Layer, Notch, Posture, Prediction,
                    evaluate, fitted_params, movement_potential, predict, predict_p,
                    predict_p_v2)
from . import citation_space

__all__ = ["Category", "CourtLevel", "EvalResult", "Layer", "Notch", "Posture", "Prediction",
           "evaluate", "fitted_params", "movement_potential", "predict", "predict_p",
           "predict_p_v2", "citation_space"]
