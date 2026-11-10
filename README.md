# Career DNA Studio

A profession-agnostic, evidence-grounded career map studio. This upgrades the existing illustrated experience in place: lavender/cream/teal surfaces, soft cards, controlled vector icons, and one small gender-neutral explorer.

## Experience

1. **Share Your Journey** — one CV (PDF/DOCX/TXT), editable voice transcript, and written notes in a combined workspace. Source IDs remain stable during the session. Common contact details are redacted server-side before model processing.
2. **Discover Your Career DNA** — real structured OpenAI generation with **1–5 journey nodes and 1–5 strengths independently**, signature, superpower, and evidence links. Sparse or conflicting evidence prompts one question instead of filling slots. Undated material is shown as **Experience Areas**.
3. **Make It Yours** — multilingual refinement beside the map, explicit consent to resend source context, direct text editing, six-step undo, evidence review, and PNG export. Unsupported credentials require clarification; unconfirmed strengths are not exported as facts.

All exported text is English. Source quotes retain their original language only inside private evidence review. Exported graphics contain no raw quotes, source IDs, evidence notes, ratings, or contact details. No generated likeness or inferred physical attributes are used.

## Run locally

Requires Python 3.11+; production code has **no third-party Python dependencies**.

```sh
python build_preview.py
# Set OPENAI_API_KEY securely in your process environment. Do not paste it into
# code, shell history, tracked files, screenshots, or chat.
python ai_server.py
```

Open `http://localhost:10000`. The API remains healthy without a key, but model generation returns an explicit configuration message. Very sparse input can receive a local clarification without a model call. Configuration keys are documented in `.env.example`; it is not automatically loaded.

## Source and API

- `career_ai.py`: schema, prompts, source redaction, moderation, grounding and refinement merge.
- `ai_server.py`: bounded JSON HTTP/CORS boundary and concurrency/rate controls.
- `preview/studio.template.html`, `studio.css`, `studio.js`: maintainable frontend sources.
- `preview/poster.js`: portrait/square deterministic renderer with font fitting and explicit overflow fallback.
- `build_preview.py`: emits a self-contained `preview/index.html`, compatible with the current static host.

Always rebuild the bundled HTML after frontend edits and commit source plus bundle.

Endpoints:

- `POST /api/career-dna/generate`: `{sources, clarification_context?}` → `{map, change_summary, accepted_source}`.
- `POST /api/career-dna/refine`: `{sources, previous, message, clarification_context?, context_consent:true}` → complete map plus a change summary. Existing fields are merged only through declared allowlisted paths, so undeclared model drift is discarded. Stable IDs are preserved.
- `POST /api/career-dna/review`: `{sources,map,context_consent:true}` → consented evidence/safety and per-field English-language review for locally edited results.
- `GET /health`: readiness and key-presence metadata only; no secret values.

Sources use `{source_id, source_type: cv|voice_transcript|typed_story, source_label, content}`. Only text crosses the API; raw uploaded files are parsed client-side and are never handled by the server. Reference IDs and literal quote provenance are independently validated. This validates provenance, not objective truth of a career claim; users still need to review the interpretation.

## Validation

Install test-only packages and Chromium using the official package/browser sources:

```sh
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python -m unittest test_ai tests.test_e2e -v
node --check preview/studio.js
node --check preview/poster.js
```

The browser suite launches the real HTTP app with **only the OpenAI transport mocked**. It covers clarification, generation, grounding, consent, scoped refinement, undo, direct edits, safety review, actual PNG download, editable CVs, normal PDF/DOCX parsing, mixed input, microphone fallback and mobile layout. All 50 combinations of 1–5 journey nodes, 1–5 strengths and two image formats are checked. Parser tests fetch version-pinned libraries from cdnjs into ignored `work/` test assets, using verified HTTPS.

Opt-in real-provider tests (billable) use a securely configured `OPENAI_API_KEY`, or an echo-disabled in-memory prompt:

```sh
python tests/live_smoke.py
```

This exercises profession specificity, Mandarin-to-English output, an actual browser refinement, stable unrelated fields, real PNG export, unsupported credentials and document injection. It has a ten-call safety cap per test process, including repair attempts. It never prints or saves the key. Artifacts go into ignored `work/`.

## Release

See [Render deployment](docs/RENDER.md), [limitations](docs/LIMITATIONS.md), and [verification](docs/VERIFICATION.md). This release is prepared on `career-dna-release`; the live site is not changed by preparing that branch.

The older `server.py`, `public/`, `test_server.py` and `launch.py` preserve the earlier optional SQLite research dashboard. They are excluded from the current app's HTTP routes and deployment artifacts. No research database is created by this version.
