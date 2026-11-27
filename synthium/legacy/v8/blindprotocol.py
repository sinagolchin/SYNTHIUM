"""Mechanical blind protocol for case grabs.

Enforcement model
-----------------
The disposition must never enter the coder's context before commitment. The
enforcement is at FETCH level, not text-processing level:
  1. SEARCH with outcome-neutral, facts-language queries only (no outcome verbs).
  2. FETCH with include_full_text=false -> leading ~2KB only. For Chinese
     judgments (linear structure: header -> procedure -> facts -> reasoning ->
     disposition at END) the leading 2KB is machine-guaranteed disposition-free.
  3. COMMIT the prediction here (timestamped, hashed).
  4. FETCH full text. REVEAL: classifier extracts the tenor; hit/miss recorded.

Known limits (logged, not hidden):
  - Japanese judgments put the tenor FIRST -> protocol does not apply to JP.
  - Search snippets can leak outcome text; every commit records a taint
    declaration of what the snippet showed. Tainted rows grade as 'disclosed'.
  - The log proves ORDER within itself; the fetch-level guarantee is the
    include_full_text=false mechanism.
"""
import csv, hashlib, os, sys, datetime, re

# RESTORED 2026-11-24: the July log now lives in data/blind_log_2026-07/ at the repo
# top; SYNTHIUM_BLIND_LOG points the tool at another log file.
LOG = os.environ.get("SYNTHIUM_BLIND_LOG") or os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "data", "blind_log_2026-07", "blind_protocol_log.csv")
FIELDS = ["case_id","source","when","stage","sha256_excerpt","taint","category",
          "posture","layer","committed_notch","actual_notch","hit","tenor"]

CN_AFFIRM  = ["驳回上诉,维持原判", "驳回上诉,维持原判", "维持原判", "维持原裁定", "驳回再审申请"]
CN_REVERSE = ["发回重审", "撤销原判", "撤销一审", "撤销原裁定"]
CN_MODIFY  = ["改判"]

def classify_cn(text):
    """Return (notch, tenor_line) from a full CN judgment text."""
    tail = text[-1500:]
    tenor = ""
    m = re.search(r"(判决如下|裁定如下)(.{0,600})", text[-3000:], re.S)
    if m: tenor = m.group(0)[:400]
    has = lambda kws, t: any(k in t for k in kws)
    zone = tenor if tenor else tail
    if has(CN_MODIFY, zone) and has(CN_AFFIRM, zone):  return "MODIFIED", tenor
    if has(CN_REVERSE, zone) and has(CN_MODIFY, zone): return "REVERSED", tenor
    if has(CN_REVERSE, zone):                          return "REVERSED", tenor
    if has(CN_MODIFY, zone):                           return "MODIFIED", tenor
    if has(CN_AFFIRM, zone):                           return "CLEAN_AFFIRM", tenor
    return "AMBIGUOUS", tenor

def _rows():
    if not os.path.exists(LOG): return []
    return list(csv.DictReader(open(LOG)))

def _write(rows):
    w = csv.DictWriter(open(LOG, "w", newline=""), fieldnames=FIELDS)
    w.writeheader(); w.writerows(rows)

def commit(case_id, source, excerpt_file, taint, category, posture, layer, notch):
    ex = open(excerpt_file, encoding="utf-8").read()
    rows = _rows()
    if any(r["case_id"]==case_id for r in rows):
        print(f"REFUSED: {case_id} already in log"); sys.exit(1)
    rows.append(dict(case_id=case_id, source=source,
        when=datetime.datetime.utcnow().isoformat(timespec="seconds"),
        stage="committed", sha256_excerpt=hashlib.sha256(ex.encode()).hexdigest()[:16],
        taint=taint, category=category, posture=posture, layer=layer,
        committed_notch=notch, actual_notch="", hit="", tenor=""))
    _write(rows)
    sealed = os.path.join(os.path.dirname(LOG), "sealed", f"{case_id}.excerpt.txt")
    open(sealed, "w", encoding="utf-8").write(ex)
    print(f"COMMITTED {case_id}: {notch} (excerpt sha {rows[-1]['sha256_excerpt']}, taint='{taint}')")

def reveal(case_id, fulltext_file):
    rows = _rows(); hitrow = None
    for r in rows:
        if r["case_id"]==case_id: hitrow=r
    if not hitrow or hitrow["stage"]!="committed":
        print(f"REFUSED: no committed row for {case_id}"); sys.exit(1)
    full = open(fulltext_file, encoding="utf-8").read()
    notch, tenor = classify_cn(full)
    hitrow.update(stage="revealed", actual_notch=notch,
                  hit=str(hitrow["committed_notch"]==notch), tenor=tenor.replace("\n"," ")[:200])
    _write(rows)
    print(f"REVEALED {case_id}: committed={hitrow['committed_notch']} actual={notch} hit={hitrow['hit']}")
    if notch=="AMBIGUOUS": print("  ! classifier ambiguous — manual review required, do not score automatically")

def status():
    for r in _rows():
        print(f"{r['case_id'][:40]:42s} {r['stage']:9s} committed={r['committed_notch']:13s} actual={r['actual_notch']:13s} hit={r['hit']}")

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd=="commit": commit(*sys.argv[2:10])
    elif cmd=="reveal": reveal(sys.argv[2], sys.argv[3])
    elif cmd=="status": status()
