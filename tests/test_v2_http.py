import json, os, threading, unittest, urllib.request, urllib.error
from unittest.mock import patch
import ai_server, request_state, ephemeral_sessions
from tests.v2_fixtures import pdf_bytes, model_transport


class HTTP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.env = patch.dict(
            os.environ,
            {
                "PM_INTERNAL_TEST_TOKEN": "synthetic-only",
                "DAILY_GENERATION_LIMIT": "1000",
                "INTERNAL_TEST_DAILY_LIMIT": "1000",
                "TRIAL_START_DATE": "",
                "PUBLIC_COUNTER_ENV": "",
            },
        )
        cls.env.start()
        cls.provider = patch("ai_transport.provider", side_effect=model_transport)
        cls.provider_mock = cls.provider.start()
        cls.server = ai_server.ThreadingHTTPServer(("127.0.0.1", 0), ai_server.Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.url = "http://127.0.0.1:" + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.provider.stop()
        cls.env.stop()

    def setUp(self):
        ai_server.RECENT.clear()
        request_state.CACHE.clear()
        ephemeral_sessions.SESSIONS.clear()
        self.serial = 0

    def request(self, path, body, mime="application/json", rid=None, origin=None):
        self.serial += 1
        headers = {
            "Content-Type": mime,
            "X-Request-ID": rid or "req_http_fixture_" + str(self.serial).zfill(4),
            "X-PM-Internal-Test": "synthetic-only",
        }
        if origin:
            headers["Origin"] = origin
        r = urllib.request.Request(
            self.url + path,
            data=body if isinstance(body, bytes) else json.dumps(body).encode(),
            headers=headers,
        )
        try:
            response = urllib.request.urlopen(r)
        except urllib.error.HTTPError as e:
            response = e
        return response.status, json.load(response)

    def extract(self):
        status, data = self.request("/api/v2/extract", pdf_bytes(), "application/pdf")
        self.assertEqual(status, 200, data)
        return data

    def review(self, data):
        return [
            {k: s[k] for k in ["id", "company", "role", "period"]}
            for s in data["stages"]
        ]

    def test_complete_real_document_boundary(self):
        data = self.extract()
        status, result = self.request(
            "/api/v2/analyse",
            {"session_id": data["session_id"], "review": self.review(data)},
        )
        self.assertEqual(status, 200, result)
        self.assertEqual(result["schema_version"], "2.0")
        self.assertNotIn("stats", result)

    def test_duplicate_extract_does_not_repeat_provider(self):
        rid = "req_duplicate_pdf_12345"
        before = self.provider_mock.call_count
        a = self.request("/api/v2/extract", pdf_bytes(), "application/pdf", rid=rid)
        # Same bytes, not a newly generated timestamped PDF.
        raw = pdf_bytes()
        a = self.request(
            "/api/v2/extract", raw, "application/pdf", rid="req_exact_pdf_12345"
        )
        calls = self.provider_mock.call_count
        b = self.request(
            "/api/v2/extract", raw, "application/pdf", rid="req_exact_pdf_12345"
        )
        self.assertEqual(a, b)
        self.assertEqual(self.provider_mock.call_count, calls)

    def test_changed_request_id_conflict(self):
        raw = pdf_bytes()
        self.request(
            "/api/v2/extract", raw, "application/pdf", rid="req_conflict_pdf_12345"
        )
        status, _ = self.request(
            "/api/v2/extract",
            pdf_bytes(text="Some entirely different CV bytes and career facts."),
            "application/pdf",
            rid="req_conflict_pdf_12345",
        )
        self.assertEqual(status, 409)

    def test_cross_origin_rejected_before_parsing(self):
        self.assertEqual(
            self.request(
                "/api/v2/extract",
                b"bad",
                "application/pdf",
                origin="https://unrelated.example",
            )[0],
            403,
        )

    def test_obsolete_voice_and_refine_routes_removed(self):
        for path in [
            "/api/transcribe",
            "/api/career-dna/refine",
            "/api/career-dna/generate",
        ]:
            self.assertEqual(self.request(path, {})[0], 404)

    def test_text_and_bad_documents_rejected(self):
        self.assertEqual(
            self.request("/api/v2/extract", b"plain text", "text/plain")[0], 415
        )
        self.assertEqual(
            self.request("/api/v2/extract", b"fake", "application/pdf")[0], 422
        )

    def test_invalid_review_and_foreign_session(self):
        self.assertEqual(
            self.request("/api/v2/analyse", {"session_id": "missing", "review": []})[0],
            410,
        )
        data = self.extract()
        self.assertEqual(
            self.request(
                "/api/v2/analyse", {"session_id": data["session_id"], "review": []}
            )[0],
            400,
        )

    def test_health_and_html_bundle(self):
        health = json.load(urllib.request.urlopen(self.url + "/health"))
        self.assertEqual(health["schema_version"], "2.0")
        page = urllib.request.urlopen(self.url).read().decode()
        self.assertNotIn("https://cdnjs", page)
        self.assertNotIn("MediaRecorder", page)
        self.assertIn("data:font/ttf;base64", page)


if __name__ == "__main__":
    unittest.main()
