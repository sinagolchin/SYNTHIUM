"""
Synthium v4.0 - Infinite Calculus
==================================

Infinite derivative chains + N-dimensional integrals
"""

import numpy as np
from typing import Callable, List, Tuple, Dict
from scipy.integrate import trapezoid


class InfiniteDerivativeChain:
    """
    Compute infinite derivative chain
    
    Position → Velocity → Acceleration → Jerk → Snap → Crackle → Pop → ...
    
    Each level reveals new patterns about dynamics
    
    Example:
        >>> chain = InfiniteDerivativeChain(position_function)
        >>> derivatives = chain.compute(t=1.0, max_order=6)
        >>> if chain.detect_chaos(): print("Chaos detected!")
    """
    
    def __init__(self, base_function: Callable, dt: float = 1e-6):
        """
        Args:
            base_function: Function of time f(t)
            dt: Step size for numerical differentiation
        """
        self.base_function = base_function
        self.dt = dt
        self.derivatives = {}
    
    def compute(self, t: float, max_order: int = 10) -> Dict[int, float]:
        """
        Compute derivative chain at time t
        
        Args:
            t: Time point
            max_order: Maximum derivative order
        
        Returns:
            dict mapping order → derivative value
            {0: position, 1: velocity, 2: acceleration, ...}
        """
        # Order 0: Position (the function itself)
        self.derivatives[0] = self.base_function(t)
        
        # Orders 1 through max_order
        current_func = self.base_function
        for order in range(1, max_order + 1):
            # Numerical derivative using central difference
            deriv = self._numerical_derivative(current_func, t)
            self.derivatives[order] = deriv
            
            # Update for next iteration
            prev_func = current_func
            current_func = lambda x, f=prev_func: self._numerical_derivative(f, x)
        
        return self.derivatives
    
    def _numerical_derivative(self, f: Callable, x: float) -> float:
        """
        Central difference: f'(x) ≈ (f(x+h) - f(x-h)) / (2h)
        """
        try:
            return (f(x + self.dt) - f(x - self.dt)) / (2 * self.dt)
        except:
            return 0.0
    
    def interpret(self) -> Dict[str, float]:
        """
        Interpret each derivative level
        
        Returns:
            Dictionary with human-readable names
        """
        names = {
            0: "Position (state)",
            1: "Velocity (rate of change)",
            2: "Acceleration (rate of rate of change)",
            3: "Jerk (smoothness)",
            4: "Snap (abruptness)",
            5: "Crackle (volatility)",
            6: "Pop (chaos measure)",
        }
        
        interpretations = {}
        for order, value in self.derivatives.items():
            name = names.get(order, f"Derivative order {order}")
            interpretations[name] = value
        
        return interpretations
    
    def detect_chaos(self, threshold: float = 1e6) -> bool:
        """
        Detect chaos via high-order derivatives
        
        If 6th derivative (Pop) is exploding → chaotic regime
        
        Args:
            threshold: Value above which we declare chaos
        
        Returns:
            True if chaotic behavior detected
        """
        if 6 in self.derivatives:
            return abs(self.derivatives[6]) > threshold
        return False


class NDimensionalIntegral:
    """
    N-dimensional integration
    
    1D: ∫ f(x) dx = area under curve (2D measure)
    2D: ∬ f(x,y) dxdy = volume under surface (3D measure)
    ND: ∫...∫ f(x₁,...,xₙ) dx₁...dxₙ = (N+1)D content
    
    Example:
        >>> integrator = NDimensionalIntegral()
        >>> area = integrator.integrate_1d(lambda x: x**2, 0, 1)
        >>> volume = integrator.integrate_2d(lambda x,y: x*y, (0,1), (0,1))
    """
    
    @staticmethod
    def integrate_1d(f: Callable, a: float, b: float, n_points: int = 1000) -> float:
        """
        1D integral: ∫ f(x) dx from a to b
        
        Returns area under curve
        """
        x = np.linspace(a, b, n_points)
        y = np.array([f(xi) for xi in x])
        return float(trapezoid(y, x))
    
    @staticmethod
    def integrate_2d(f: Callable, 
                     x_range: Tuple[float, float],
                     y_range: Tuple[float, float],
                     n_points: int = 100) -> float:
        """
        2D integral: ∬ f(x,y) dxdy (Monte Carlo)
        
        Returns volume under surface
        """
        n_samples = n_points ** 2
        x_samples = np.random.uniform(*x_range, n_samples)
        y_samples = np.random.uniform(*y_range, n_samples)
        
        values = np.array([f(x, y) for x, y in zip(x_samples, y_samples)])
        
        # Volume of integration box
        box_volume = (x_range[1] - x_range[0]) * (y_range[1] - y_range[0])
        
        return float(box_volume * np.mean(values))
    
    @staticmethod
    def integrate_nd(f: Callable, ranges: List[Tuple[float, float]],
                     n_samples: int = 10000) -> float:
        """
        N-dimensional integral (Monte Carlo)
        
        ∫...∫ f(x₁,...,xₙ) dx₁...dxₙ
        
        Args:
            f: Function taking array of length N
            ranges: List of (min, max) for each dimension
            n_samples: Number of Monte Carlo samples
        
        Returns:
            (N+1)-dimensional content
        """
        n_dims = len(ranges)
        
        # Generate random samples in N-D box
        samples = np.random.uniform(
            low=[r[0] for r in ranges],
            high=[r[1] for r in ranges],
            size=(n_samples, n_dims)
        )
        
        # Evaluate function at each sample point
        values = np.array([f(sample) for sample in samples])
        
        # Volume of N-D box
        box_volume = np.prod([r[1] - r[0] for r in ranges])
        
        return float(box_volume * np.mean(values))
    
    @staticmethod
    def interpret(n_dims: int) -> str:
        """
        What does N-D integral mean?
        
        Returns human-readable interpretation
        """
        if n_dims == 1:
            return "Area under curve (2D measure)"
        elif n_dims == 2:
            return "Volume under surface (3D measure)"
        elif n_dims == 3:
            return "Hypervolume (4D measure)"
        else:
            return f"{n_dims+1}-dimensional content beneath {n_dims}D hypersurface"


def integrate_along_path(f: Callable, path: np.ndarray) -> float:
    """
    Integrate function along a path
    
    ∫_path f(x) ds
    
    Args:
        f: Function to integrate
        path: Array of shape (n_points, dim) representing path
    
    Returns:
        Line integral value
    
    Example:
        >>> path = geodesic.points  # From manifold
        >>> integral = integrate_along_path(energy_function, path)
    """
    # Evaluate function at each point
    values = np.array([f(point) for point in path])
    
    # Compute path segment lengths
    segments = np.linalg.norm(np.diff(path, axis=0), axis=1)
    
    # Trapezoidal integration
    integral = np.sum((values[:-1] + values[1:]) / 2 * segments)
    
    return float(integral)
