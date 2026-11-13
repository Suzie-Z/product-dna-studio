"""Bounded ten-minute extraction memory. No files or durable identifiers."""

import copy, secrets, threading, time
from ai_transport import AppError

TTL = 600
MAX_SESSIONS = 20
LOCK = threading.Lock()
SESSIONS = {}


def discard(key, stamp=None):
    with LOCK:
        if stamp is None or SESSIONS.get(key, {}).get("expires") == stamp:
            SESSIONS.pop(key, None)


def put(value):
    with LOCK:
        now = time.monotonic()
        for k in list(SESSIONS):
            if SESSIONS[k]["expires"] <= now:
                del SESSIONS[k]
        if len(SESSIONS) >= MAX_SESSIONS:
            raise AppError(
                429,
                "The studio is holding a few journeys. Please try again shortly.",
                "session_capacity",
            )
        key = secrets.token_urlsafe(32)
        expires = now + TTL
        SESSIONS[key] = {"expires": expires, "value": copy.deepcopy(value)}
    timer = threading.Timer(TTL, discard, args=(key, expires))
    timer.daemon = True
    timer.start()
    return key


def get(key):
    with LOCK:
        item = SESSIONS.get(key) if isinstance(key, str) else None
        if not item or item["expires"] <= time.monotonic():
            SESSIONS.pop(key, None) if isinstance(key, str) else None
            raise AppError(
                410,
                "Your private review has expired. Upload your CV again to continue.",
                "session_expired",
            )
        return copy.deepcopy(item["value"])
