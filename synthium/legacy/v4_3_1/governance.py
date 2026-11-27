from __future__ import annotations
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Dict, List, Optional
import numpy as np
from .confidence import Confidence

class ActionLevel(IntEnum):
    ALLOW = 1
    WATCH = 2
    SHADOW_OBSERVE = 3
    COLLECT_EVIDENCE = 4
    STEP_UP_AUTH = 5
    SESSION_REVERIFY = 6
    QUEUE_REVIEW = 7
    HUMAN_REVIEW = 8
    BLOCK = 9
    PRIVILEGE_FREEZE = 10
    RMA_CONTAINMENT = 11

@dataclass
class GovernanceDecision:
    action: ActionLevel
    applied_friction_coefficient: float
    justification: str
    risk_score: float
    recommended_review_window: int = 0

@dataclass
class GovernanceState:
    last_action: ActionLevel = ActionLevel.ALLOW
    consecutive_high_risk: int = 0
    history: List[float] = field(default_factory=list)

class GovernanceEngine:
    def __init__(self, chaos_threshold: float = 1e6, hysteresis_margin: float = 0.15, history_window: int = 5):
        self.chaos_threshold = chaos_threshold
        self.hysteresis_margin = hysteresis_margin
        self.history_window = history_window
        self.state = GovernanceState()

    def evaluate_trajectory(self, derivatives: Dict[int, float], fusion_score: float, derivative_uncertainty: Optional[Dict[int, float]] = None, confidence: Optional[Confidence] = None) -> GovernanceDecision:
        derivative_uncertainty = derivative_uncertainty or {}
        pop = abs(derivatives.get(6, 0.0))
        velocity = abs(derivatives.get(1, 0.0))
        uncertainty_penalty = min(1.0, derivative_uncertainty.get(6, 0.0) / (abs(pop) + 1e-9)) if pop != 0 else 0.0
        conf_penalty = 0.0 if confidence is None else (1.0 - confidence.decayed_score())
        trend_term = self._update_history(pop)
        incoherence = 1.0 - max(0.0, min(1.0, fusion_score))

        risk_score = (
            0.45 * min(1.0, pop / self.chaos_threshold)
            + 0.15 * min(1.0, velocity / 10.0)
            + 0.20 * incoherence
            + 0.10 * uncertainty_penalty
            + 0.10 * conf_penalty
        )
        risk_score = min(1.0, risk_score + 0.1 * trend_term)

        proposed = self._risk_to_action(risk_score)
        action = self._apply_hysteresis(proposed, risk_score)
        if risk_score >= 0.75:
            self.state.consecutive_high_risk += 1
        else:
            self.state.consecutive_high_risk = 0
        action = self._escalate_for_persistence(action)
        self.state.last_action = action

        friction = min(1.0, (action.value - 1) / 10.0)
        review_window = max(1, int(10 * (1.0 - risk_score))) if action.value >= ActionLevel.COLLECT_EVIDENCE else 0
        justification = (
            f"risk={risk_score:.3f}, pop={pop:.2e}, velocity={velocity:.2f}, "
            f"fusion={fusion_score:.3f}, uncertainty_penalty={uncertainty_penalty:.3f}, "
            f"confidence_penalty={conf_penalty:.3f}, trend={trend_term:.3f}"
        )
        return GovernanceDecision(action, friction, justification, risk_score, review_window)

    def _update_history(self, pop: float) -> float:
        norm_pop = min(1.0, abs(pop) / self.chaos_threshold)
        self.state.history.append(norm_pop)
        self.state.history = self.state.history[-self.history_window :]
        if len(self.state.history) < 2:
            return norm_pop
        diffs = np.diff(self.state.history)
        upward = np.mean(np.maximum(diffs, 0.0))
        return float(min(1.0, upward + np.mean(self.state.history)))

    def _risk_to_action(self, risk: float) -> ActionLevel:
        if risk >= 0.98:
            return ActionLevel.RMA_CONTAINMENT
        if risk >= 0.90:
            return ActionLevel.PRIVILEGE_FREEZE
        if risk >= 0.82:
            return ActionLevel.BLOCK
        if risk >= 0.72:
            return ActionLevel.HUMAN_REVIEW
        if risk >= 0.62:
            return ActionLevel.QUEUE_REVIEW
        if risk >= 0.52:
            return ActionLevel.SESSION_REVERIFY
        if risk >= 0.42:
            return ActionLevel.STEP_UP_AUTH
        if risk >= 0.32:
            return ActionLevel.COLLECT_EVIDENCE
        if risk >= 0.22:
            return ActionLevel.SHADOW_OBSERVE
        if risk >= 0.12:
            return ActionLevel.WATCH
        return ActionLevel.ALLOW

    def _apply_hysteresis(self, proposed: ActionLevel, risk: float) -> ActionLevel:
        last = self.state.last_action
        if proposed.value < last.value and risk > max(0.0, (last.value - 1) / 10.0 - self.hysteresis_margin):
            return last
        return proposed

    def _escalate_for_persistence(self, action: ActionLevel) -> ActionLevel:
        if self.state.consecutive_high_risk >= 3 and action.value < ActionLevel.HUMAN_REVIEW:
            return ActionLevel.HUMAN_REVIEW
        if self.state.consecutive_high_risk >= 5 and action.value < ActionLevel.BLOCK:
            return ActionLevel.BLOCK
        return action
