# Career DNA V2 rebuild — implementation and QA

13 November 2026 (Australia/Sydney). Branch: `career-dna-v2-rebuild`, based on `c065bdfccc5d37cf336b9e40acc62c8adfeab142`.

**Engineering preview implemented. Not deployed to production. Live-model insight quality remains to be evaluated.** No production branch, Render service, credential, plan or database was changed. The current production application remains the previously published PM Studio. This branch is the proposed replacement, not a second active architecture inside the application.

## Architecture and retained components

Replaced the coupled PM-only multi-input workflow with these boundaries:

1. **Document parsing:** `document_parser.py` accepts only PDF and DOCX. It checks signatures/ZIP structure, encryption, size, page count, expansion and readable text. Parsing runs in a disposable child process with 512 MB address-space, eight-second CPU and twelve-second wall limits. Original document bytes are released after reading. There is no upload directory.
2. **Experience extraction:** `career_intelligence.py` uses the extraction schema in `career_schema.py` to identify up to twelve significant stages. Each includes company, role, period or explicit uncertainty, professional domain, kind and source-backed factual claims. Multiple jobs at a company, overlaps and explicit career breaks are retained. More than twelve chapters should produce a request for a shorter CV rather than silent omissions.
3. **Lightweight review:** users may correct company, role, period and order. They cannot inject evidence, delete chapters or supply a forged model output through the review API. Corrections are display context and user testimony, not new evidence of expertise. Source facts remain unchanged.
4. **Career intelligence:** a second structured model request synthesizes stage capabilities, overall identity, core DNA, career evolution and personal recognition. This is four logical analysis layers in two structured model calls, not four paid requests by design. Prompts separate judgement, constraints and recurring patterns from activity lists, prohibit fabricated seniority and avoid a mandatory linear-promotion narrative. Use three to five core capabilities when supported, one or two rather than fill slots when evidence is sparse.
5. **Runtime validation:** strict object fields, length/cardinality bounds, English-script public copy, literal source quotations, unique stage/fact IDs, known evidence references and stage-local attribution. Every major narrative and capability carries evidence. Invalid output produces a retryable error; the selected document/review stays available. Evidence links establish provenance, not independent semantic entailment or career certification.
6. **Visual planning:** `preview/visual-design.js` maps professional domains to an artwork plan with stable IDs, semantic affinities, harmonious palettes, shared camera/light conventions and duplicate-aware variation. The `artworkProvider` field is the boundary for a future image provider; no real-time image generation is required or called.
7. **Rendering:** `preview/islands.js` builds six structurally different worlds: workshop, laboratory, connected archipelago, studio garden, elevated observatory and community. Terrain silhouette, elevation, buildings and environmental composition differ. These are original SVG compositions, not recolored copies. `journey.js` keeps labels/capabilities accessible outside artwork and draws responsive connecting paths. `dna.js` separately presents identity, core strengths, evolution and recognition.
8. **Request/session boundary:** `ai_server.py`, `ephemeral_sessions.py` and retained `request_state.py` provide same-origin requests, bounded concurrency before body reading, short-lived review memory, idempotent replay/conflict handling and cancellation-safe client state. Untrusted CVs never become executable HTML or SVG.

Retained: provider configuration conventions and quota guards, anonymous count schema/receipt deduplication, expiring request memory, rounded bundled fonts with OFL licenses, useful design assets and the purple/teal brand language. The assembled entry page is approximately 130 KB rather than the earlier multi-megabyte atlas/font-poster bundle; unused illustration assets remain in the repository for future reuse.

Removed from the active branch: PM-only gates/taxonomy, voice/transcription, text/URL onboarding, conversational Refine, poster editing/export logic, historical personal-data SQLite/admin server and obsolete alternate deployment entry points. V1 is recoverable from the baseline commit and existing production branches. Historical documentation remains clearly labelled as earlier releases.

## Changed file groups

| Files | Change |
|---|---|
| `ai_server.py`, `ai_transport.py`, `model_config.py` | Focused V2 API and profession-independent provider boundary |
| `document_parser.py`, `ephemeral_sessions.py` | Isolated reading and bounded private review sessions |
| `career_schema.py`, `career_intelligence.py` | Typed, source-linked extraction and four-layer intelligence pipeline |
| `preview/cv-upload.js`, `preview/studio.js` | One input path and one three-screen state flow |
| `preview/visual-design.js`, `preview/islands.js` | Semantic artwork plan and original modular miniature environments |
| `preview/journey.js`, `preview/dna.js` | Independent accessible journey and reflection rendering |
| `preview/studio.template.html`, `studio.css`, `index.html`, `build_preview.py` | Responsive English interface and self-contained bundle |
| `requirements.txt`, `Dockerfile`, `.dockerignore`, `render.yaml` | Linux parsing runtime and review-only same-origin deployment configuration |
| `tests/test_v2_*.py`, `tests/v2_fixtures.py`, retained `tests/test_counts.py` | Replacement QA for the new product contract |
| `tools/preview_v2.py`, `tools/evaluate_v2.py` | Clearly labelled synthetic preview and explicit live-model evaluation harness |
| `README.md`, `docs/v2/*`, `docs/DEPLOYED.md` | Audit, requirements, local instructions and deployment status |

## Three screens

- **Discover:** one PDF/DOCX file selector/drop zone, concise privacy copy, reading state, retry and lightweight chapter review. No alternative onboarding modes.
- **Career Journey:** connected miniature islands with company, role, period, up to four higher-order capability labels and expandable stage contribution/evidence. Unknown periods stay unknown.
- **My Career DNA:** professional identity, evidence-linked core capabilities, career evolution and a personal recognition statement. No rating, job matching, future prediction or generic coaching.

Desktop/mobile screenshots and a same-palette six-world contact sheet are included in the delivery directory. Screenshots use synthetic CVs and mocked AI transport; they are not presented as live model outputs.

## Verification results

**62 automated tests passed**, including real PDF/DOCX bytes through the isolated parser, HTTP server and Chromium UI. The final full suite completed in 14.273 seconds. After formatting and rebuilding, both complete desktop and mobile flows passed again (two smoke tests, 3.797 seconds).

```sh
python build_preview.py
python -m unittest discover -v
```

Coverage includes:

- Valid PDF/DOCX, malformed/unsupported files, blank/scanned PDFs, encrypted PDFs, oversized/long documents, too many pages, ZIP expansion and XML entity declarations.
- Technology, education, healthcare, design, finance and multilingual research fixtures; multiple jobs at one company, overlapping periods, career break and missing dates.
- Literal quotation grounding, fabricated references, wrong-stage attribution, repeated/missing stages, duplicated capabilities, sparse evidence, non-English-script public copy and unsafe display text.
- Review correction/reordering, missing/expired sessions, immutable session/cache values, replay, conflicting duplicate IDs, incomplete/refused model output and unchanged public quota behavior.
- Loading, cancellation without late result insertion, retry with preserved review, backward navigation without an unnecessary repeat analysis, dialogs and evidence links.
- Desktop 1440×900 / 1366×768, effective-zoom-size 1092×614, tablet 768×1024, mobile 390×844 and 320-pixel widths. No horizontal page overflow in tested fixtures. SVG artwork bounds remain fully within their viewboxes.
- Twelve stages receive twelve distinct family/variant combinations; six materially different environments are shown using the same palette, camera and lighting. Long role labels and four capability chips wrap without clipping.
- No browser script errors in the automated flows. Obsolete voice/refinement routes return 404. No external parser/font CDN request remains.

Both JSON schemas passed Draft 2020-12 schema checks. Python compilation, JavaScript syntax and Git whitespace checks passed. Docker packaging is prepared but a container build and real Render deployment were not performed.

## AI quality status and evaluation plan

There is **no OpenAI API credential configured in this task environment**. No production credential was retrieved, no real provider call was made and no production count was touched. Therefore this delivery does not claim that the new synthesis prompt has achieved the intended live model quality, multilingual accuracy, adversarial resistance, latency or cost.

The local pipeline and provider boundary are implemented. After securely configuring a local key, run:

```sh
python -m tools.evaluate_v2 --profiles technology education healthcare
```

This makes billable model calls under the existing daily attempt guard, writes per-stage token/time observations and synthetic outputs to `work/v2-live-evaluation/`, and never increments production creation counts. Human acceptance must check semantic evidence support, specificity, professional credibility, meaningful career connections, no seniority inflation and warm-but-restrained recognition. Merely passing literal-quote/reference checks does not satisfy that editorial review.

## Local testing and preview

Use Linux/Python 3.11+; the parser's process limits target the Linux production runtime.

```sh
pip install -r requirements.txt -r requirements-dev.txt
python build_preview.py
python -m tools.preview_v2 --port 10001
```

Open **http://127.0.0.1:10001** on the machine running the command. Download a synthetic CV from the visible preview banner and upload it. This design preview makes no AI calls, refuses non-synthetic CVs and disables production counting. It demonstrates design and interaction only. Screenshots can be viewed without running a server through the delivery gallery.

For real analysis, securely configure `OPENAI_API_KEY`, optionally the existing extraction/summary model variables, then run `python ai_server.py` and open **http://127.0.0.1:10000**. Keep production counting disabled for local testing. No key belongs in browser code, chat or Git.

## Privacy, deployment and known limits

- CV bytes are not stored on disk/database. Common contact details are redacted before model processing, but redaction is not exhaustive. Text, review context and facts go to OpenAI; provider/hosting policies are separate from application retention.
- Server extraction sessions and replay results use bounded process memory for up to ten minutes. Browser file/result memory is cleared on reset/replacement/navigation. Cancelling prevents stale UI commits but cannot guarantee that an already-running provider call stops or avoids billing.
- Existing optional production counters retain aggregates and expiring random-request receipt metadata, not CVs/results. Counts are not unique people. Public model-attempt limits remain unchanged; two structured calls plus moderation normally make one complete flow, so ten attempts is not ten visitors. Local guards reset on restart and are not durable billing caps.
- Maximum 5 MB, 15 PDF pages, 32,000 extracted characters and 12 stages. No OCR, legacy DOC or multilingual review correction UI; generated review fields are English and original-language quotes remain available as evidence. Parser resource isolation is Linux-specific.
- Vector worlds are a reliable composed MVP, not bespoke raster/3D artwork. Future image-generation integration has a clean boundary but no implemented provider. The catalogue is finite; visual sophistication can be refined without coupling artwork to analysis.
- Conversational Refine and exports are intentionally outside this new MVP, consistent with the specification's later-iteration sharing direction. V1's existing site remains available until replacement is approved.
- Browser tests use Chromium. Safari/device-specific file behavior, physical device testing, comprehensive accessibility certification and a live multi-user load test have not been performed.
- `render.yaml` is review-only and targets the existing API service with automatic deployment off. V2 uses same-origin `/api/v2/*` requests. A future approved rollout must serve V2 from that origin or configure an explicit proxy on the existing static frontend; simply replacing the static HTML would not connect its API. No rollout was attempted.
- Production release requires live AI editorial evaluation, review of the new design and explicit deployment approval. This branch does not represent a published replacement.
