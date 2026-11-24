"""Disposition (tenor) classifier for Chinese appellate judgments.

Carried forward from the July 2026 blind protocol. Chinese judgments are linear
(header -> procedure -> facts -> reasoning -> disposition at the END), so the
tenor sits after 判决如下 / 裁定如下 near the end of the text. AMBIGUOUS means a
person must read it; never score an AMBIGUOUS result automatically.
"""
from __future__ import annotations

import re
from typing import Tuple

CN_AFFIRM = ("驳回上诉,维持原判", "驳回上诉，维持原判", "维持原判", "维持原裁定", "驳回再审申请")
CN_REVERSE = ("发回重审", "撤销原判", "撤销一审", "撤销原裁定")
CN_MODIFY = ("改判",)

_TENOR = re.compile(r"(判决如下|裁定如下)(.{0,600})", re.S)


def _has(keywords, text: str) -> bool:
    return any(k in text for k in keywords)


def classify_cn(text: str) -> Tuple[str, str]:
    """Return ``(notch, tenor)`` from a full Chinese judgment.

    notch is CLEAN_AFFIRM, MODIFIED, REVERSED or AMBIGUOUS.
    """
    m = _TENOR.search(text[-3000:])
    tenor = m.group(0)[:400] if m else ""
    zone = tenor or text[-1500:]
    if _has(CN_MODIFY, zone) and _has(CN_AFFIRM, zone):
        return "MODIFIED", tenor
    if _has(CN_REVERSE, zone):
        return "REVERSED", tenor
    if _has(CN_MODIFY, zone):
        return "MODIFIED", tenor
    if _has(CN_AFFIRM, zone):
        return "CLEAN_AFFIRM", tenor
    return "AMBIGUOUS", tenor
