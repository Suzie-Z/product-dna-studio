"""Non-secret stage selection. API credentials never reach the browser."""

import contextvars, os

INTERNAL_TEST = contextvars.ContextVar("internal_test", default=False)
USAGE = contextvars.ContextVar("career_usage", default=None)


def career_model(stage="career"):
    return (
        (
            os.environ.get("OPENAI_SUMMARY_MODEL", "").strip()
            if stage == "summary"
            else ""
        )
        or os.environ.get("OPENAI_CAREER_MODEL", "").strip()
        or os.environ.get("OPENAI_MODEL", "").strip()
        or "gpt-5-mini"
    )


def configuration():
    return {
        "stages": {
            "experience_extraction": career_model(),
            "career_intelligence": career_model("summary"),
        },
        "provider_endpoint": "https://api.openai.com/v1/responses",
        "provider_store": False,
        "visual_engine": "modular isometric SVG, no image API",
        "production_counter_enabled": os.environ.get("PUBLIC_COUNTER_ENV")
        == "production",
    }
