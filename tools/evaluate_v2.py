"""Explicit, local live-provider evaluation on synthetic professions. Never counts production."""

import argparse, json, os, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from career_intelligence import extract_document, analyse_review
from tests.v2_fixtures import PROFILES, cv_text
from model_config import USAGE, configuration


def main():
    parser = argparse.ArgumentParser(
        description="Makes billable OpenAI calls on synthetic CVs. Uses existing daily attempt guards."
    )
    parser.add_argument(
        "--profiles",
        nargs="+",
        choices=list(PROFILES),
        default=["technology", "education", "healthcare"],
    )
    parser.add_argument("--output", default="work/v2-live-evaluation")
    args = parser.parse_args()
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit(
            "Set OPENAI_API_KEY securely in the local server environment. No calls were made."
        )
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    report = {
        "configuration": configuration(),
        "provider_calls_are_real": True,
        "profiles": [],
        "human_quality_review": "required; evidence references alone do not establish semantic entailment",
    }
    # No HTTP or production count increment occurs in this evaluation. Keep the public attempt guard.
    for profile in args.profiles:
        token = USAGE.set([])
        started = time.monotonic()
        try:
            extraction = extract_document(cv_text(profile))
            if extraction["status"] != "ready":
                raise ValueError("Synthetic career CV returned insufficient")
            review = [
                {k: s[k] for k in ["id", "company", "role", "period"]}
                for s in extraction["stages"]
            ]
            result = analyse_review(
                {"session_id": extraction["session_id"], "review": review}
            )
            (out / (profile + ".json")).write_text(
                json.dumps(result, ensure_ascii=False, indent=2)
            )
            report["profiles"].append(
                {
                    "profile": profile,
                    "passed_structural_and_literal_evidence_checks": True,
                    "seconds": round(time.monotonic() - started, 2),
                    "usage": USAGE.get(),
                    "human_review": {
                        "distinctive_insight": None,
                        "meaningfully_supported_claims": None,
                        "appropriate_emotional_tone": None,
                        "no_seniority_inflation": None,
                        "correct_evolution": None,
                        "cross_profession_fit": None,
                    },
                }
            )
        except Exception as e:
            report["profiles"].append(
                {
                    "profile": profile,
                    "passed_structural_and_literal_evidence_checks": False,
                    "error_code": getattr(e, "code", type(e).__name__),
                    "seconds": round(time.monotonic() - started, 2),
                    "usage": USAGE.get(),
                }
            )
        finally:
            USAGE.reset(token)
        (out / "report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2)
        )
    print("Saved evaluation to", out / "report.json")


if __name__ == "__main__":
    main()
