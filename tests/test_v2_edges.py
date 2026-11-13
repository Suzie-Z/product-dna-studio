import copy, io, json, os, threading, unittest, zipfile
from unittest.mock import patch
from pypdf import PdfReader, PdfWriter
from ai_transport import AppError, structured, COUNTER
from career_schema import validate_extraction, validate_analysis, EXTRACTION
from career_intelligence import extract_document, reviewed_stages
from document_parser import parse_bytes
import ephemeral_sessions as sessions, request_state
from tests.v2_fixtures import *


class Edges(unittest.TestCase):
    def test_insufficient_is_a_valid_explicit_result(self):
        data = {
            "status": "insufficient",
            "stages": [],
            "note": "Upload a CV with substantive work or project experience.",
        }
        validate_extraction(data, "A very short document")
        with (
            patch("career_intelligence.moderate"),
            patch("career_intelligence.structured", return_value=data),
        ):
            result = extract_document("A very short document")
        self.assertEqual(result["status"], "insufficient")
        self.assertNotIn("session_id", result)

    def test_encrypted_pdf_has_specific_guidance(self):
        writer = PdfWriter()
        writer.add_page(PdfReader(io.BytesIO(pdf_bytes())).pages[0])
        writer.encrypt("password")
        out = io.BytesIO()
        writer.write(out)
        with self.assertRaisesRegex(ValueError, "unlocked"):
            parse_bytes(out.getvalue(), "pdf")

    def test_docx_external_entity_declaration_rejected(self):
        out = io.BytesIO()
        with zipfile.ZipFile(out, "w") as z:
            z.writestr("[Content_Types].xml", "x")
            z.writestr(
                "word/document.xml",
                '<!DOCTYPE foo [<!ENTITY x SYSTEM "file:///etc/passwd">]><foo>&x;</foo>',
            )
        with self.assertRaisesRegex(ValueError, "unsupported XML"):
            parse_bytes(out.getvalue(), "docx")

    def test_pdf_text_length_limit(self):
        with self.assertRaises(ValueError):
            parse_bytes(docx_bytes(text="Experience evidence " * 2000), "docx")

    def test_empty_and_repeated_review_roles(self):
        review = [
            {k: s[k] for k in ["id", "company", "role", "period"]}
            for s in extraction()["stages"]
        ]
        review[0]["role"] = ""
        with self.assertRaises(AppError):
            reviewed_stages(extraction(), review)
        review[0] = copy.deepcopy(review[1])
        with self.assertRaises(AppError):
            reviewed_stages(extraction(), review)

    def test_review_contact_and_non_english_rejected(self):
        for bad in ["person@example.test", "岗位"]:
            review = [
                {k: s[k] for k in ["id", "company", "role", "period"]}
                for s in extraction()["stages"]
            ]
            review[0]["role"] = bad
            with self.assertRaises(AppError):
                reviewed_stages(extraction(), review)

    def test_session_capacity_and_expiry_do_not_evict_active_reviews(self):
        with (
            patch.dict(sessions.SESSIONS, {}, clear=True),
            patch.object(sessions, "MAX_SESSIONS", 1),
        ):
            key = sessions.put({"secret": "test"})
            with self.assertRaises(AppError):
                sessions.put({"other": "test"})
            self.assertEqual(sessions.get(key), {"secret": "test"})
            sessions.discard(key)
            self.assertNotIn(key, sessions.SESSIONS)

    def test_mutation_does_not_change_private_session(self):
        key = sessions.put({"a": [1]})
        value = sessions.get(key)
        value["a"].append(2)
        self.assertEqual(sessions.get(key), {"a": [1]})
        sessions.discard(key)

    def test_incomplete_provider_payload_never_enters_pipeline(self):
        with (
            patch.dict(
                os.environ, {"DAILY_GENERATION_LIMIT": "1000", "TRIAL_START_DATE": ""}
            ),
            patch(
                "ai_transport.provider",
                return_value={"status": "incomplete", "output": []},
            ),
        ):
            with self.assertRaises(AppError) as e:
                structured({}, EXTRACTION, "test")
        self.assertEqual(e.exception.code, "invalid_response")

    def test_provider_refusal_is_actionable(self):
        with (
            patch.dict(
                os.environ, {"DAILY_GENERATION_LIMIT": "1000", "TRIAL_START_DATE": ""}
            ),
            patch(
                "ai_transport.provider",
                return_value={
                    "status": "completed",
                    "output": [
                        {
                            "type": "message",
                            "content": [{"type": "refusal", "refusal": "test"}],
                        }
                    ],
                },
            ),
        ):
            with self.assertRaises(AppError) as e:
                structured({}, EXTRACTION, "test")
        self.assertEqual(e.exception.code, "model_refusal")

    def test_request_cache_is_immutable(self):
        key = "req_immutable_12345"
        request_state.discard(key)
        request_state.begin(key, {"x": 1})
        data = {"a": [1]}
        request_state.finish(key, data)
        data["a"].append(2)
        _, cached = request_state.begin(key, {"x": 1})
        cached["a"].append(3)
        self.assertEqual(request_state.begin(key, {"x": 1})[1], {"a": [1]})
        request_state.discard(key)

    def test_public_model_limit_is_not_increased_for_rebuild(self):
        import ai_transport

        with (
            patch.dict(
                os.environ, {"DAILY_GENERATION_LIMIT": "10", "TRIAL_START_DATE": ""}
            ),
            patch.dict(COUNTER, {"day": "", "count": 0}, clear=True),
        ):
            for _ in range(10):
                ai_transport.reserve_attempt()
            with self.assertRaises(AppError) as e:
                ai_transport.reserve_attempt()
            self.assertEqual(e.exception.code, "daily_limit")


if __name__ == "__main__":
    unittest.main()
