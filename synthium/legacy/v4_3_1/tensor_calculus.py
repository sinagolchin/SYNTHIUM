from __future__ import annotations
import numpy as np

class RealityTensor:
    def __init__(self, data: np.ndarray, tensor_type: str = "contravariant"):
        arr = np.asarray(data, dtype=float)
        if arr.ndim != 1:
            raise ValueError("RealityTensor currently expects a rank-1 tensor (vector/covector).")
        self.data = arr
        self.tensor_type = tensor_type

    def raise_index(self, metric_inv: np.ndarray):
        if self.tensor_type == "covariant":
            self.data = np.asarray(metric_inv, dtype=float) @ self.data
            self.tensor_type = "contravariant"

    def lower_index(self, metric: np.ndarray):
        if self.tensor_type == "contravariant":
            self.data = np.asarray(metric, dtype=float) @ self.data
            self.tensor_type = "covariant"
