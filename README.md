# Career DNA V2 — rebuild preview

**Discover the strengths behind your story.**

A three-screen, cross-profession career reflection experience: upload one PDF/DOCX → lightly review the extracted chapters → explore the island journey → reveal a grounded professional identity, core capabilities, evolution and recognition.

This dedicated `career-dna-v2-rebuild` branch replaces the active V1 architecture. **It has not been deployed to production.** The existing live application and production branches are untouched. V1 code, its workflows and assets remain recoverable through Git history; historical documents under `docs/` describe earlier versions, not the active V2 contract.

## Try the design without an API key

```sh
pip install -r requirements.txt -r requirements-dev.txt
python build_preview.py
python -m tools.preview_v2 --port 10001
```

Open http://127.0.0.1:10001. Download one of the synthetic CVs linked in the preview banner and upload it. This mode accepts **synthetic samples only**, uses deterministic test responses, has no AI calls and cannot write production counts. It demonstrates interaction and layout, not model quality.

## Run the real application locally

```sh
pip install -r requirements.txt
python build_preview.py
python ai_server.py
```

Use Linux with Python 3.11+ (the parser uses Linux process/resource limits; the Render and Docker targets are Linux). Open http://127.0.0.1:10000. Set `OPENAI_API_KEY` securely in your server environment first; never paste a key into chat, browser code or Git. `OPENAI_CAREER_MODEL` (or existing `OPENAI_MODEL`) selects extraction; `OPENAI_SUMMARY_MODEL` selects synthesis and defaults to that same model. The fallback is `gpt-5-mini`. `/health` reports effective non-secret configuration. No credentials were changed or copied from production for this rebuild.

Do not set `PUBLIC_COUNTER_ENV=production` for previews. Existing trial, daily model-attempt quotas and production count tables remain available; local memory quotas reset on restart. A complete new analysis normally uses two structured model calls plus moderation. Retry after an invalid model response may use additional calls; replay of a completed identical request avoids them.

## Architecture

- `document_parser.py`: PDF/DOCX validation and parsing in a disposable process with 5 MB, 15-page, ZIP expansion, CPU, memory and timeout limits. No OCR or binary DOC support.
- `career_schema.py`: strict extraction and analysis JSON schemas, literal CV quote checks, English output and evidence-reference validation.
- `career_intelligence.py`: factual stages → capability synthesis → career pattern recognition → personalised reflection. Only company/role/period/order can be corrected in the lightweight review. Corrections are not treated as proof of new expertise.
- `ephemeral_sessions.py`: bounded ten-minute extraction memory; no document database.
- `ai_transport.py`, `model_config.py`: bounded provider transport, quotas and model configuration, independent of rendering and professions.
- `ai_server.py`: same-origin API, isolated parsing boundary, expiring idempotent requests and optional anonymous aggregate counts. No voice, manual history or Refine endpoints.
- `preview/cv-upload.js`, `studio.js`: single upload input and one state flow. No text/voice/URL alternatives, local storage or user tracking.
- `preview/visual-design.js`: semantic world plan, with a future artwork-provider boundary.
- `preview/islands.js`: six genuinely different modular isometric environments, shared camera/light/material language, seeded geography and environmental details.
- `preview/journey.js`, `dna.js`: accessible HTML labels, evidence and reflections outside artwork. No model-generated HTML/SVG is executed.
- `build_preview.py`: one self-contained page with bundled rounded fonts, no parser/font CDN dependency.

## Tests

```sh
python build_preview.py
python -m unittest discover -v
```

Browser tests require Chromium (`chromium` on PATH) and Playwright. They exercise the real upload/parser/server/UI boundary with **only AI transport mocked**. Test fixtures cover technology, education, healthcare/career break, design, finance and multilingual research. Screenshots are generated under `work/v2-qa/`.

For live-model quality evaluation on synthetic CVs (billable calls, existing attempt limits), run `python -m tools.evaluate_v2`. It records per-stage usage and leaves a human-review rubric for semantic support, specificity and emotional tone. It never increments production counts.

See [audit](docs/v2/AUDIT.md), [specification](docs/v2/IMPLEMENTATION_SPEC.md) and [delivery/QA record](docs/v2/DELIVERY.md).

## Privacy and boundaries

CV bytes are parsed in process memory and discarded. Redacted extracted text and facts go to OpenAI; common contact redaction is not exhaustive. Extraction sessions and replay results expire after ten minutes in server memory. The browser retains the selected file and result until reset/replacement/navigation. Providers have separate retention policies; this is not a zero-retention guarantee.

When enabled for production, the existing counter stores aggregate counts and expiring random request receipts, not CVs/maps. Operational hosting metadata is distinct. No personal-data database or admin archive is retained in V2.

This MVP intentionally omits conversational Refine, voice/manual onboarding, custom artwork generation, accounts, career advice and share/export services. Content is evidence-linked, not independently fact-verified. It can only interpret what the uploaded document supports. Generation quality and latency need live model evaluation before production approval.

## Deployment

`render.yaml` is a **review-only configuration** for the existing API service on this branch. The V2 frontend and API must share an origin, since uploads use relative URLs. Do not deploy it over the existing services without approval. The old separate static preview is still the live V1 website. No hosting plan, secret, database or production counter was changed.
