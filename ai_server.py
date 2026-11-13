"""Career DNA V2 HTTP boundary. No document, response or request-body logging."""

import hashlib, hmac, json, os, secrets, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from ai_transport import AppError
from career_intelligence import extract_document, analyse_review
from document_parser import parse_document, MAX_BYTES
from generation_counts import snapshot
from model_config import configuration, USAGE, INTERNAL_TEST
import request_state

ROOT = Path(__file__).parent / "preview"
ALLOWED_ORIGINS = set(filter(None, os.environ.get("ALLOWED_ORIGINS", "").split(",")))
ACTIVE = threading.BoundedSemaphore(2)
LOCK = threading.Lock()
RECENT = {}


def rate_limit(client):
    ident = hashlib.sha256(client.encode()).hexdigest()[:20]
    now = time.monotonic()
    with LOCK:
        for key in list(RECENT):
            RECENT[key] = [t for t in RECENT[key] if now - t < 60]
            if not RECENT[key]:
                del RECENT[key]
        times = RECENT.get(ident, [])
        if len(times) >= 8:
            raise AppError(
                429, "Please wait a minute before trying again.", "rate_limit"
            )
        RECENT[ident] = times + [now]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def origin_allowed(self):
        origin = self.headers.get("Origin")
        return (
            not origin
            or origin in ALLOWED_ORIGINS
            or origin
            in {
                "http://" + self.headers.get("Host", ""),
                "https://" + self.headers.get("Host", ""),
            }
        )

    def reply(self, status, data, typ="application/json; charset=utf-8"):
        body = (
            json.dumps(data, ensure_ascii=False).encode()
            if typ.startswith("application/json")
            else data
        )
        self.send_response(status)
        headers = {
            "Content-Type": typ,
            "Content-Length": str(len(body)),
            "Cache-Control": "no-store",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Referrer-Policy": "same-origin",
            "Permissions-Policy": "microphone=(), camera=()",
            "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; font-src data:; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'",
        }
        if self.headers.get("Origin") and self.origin_allowed():
            headers.update(
                {
                    "Access-Control-Allow-Origin": self.headers["Origin"],
                    "Vary": "Origin",
                }
            )
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        if not self.origin_allowed():
            return self.reply(403, {"error": "Origin not allowed."})
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", self.headers.get("Origin", ""))
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Request-ID")
        self.send_header("Access-Control-Max-Age", "600")
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/health":
            return self.reply(
                200,
                {
                    "ok": True,
                    "schema_version": "2.0",
                    "ai_configured": bool(os.environ.get("OPENAI_API_KEY")),
                    **configuration(),
                },
            )
        if path == "/api/stats":
            try:
                return self.reply(200, snapshot())
            except Exception:
                return self.reply(503, {"error": "Count temporarily unavailable."})
        if path == "/":
            return self.reply(
                200, (ROOT / "index.html").read_bytes(), "text/html; charset=utf-8"
            )
        return self.reply(404, {"error": "Not found."})

    def do_POST(self):
        acquired = False
        cache_key = None
        finished = False
        tokens = []
        try:
            if not self.origin_allowed():
                raise AppError(403, "Origin not allowed.", "origin_rejected")
            if self.path not in ["/api/v2/extract", "/api/v2/analyse"]:
                raise AppError(404, "Not found.", "not_found")
            length = int(self.headers.get("Content-Length", "0"))
            maximum = MAX_BYTES if self.path.endswith("extract") else 16000
            if not 0 < length <= maximum:
                raise AppError(
                    413, "This request exceeds the safe size limit.", "request_size"
                )
            rid = self.headers.get("X-Request-ID", "")
            if not __import__("re").fullmatch(r"[A-Za-z0-9_-]{16,80}", rid):
                raise AppError(400, "A request identifier is required.", "request_id")
            mime = self.headers.get("Content-Type", "").split(";")[0]
            kinds = {
                "application/pdf": "pdf",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
            }
            if self.path.endswith("extract") and mime not in kinds:
                raise AppError(415, "Choose a PDF or DOCX file.", "file_type")
            if self.path.endswith("analyse") and mime != "application/json":
                raise AppError(415, "This review could not be read.", "content_type")
            rate_limit(self.client_address[0])
            acquired = ACTIVE.acquire(blocking=False)
            if not acquired:
                raise AppError(429, "The studio is busy. Try again shortly.", "busy")
            self.connection.settimeout(20)
            raw = self.rfile.read(length)
            if len(raw) != length:
                raise AppError(
                    400, "The upload was interrupted. Try again.", "incomplete_upload"
                )
            key = os.environ.get("PM_INTERNAL_TEST_TOKEN", "")
            internal = bool(
                key
                and hmac.compare_digest(self.headers.get("X-PM-Internal-Test", ""), key)
            )
            tokens = [
                (INTERNAL_TEST, INTERNAL_TEST.set(internal)),
                (USAGE, USAGE.set([])),
            ]
            fingerprint = {
                "endpoint": self.path,
                "mime": mime,
                "hash": hashlib.sha256(raw).hexdigest(),
                "internal": internal,
            }
            state, cached = request_state.begin(rid, fingerprint)
            if state == "replay":
                return self.reply(200, cached)
            if state in ["pending", "conflict"]:
                raise AppError(
                    409,
                    "This request is still running."
                    if state == "pending"
                    else "This request changed. Please start it again.",
                    "request_" + state,
                )
            cache_key = rid
            if self.path.endswith("extract"):
                source = parse_document(raw, kinds[mime])
                raw = None
                result = extract_document(source)
            else:
                body = json.loads(raw)
                if not isinstance(body, dict) or set(body) != {"session_id", "review"}:
                    raise AppError(400, "Check your career review.", "review_invalid")
                result = analyse_review(body)
                if (
                    os.environ.get("PUBLIC_COUNTER_ENV") == "production"
                    and not internal
                ):
                    try:
                        result["stats"] = snapshot(True, request_id=rid, eligible=True)
                    except Exception:
                        result["stats_unavailable"] = True
            if internal:
                result["usage_metrics"] = USAGE.get()
            request_state.finish(rid, result)
            finished = True
            self.reply(200, result)
        except AppError as e:
            self.reply(e.status, {"error": e.message, "code": e.code})
        except (ValueError, TypeError, KeyError):
            self.reply(
                400,
                {
                    "error": "This request could not be read. Please try again.",
                    "code": "invalid_request",
                },
            )
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception:
            self.reply(
                500,
                {
                    "error": "Something interrupted your journey. Please try again.",
                    "code": "internal_error",
                },
            )
        finally:
            if cache_key and not finished:
                request_state.discard(cache_key)
            for var, token in reversed(tokens):
                var.reset(token)
            if acquired:
                ACTIVE.release()


if __name__ == "__main__":
    ThreadingHTTPServer(
        ("0.0.0.0", int(os.environ.get("PORT", "10000"))), Handler
    ).serve_forever()
