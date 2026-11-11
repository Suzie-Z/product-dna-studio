# PM Career DNA

Current integrated release: see [PM_IMPLEMENTATION.md](docs/PM_IMPLEMENTATION.md). PM-only scope, PM branding/logo, six background themes, 24 avatar/icon libraries, stable per-result variants and single-image export are implemented.


An evidence-grounded PM journey and capability map for internet/technology product managers. This upgrades the existing illustrated experience in place: lavender/cream/teal surfaces, soft cards, illustrated professional icons, and one of 24 neutral human chibi avatars with uniform cartoon skin material.

## Experience

1. **Share Your PM Journey** — one CV (PDF/DOCX/TXT), editable voice transcript, and written notes in a combined workspace. Source IDs remain stable during the session. Common contact details are redacted server-side before model processing.
2. **Discover Your PM Career DNA** — real structured OpenAI generation with **1–4 evidenced PM role types and 1–4 transferable capabilities independently**, signature, superpower, and evidence links. Sparse or conflicting evidence prompts one question instead of filling slots. Undated material is shown as **Experience Areas**.
3. **Download PNG** — one fixed high-resolution landscape map. To request changes, return to the original story input, add context or preferences, and generate again. There is no separate refinement form, manual map editor, format chooser, or third step.

All exported text is English. Evidence quotes retain their source language internally. Exported visible graphics contain no raw quotes, source IDs, ratings, or contact details. Each illustrated category has a noneditable SVG tooltip with a brief English evidence explanation; no raw quotes are placed in the SVG. No generated likeness or inferred physical attributes are used.

## Run locally

Requires Python 3.11+; the core generator uses the standard library; optional persistent counting uses the pinned PostgreSQL driver in `requirements.txt`.

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
- `skills/pm-dna-editorial/SKILL.md`: runtime-loaded editorial standard for distinctive decision-value copy and individually evidenced method labels.
- `preview/poster.js`: one controlled SVG scene with collision checks, responsive layouts, illustrated rocky islands, 24 PM icons and 24 neutral avatars, and single landscape PNG export (3200×2100, or 3200×2180 with dates). User copy is XML-escaped; overlong text blocks download rather than clipping.
- `build_preview.py`: emits a self-contained `preview/index.html`, compatible with the current static host.

Always rebuild the bundled HTML after frontend edits and commit source plus bundle.

Endpoints:

- `POST /api/career-dna/generate`: `{sources, clarification_context?}` → `{map, change_summary, accepted_source}`.
- Legacy API (not exposed in the current UI), `POST /api/career-dna/refine`: `{sources, previous, message, clarification_context?, context_consent:true}` → complete map plus a change summary. Existing fields are merged only through declared allowlisted paths, so undeclared model drift is discarded. Stable IDs are preserved.
- Legacy API (not exposed in the current UI), `POST /api/career-dna/review`: `{sources,map,context_consent:true}` → consented evidence/safety and per-field English-language review for locally edited results.
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

The browser suite launches the real HTTP app with **only the OpenAI transport mocked**. It covers clarification, generation, original-input regeneration, actual PNG download, editable CV inputs, normal PDF/DOCX parsing, mixed-language input, microphone fallback, mobile layout, XML escaping and overflow. All 32 combinations of 1–4 journey nodes, 1–4 strengths and desktop/mobile layouts are checked. Backend tests retain coverage of the legacy stateless refinement endpoints, which are not exposed in the simplified UI. Parser tests fetch version-pinned libraries from cdnjs into ignored `work/` test assets, using verified HTTPS.

Opt-in real-provider tests (billable) use a securely configured `OPENAI_API_KEY`, or an echo-disabled in-memory prompt:

```sh
python tests/live_smoke.py
```

This exercises profession specificity, Mandarin-to-English output, original-input regeneration, real PNG export, unsupported credentials and document injection. It has a ten-call safety cap per test process, including repair attempts. It never prints or saves the key. Artifacts go into ignored `work/`.

## Release

See [Render deployment](docs/RENDER.md), [limitations](docs/LIMITATIONS.md), and [verification](docs/VERIFICATION.md). PR #1 is merged and this release is published on the existing services. See [deployment verification](docs/DEPLOYED.md) for the deployed commits, production checks and export-review hotfix.

The older `server.py`, `public/`, `test_server.py` and `launch.py` preserve the earlier optional SQLite research dashboard. They are excluded from the current app's HTTP routes and deployment artifacts. No research database is created by this version. The separately reviewed `render-counts.yaml` option stores only aggregate dates and integers.

## Anonymous generation counts

`GET /api/stats` returns only total/today generation counts and a storage scope. A successful `/generate` response includes `generation_number` and the same count snapshot. Failed and clarification responses, refinements, and exports do not increment it. `generation_counts.py` is deliberately separate from AI/content processing.

The default mode is process memory and is labelled accordingly in the UI. To retain counts across service restarts, review and approve `render-counts.yaml`, which adopts the existing free API service and connects a private free Postgres instance. The table stores only `generation_day` and `generated_count`. No names, sources, CVs, maps or visitor IDs are written. The free database expires after 30 days; export/migrate totals before then. The live API currently reports persistent counting; this release preserves its existing connection without provisioning new resources. The observer goal of 20 generations/day does not change the existing AI call limit.

The latest [reference-fidelity correction](docs/VISUAL_FIDELITY.md) uses a local illustrated atlas, one responsive map root, and read-only View Full Journey. It preserves the original two-band illustrated world without generating two alternatives.
