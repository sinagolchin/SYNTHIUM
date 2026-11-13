"""Blind-protocol tooling.

  protocol  seal -> blind -> commit -> reveal -> record, with a hash-chained log
  classify  reads the disposition (tenor) of a Chinese judgment into a notch
"""
from .classify import classify_cn

__all__ = ["classify_cn"]
