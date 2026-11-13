import copy, io, json, os, unittest, zipfile
from unittest.mock import patch
import career_intelligence as engine, career_schema as schema, ephemeral_sessions as sessions, ai_transport, request_state
from ai_transport import AppError
from document_parser import parse_bytes, parse_document
from tests.v2_fixtures import *


class Contracts(unittest.TestCase):
    def test_professions_and_literal_provenance(self):
        for profile in PROFILES:
            with self.subTest(profile=profile):
                schema.validate_extraction(extraction(profile), cv_text(profile))
                schema.validate_analysis(
                    analysis(profile), extraction(profile)["stages"]
                )

    def test_fabricated_quote_rejected(self):
        data = extraction()
        data["stages"][0]["facts"][0]["quote"] = (
            "Invented international leadership achievement"
        )
        with self.assertRaises(ValueError):
            schema.validate_extraction(data, cv_text())

    def test_header_fabrication_rejected(self):
        data = extraction()
        data["stages"][0]["header_quote"] = "Invented employer"
        with self.assertRaises(ValueError):
            schema.validate_extraction(data, cv_text())

    def test_wrong_stage_attribution_rejected(self):
        data = analysis()
        data["stage_insights"][0]["capabilities"][0]["fact_ids"] = ["f3"]
        with self.assertRaises(ValueError):
            schema.validate_analysis(data, extraction()["stages"])

    def test_unknown_fact_in_each_major_narrative_rejected(self):
        for key in ["identity", "evolution", "recognition"]:
            data = analysis()
            data[key]["fact_ids"] = ["invented"]
            with self.assertRaises(ValueError):
                schema.validate_analysis(data, extraction()["stages"])

    def test_duplicate_and_missing_stages_rejected(self):
        data = analysis()
        data["stage_insights"][1] = copy.deepcopy(data["stage_insights"][0])
        with self.assertRaises(ValueError):
            schema.validate_analysis(data, extraction()["stages"])

    def test_duplicate_strength_rejected(self):
        data = analysis()
        data["core_dna"][1]["title"] = data["core_dna"][0]["title"]
        with self.assertRaises(ValueError):
            schema.validate_analysis(data, extraction()["stages"])

    def test_sparse_evidence_does_not_fill_slots(self):
        data = analysis("multilingual")
        self.assertEqual(len(data["core_dna"]), 1)
        schema.validate_analysis(data, extraction("multilingual")["stages"])

    def test_unknown_dates_and_overlaps_retained(self):
        data = extraction("education")
        self.assertEqual(data["stages"][0]["company"], data["stages"][1]["company"])
        self.assertIsNone(data["stages"][2]["period"])
        schema.validate_extraction(data, cv_text("education"))

    def test_career_break_is_not_promotion(self):
        self.assertEqual(extraction("healthcare")["stages"][1]["kind"], "career_break")

    def test_english_output_and_safe_text(self):
        for text in ["新的能力", "<script>alert(1)</script>", "reach me@example.test"]:
            data = analysis()
            data["core_dna"][0]["title"] = text
            with self.assertRaises(ValueError):
                schema.validate_analysis(data, extraction()["stages"])

    def test_caps_and_unknown_fields(self):
        data = analysis()
        data["core_dna"] *= 3
        with self.assertRaises(ValueError):
            schema.validate_analysis(data, extraction()["stages"])
        data = analysis()
        data["html"] = "unsafe"
        with self.assertRaises(ValueError):
            schema.validate_analysis(data, extraction()["stages"])


class ReviewAndPipeline(unittest.TestCase):
    def setUp(self):
        sessions.SESSIONS.clear()
        self.patch = patch("ai_transport.provider", side_effect=model_transport)
        self.patch.start()
        self.env = patch.dict(
            os.environ, {"DAILY_GENERATION_LIMIT": "1000", "TRIAL_START_DATE": ""}
        )
        self.env.start()

    def tearDown(self):
        self.patch.stop()
        self.env.stop()

    def test_pipeline_and_material_correction(self):
        value = engine.extract_document(cv_text())
        review = [
            {k: s[k] for k in ["id", "company", "role", "period"]}
            for s in value["stages"]
        ]
        review[1]["role"] = "Technical Product Manager"
        review.reverse()
        result = engine.analyse_review(
            {"session_id": value["session_id"], "review": review}
        )
        self.assertEqual(result["stages"][1]["role"], "Technical Product Manager")
        self.assertEqual(result["stages"][0]["id"], "s3")
        self.assertTrue(result["review_corrected"])

    def test_review_cannot_inject_evidence_or_delete_stages(self):
        review = [
            {k: s[k] for k in ["id", "company", "role", "period"]}
            for s in extraction()["stages"]
        ]
        with self.assertRaises(AppError):
            engine.reviewed_stages(extraction(), review[:1])
        review[0]["facts"] = [{"claim": "invented"}]
        with self.assertRaises(AppError):
            engine.reviewed_stages(extraction(), review)

    def test_foreign_or_expired_session(self):
        with self.assertRaises(AppError):
            engine.analyse_review({"session_id": "invented", "review": []})
        key = sessions.put({"value": "sensitive"})
        sessions.SESSIONS[key]["expires"] = 0
        with self.assertRaises(AppError):
            sessions.get(key)
        self.assertNotIn(key, sessions.SESSIONS)

    def test_redaction_and_untrusted_prompt_boundary(self):
        text = schema.redact(cv_text())
        self.assertNotIn("contact@example.test", text)
        self.assertNotIn("+61 400", text)
        self.assertIn("untrusted", engine.EXTRACTION_PROMPT)
        self.assertIn("not instructions", engine.ANALYSIS_PROMPT)

    def test_incomplete_ai_response_retryable(self):
        with patch("career_intelligence.structured", return_value={"status": "ready"}):
            with self.assertRaises(AppError) as failure:
                engine.extract_document(cv_text())
        self.assertEqual(failure.exception.code, "extraction_invalid")

    def test_unsupported_analysis_retryable(self):
        value = engine.extract_document(cv_text())
        review = [
            {k: s[k] for k in ["id", "company", "role", "period"]}
            for s in value["stages"]
        ]
        bad = analysis()
        bad["identity"]["fact_ids"] = ["invented"]
        with patch("career_intelligence.structured", return_value=bad):
            with self.assertRaises(AppError) as failure:
                engine.analyse_review(
                    {"session_id": value["session_id"], "review": review}
                )
        self.assertEqual(failure.exception.code, "analysis_invalid")
        self.assertTrue(sessions.get(value["session_id"]))


class Documents(unittest.TestCase):
    def test_real_pdf_and_docx(self):
        for kind, data in [("pdf", pdf_bytes()), ("docx", docx_bytes())]:
            with self.subTest(kind=kind):
                self.assertIn("Northstar Labs", parse_document(data, kind))

    def test_multilingual_docx(self):
        self.assertIn("研究实验", parse_bytes(docx_bytes("multilingual"), "docx"))

    def test_invalid_files(self):
        for data, kind in [(b"fake pdf", "pdf"), (b"PKfake", "docx"), (b"file", "txt")]:
            with self.assertRaises(ValueError):
                parse_bytes(data, kind)

    def test_scanned_or_blank_pdf(self):
        data = io.BytesIO()
        c = Canvas(data)
        c.showPage()
        c.save()
        with self.assertRaises(ValueError):
            parse_bytes(data.getvalue(), "pdf")

    def test_too_many_pages(self):
        data = io.BytesIO()
        c = Canvas(data)
        for _ in range(16):
            c.drawString(30, 700, "Example content")
            c.showPage()
        c.save()
        with self.assertRaises(ValueError):
            parse_bytes(data.getvalue(), "pdf")

    def test_oversize_file(self):
        with self.assertRaises(AppError):
            parse_document(b"x" * (5 * 1024 * 1024 + 1), "pdf")

    def test_docx_zip_bomb(self):
        data = io.BytesIO()
        with zipfile.ZipFile(data, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", "x")
            z.writestr("word/document.xml", "A" * 100000)
        with self.assertRaises(ValueError):
            parse_bytes(data.getvalue(), "docx")

    def test_missing_data(self):
        with self.assertRaises(ValueError):
            parse_bytes(docx_bytes(text="Name only"), "docx")


class RequestMemory(unittest.TestCase):
    def tearDown(self):
        request_state.CACHE.clear()

    def test_replay_conflict_and_pending(self):
        key = "req_test_request_12345"
        self.assertEqual(request_state.begin(key, {"a": 1})[0], "new")
        self.assertEqual(request_state.begin(key, {"a": 1})[0], "pending")
        self.assertEqual(request_state.begin(key, {"a": 2})[0], "conflict")
        request_state.finish(key, {"ok": True})
        self.assertEqual(request_state.begin(key, {"a": 1}), ("replay", {"ok": True}))


if __name__ == "__main__":
    unittest.main()
