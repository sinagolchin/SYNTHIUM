"""Tests for synthium.blind.protocol. Run from codebase/: python -m pytest -q"""
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from synthium.blind import protocol as bp

FILLER = " ".join(["The parties dispute the meaning of clause 4 and the record shows the contract was signed in 2019."] * 12)

US_OPINION = f"""SUPREME COURT OF TEXAS
Syllabus
Held: the protected parties may compel arbitration. Reversed and remanded.
JUSTICE BLAND delivered the opinion of the Court.
A mother signed an agreement for her daughter at a trampoline park. {FILLER}
The trial court denied the motion. The court of appeals affirmed in part and reversed in part. {FILLER}
DISCUSSION
We consider whether the clause binds the child. {FILLER}
The court of appeals erred in holding otherwise. {FILLER}
{FILLER}
For the foregoing reasons, we reverse the portion of the court of appeals' judgment and remand.
The judgment of the court of appeals is reversed.
"""

NZ_JUDGMENT = f"""IN THE SUPREME COURT OF NEW ZEALAND
JUDGMENT OF THE COURT
A The appeal is allowed.
B The conviction is quashed and a new trial ordered.
REASONS
Introduction
[1] Mr Bailey was convicted of an offence. {FILLER}
[2] The Court of Appeal dismissed his appeal. {FILLER}
Analysis
[3] The directions to the jury were inadequate. {FILLER}
{FILLER}
Result
[40] The appeal is allowed. The conviction is quashed.
"""

FRONT_LOADED = f"""PER CURIAM. Because the parent signed for the child, we reverse this portion of the court of appeals' judgment.
{FILLER}
Background
{FILLER}
Analysis
{FILLER} {FILLER}
Conclusion
We reverse and remand.
"""

CN_JUDGMENT = ("北京市高级人民法院刑事裁定书\n上诉人王某因故意伤害一案，不服一审判决，提出上诉。\n经审理查明，" + "被告人于某日在某地与被害人发生争执。" * 40 +
               "\n本院认为，" + "原审认定事实清楚，证据确实充分。" * 30 + "上诉理由不能成立，本院不予支持。" +
               "依照《中华人民共和国刑事诉讼法》第二百三十六条第一款第（一）项之规定，裁定如下：\n驳回上诉，维持原判。\n本裁定为终审裁定。")

JP_JUDGMENT = ("主 文\n本件上告を棄却する。\n上告費用は上告人の負担とする。\n理 由\n" + "上告代理人の上告理由について。本件は、売買契約に関する事案である。" * 40 +
               "\n所論の点に関する原審の判断は正当として是認することができる。\n" + "原審の確定した事実関係は次のとおりである。" * 20 +
               "\nよって、裁判官全員一致の意見で、主文のとおり判決する。")

NO_MARKER = "Opinion. " + FILLER * 3


class TestCut(unittest.TestCase):
    def test_common_cut_and_syllabus(self):
        b = bp.blind_text(US_OPINION, scope="reasoning")
        self.assertEqual(b.kind, "common")
        self.assertNotIn("Reversed and remanded", b.shown)
        self.assertNotIn("we reverse", b.shown.lower())
        self.assertNotIn("is reversed", b.shown)
        self.assertIn("A mother signed", b.shown)
        self.assertIn("For the foregoing reasons", b.sealed_tail)
        self.assertEqual(b.strong_after, 0)
        # procedural history ("The court of appeals affirmed in part") must survive
        self.assertIn("court of appeals affirmed in part", b.shown)

    def test_nz_front_orders_removed(self):
        b = bp.blind_text(NZ_JUDGMENT, scope="reasoning")
        self.assertNotIn("appeal is allowed", b.shown)
        self.assertNotIn("quashed", b.shown)
        self.assertIn("Court of Appeal dismissed his appeal", b.shown)  # history kept
        self.assertTrue(b.sealed_tail.lstrip().startswith("Result"))

    def test_front_loaded_disposition_is_redacted_and_flagged(self):
        b = bp.blind_text(FRONT_LOADED, scope="reasoning")
        self.assertNotIn("we reverse", b.shown.lower())
        self.assertIn("[REDACTED-OUTCOME #1]", b.shown)
        self.assertEqual(b.grade, "uncertain_exposure")
        self.assertTrue(any("front-loaded" in n for n in b.notes))

    def test_facts_scope(self):
        b = bp.blind_text(US_OPINION, scope="facts")
        self.assertNotIn("We consider whether", b.shown)
        self.assertIn("trampoline park", b.shown)

    def test_cn(self):
        b = bp.blind_text(CN_JUDGMENT, scope="reasoning")
        self.assertEqual(b.kind, "cn")
        for leak in ("驳回上诉", "维持原判", "裁定如下", "第二百三十六条", "不予支持"):
            self.assertNotIn(leak, b.shown, leak)
        self.assertIn("经审理查明", b.shown)

    def test_cn_facts_scope(self):
        b = bp.blind_text(CN_JUDGMENT, scope="facts")
        self.assertNotIn("本院认为", b.shown)

    def test_jp(self):
        b = bp.blind_text(JP_JUDGMENT, scope="reasoning")
        self.assertEqual(b.kind, "jp")
        for leak in ("棄却する", "主文のとおり", "是認することができる"):
            self.assertNotIn(leak, b.shown, leak)
        self.assertIn("原審の確定した事実関係", b.shown)

    def test_fail_closed_without_marker(self):
        b = bp.blind_text(NO_MARKER, scope="reasoning")
        self.assertEqual(b.grade, "no_cut")
        self.assertEqual(b.shown, "")

    def test_html_input(self):
        h = "<html><p>" + US_OPINION.replace("\n", "</p><p>") + "</p></html>"
        b = bp.blind_text(h, scope="reasoning")
        self.assertNotIn("we reverse", b.shown.lower())
        self.assertIn("trampoline", b.shown)


class TestProtocol(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = self.tmp.name
        self.src = Path(self.home) / "op.txt"
        self.src.write_text(US_OPINION, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = bp.main(["--home", self.home, *args])
        return rc, buf.getvalue()

    def test_full_flow_and_reveal_refused_without_commit(self):
        self.run_cli("seal-file", "--case", "t1", "--file", str(self.src))
        _, out = self.run_cli("blind", "--case", "t1", "--scope", "reasoning")
        self.assertNotIn("For the foregoing reasons", out)
        with self.assertRaises(SystemExit) as cm:
            self.run_cli("reveal", "--case", "t1")
        self.assertIn("REFUSED", str(cm.exception))
        self.run_cli("commit", "--case", "t1", "--prediction", '{"layer":"pure_law","notch":"REVERSED"}',
                     "--prior-exposure", "none")
        with self.assertRaises(SystemExit):  # one commit per blind
            self.run_cli("commit", "--case", "t1", "--prediction", '{"notch":"CLEAN_AFFIRM"}', "--prior-exposure", "none")
        _, out = self.run_cli("reveal", "--case", "t1")
        self.assertIn("For the foregoing reasons", out)
        _, out = self.run_cli("record", "--case", "t1", "--actual", '{"layer":"pure_law","notch":"REVERSED"}')
        self.assertEqual(json.loads(out)["score"], {"layer": True, "notch": True})
        self.assertEqual(json.loads(out)["grade"], "uncertain_exposure")  # file intake is capped
        rc, out = self.run_cli("verify")
        self.assertEqual(rc, 0, out)

    def test_tamper_detected(self):
        self.run_cli("seal-file", "--case", "t2", "--file", str(self.src))
        self.run_cli("blind", "--case", "t2")
        log = Path(self.home) / "blindlog.jsonl"
        lines = log.read_text().splitlines()
        e = json.loads(lines[1])
        e["grade"] = "blind"
        lines[1] = json.dumps(e, sort_keys=True)
        log.write_text("\n".join(lines) + "\n")
        rc, out = self.run_cli("verify")
        self.assertEqual(rc, 1)
        self.assertIn("edited", out)

    def test_sealed_file_change_voids(self):
        self.run_cli("seal-file", "--case", "t3", "--file", str(self.src))
        p = Path(self.home) / "sealed" / "t3.full.txt"
        os.chmod(p, 0o600)
        p.write_text(US_OPINION + "x")
        with self.assertRaises(SystemExit) as cm:
            self.run_cli("blind", "--case", "t3")
        self.assertIn("CHANGED", str(cm.exception))

    def test_no_overwrite_of_sealed(self):
        self.run_cli("seal-file", "--case", "t4", "--file", str(self.src))
        with self.assertRaises(SystemExit):
            self.run_cli("seal-file", "--case", "t4", "--file", str(self.src))


class TestCourierIngest(unittest.TestCase):
    def test_ingest_from_fake_transcript(self):
        with tempfile.TemporaryDirectory() as home, tempfile.TemporaryDirectory() as tdir:
            buf = io.StringIO()
            with redirect_stdout(buf):
                bp.main(["--home", home, "courier-prompt", "--case", "c1", "--source", "courtlistener",
                         "--opinion-id", "123"])
            prompt = buf.getvalue()
            nonce = prompt.split("Protocol nonce (do not repeat it): ")[1].split()[0]
            lines = [
                {"type": "user", "message": {"role": "user", "content": prompt}},
                {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "u1",
                    "name": "mcp__CourtListener__read_document", "input": {"opinion_id": 123}}]}},
                {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "u1",
                    "content": [{"type": "text", "text": json.dumps({"opinion_id": 123, "text": US_OPINION})}]}]}},
                {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "u2",
                    "name": "SubagentHandback", "input": {"message": "DONE"}}]}},
            ]
            with open(os.path.join(tdir, "agent-x.jsonl"), "w") as f:
                for l in lines:
                    f.write(json.dumps(l) + "\n")
            buf = io.StringIO()
            with redirect_stdout(buf):
                bp.main(["--home", home, "ingest", "--case", "c1", "--transcripts", tdir, "--scope", "facts"])
            out = buf.getvalue()
            self.assertIn("provenance=courier", out)
            self.assertIn("grade=blind", out)
            self.assertNotIn("we reverse", out.lower())
            self.assertNotIn("We consider whether", out)
            self.assertTrue(nonce.startswith("BP-"))

    def test_wrong_document_rejected(self):
        with tempfile.TemporaryDirectory() as home, tempfile.TemporaryDirectory() as tdir:
            buf = io.StringIO()
            with redirect_stdout(buf):
                bp.main(["--home", home, "courier-prompt", "--case", "c2", "--source", "courtlistener",
                         "--opinion-id", "123"])
            prompt = buf.getvalue()
            lines = [
                {"type": "user", "message": {"content": prompt}},
                {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "u1",
                    "name": "mcp__CourtListener__read_document", "input": {"opinion_id": 999}}]}},
                {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "u1",
                    "content": [{"type": "text", "text": json.dumps({"text": US_OPINION})}]}]}},
            ]
            with open(os.path.join(tdir, "agent-y.jsonl"), "w") as f:
                for l in lines:
                    f.write(json.dumps(l) + "\n")
            with self.assertRaises(SystemExit) as cm, redirect_stdout(io.StringIO()):
                bp.main(["--home", home, "ingest", "--case", "c2", "--transcripts", tdir])
            self.assertIn("not 123", str(cm.exception))


class TestRegressionsFromDryRun(unittest.TestCase):
    """Bugs found on the 2026-11-10 dry run against real CourtListener texts."""

    def test_hard_wrapped_sentence_fully_redacted(self):
        t = ("PER CURIAM\nBecause the protected\nparties are beneficiaries, we reverse this portion of the court of appeals'\n"
             "judgment and remand the case to the\ntrial court for further proceedings.\nI\n" + FILLER * 3 +
             "\nII\n" + FILLER * 3 + "\nFor these reasons, we reverse.")
        b = bp.blind_text(t, scope="reasoning")
        self.assertNotIn("remand the case", b.shown)
        self.assertNotIn("Because the protected", b.shown)

    def test_abbreviations_do_not_end_sentence(self):
        t = ("Opinion\n" + FILLER + " We therefore affirm the conviction under G. L. c. 272, \u00a7 105 (b), and "
             "reverse the conviction under G. L. c. 272, \u00a7 105 (c).\n" + FILLER * 4 + "\nConclusion.\nSo ordered.")
        b = bp.blind_text(t, scope="reasoning")
        self.assertNotIn("reverse the conviction", b.shown)

    def test_negated_disposition_is_strong(self):
        t = "Opinion\n" + FILLER * 4 + " Without evidence of prejudice, we will not set aside the agency's denial.\n***\nPetition denied."
        b = bp.blind_text(t, scope="reasoning")
        self.assertNotIn("will not set aside", b.shown)

    def test_procedural_history_not_redacted(self):
        t = ("Opinion\nI\nThe court of appeals reversed and remanded with instructions. " + FILLER * 3 +
             "\nII\n" + FILLER * 3 + "\nFor these reasons, we affirm.")
        b = bp.blind_text(t, scope="reasoning")
        self.assertIn("court of appeals reversed and remanded", b.shown)
        self.assertEqual(len(b.redactions), 0)

    def test_facts_scope_roman_parts(self):
        t = ("PER CURIAM\nWe hold the clause binds the child.\nI\nThe facts are these. " + FILLER * 2 +
             "\nII\nWe now turn to the law. " + FILLER * 3 + "\nFor these reasons, we reverse.")
        b = bp.blind_text(t, scope="facts")
        self.assertIn("The facts are these", b.shown)
        self.assertNotIn("We hold", b.shown)
        self.assertNotIn("turn to the law", b.shown)

    def test_facts_scope_inline_heading(self):
        t = ("Opinion\n" + FILLER + "\nBackground. 1. Facts. The defendant lived nearby. " + FILLER * 2 +
             "\nDiscussion. a. Standard. We review de novo. " + FILLER * 3 + "\nConclusion.\nSo ordered.")
        b = bp.blind_text(t, scope="facts")
        self.assertIn("The defendant lived nearby", b.shown)
        self.assertNotIn("We review de novo", b.shown)

    def test_persisted_output_is_loaded(self):
        home = os.path.expanduser("~/.claude/projects/_bp_test")
        os.makedirs(home, exist_ok=True)
        p = os.path.join(home, "tool.json")
        try:
            with open(p, "w") as f:
                json.dump([{"type": "text", "text": json.dumps({"text": "hello"})}], f)
            msg = f"<persisted-output>\nOutput too large (55.9KB). Full output saved to: {p}\n\nPreview (first 2KB):\n..."
            self.assertEqual(json.loads(bp._resolve_persisted(msg))["text"], "hello")
            with self.assertRaises(SystemExit):
                bp._resolve_persisted("<persisted-output>\nOutput too large (1KB). Full output saved to: /etc/passwd\n")
        finally:
            os.remove(p)
            os.rmdir(home)


if __name__ == "__main__":
    unittest.main()
