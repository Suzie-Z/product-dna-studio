"""Bounded AI transport shared by extraction and intelligence; no UI or profession rules."""

import json, os, re, socket, threading, time, urllib.request, urllib.error
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from model_config import career_model, USAGE, INTERNAL_TEST

LOCK = threading.Lock()
COUNTER = {"day": "", "count": 0}
TEST_COUNTER = {"day": "", "count": 0}


class AppError(Exception):
    def __init__(self, status, message, code):
        super().__init__(message)
        self.status = status
        self.message = message
        self.code = code


def reserve_attempt():
    today = datetime.now(ZoneInfo("Australia/Sydney")).date()
    start = os.environ.get("TRIAL_START_DATE", "")
    if start:
        try:
            launch = date.fromisoformat(start)
        except ValueError:
            raise AppError(
                503, "The preview schedule needs attention.", "configuration_error"
            )
        if not launch <= today < launch + timedelta(days=7):
            raise AppError(
                403, "This seven-day preview is not currently open.", "trial_closed"
            )
    with LOCK:
        counter = TEST_COUNTER if INTERNAL_TEST.get() else COUNTER
        limit = (
            int(os.environ.get("INTERNAL_TEST_DAILY_LIMIT", "40"))
            if INTERNAL_TEST.get()
            else int(os.environ.get("DAILY_GENERATION_LIMIT", "10"))
        )
        if counter["day"] != str(today):
            counter.update(day=str(today), count=0)
        if counter["count"] >= limit:
            raise AppError(
                429,
                "Today’s analysis slots are full. Please return tomorrow.",
                "daily_limit",
            )
        counter["count"] += 1


def provider(path, payload, timeout=90):
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        raise AppError(503, "The AI service is not configured yet.", "not_configured")
    req = urllib.request.Request(
        "https://api.openai.com/v1/" + path,
        data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.load(response)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise AppError(
                429,
                "The AI service has reached its usage limit. Please try later.",
                "provider_limit",
            )
        if e.code in [401, 403]:
            raise AppError(
                503,
                "The studio owner needs to check the AI service access.",
                "provider_auth",
            )
        failure = AppError(
            502,
            "The AI service is temporarily unavailable. Please try again.",
            "provider_unavailable",
        )
        try:
            detail = json.load(e).get("error", {})
            failure.provider_detail = {
                k: v
                for k, v in detail.items()
                if k in ["code", "type", "param"]
                and isinstance(v, str)
                and re.fullmatch(r"[A-Za-z0-9_./-]{1,100}", v)
            }
        except Exception:
            pass
        raise failure
    except (TimeoutError, socket.timeout, urllib.error.URLError):
        raise AppError(
            504, "The AI service took too long. Please try again.", "provider_timeout"
        )


def moderate(content):
    response = provider(
        "moderations", {"model": "omni-moderation-latest", "input": content[:40000]}, 25
    )
    if not isinstance(response.get("results"), list) or not response["results"]:
        raise AppError(
            502,
            "The safety check could not complete. Please try again.",
            "safety_unavailable",
        )
    if any(r.get("flagged") for r in response["results"]):
        raise AppError(
            422,
            "Please keep this map focused on safe, professional work experience. Revise the flagged content and try again.",
            "unsafe_content",
        )


def structured(payload, schema, prompt, stage="career"):
    reserve_attempt()
    request = {
        "model": career_model(stage),
        "store": False,
        "max_output_tokens": 8500,
        "reasoning": {"effort": "medium"},
        "input": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "career_dna_v2",
                "schema": schema,
                "strict": True,
            }
        },
    }
    started = time.monotonic()
    response = provider("responses", request, 110)
    if USAGE.get() is not None:
        USAGE.get().append(
            {
                "stage": stage,
                "model": request["model"],
                "provider_model": response.get("model", request["model"]),
                "seconds": round(time.monotonic() - started, 2),
                "usage": response.get("usage", {}),
            }
        )
    try:
        if response.get("status") != "completed":
            raise ValueError("incomplete response")
        parts = [
            p
            for item in response.get("output", [])
            if item.get("type") == "message"
            for p in item.get("content", [])
        ]
        if any(p.get("type") == "refusal" for p in parts):
            raise AppError(
                422,
                "The AI cannot create a professional map from this request. Try focusing on your work experience.",
                "model_refusal",
            )
        return json.loads(
            "".join(p["text"] for p in parts if p.get("type") == "output_text")
        )
    except AppError:
        raise
    except (ValueError, KeyError, TypeError):
        raise AppError(
            502, "The AI response was incomplete. Please try again.", "invalid_response"
        )
