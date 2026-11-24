"""Render the catalogue into docs/UNDER_CONSIDERATION.md (between two markers)."""

from __future__ import annotations

import os
from collections import OrderedDict
from typing import List

from .catalogue import RECORDS, Record

START = "<!-- BEGIN GENERATED: python -m synthium.phenomena index --write -->"
END = "<!-- END GENERATED -->"


def _cell(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def _where(r: Record) -> str:
    parts = [p.strip() for p in r.where.split(";") if p.strip()]
    out = []
    for p in parts:
        if p.startswith(("synthium/", "archive/", "docs/", "tests/")):
            out.append(f"`{p}`")
        else:
            out.append(_cell(p))
    return "; ".join(out)


def render() -> str:
    groups: "OrderedDict[str, List[Record]]" = OrderedDict()
    for r in RECORDS:
        era = r.version.split(" (")[0]
        groups.setdefault(era, []).append(r)
    L = [START, "", f"{len(RECORDS)} entries. Every one: status **{RECORDS[0].status}**, evidence **UNTESTED** "
         "unless the earlier result column says what an earlier test found.", ""]
    for era, recs in groups.items():
        L += [f"### {era}", "",
              "| id | version | kind | phenomenon | what it says | dimensions | what it claimed | why it was set aside | earlier result | where it lives now |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for r in recs:
            src = "" if r.source == "original" else f" ({r.source})"
            L.append("| " + " | ".join([
                f"`{r.id}`", _cell(r.version), r.kind, _cell(r.phenomenon), _cell(r.statement),
                _cell(", ".join(r.dimensions)) or "-", _cell(r.claimed),
                _cell(r.set_aside) or "-", _cell(r.earlier_verdict) or "-",
                _where(r) + _cell(src),
            ]) + " |")
        L.append("")
    L.append(END)
    return "\n".join(L)


def doc_path() -> str:
    here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(here, "docs", "UNDER_CONSIDERATION.md")


def write(path: str = None) -> bool:
    """Replace the generated part of the doc. Returns True if it changed."""
    path = path or doc_path()
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    a, b = text.index(START), text.index(END) + len(END)
    new = text[:a] + render() + text[b:]
    if new != text:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new)
        return True
    return False


def in_sync(path: str = None) -> bool:
    path = path or doc_path()
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    a, b = text.index(START), text.index(END) + len(END)
    return text[a:b] == render()
