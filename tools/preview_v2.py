"""Local design preview. Synthetic files only; never invokes OpenAI or production storage."""

import argparse, os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from unittest.mock import patch
import ai_server, ai_transport
from tests.v2_fixtures import model_transport, pdf_bytes, docx_bytes, PROFILES

BANNER = b'<aside style="padding:12px;text-align:center;background:#e8f4ed;color:#285644;font:14px system-ui">Design preview: synthetic CVs only. No AI calls or production counts. <a href="/demo/technology.pdf">Technology CV</a> &middot; <a href="/demo/education.docx">Education CV</a> &middot; <a href="/demo/healthcare.docx">Healthcare CV</a></aside>'


def fixture_provider(path, payload, timeout=90):
    import json

    if path == "responses":
        data = json.loads(payload["input"][-1]["content"])
        if "cv_text" in data and "SYNTHETIC CAREER CV" not in data["cv_text"]:
            raise ai_transport.AppError(
                422,
                "This design preview accepts only the synthetic CVs linked at the top. Use the real local server for your own CV.",
                "synthetic_only",
            )
    return model_transport(path, payload, timeout)


class PreviewHandler(ai_server.Handler):
    def do_GET(self):
        if self.path.startswith("/demo/"):
            name = self.path.removeprefix("/demo/")
            profile, _, extension = name.partition(".")
            if profile not in PROFILES or extension not in ["pdf", "docx"]:
                return self.reply(404, {"error": "No such sample."})
            data = pdf_bytes(profile) if extension == "pdf" else docx_bytes(profile)
            mime = (
                "application/pdf"
                if extension == "pdf"
                else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            return self.reply(200, data, mime)
        return super().do_GET()

    def reply(self, status, data, typ="application/json; charset=utf-8"):
        if typ.startswith("text/html"):
            data = data.replace(b"<body>", b"<body>" + BANNER)
        return super().reply(status, data, typ)


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--port", type=int, default=10001)
    config = args.parse_args()
    os.environ.update(
        PUBLIC_COUNTER_ENV="",
        COUNTER_DATABASE_URL="",
        DAILY_GENERATION_LIMIT="1000",
        TRIAL_START_DATE="",
    )
    print(f"Synthetic-only design preview: http://127.0.0.1:{config.port}", flush=True)
    with patch("ai_transport.provider", side_effect=fixture_provider):
        ai_server.ThreadingHTTPServer(
            ("127.0.0.1", config.port), PreviewHandler
        ).serve_forever()


if __name__ == "__main__":
    main()
