"""Tensors with upper and lower indices (restored from V4, extended to any rank).

V4's ``RealityTensor`` handled rank 1 only. Here each index is marked ``'u'`` (upper,
contravariant, moves like a step dx) or ``'d'`` (lower, covariant, moves like a slope
d/dx), and any index can be raised with g^ij or lowered with g_ij.

Example: a case's position is a rank-1 upper tensor; the spread of cases (covariance)
is a rank-2 upper tensor; the metric is a rank-2 lower tensor.
"""

from __future__ import annotations

import string

import numpy as np


class RealityTensor:
    def __init__(self, components, indices: str = "u"):
        components = np.asarray(components, float)
        if components.ndim != len(indices) or set(indices) - {"u", "d"}:
            raise ValueError("indices must be a string of 'u'/'d', one per axis")
        self.components = components
        self.indices = indices

    @property
    def rank(self) -> int:
        return self.components.ndim

    # V4 names kept: a rank-1 tensor is 'contravariant' (u) or 'covariant' (d).
    @property
    def index_type(self) -> str:
        if self.rank == 1:
            return "contravariant" if self.indices == "u" else "covariant"
        return self.indices

    def _move(self, axis: int, matrix: np.ndarray, new: str) -> "RealityTensor":
        letters = string.ascii_lowercase[: self.rank]
        src = letters
        dst = letters[:axis] + "z" + letters[axis + 1 :]
        comps = np.einsum(f"z{letters[axis]},{src}->{dst}", matrix, self.components)
        idx = self.indices[:axis] + new + self.indices[axis + 1 :]
        return RealityTensor(comps, idx)

    def lower_index(self, metric: np.ndarray, axis: int = 0) -> "RealityTensor":
        if self.indices[axis] == "d":
            return self
        return self._move(axis, np.asarray(metric, float), "d")

    def raise_index(self, metric_inv: np.ndarray, axis: int = 0) -> "RealityTensor":
        if self.indices[axis] == "u":
            return self
        return self._move(axis, np.asarray(metric_inv, float), "u")

    def inner_product(self, other: "RealityTensor", metric: np.ndarray) -> float:
        """<v, w> = g_ij v^i w^j for two rank-1 tensors, whatever their index type."""
        if self.rank != 1 or other.rank != 1:
            raise ValueError("inner_product is for rank-1 tensors")
        metric = np.asarray(metric, float)
        v = self.raise_index(np.linalg.inv(metric))
        w = other.lower_index(metric)
        return float(v.components @ w.components)

    def contract(self, axis_a: int = 0, axis_b: int = 1) -> "RealityTensor":
        """Sum over one upper and one lower index (the trace)."""
        if {self.indices[axis_a], self.indices[axis_b]} != {"u", "d"}:
            raise ValueError("contract one upper with one lower index")
        comps = np.trace(self.components, axis1=axis_a, axis2=axis_b)
        idx = "".join(c for i, c in enumerate(self.indices) if i not in (axis_a, axis_b))
        return RealityTensor(comps, idx)

    def __float__(self) -> float:
        if self.rank != 0:
            raise TypeError("only a fully contracted tensor is a number")
        return float(self.components)

    def tensor_product(self, other: "RealityTensor") -> "RealityTensor":
        return RealityTensor(
            np.multiply.outer(self.components, other.components),
            self.indices + other.indices,
        )

    def __repr__(self) -> str:
        return f"RealityTensor(indices='{self.indices}', shape={self.components.shape})"
