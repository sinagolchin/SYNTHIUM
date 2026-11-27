"""
Synthium v4.0 - Applications
=============================

Real-world applications: trading, communication optimization, etc.
"""

import numpy as np
from typing import Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class TradingDecision:
    """Trading decision with full uncertainty"""
    risk_point: float
    risk_pessimistic: float
    risk_optimistic: float
    contracts_point: int
    contracts_pessimistic: int
    contracts_optimistic: int
    sustainability_E: float
    chaos_detected: bool
    confidence: str
    warnings: list
    
    def __str__(self):
        s = ["\n" + "="*70]
        s.append("SYNTHIUM TRADING DECISION (v4.0)")
        s.append("="*70)
        s.append(f"\nPosition Size:")
        s.append(f"  Point:        {self.contracts_point} contracts (${self.risk_point:.2f})")
        s.append(f"  Conservative: {self.contracts_pessimistic} contracts (${self.risk_pessimistic:.2f})")
        s.append(f"  Aggressive:   {self.contracts_optimistic} contracts (${self.risk_optimistic:.2f})")
        s.append(f"\nSustainability (E): {self.sustainability_E:.3f}")
        s.append(f"Chaos Detected: {'YES ⚠️' if self.chaos_detected else 'No'}")
        s.append(f"Confidence: {self.confidence}")
        if self.warnings:
            s.append("\nWarnings:")
            for w in self.warnings:
                s.append(f"  • {w}")
        s.append("="*70)
        return "\n".join(s)


class GoldAssistantV4:
    """
    Gold Assistant v4.0 with proper N-D mathematics
    
    Improvements over v3.4:
    - Discovers N trading dimensions (not assumes 5)
    - Uses manifold geometry
    - Detects chaos via 6th derivative
    - Provides uncertainty ranges
    
    Example:
        >>> assistant = GoldAssistantV4()
        >>> assistant.fit(trading_history)
        >>> decision = assistant.decide(...)
    """
    
    def __init__(self):
        self.manifold = None
        self.history = []
        self.discovered_dims = None
    
    def fit(self, trading_history: np.ndarray):
        """
        Learn from trading history
        
        Args:
            trading_history: (n_samples, n_features) array of past states
        """
        from sklearn.decomposition import PCA
        
        # Discover dimensions
        pca = PCA()
        pca.fit(trading_history)
        explained_var = pca.explained_variance_ratio_
        self.discovered_dims = np.sum(explained_var > 0.01)
        
        print(f"✓ Discovered {self.discovered_dims} trading dimensions (not 5!)")
        
        # Learn metric from data
        data_centered = trading_history - trading_history.mean(axis=0)
        cov = (data_centered.T @ data_centered) / len(trading_history)
        cov += np.eye(trading_history.shape[1]) * 1e-6
        
        # Create manifold
        from .manifold_geometry import RiemannianManifold
        self.manifold = RiemannianManifold(self.discovered_dims, metric=cov[:self.discovered_dims, :self.discovered_dims])
    
    def decide(self,
              account_balance: float,
              posterior_edge: float,
              edge_confidence: str,
              ewma_vol: float,
              vol_median: float,
              drawdown: float,
              entropy: float,
              daily_risk_budget: float,
              account_balance_function: Optional[callable] = None) -> Optional[TradingDecision]:
        """
        Make trading decision with v4.0 mathematics
        
        Args:
            account_balance: Current account size
            posterior_edge: Estimated edge (0-1)
            edge_confidence: 'HIGH', 'MODERATE', 'LOW', 'SPECULATIVE'
            ewma_vol: EWMA volatility (20-day)
            vol_median: Median volatility (30-day)
            drawdown: Current drawdown (0-1)
            entropy: Market entropy (0-1)
            daily_risk_budget: Daily risk budget in R multiples
            account_balance_function: Optional function for chaos detection
        
        Returns:
            TradingDecision with uncertainty ranges, or None if halted
        """
        # Base calculations
        R_value = account_balance * 0.01
        
        # Check for chaos if function provided
        chaos_detected = False
        if account_balance_function:
            from .infinite_calculus import InfiniteDerivativeChain
            chain = InfiniteDerivativeChain(account_balance_function)
            try:
                derivatives = chain.compute(t=1.0, max_order=6)
                chaos_detected = chain.detect_chaos(threshold=1e6)
            except:
                pass
        
        # Base risk (confidence-adjusted thresholds)
        if edge_confidence == 'HIGH':
            threshold_normal = 0.65
        elif edge_confidence == 'MODERATE':
            threshold_normal = 0.70
        else:
            threshold_normal = 0.75
        
        if posterior_edge >= threshold_normal:
            base_risk = 0.60 * R_value
        else:
            base_risk = 0.30 * R_value
        
        # Volatility scaler
        vol_ratio = ewma_vol / vol_median
        if vol_ratio > 1.80:
            vol_scaler = 0.30
        elif vol_ratio > 1.40:
            vol_scaler = 0.60
        else:
            vol_scaler = 1.00
        
        # Drawdown scaler
        if drawdown > 0.18:
            return None  # Halt trading
        elif drawdown > 0.12:
            dd_scaler = 0.35
        elif drawdown > 0.08:
            dd_scaler = 0.65
        else:
            dd_scaler = 1.00
        
        # Entropy penalty
        entropy_penalty = max(0, (entropy - 0.55) * 4)
        
        # Calculate sustainability (E metric)
        vol_stress = min(1.0, drawdown * 3.0 + max(0, vol_ratio - 1.0) * 0.5)
        risk_aversion = min(1.0, max(0.0, 1.0 - (daily_risk_budget / 5.0)))
        E = 1.0 - (vol_stress * risk_aversion + entropy)
        E = max(0, min(1, E))
        
        # Three scenarios: pessimistic, point, optimistic
        risk_point = base_risk * vol_scaler * dd_scaler * (1 - entropy_penalty)
        risk_point = min(risk_point, daily_risk_budget * R_value)
        
        risk_pessimistic = risk_point * 0.5
        risk_optimistic = risk_point * 1.3
        
        # Convert to contracts (assuming $125 per contract)
        contracts_point = int(risk_point // 125)
        contracts_pessimistic = int(risk_pessimistic // 125)
        contracts_optimistic = int(risk_optimistic // 125)
        
        # Warnings
        warnings = []
        if E < 0.3:
            warnings.append("Low sustainability (E < 0.3) - consider reducing exposure")
        if chaos_detected:
            warnings.append("CHAOS DETECTED (6th derivative exploding) - extreme caution advised")
        if entropy > 0.7:
            warnings.append("High market entropy - reduced predictability")
        if edge_confidence in ['LOW', 'SPECULATIVE']:
            warnings.append(f"Low confidence in edge ({edge_confidence})")
        if vol_ratio > 1.5:
            warnings.append(f"Elevated volatility ({vol_ratio:.1f}x median)")
        
        # If chaos detected, force very conservative
        if chaos_detected:
            contracts_point = min(1, contracts_point)
            contracts_optimistic = 1
        
        decision = TradingDecision(
            risk_point=risk_point,
            risk_pessimistic=risk_pessimistic,
            risk_optimistic=risk_optimistic,
            contracts_point=max(0, contracts_point),
            contracts_pessimistic=max(0, contracts_pessimistic),
            contracts_optimistic=max(0, contracts_optimistic),
            sustainability_E=E,
            chaos_detected=chaos_detected,
            confidence=edge_confidence,
            warnings=warnings
        )
        
        self.history.append(decision)
        return decision


class CommunicationOptimizer:
    """
    Optimize communication using Synthium v4.0
    
    Maps text to state on communication manifold
    Finds geodesic to optimal state
    
    Example:
        >>> optimizer = CommunicationOptimizer(dimension=10)
        >>> result = optimizer.optimize_text(text_features, target_E=0.7)
    """
    
    def __init__(self, dimension: int = 10):
        """
        Args:
            dimension: Dimensionality of communication space
        """
        self.dim = dimension
        from .manifold_geometry import RiemannianManifold
        self.manifold = RiemannianManifold(dimension)
    
    def optimize_text(self, text_features: np.ndarray,
                     target_E: float = 0.7) -> Dict:
        """
        Optimize text features
        
        Args:
            text_features: Current text as feature vector
            target_E: Target enjoyment/receptivity
        
        Returns:
            Dict with optimization results
        """
        from .reality_state import RealityState
        
        # Ensure correct dimension
        if len(text_features) < self.dim:
            text_features = np.pad(text_features, (0, self.dim - len(text_features)))
        elif len(text_features) > self.dim:
            text_features = text_features[:self.dim]
        
        # Current state
        current_state = RealityState(text_features, self.manifold)
        
        # Find optimal (simplified: move toward zero stress)
        optimal_features = text_features * 0.5  # Reduce intensity
        optimal_state = RealityState(optimal_features, self.manifold)
        
        # Geodesic path
        path = self.manifold.geodesic(current_state.coordinates, optimal_state.coordinates)
        
        return {
            'current_E': current_state.enjoyment,
            'optimal_E': optimal_state.enjoyment,
            'improvement': optimal_state.enjoyment - current_state.enjoyment,
            'path': path,
            'distance': current_state.distance_to(optimal_state)
        }
