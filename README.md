# PM Career DNA

An enhancement of the existing illustrated app: PM career intelligence, deterministic visuals and session-only conversational refinement. See [architecture and privacy](docs/CAREER_STUDIO_ARCHITECTURE.md), [visual acceptance standard](docs/PM_DNA_DELIVERY_STANDARD.md) and [observed live deployment](docs/DEPLOYED.md).

## Experience

1. Existing landing page → **Explore My Career DNA** → **Explore My PM Career**.
2. Upload a PDF/DOCX/TXT CV or use one editable text/voice composer. Uploads show filename/checkmark, removal and replacement, without a full CV preview. Legacy binary DOC and scanned PDFs require conversion/OCR.
3. **Generate** one English map. Evidence-backed role highlights lead to a maximum of four differentiated capabilities. Actual prior engineering/consulting roles remain truthful.
4. Return to the same composer → **Update My DNA Map**. Targeted changes preserve unrelated facts, IDs and visual configuration. Version selection and Undo restore earlier results; refining an older version creates a new branch revision.
5. Download one rounded-font landscape PNG. Maps, sources and up to30 versions remain only in browser/session and short-lived request memory, not a personal-data database. Refresh clears the browser history.

## Run

```sh
pip install -r requirements.txt
python build_preview.py
python ai_server.py
```

Set API credentials through server environment settings. The server binds to `0.0.0.0:$PORT` (default10000). `OPENAI_CAREER_MODEL` takes precedence over legacy `OPENAI_MODEL`; fallback is `gpt-5-mini`. Never infer the deployed model from a default: `/health` reports the effective non-secret selection. The renderer uses local assets and SVG; there is no per-map image-model request.

The existing Render services and private counter database are retained. No new hosting resources are required. The source is a public Git URL and uses explicit deploys after tested pushes. Do not apply historical Blueprints automatically or overwrite the existing key/model/quota/database variables. See [Render notes](docs/RENDER.md).

## Components

- `career_ai.py`: bounded schema, PM/transition interpretation, moderation, literal provenance and allowlisted refinement merge.
- `model_config.py`: separate career-model selection, token/latency observations and authenticated access diagnostics.
- `request_state.py`: five-minute request-memory replay, conflict/concurrent-request protection and timed content eviction.
- `generation_counts.py`: v2 production aggregates and expiring anonymous random-request receipts. Historical counts are preserved as unverified legacy totals.
- `preview/studio.js`: unified composer, browser file parsing/speech controls, session documents/version branches, retries and one detached export canvas.
- `preview/poster.js`, `pm-fonts.js`, `pm-library.js`: reference-style SVG, local rounded typography, exact glyph-outline PNG export, six themes and24 avatars/icons.
- `skills/pm-dna-editorial/SKILL.md`: runtime-loaded editorial requirements for challenge, judgement, specific practice and evidence.
- `build_preview.py`: self-contained committed HTML; the existing static host needs no extra asset-serving configuration. Font/illustration assets make it approximately12 MB.

## API and counting

Initial `/api/career-dna/generate` requests carry a random `request_id`. Refinements carry sources, selected structured map, `map_version`, `next_version`, instruction, context consent and a new request ID. Only declared changed fields are merged. Public requests cannot choose arbitrary benchmark models.

`PUBLIC_COUNTER_ENV=production` enables counting on the real API only. `PM_INTERNAL_TEST_TOKEN` identifies authorised synthetic tests and protects model/counter diagnostics; it is not embedded in the frontend. Duplicate logical requests replay temporary cached results and durable counter receipts prevent recounting after a restart. Only successful initial creations count; refinements, failures, clarifications, downloads and identified tests do not.

The old23-count aggregate included internal testing and cannot be reliably split. It is not reset or presented as genuine users. V2 starts a labelled new tracking period with a separate table. The database retains date/integer counts, start metadata and hashes of random request IDs/ordinals/timestamps for deduplication, never CVs or maps. Receipts expire after48 hours and are removed on the next counter access. Anonymous counts are not unique people and cannot independently identify undisclosed manual tests or bots.

The existing free Postgres expiry still applies. No paid plan was introduced. App processing is temporary; OpenAI and browser speech-provider retention policies are disclosed separately. `store:false` does not mean zero provider abuse-monitoring retention.

## Verification

```sh
python -m unittest test_ai tests.test_e2e tests.test_counts tests.test_session_architecture -v
```

The73 automated tests use the real HTTP boundary with only model transport mocked. They cover truthful prior-role labels, provenance, unified input, PDF/DOCX parsing, speech pause/resume/fallback, targeted updates and unrelated-field preservation, restoration/branch revisions, failure/retry state, count eligibility and idempotency, model configuration, typography, real foreground bounds, layouts and one PNG.

For opt-in real-project benchmarks, use `tools/benchmark_pm_models.py` with the deployment's test-token file (never an OpenAI key). It checks active-project model access, five synthetic PM profiles, role truthfulness, English/schema/evidence, latency, token-based cost estimates and test exclusion. Production observations and remaining limitations are recorded in DEPLOYED.md, not inferred from mock tests.

The historical optional research dashboard (`server.py`, `public/`, `launch.py`) remains outside this app's routes and deployment artifacts. It is not a new personal-data backend.
