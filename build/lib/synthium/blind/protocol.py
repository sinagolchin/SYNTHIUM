#!/usr/bin/env python3
"""
synthium.blind.protocol — mechanical blinding for Synthium case coding.

Rebuilt 2026-11-10 from the roadmap's description. The July 13 original (a smaller
commit/reveal log for Chinese judgments) was later recovered from the old project;
its tenor classifier lives on in synthium.blind.classify, and its log is kept as
data in data/blind_log_2026-07/.

Run it as `python -m synthium blind <command> ...` (same commands as below).

Goal: the disposition of an appellate decision is removed BY CODE before any text
reaches the coding model's context. The coder sees only the blinded part, commits a
prediction (timestamped, hash-chained), and only then can the tail be revealed.

Flow
----
  courier-prompt  -> prints a prompt for a courier subagent (separate context) that
                     fetches the document via an MCP connector and replies only "DONE".
  ingest          -> pulls that tool result from the courier's transcript on disk,
                     seals the full text (never printed), then runs `blind`.
  seal-file / fetch -> alternative intake: a local file, or direct HTTP (when the
                     sandbox's egress allows the host).
  blind           -> cuts the disposition, strips outcome headnotes, redacts
                     outcome sentences, prints ONLY the blinded part, logs hashes.
  commit          -> appends the prediction to the append-only, hash-chained log.
  reveal          -> prints the sealed tail + redacted sentences, ONLY if a commit
                     exists after the last blind for that case.
  record          -> logs the actual coding and scores it against the commit.
  status / verify -> per-case state; chain + sealed-file integrity check.

Honest limit: this is enforcement against accident, not against a determined reader.
Anything with shell access can `cat` the sealed file. What the tool guarantees is
that the default path never shows the disposition, and that the log proves the
order of events (sealed hash -> commit -> reveal) and detects later edits.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import glob
import hashlib
import html
import json
import os
import re
import secrets
import stat
import sys
import urllib.request
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Optional, Tuple

VERSION = "2.0.0"
DEFAULT_HOME = Path(os.environ.get("BLIND_HOME", "/mnt/project-files/synthium/blind"))
GENESIS = "0" * 64

# --------------------------------------------------------------------------- text


class _Stripper(HTMLParser):
    BLOCK = {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr",
             "blockquote", "pre", "section", "article", "center", "table"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out: List[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
        elif tag in self.BLOCK:
            self.out.append("\n\n" if tag != "br" else "\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip = max(0, self._skip - 1)
        elif tag in self.BLOCK:
            self.out.append("\n\n")

    def handle_data(self, data):
        if not self._skip:
            self.out.append(data)


def normalize(text: str) -> str:
    """HTML -> text when it looks like HTML; normalise whitespace, keep paragraphs."""
    if re.search(r"<(p|div|br|span|a|pre|html)\b", text[:20000], re.I):
        s = _Stripper()
        s.feed(text)
        text = "".join(s.out)
    text = html.unescape(text).replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace(" ", " ")
    text = re.sub(r"[ \t\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def detect_kind(text: str) -> str:
    cjk = len(re.findall(r"[一-鿿]", text[:20000]))
    kana = len(re.findall(r"[぀-ヿ]", text[:20000]))
    if kana > 50 and "主文" in text and "理由" in text:
        return "jp"
    if cjk > 200 and re.search(r"(判决|裁定|决定)如下|本院认为|审理查明", text):
        return "cn"
    return "common"


def _paragraph_starts(text: str) -> List[int]:
    starts = [0]
    for m in re.finditer(r"\n", text):
        starts.append(m.end())
    return starts


def _para_start_before(text: str, idx: int) -> int:
    j = text.rfind("\n", 0, idx)
    return 0 if j < 0 else j + 1


# ----------------------------------------------------------------- outcome patterns

V_ACT = (r"(?:affirm|reverse|vacate|remand|allow|dismiss|grant|deny|set\s+aside|quash|"
         r"uphold|refuse|reinstate|modify|overturn|restore)")
V_PASS = (r"(?:affirmed|reversed|vacated|remanded|allowed|dismissed|granted|denied|"
          r"set\s+aside|quashed|upheld|refused|reinstated|modified|overturned|restored)")

# STRONG = this court stating its own disposition. Redacted from the shown text.
STRONG_EN = [
    re.compile(r"\b(?:we|I)\s+(?:would\s+|therefore\s+|accordingly\s+|thus\s+|now\s+|must\s+|"
               r"shall\s+|will\s+|hereby\s+|respectfully\s+)*" + V_ACT + r"(?:s|ed)?\b", re.I),
    re.compile(r"\b(?:this|the)\s+Court\b(?!\s+of\b)(?:\s+\w+){0,2}?\s+(?:therefore\s+|accordingly\s+|hereby\s+)?"
               + V_ACT + r"s\b"),
    re.compile(r"\b(?:the|this|her|his|their|its)\s+(?:appeals?|cross-appeals?|petitions?(?:\s+for\s+\w+)?|"
               r"applications?|motions?)\s+(?:is|are|must\s+be|should\s+be|will\s+be|be|stands?)\s+"
               r"(?:hereby\s+|therefore\s+|accordingly\s+|accordingly\s+)?(?:" + V_PASS + r"|"
               r"allowed\s+in\s+part|dismissed\s+in\s+part)\b", re.I),
    re.compile(r"\b(?:judgment|order|decision|conviction|sentence|ruling|determination|award)s?\b[^.;\n]{0,90}?"
               r"\b(?:is|are)\s+(?:hereby\s+|therefore\s+|accordingly\s+)?" + V_PASS + r"\b", re.I),
    re.compile(r"\bso\s+ordered\b", re.I),
    re.compile(r"\b(?:we|I|this\s+Court)\s+(?:will|would|do|does|shall|must|can|cannot|could)\s*(?:not|n't)?\s+"
               r"(?:not\s+)?(?:set\s+aside|disturb|reverse|vacate|overturn|interfere\s+with|upset|affirm)\b", re.I),
    re.compile(r"\b(?:we|I)\s+(?:therefore\s+|accordingly\s+)?decline\s+to\s+(?:set\s+aside|disturb|reverse|vacate|"
               r"overturn|interfere|grant|affirm)\b", re.I),
    re.compile(r"\b(?:the|this)\s+(?:appeal|petition|application|challenge|claim)s?\s+(?:therefore\s+|accordingly\s+)?"
               r"(?:fails?|succeeds?|must\s+fail|must\s+succeed)\b", re.I),
    re.compile(r"^\s*(?:the\s+)?(?:appeal|petition|application|leave)\s+(?:is\s+)?(?:allowed|dismissed|granted|"
               r"refused|denied)\b", re.I | re.M),
    re.compile(r"\b(?:petition|application)\s+for\s+review\s+(?:is\s+)?(?:granted|denied)\b(?=[^.]*\.\s*$)", re.I | re.M),
    # a bare disposition line ("REVERSED AND REMANDED.") — line-anchored so that procedural
    # history ("The court of appeals reversed and remanded ...") is not caught
    re.compile(r"^\s*(?:judgment\s+)?(?:affirmed|reversed|vacated|modified)(?:,|\s+and|\s+in\s+part)?(?:\s+(?:and\s+)?"
               r"(?:remanded|reversed|affirmed|vacated|rendered|modified)(?:\s+in\s+part)?)*\s*[.;]?\s*$", re.I | re.M),
]
# WEAK = words that often signal direction but also appear in procedural history and
# in parties' arguments. Counted and reported, never redacted.
WEAK_EN = [
    re.compile(r"\b(?:affirm|revers|vacat|remand|quash|set\s+aside|uphold|upheld)\w*", re.I),
    re.compile(r"\b(?:did\s+not\s+err|no\s+error|erred|harmless|abuse\s+of\s+discretion)\b", re.I),
    re.compile(r"\bwe\s+(?:hold|conclude|agree|disagree|are\s+(?:not\s+)?persuaded)\b", re.I),
]
STRONG_CN = [re.compile(p) for p in (
    r"维持原判", r"驳回上诉", r"发回重审", r"改判", r"撤销[^。；]{0,30}(判决|裁定|决定)", r"予以维持",
    r"(?:上诉|申诉|再审)(?:请求|理由)[^。；]{0,20}(?:成立|不能成立|不成立)", r"本院(?:予以|不予)(?:支持|采纳)",
    r"(?:判决|裁定)如下")]
WEAK_CN = [re.compile(p) for p in (r"支持", r"采纳", r"撤销", r"维持")]
STRONG_JP = [re.compile(p) for p in (
    r"論旨は(?:理由がある|理由がない|採用することができない|採用できない)", r"(?:上告|控訴|抗告)を棄却",
    r"原判決を破棄", r"差し戻", r"破棄(?:し|する|自判)", r"主文のとおり", r"是認することができ(?:る|ない)",
    r"(?:判決|決定)に(?:影響を及ぼすことが明らかな)?法令の違反がある", r"所論の違法はない")]
WEAK_JP = [re.compile(p) for p in (r"棄却", r"破棄", r"違法", r"理由がない", r"理由がある")]


def patterns_for(kind: str):
    if kind == "cn":
        return STRONG_CN, WEAK_CN
    if kind == "jp":
        return STRONG_JP, WEAK_JP
    return STRONG_EN, WEAK_EN


# ----------------------------------------------------------------- front matter

HEADNOTE_LINE = re.compile(
    r"^(?:HELD|Held|Holding|Holdings|DISPOSITION|Disposition|RESULT|Result|OUTCOME|Outcome|"
    r"Decision|DECISION|Summary|SUMMARY|Synopsis|SYNOPSIS|Headnote|HEADNOTE|Orders?|ORDERS?|"
    r"Judgment|JUDGMENT)\s*[:\-—]\s*\S.*$", re.M)
ORDERS_BLOCK_START = re.compile(
    r"^(?:JUDGMENT OF THE COURT|ORDERS?|ORDER OF THE COURT|ORDERS? MADE|THE ORDERS? OF THE COURT ARE|"
    r"DECISION|Judgment of the Court|Orders?)\s*:?\s*$", re.M)
REASONS_START = re.compile(
    r"^(?:REASONS(?: FOR JUDGMENT)?|Reasons(?: for judgment)?|REASONS OF THE COURT|JUDGMENT$|"
    r"Introduction|INTRODUCTION|Background|BACKGROUND)\b.*$", re.M)
SYLLABUS = re.compile(r"^\s*Syllabus\s*$", re.M | re.I)
OPINION_START = re.compile(r"(?:delivered the opinion of the Court|^\s*Opinion of the Court\s*$|"
                           r"^\s*OPINION\s*$|PER CURIAM)", re.M | re.I)
CN_DIGEST = re.compile(r"裁判要点[\s\S]*?(?=\n(?:相关法条|基本案情|裁判结果|裁判理由)|\Z)")
JP_SHUBUN = re.compile(r"^\s*主\s*文\s*$[\s\S]*?(?=^\s*理\s*由\s*$)", re.M)


def strip_front_matter(text: str, kind: str) -> Tuple[str, List[str]]:
    notes = []
    if kind == "cn":
        new = CN_DIGEST.sub("", text)
        if new != text:
            notes.append("cn: removed 裁判要点 digest block")
            text = new
        # 裁判结果 section of a 指导性案例 states the outcome; drop it to the next heading
        new = re.sub(r"\n裁判结果[\s\S]*?(?=\n裁判理由|\Z)", "\n", text)
        if new != text:
            notes.append("cn: removed 裁判结果 block")
            text = new
        return text, notes
    if kind == "jp":
        m = JP_SHUBUN.search(text)
        if m:
            text = text[:m.start()] + text[m.end():]
            notes.append("jp: removed 主文 block")
        else:
            notes.append("jp: no 主文 block found (WARNING)")
        return text, notes
    # common law
    lim = max(4000, int(len(text) * 0.2))
    m = SYLLABUS.search(text[:lim])
    if m:
        o = OPINION_START.search(text, m.end())
        if o:
            text = text[:m.start()] + text[_para_start_before(text, o.start()):]
            notes.append("removed syllabus block")
    lim = max(4000, int(len(text) * 0.2))
    m = ORDERS_BLOCK_START.search(text[:lim])
    if m:
        r = REASONS_START.search(text, m.end())
        if r and r.start() - m.start() < 6000:
            text = text[:m.start()] + text[r.start():]
            notes.append("removed front orders block")
    lim = max(4000, int(len(text) * 0.15))
    head, rest = text[:lim], text[lim:]
    n = len(HEADNOTE_LINE.findall(head))
    if n:
        head = HEADNOTE_LINE.sub("[HEADNOTE LINE REMOVED]", head)
        notes.append(f"removed {n} headnote/summary line(s)")
    return head + rest, notes


# ----------------------------------------------------------------- tail cut

CONCL_HEADING = re.compile(
    r"^(?:[IVXLC]+\.?|[0-9]+\.?|[A-Z]\.|\([a-z0-9]+\))?\s*(?:CONCLUSIONS?(?: AND ORDERS?| AND DISPOSITION)?|"
    r"Conclusions?(?: and orders?| and disposition)?|DISPOSITION|Disposition|DISPOSITIVE ORDER|"
    r"RESULT|Result|ORDERS?|Orders?|DECISION|Decision|Outcome|OUTCOME|Summary of (?:conclusions|decision)|"
    r"Costs and orders|Order of the Court|Summary and conclusion|Final orders?)\s*:?\s*$", re.M)
FOREGOING = re.compile(r"\b(?:for|in light of|given)\s+(?:the|these|all\s+the|all\s+of\s+the)\s+"
                       r"(?:foregoing|above|preceding|stated|aforementioned|aforesaid)?\s*reasons\b", re.I)
CONCL_OPENERS = re.compile(r"^\s*(?:In\s+conclusion|To\s+conclude|In\s+summary|In\s+sum|Accordingly|"
                           r"For\s+the(?:se)?\s+reasons|For\s+all\s+(?:these|those)\s+reasons|Conclusion)\b",
                           re.M | re.I)
CN_CUT = re.compile(r"(?:判决|裁定|决定)如下")
JP_TAIL = re.compile(r"^\s*(?:よって|以上によれば|以上のとおり|以上の次第で)", re.M)


@dataclass
class CutResult:
    kind: str
    rule: str
    cut_at: Optional[int]          # index into normalized (front-stripped) text
    head: str = ""
    tail: str = ""
    notes: List[str] = field(default_factory=list)


def find_cut(text: str, kind: str) -> CutResult:
    n = len(text)
    if kind == "cn":
        m = CN_CUT.search(text)
        if not m:
            return CutResult(kind, "cn: no 判决如下/裁定如下", None)
        # back to the start of the sentence: "依照…第X条…之规定，判决如下" names the
        # disposition article (e.g. CPL/CCP 177(1)(1) = affirm), so it must go too.
        s = max(text.rfind("。", 0, m.start()), text.rfind("\n", 0, m.start()))
        return CutResult(kind, "cn: cut at sentence containing 判决如下/裁定如下", s + 1)
    if kind == "jp":
        cands = [m.start() for m in JP_TAIL.finditer(text) if m.start() > 0.6 * n]
        if not cands:
            return CutResult(kind, "jp: no よって/以上 closing paragraph in last 40%", None)
        return CutResult(kind, "jp: cut at first よって/以上 paragraph in last 40%", _para_start_before(text, cands[0]))
    cands: List[Tuple[int, str]] = []
    for m in CONCL_HEADING.finditer(text):
        if m.start() > 0.5 * n:
            cands.append((m.start(), "conclusion/disposition heading"))
    for m in FOREGOING.finditer(text):
        if m.start() > 0.7 * n:
            cands.append((sentence_start(text, m.start()), "'for the foregoing reasons' sentence"))
    for m in CONCL_OPENERS.finditer(text):
        if m.start() > 0.75 * n:
            cands.append((m.start(), "concluding-paragraph opener"))
    for rx in STRONG_EN:
        for m in rx.finditer(text):
            if m.start() > 0.75 * n:
                cands.append((sentence_start(text, m.start()), "disposition sentence in last 25%"))
                break
    if not cands:
        return CutResult(kind, "common: no disposition marker found", None)
    pos, why = min(cands)
    return CutResult(kind, f"common: earliest of [{', '.join(sorted(set(w for _, w in cands)))}] -> {why}", pos)


# ----------------------------------------------------------------- redaction

_ABBREV = {"v", "vs", "no", "nos", "l", "c", "ch", "mass", "u.s", "s.w", "s.w.2d", "s.w.3d", "f", "f.2d", "f.3d",
           "f.4th", "supp", "inc", "co", "corp", "ltd", "dep't", "dept", "st", "mr", "mrs", "ms", "dr", "j", "jj", "cj",
           "jca", "art", "arts", "s", "ss", "sec", "para", "paras", "pp", "p", "id", "cf", "e.g", "i.e", "etc", "al",
           "app", "ct", "cir", "tex", "civ", "rem", "prac", "ann", "stat", "rev", "gen", "u.s.c", "n", "fn", "op", "cl",
           "r", "cr", "crim", "pet", "jr", "sr", "hon", "ord", "reg", "regs", "approx", "ibid", "supra", "infra", "nz",
           "ewca", "uksc", "sgca", "nzsc", "zacc", "ieca", "fca", "a.2d", "a.3d", "n.e", "n.e.2d", "n.e.3d", "s.e", "so",
           "p.2d", "p.3d", "n.w", "cal", "fla", "ill", "conn", "va", "pa", "ga", "md", "wis", "minn", "colo", "ariz"}
_HARD_END = "。！？"
_SENT_CAP = 700


def _is_sentence_end(text: str, i: int) -> bool:
    ch = text[i]
    if ch in _HARD_END:
        return True
    if ch not in ".!?":
        return False
    j = i + 1
    while j < len(text) and text[j] in "\"'”’)]":
        j += 1
    if j < len(text) and not text[j].isspace():
        return False                       # "U.S.C." "3.2" etc.
    k = j
    while k < len(text) and text[k].isspace():
        k += 1
    if k < len(text) and not (text[k].isupper() or text[k] in "\"“‘[(*" or text[k].isdigit()):
        return False                       # next word lower-case: not a sentence break
    if ch != ".":
        return True
    a = i
    while a > 0 and not text[a - 1].isspace():
        a -= 1
    tok = text[a:i].strip("(\"“‘[").lower()
    if len(tok) <= 1 or tok in _ABBREV or tok.rstrip(".") in _ABBREV:
        return False
    return True


def _sentence_bounds(text: str, idx: int) -> Tuple[int, int]:
    """Sentence around idx. Newlines are treated as soft (sources hard-wrap and break lines at
    citations), so boundaries come from punctuation plus an abbreviation guard, capped at
    _SENT_CAP characters each way."""
    a = idx
    lo = max(0, idx - _SENT_CAP)
    while a > lo and not _is_sentence_end(text, a - 1):
        a -= 1
    if a == lo and lo > 0:                 # no boundary found: cut back to a blank line if any
        bl = text.rfind("\n\n", lo, idx)
        a = bl + 2 if bl >= 0 else lo
    b = idx
    hi = min(len(text), idx + _SENT_CAP)
    while b < hi and not _is_sentence_end(text, b):
        b += 1
    return a, min(len(text), b + 1)


def sentence_start(text: str, idx: int) -> int:
    return _sentence_bounds(text, idx)[0]


_LAST_TRIGGERS: List[str] = []


def redact(text: str, strong) -> Tuple[str, List[Tuple[int, int, str]]]:
    spans = []
    for rx in strong:
        for m in rx.finditer(text):
            spans.append(_sentence_bounds(text, m.start()))
            _LAST_TRIGGERS.append(m.group(0))
    if not spans:
        return text, []
    spans.sort()
    merged = [list(spans[0])]
    for a, b in spans[1:]:
        if a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    out, removed, last = [], [], 0
    for k, (a, b) in enumerate(merged, 1):
        out.append(text[last:a])
        out.append(f"[REDACTED-OUTCOME #{k}]")
        removed.append((a, b, text[a:b]))
        last = b
    out.append(text[last:])
    return "".join(out), removed


def count_hits(text: str, rxs) -> int:
    return sum(len(rx.findall(text)) for rx in rxs)


# ----------------------------------------------------------------- facts scope

ANALYSIS_HEADING = re.compile(
    r"^(?:[IVXLC]+\.?|[0-9]+\.?|[A-Z]\.|\([a-z0-9]+\))?\s*(?:DISCUSSION|Discussion|ANALYSIS|Analysis|"
    r"LAW AND ANALYSIS|Law and analysis|Legal analysis|Our analysis|Our assessment|Assessment|Evaluation|"
    r"Consideration|Grounds of appeal|GROUNDS OF APPEAL|The issues?|THE ISSUES?|Issues?(?: on appeal)?|"
    r"ISSUES?(?: ON APPEAL)?|Standard of review|STANDARD OF REVIEW|Decision|The appeal|THE APPEAL|"
    r"Our reasons|Analysis and decision)\s*:?\s*$", re.M)


INLINE_ANALYSIS = re.compile(r"^\s*(?:[0-9]+\.\s*|[IVX]+\.\s*)?(?:Discussion|DISCUSSION|Analysis|ANALYSIS)\.\s", re.M)
BACKGROUND_HEADING = re.compile(
    r"^\s*(?:[IVX]+\.?\s*|[0-9]+\.\s*|[A-Z]\.\s*)?(?:Background|BACKGROUND|Facts|FACTS|The facts|THE FACTS|"
    r"Factual background|Factual and procedural background|FACTUAL AND PROCEDURAL BACKGROUND|"
    r"Procedural history|PROCEDURAL HISTORY)\b\.?", re.M)
ROMAN_I = re.compile(r"^\s*I\.?\s*$", re.M)
ROMAN_II = re.compile(r"^\s*II\.?\s*$", re.M)


def facts_cut(text: str, kind: str) -> Tuple[Optional[int], Optional[int], str]:
    """Return (start, end, rule) of the facts section inside the reasoning head."""
    if kind == "cn":
        a = re.search(r"经审理查明|审理查明|原审(?:判决)?认定", text)
        m = re.search(r"本院认为", text)
        return ((a.start() if a else 0), m.start(), "cn facts: 审理查明 .. 本院认为") if m else (None, None, "cn facts: no 本院认为")
    if kind == "jp":
        return None, None, "jp facts: no reliable facts/reasoning boundary; use scope=reasoning"
    lo = int(0.03 * len(text))
    bg = BACKGROUND_HEADING.search(text, lo)
    cands = []
    for rx, why in ((ANALYSIS_HEADING, "analysis heading"), (INLINE_ANALYSIS, "inline analysis heading")):
        m = rx.search(text, bg.end() if bg else lo)
        if m:
            cands.append((m.start(), f"{why} '{m.group(0).strip()[:30]}'"))
    if cands:
        end, why = min(cands)
        start = bg.start() if bg and bg.start() < end else 0
        return start, end, f"facts: {'from background heading ' if start else ''}to {why}"
    r1 = ROMAN_I.search(text)
    if r1:
        r2 = ROMAN_II.search(text, r1.end())
        if r2:
            return r1.start(), r2.start(), ("facts: Part I only (US convention: Part I = background, Part II = "
                                            "analysis); CHECK the section is background")
    return None, None, "facts: no analysis/discussion heading found"


# ----------------------------------------------------------------- blind

@dataclass
class Blinded:
    kind: str
    scope: str
    shown: str
    grade: str
    rule: str
    notes: List[str]
    redactions: List[Tuple[int, int, str]]
    strong_after: int
    weak_cues: int
    shown_frac: float
    sealed_tail: str


def blind_text(full: str, scope: str = "facts", provenance: str = "courier") -> Blinded:
    text = normalize(full)
    kind = detect_kind(text)
    text2, notes = strip_front_matter(text, kind)
    cut = find_cut(text2, kind)
    rule = cut.rule
    strong, weak = patterns_for(kind)
    if cut.cut_at is None:
        return Blinded(kind, scope, "", "no_cut", rule, notes + ["FAIL-CLOSED: nothing shown"], [], 0, 0, 0.0, text2)
    head, tail = text2[:cut.cut_at], text2[cut.cut_at:]
    if scope == "facts":
        fs, fe, frule = facts_cut(head, kind)
        rule += " | " + frule
        if fe is None:
            return Blinded(kind, scope, "", "no_cut", rule, notes + ["FAIL-CLOSED: nothing shown"], [], 0, 0, 0.0, text2)
        tail = head[:fs] + "\n[...FACTS SECTION SHOWN BEFORE COMMIT...]\n" + head[fe:] + tail
        head = head[fs:fe]
    shown, removed = redact(head, strong)
    strong_after = count_hits(shown, strong)
    weak_cues = count_hits(shown, weak)
    front = [r for r in removed if r[0] < 0.15 * max(1, len(text2))]
    if front:
        notes.append(f"{len(front)} outcome sentence(s) in the first 15% of the text (front-loaded disposition); "
                     f"reasoning direction may still be inferable -> consider scope=facts")
    if scope == "reasoning":
        notes.append("scope=reasoning shows the court's own analysis, which states its conclusions; good for "
                     "layer coding, not a blind notch test. Grade capped at uncertain_exposure; use scope=facts")
    if strong_after:
        grade = "disclosed"
    elif removed or provenance != "courier" or scope == "reasoning":
        grade = "uncertain_exposure"
    else:
        grade = "blind"
    if provenance != "courier":
        notes.append(f"provenance={provenance}: intake path not proven blind; grade capped at uncertain_exposure")
    return Blinded(kind, scope, shown, grade, rule, notes, removed, strong_after, weak_cues,
                   len(head) / max(1, len(text2)), tail)


# ----------------------------------------------------------------- store + log

def now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def safe_id(case: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,120}", case):
        raise SystemExit("case id must be [A-Za-z0-9._-], e.g. tx-2026-uatp-geter")
    return case


class Store:
    def __init__(self, home: Path):
        self.home = Path(home)
        self.sealed = self.home / "sealed"
        self.log = self.home / "blindlog.jsonl"
        self.home.mkdir(parents=True, exist_ok=True)
        self.sealed.mkdir(exist_ok=True)

    # -- log
    def entries(self) -> List[dict]:
        if not self.log.exists():
            return []
        return [json.loads(l) for l in self.log.read_text(encoding="utf-8").splitlines() if l.strip()]

    def append(self, event: str, case: str, **data) -> dict:
        prev = self.entries()
        e = {"seq": len(prev), "ts": now(), "event": event, "case": case, "tool_version": VERSION,
             "prev": prev[-1]["h"] if prev else GENESIS, **data}
        e["h"] = sha256(json.dumps(e, sort_keys=True, ensure_ascii=False))
        with open(self.log, "a", encoding="utf-8") as f:
            f.write(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n")
            f.flush()
            os.fsync(f.fileno())
        return e

    def case_events(self, case: str) -> List[dict]:
        return [e for e in self.entries() if e["case"] == case]

    # -- sealed text
    def sealed_path(self, case: str) -> Path:
        return self.sealed / f"{case}.full.txt"

    def seal(self, case: str, raw: str, provenance: str, source_ref: dict) -> dict:
        p = self.sealed_path(case)
        if p.exists():
            raise SystemExit(f"{case}: already sealed. Use a new case id; sealed texts are never overwritten.")
        p.write_text(raw, encoding="utf-8")
        os.chmod(p, stat.S_IRUSR)
        return self.append("SEAL", case, full_sha256=sha256(raw), chars=len(raw), provenance=provenance,
                           source=source_ref)

    def read_sealed(self, case: str) -> Tuple[str, dict]:
        seals = [e for e in self.case_events(case) if e["event"] == "SEAL"]
        if not seals:
            raise SystemExit(f"{case}: nothing sealed")
        raw = self.sealed_path(case).read_text(encoding="utf-8")
        if sha256(raw) != seals[-1]["full_sha256"]:
            raise SystemExit(f"{case}: SEALED FILE CHANGED since it was sealed (hash mismatch). Case is void.")
        return raw, seals[-1]


def verify_chain(entries: List[dict]) -> List[str]:
    problems, prev = [], GENESIS
    for i, e in enumerate(entries):
        body = {k: v for k, v in e.items() if k != "h"}
        if e.get("seq") != i:
            problems.append(f"line {i}: seq {e.get('seq')} out of order")
        if e.get("prev") != prev:
            problems.append(f"line {i}: prev-hash break (entry removed, inserted or reordered)")
        if sha256(json.dumps(body, sort_keys=True, ensure_ascii=False)) != e.get("h"):
            problems.append(f"line {i}: entry edited after it was written")
        prev = e.get("h")
    return problems


def case_state(events: List[dict]) -> str:
    st = "none"
    for e in events:
        ev = e["event"]
        if ev == "SEAL":
            st = "sealed"
        elif ev == "BLIND":
            st = "blinded" if st in ("sealed", "blinded") else st
        elif ev == "COMMIT" and st in ("blinded", "committed"):
            st = "committed"
        elif ev == "REVEAL" and st in ("committed", "revealed"):
            st = "revealed"
        elif ev == "RECORD" and st in ("revealed", "recorded"):
            st = "recorded"
        elif ev == "VOID":
            st = "void"
    return st


# ----------------------------------------------------------------- courier intake

COURIER_TEMPLATE = """You are a document courier for a blinded coding protocol. Do exactly this and nothing else.
Do not call any mcp__hearthbot__ tools. Do not write any files.
Protocol nonce (do not repeat it): {nonce}

1. Load the tool with ToolSearch query "select:{tool}".
2. Call {tool} with {args}.
3. {page_rule}
4. Your final reply must be exactly the single word DONE, or FAILED followed by the error message only.
   Never summarise, quote, paraphrase or characterise the document, its parties' success, its outcome,
   or any part of its text. Saying anything about the content voids the blind test."""

SOURCES = {
    "courtlistener": ("mcp__CourtListener__read_document",
                      "If the result is paginated or reports more chunks, call it again with chunk_index lists "
                      "(chunk_size 8000) until every chunk has been returned."),
    "ldh": ("mcp__Legal_Data_Hunter__get_document",
            "Always pass include_full_text true. Call it once."),
}


def courier_prompt(source: str, ref: dict, nonce: str) -> str:
    tool, page_rule = SOURCES[source]
    if source == "courtlistener":
        args = json.dumps({"opinion_id": int(ref["opinion_id"])})
    else:
        args = json.dumps({"source": ref["ldh_source"], "source_id": ref["ldh_id"], "include_full_text": True},
                          ensure_ascii=False)
    return COURIER_TEMPLATE.format(nonce=nonce, tool=tool, args=args, page_rule=page_rule)


def default_transcript_dirs() -> List[str]:
    base = os.path.expanduser("~/.claude/projects")
    return sorted(glob.glob(os.path.join(base, "*", "*", "subagents")), key=os.path.getmtime, reverse=True)


def _blocks(entry: dict):
    c = entry.get("message", {}).get("content")
    return c if isinstance(c, list) else []


def _first_user_text(lines: List[dict]) -> str:
    for d in lines:
        if d.get("type") == "user":
            c = d.get("message", {}).get("content")
            if isinstance(c, str):
                return c
            return " ".join(b.get("text", "") for b in c if isinstance(b, dict))
    return ""


def _resolve_persisted(txt: str) -> str:
    """Large tool results are saved to a tool-results file and only a preview stays in
    the transcript. Load the saved file (only from under ~/.claude/projects)."""
    m = re.match(r"\s*<persisted-output>\s*Output too large[^\n]*?saved to:\s*(\S+)", txt)
    if not m:
        return txt
    path = os.path.realpath(m.group(1))
    root = os.path.realpath(os.path.expanduser("~/.claude/projects"))
    if not path.startswith(root + os.sep):
        raise SystemExit("persisted tool output points outside ~/.claude/projects; refusing")
    data = json.load(open(path, encoding="utf-8"))
    if isinstance(data, list):
        return "".join(x.get("text", "") for x in data if isinstance(x, dict))
    return json.dumps(data) if not isinstance(data, str) else data


def extract_from_transcript(path: str, nonce: str, tool: str) -> Optional[Tuple[str, dict]]:
    """Return (raw_text, info) from the courier transcript carrying `nonce`, or None."""
    lines = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    if nonce not in _first_user_text(lines):
        return None
    uses, results, final_texts = {}, {}, []
    for d in lines:
        for b in _blocks(d):
            if b.get("type") == "tool_use":
                uses[b["id"]] = b
                if b.get("name") == "SubagentHandback":
                    final_texts.append(json.dumps(b.get("input", {})))
            elif b.get("type") == "tool_result":
                cc = b.get("content")
                txt = "".join(x.get("text", "") for x in cc) if isinstance(cc, list) else str(cc)
                results[b["tool_use_id"]] = _resolve_persisted(txt)
            elif b.get("type") == "text" and d.get("type") == "assistant":
                final_texts.append(b.get("text", ""))
    calls = [(uid, u) for uid, u in uses.items() if u.get("name") == tool and uid in results]
    if not calls:
        raise SystemExit(f"courier transcript {path}: no {tool} result found")
    chunks, full, inputs = {}, None, []
    for uid, u in calls:
        inputs.append(u.get("input"))
        try:
            j = json.loads(results[uid])
        except Exception:
            raise SystemExit("courier result is not JSON; unknown format, refusing to seal (fail closed)")
        if "chunks" in j and isinstance(j["chunks"], list):
            for ch in j["chunks"]:
                chunks[int(ch.get("chunk_index", len(chunks)))] = ch.get("text", "")
        elif "chunk_index" in j and isinstance(j.get("text"), str):
            chunks[int(j["chunk_index"])] = j["text"]
        elif isinstance(j.get("text"), str):
            full = j["text"] if full is None or len(j["text"]) > len(full) else full
            if j.get("text_truncated"):
                raise SystemExit("courier got a truncated text (text_truncated=true); re-run with full text")
        elif isinstance(j.get("document"), dict) and isinstance(j["document"].get("text"), str):
            full = j["document"]["text"]
        else:
            raise SystemExit(f"courier result has no text field (keys {sorted(j)[:12]}); refusing to seal")
    raw = full if full is not None else "".join(chunks[k] for k in sorted(chunks))
    # Only the courier's hand-back reaches the coder. It must be exactly DONE.
    handback = [t for t in final_texts if t.startswith("{")]
    if handback:
        hb_clean = all(json.loads(t).get("message", "").strip() == "DONE" for t in handback)
    else:  # older harnesses: the last assistant text is the reply
        hb_clean = bool(final_texts) and final_texts[-1].strip() == "DONE"
    return raw, {"transcript": os.path.basename(path), "calls": inputs, "handback_is_DONE": hb_clean,
                 "chunks": len(chunks) or None}


# ----------------------------------------------------------------- printing

def print_blinded(case: str, b: Blinded, out=None):
    w = (out or sys.stdout).write
    w(f"=== BLINDED TEXT: {case} | kind={b.kind} scope={b.scope} grade={b.grade} ===\n")
    w(f"rule: {b.rule}\n")
    for n in b.notes:
        w(f"note: {n}\n")
    w(f"shown {b.shown_frac:.0%} of text | redacted outcome sentences: {len(b.redactions)} | "
      f"strong hits left: {b.strong_after} | weak cues (not redacted): {b.weak_cues}\n")
    w("=" * 70 + "\n")
    w(b.shown + "\n")
    w("=" * 70 + "\n[END OF BLINDED TEXT — tail sealed until commit]\n")


# ----------------------------------------------------------------- CLI

def cmd_courier_prompt(st: Store, a):
    case = safe_id(a.case)
    if st.case_events(case):
        raise SystemExit(f"{case}: already has log entries ({case_state(st.case_events(case))}). Use a new id.")
    nonce = "BP-" + secrets.token_hex(8)
    ref = {"opinion_id": a.opinion_id} if a.source == "courtlistener" else {"ldh_source": a.ldh_source, "ldh_id": a.ldh_id}
    st.append("REQUEST", case, source=a.source, ref=ref, nonce=nonce)
    print(courier_prompt(a.source, ref, nonce))


def cmd_ingest(st: Store, a):
    case = safe_id(a.case)
    reqs = [e for e in st.case_events(case) if e["event"] == "REQUEST"]
    if not reqs:
        raise SystemExit(f"{case}: no courier REQUEST logged; run courier-prompt first")
    req = reqs[-1]
    tool = SOURCES[req["source"]][0]
    dirs = [a.transcripts] if a.transcripts else default_transcript_dirs()
    found = None
    for d in dirs:
        for p in sorted(glob.glob(os.path.join(d, "*.jsonl")), key=os.path.getmtime, reverse=True):
            r = extract_from_transcript(p, req["nonce"], tool)
            if r:
                found = r
                break
        if found:
            break
    if not found:
        raise SystemExit(f"{case}: no courier transcript carrying nonce found in {dirs}")
    raw, info = found
    # the courier must have fetched exactly what was requested
    want = req["ref"]
    for inp in info["calls"]:
        if req["source"] == "courtlistener" and int(inp.get("opinion_id", -1)) != int(want["opinion_id"]):
            raise SystemExit(f"courier fetched opinion {inp.get('opinion_id')}, not {want['opinion_id']}")
        if req["source"] == "ldh" and (inp.get("source"), inp.get("source_id")) != (want["ldh_source"], want["ldh_id"]):
            raise SystemExit("courier fetched a different LDH document than requested")
    prov = "courier" if info["handback_is_DONE"] is not False else "courier_reply_not_clean"
    st.seal(case, raw, prov, {"source": req["source"], **want, **{k: v for k, v in info.items() if k != "calls"}})
    print(f"sealed {case}: {len(raw)} chars, provenance={prov}")
    a.scope = a.scope or "facts"
    cmd_blind(st, a)


def cmd_seal_file(st: Store, a):
    case = safe_id(a.case)
    raw = Path(a.file).read_text(encoding="utf-8")
    st.seal(case, raw, a.provenance, {"file": os.path.basename(a.file)})
    print(f"sealed {case}: {len(raw)} chars from file (not printed), provenance={a.provenance}")


def cmd_fetch(st: Store, a):
    """Direct HTTP intake. Body goes straight to the sealed file; nothing is printed."""
    case = safe_id(a.case)
    url = a.url
    headers = {"User-Agent": "blindprotocol/2"}
    if a.courtlistener_opinion:
        url = (f"https://www.courtlistener.com/api/rest/v4/opinions/{int(a.courtlistener_opinion)}/"
               f"?fields=plain_text,html_with_citations,html,xml_harvard")
        tok = os.environ.get("COURTLISTENER_API_TOKEN") or os.environ.get("COURTLISTENER_TOKEN")
        if tok:
            headers["Authorization"] = f"Token {tok}"
    if not url:
        raise SystemExit("give --url or --courtlistener-opinion")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read().decode("utf-8", "replace")
    except Exception as e:
        raise SystemExit(f"fetch failed: {type(e).__name__}: {str(e)[:200]}")
    if a.courtlistener_opinion:
        j = json.loads(body)
        body = next((j[k] for k in ("html_with_citations", "plain_text", "html", "xml_harvard") if j.get(k)), "")
        if not body:
            raise SystemExit("CourtListener returned no text fields; nothing sealed")
    st.seal(case, body, "direct_http", {"url": url})
    print(f"sealed {case}: {len(body)} chars via HTTP (not printed)")
    if a.blind:
        a.scope = a.scope or "facts"
        cmd_blind(st, a)


def cmd_blind(st: Store, a):
    case = safe_id(a.case)
    evs = st.case_events(case)
    if any(e["event"] in ("REVEAL",) for e in evs):
        raise SystemExit(f"{case}: already revealed; blinding again is meaningless")
    raw, seal = st.read_sealed(case)
    b = blind_text(raw, a.scope, "courier" if seal["provenance"] == "courier" else seal["provenance"])
    st.append("BLIND", case, scope=b.scope, kind=b.kind, grade=b.grade, rule=b.rule, notes=b.notes,
              shown_sha256=sha256(b.shown), shown_chars=len(b.shown), shown_frac=round(b.shown_frac, 4),
              redactions=len(b.redactions), weak_cues=b.weak_cues, full_sha256=seal["full_sha256"])
    print_blinded(case, b)


def cmd_commit(st: Store, a):
    case = safe_id(a.case)
    evs = st.case_events(case)
    s = case_state(evs)
    if s not in ("blinded",):
        raise SystemExit(f"{case}: state is '{s}'; commit needs a BLIND first and only one commit per blind")
    pred = json.loads(a.prediction)
    if not isinstance(pred, dict) or not pred:
        raise SystemExit("--prediction must be a JSON object, e.g. '{\"layer\":\"pure_law\",\"notch\":\"REVERSED\"}'")
    last_blind = [e for e in evs if e["event"] == "BLIND"][-1]
    e = st.append("COMMIT", case, prediction=pred, prior_exposure=a.prior_exposure, rationale=a.rationale or "",
                  blind_seq=last_blind["seq"], full_sha256=last_blind["full_sha256"])
    print(f"committed {case} at {e['ts']} (entry {e['seq']}, hash {e['h'][:16]})")


def cmd_reveal(st: Store, a):
    case = safe_id(a.case)
    evs = st.case_events(case)
    if case_state(evs) not in ("committed", "revealed", "recorded"):
        raise SystemExit(f"{case}: REFUSED. No commit logged after the blind (state '{case_state(evs)}').")
    raw, seal = st.read_sealed(case)
    last_blind = [e for e in evs if e["event"] == "BLIND"][-1]
    b = blind_text(raw, last_blind["scope"], "courier" if seal["provenance"] == "courier" else seal["provenance"])
    mismatch = sha256(b.shown) != last_blind["shown_sha256"]
    if mismatch and not a.allow_tool_change:
        raise SystemExit(f"{case}: the blinded text no longer reproduces (tool version {VERSION} vs "
                         f"{last_blind.get('tool_version')} at blind time). Re-run with --allow-tool-change to reveal "
                         f"anyway; the mismatch is logged.")
    st.append("REVEAL", case, tail_sha256=sha256(b.sealed_tail), tail_chars=len(b.sealed_tail),
              blind_reproduced=not mismatch)
    print(f"=== REVEAL: {case} ===")
    for k, (_, _, s) in enumerate(b.redactions, 1):
        print(f"[REDACTED-OUTCOME #{k}] {s.strip()}")
    print("=" * 70)
    print(b.sealed_tail)


def cmd_record(st: Store, a):
    case = safe_id(a.case)
    evs = st.case_events(case)
    if case_state(evs) not in ("revealed", "recorded"):
        raise SystemExit(f"{case}: record needs a REVEAL first")
    actual = json.loads(a.actual)
    commit = [e for e in evs if e["event"] == "COMMIT"][-1]
    pred = commit["prediction"]
    score = {k: (pred.get(k) == actual.get(k)) for k in pred if k in actual}
    blind = [e for e in evs if e["event"] == "BLIND"][-1]
    grade = blind["grade"]
    if commit.get("prior_exposure", "none") not in ("none", "case_name_only") and grade == "blind":
        grade = "uncertain_exposure"
    e = st.append("RECORD", case, actual=actual, score=score, final_grade=grade, note=a.note or "")
    print(json.dumps({"case": case, "prediction": pred, "actual": actual, "score": score, "grade": grade,
                      "committed_at": commit["ts"], "recorded_at": e["ts"]}, indent=2, ensure_ascii=False))


def cmd_void(st: Store, a):
    case = safe_id(a.case)
    st.append("VOID", case, reason=a.reason)
    print(f"{case}: VOID logged")


def cmd_status(st: Store, a):
    cases = {}
    for e in st.entries():
        cases.setdefault(e["case"], []).append(e)
    for c, evs in cases.items():
        if a.case and c != a.case:
            continue
        b = [e for e in evs if e["event"] == "BLIND"]
        r = [e for e in evs if e["event"] == "RECORD"]
        g = r[-1]["final_grade"] if r else (b[-1]["grade"] + " (pre-commit)" if b else "-")
        print(f"{c:40s} {case_state(evs):10s} grade={g:30s} "
              f"score={json.dumps(r[-1]['score']) if r else '-'}")


def cmd_verify(st: Store, a):
    ents = st.entries()
    problems = verify_chain(ents)
    for c in sorted({e["case"] for e in ents}):
        seals = [e for e in ents if e["case"] == c and e["event"] == "SEAL"]
        if seals:
            p = st.sealed_path(c)
            if not p.exists():
                problems.append(f"{c}: sealed file missing")
            elif sha256(p.read_text(encoding="utf-8")) != seals[-1]["full_sha256"]:
                problems.append(f"{c}: sealed file changed after sealing")
        evs = [e for e in ents if e["case"] == c]
        order = [e["event"] for e in evs]
        if "REVEAL" in order and ("COMMIT" not in order or order.index("COMMIT") > order.index("REVEAL")):
            problems.append(f"{c}: reveal without a prior commit")
    print("OK: chain intact, sealed files match, order valid" if not problems else "\n".join(problems))
    return 0 if not problems else 1


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--home", default=str(DEFAULT_HOME), help="store directory (env BLIND_HOME)")
    sp = p.add_subparsers(dest="cmd", required=True)
    q = sp.add_parser("courier-prompt")
    q.add_argument("--case", required=True)
    q.add_argument("--source", choices=sorted(SOURCES), required=True)
    q.add_argument("--opinion-id", type=int)
    q.add_argument("--ldh-source")
    q.add_argument("--ldh-id")
    q = sp.add_parser("ingest")
    q.add_argument("--case", required=True)
    q.add_argument("--transcripts", help="directory of courier transcripts (default: auto)")
    q.add_argument("--scope", choices=["facts", "reasoning"], default="facts")
    q = sp.add_parser("seal-file")
    q.add_argument("--case", required=True)
    q.add_argument("--file", required=True)
    q.add_argument("--provenance", default="file_unverified")
    q = sp.add_parser("fetch")
    q.add_argument("--case", required=True)
    q.add_argument("--url")
    q.add_argument("--courtlistener-opinion", type=int)
    q.add_argument("--blind", action="store_true")
    q.add_argument("--scope", choices=["facts", "reasoning"], default="facts")
    q = sp.add_parser("blind")
    q.add_argument("--case", required=True)
    q.add_argument("--scope", choices=["facts", "reasoning"], default="facts")
    q = sp.add_parser("commit")
    q.add_argument("--case", required=True)
    q.add_argument("--prediction", required=True, help="JSON object, e.g. layer/notch")
    q.add_argument("--prior-exposure", choices=["none", "case_name_only", "search_snippet", "other"], required=True)
    q.add_argument("--rationale")
    q = sp.add_parser("reveal")
    q.add_argument("--case", required=True)
    q.add_argument("--allow-tool-change", action="store_true")
    q = sp.add_parser("record")
    q.add_argument("--case", required=True)
    q.add_argument("--actual", required=True)
    q.add_argument("--note")
    q = sp.add_parser("void")
    q.add_argument("--case", required=True)
    q.add_argument("--reason", required=True)
    q = sp.add_parser("status")
    q.add_argument("--case")
    sp.add_parser("verify")
    a = p.parse_args(argv)
    st = Store(Path(a.home))
    if a.cmd == "courier-prompt":
        if a.source == "courtlistener" and not a.opinion_id:
            p.error("--opinion-id required")
        if a.source == "ldh" and not (a.ldh_source and a.ldh_id):
            p.error("--ldh-source and --ldh-id required")
    fn = {"courier-prompt": cmd_courier_prompt, "ingest": cmd_ingest, "seal-file": cmd_seal_file,
          "fetch": cmd_fetch, "blind": cmd_blind, "commit": cmd_commit, "reveal": cmd_reveal,
          "record": cmd_record, "void": cmd_void, "status": cmd_status, "verify": cmd_verify}[a.cmd]
    rc = fn(st, a)
    return rc or 0


if __name__ == "__main__":
    sys.exit(main())
