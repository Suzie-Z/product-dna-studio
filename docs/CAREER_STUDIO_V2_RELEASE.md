# Refinement reliability patch — 12 November 2026

- The Refine composer now gives an English copy-and-replace example using the original phrase and intended replacement. Long replacements are summarised to the existing field limits.
- Unique quoted phrases resolve to a single allowlisted field. The model receives only that item and associated evidence rather than a complete CV/map, plus a compact edit prompt. Other fields are copied unchanged.
- Refinement no longer requires old valid literal quotes to appear in newly sampled citation enums. Source-ID bounds and independent original-text validation still apply. Repeated edits retain necessary detail proofs and the original anchor within the six-quote bound.
- Text overflow is measured on both desktop and mobile before a new result replaces the old map. A bounded, field-only shortening request runs when required; it keeps existing factual citations. The old in-image “Regenerate for shorter wording” placeholder is removed. Three-line capability titles have reserved space with no icon/text collision.
- Refinement remains an AI call and consumes tokens; small edits avoid the two-stage career-generation pipeline. Optional shortening/validation repair can require an additional small call. No model, public quota or infrastructure plan was changed.

---

# Career Studio V2 — verified release

Published 12 November 2026 (Australia/Sydney).

Live app: https://product-dna-studio-preview.onrender.com

Runtime commit: `e21394da064010e4392ed84665533f7eb2e11d72`. Existing API deploy `dep-dbqlph5bedkc73e1hidg` and frontend deploy `dep-dbqlplajnfac7393ah7g` both reached `live`. The public HTML matched the tested bundle byte for byte. No new hosting/database service or paid compute plan was introduced.

## Product and architecture

The existing landing composition, logo, animated orbs and exploration-first interaction remain. The brand is Career Studio. The unified composer supports a filename/checkmark-only CV, typing and editable microphone transcripts; no full CV preview or separate voice box is rendered. Generate/Analysing, Refine My DNA/Updating and Download DNA Map provide the main flow.

Career interpretation/extraction and capability summarisation now run as distinct structured requests. Each fact/highlight/practice cites original source text. The second stage consolidates higher-level judgement, frameworks and system-building where evidenced; sparse material is not padded. Maps contain1–4 actual roles and independently1–4 capabilities. Prior Software Engineer and Business Consultant roles remain truthful, rather than becoming fictitious PM positions. Capability cards support up to three specific, evidenced practices.

Conversational refinement uses semantic, typed patches against stable item IDs. Explicit first-person corrections add source testimony. Only declared fields are merged; new detail citations are attached to their parent evidence automatically. Version1 can be selected in natural language even when Version2 is visible. Successful changes append a new revision; selection and Undo restore data and presentation. Unsupported credential requests ask for evidence and retain the map. Simple theme/neutral-avatar requests make no model call.

The renderer remains deterministic SVG/local illustrations, with exact rounded-font glyph outlines for PNG. It removes both top corner clouds, centres the title against the full canvas, keeps the logo close, measures highlights before laying out islands and uses semantically selected complete icons. Sprite viewports now match source aspect ratios, preventing adjacent atlas artwork from appearing in letterboxed areas. Six coordinated palettes,24 neutral avatars and left/right character layouts provide controlled variety. Text edits retain the selected variant. There is one visible map and one PNG per download.

## Actual models and configuration

| Stage | Before V2 | Current verified selection |
| --- | --- | --- |
| Career interpretation/extraction | Unified `gpt-6.1-sol` request | `gpt-6-astra` |
| Capability summarisation | Same unified request | Separate `gpt-6-astra` request |
| Refinement | `gpt-6.1-sol` | `gpt-6-astra` |
| Speech | Browser speech provider | `gpt-transcribe`; browser compatibility fallback |
| Runtime image model | None | None; existing local assets/SVG retained |
| Safety moderation | `omni-moderation-latest` | Unchanged |

The four stage selections were merged into the existing Render API environment as `OPENAI_CAREER_MODEL`, `OPENAI_SUMMARY_MODEL`, `OPENAI_REFINEMENT_MODEL` and `OPENAI_TRANSCRIPTION_MODEL`. Existing API secret, legacy `OPENAI_MODEL=gpt-5`, private database connection, quota and trial schedule were preserved. Configured model failures do not silently downgrade to GPT-5 or Sol. Python urllib calls the APIs directly; no SDK-version assumption is required.

Authenticated active-project diagnostics listed Astra, Sol and GPT-Transcribe as available. Successful real structured calls confirmed Astra on career, summary and refinement response metadata. Real transcription requests accepted `model=gpt-transcribe` and returned transcripts; the transcription response does not independently guarantee an echoed model identity. The public client cannot select benchmark models or read credentials.

## Trust & Safety regression

The original failed visitor draft was not retained, so its precise historical failure cannot be recovered. Three old verification-chain blockers were reproduced: a30-character highlight limit could not accept the required40-character pipeline label; nested array-index edits were unsupported; new correction quotes failed when their parent evidence associations were not updated.

V2 allows complete role-highlight phrases up to64 characters, uses stable-ID typed highlight-array changes and attaches new detail evidence before validating the merged map. One bounded repair remains available; a valid first-person correction is not rejected merely because it was absent from the CV.

The exact English request produced:

- Safety Framework Development
- 0-to-1 Safety Pipelines & Infrastructure

The Chinese request produced English capability-level highlights, including Safety Framework Development and 0-to-1 Safety Pipeline Development. Its equivalent wording was accepted rather than treated as a failure. Both targeted the correct Trust & Safety role. Other roles, capability cards, icons, palette and avatar were unchanged. The target’s evidence note was updated to reflect the new testimony; the Chinese edit also synchronised that target’s legacy/accessibility description. These target-local provenance updates are distinguished from unrelated visible changes.

## Verification

86 local automated tests passed. Coverage includes schema/provenance, literal multilingual quotes, targeted patches, PM scope and transitions, PDF/DOCX/TXT parsing, upload removal/replacement, browser speech compatibility, audio signature/size checks and replay, separate stage configuration, internal/public quotas, versions/branch restoration, retry state, public counting, independent1–4 cardinalities, long highlights, actual foreground bounds, typography and outlined PNG export.

Seven real two-stage generations covered five PM backgrounds, with paired Astra/Sol comparisons on AI PM and consulting-to-PM. All passed independent schema/evidence and desktop/mobile renderer checks. Six themes and both avatar-side layouts were exercised; no foreground collisions, clipped illustrations or mobile horizontal overflow were found in those cases.

Public-site browser checks used a synthetic CV and the real API: MediaRecorder fake-device audio → original-language editable transcript → multilingual input → Astra initial map → exact English edit → Chinese edit explicitly based on Version1 → correct branch. Undo/restoration, unsupported-credential clarification, a no-model colour update, retry replay, one PNG download and phone layout also passed. The export/restoration continuation loaded the recorded synthetic session documents to avoid repeating paid model calls; original generation and both text edits were genuine UI-driven API calls. No physical-microphone quality claim is made from headless tests.

The downloaded file was decoded and visually inspected: **3200×2400**, one PNG, outlined rounded typography, no foreground overlap or clipped illustrations. Height is content-aware rather than a fixed square/format choice. Navigation/refresh clears session history; no browser errors or local storage were observed.

Separate real Mandarin, English and mixed Mandarin/English recordings all preserved their spoken languages and PM terminology. Mixed-language text remained intact even when the provider language metadata listed only Chinese. Replay returned the same transcript without a second transcription. Final map display content stayed English.

## Counts, privacy and cost

The earlier23-count aggregate included internal testing. Date/integer history cannot reliably distinguish each genuine creation, so it remains preserved as unverified history. The existing separate production counter was1 before this release’s verification and remained1 afterward; it was not reset. Refinements, downloads, clarifications, failures, retries and authenticated tests did not add creations. A real PostgreSQL force-rollback check verified increment/deduplication and left no test write behind. Counts represent creations, not unique people.

No CV/map/audio is written to the counter database. Sources, audio and results use browser/request memory. The bounded replay cache retains results for up to10 minutes; random counter receipt hashes expire after48 hours and are removed on the next counter access. OpenAI/browser speech and hosting providers apply their own policies; `store:false` is not a promise of zero provider retention.

Astra’s five two-stage benchmark generations took28.49–50.66 seconds (median40.9), estimated US$0.167–0.212 each. The richer three-role live example took62.42 seconds in the API and approximately US$0.3025. Its English and Chinese updates took11.02/13.04 seconds and approximately US$0.1802/0.2037. Sol’s two paired generations took31.01–37.87 seconds and approximately US$0.036–0.037. This small sample supports grounded output from both models, not universal Astra superiority; Astra remains selected because the requested priority is quality. Full records and rate methodology are in [the benchmark report](PM_MODEL_BENCHMARK.md).

Transcription’s documented rate is US$0.0045/minute. The separate8/5/12-second speech cases together represent approximately US$0.001875, excluding the synthetic test-only TTS fixture. Estimates include observed text cache writes and reasoning output, exclude taxes/hosting, and are not invoices or timing guarantees.

The existing **10 model-attempts/day** process-memory limit was not raised. An ordinary initial map now uses two attempts; an update or recording uses another, and repairs consume attempts. Thus this is not ten visitors or ten complete maps, and restart resets the guard. The20/day figure remains an observation target, not an increased quota. No durable provider billing cap was added.

## Remaining limits and review artifacts

Legacy binary DOC needs conversion, scanned PDFs need OCR, and browser parsing depends on the CDN. Physical microphone quality, accents/noise and every mobile/Safari version still need device testing. The current free Postgres retains its original30-day expiry. Model interpretations remain subject to review; literal provenance is not independent proof of competence. The backup Docker file list and ignore rules were repaired and checked by importing the isolated packaged runtime; the published service remains native Python, and no Docker deployment was performed.

Local synthetic artifacts are in `/workspace/deliverables/career-studio-v2/`: initial/refined/mobile/theme screenshots, one downloaded PNG, model access, voice and visual verification JSON. Raw synthetic requests, responses and benchmark token metrics remain under ignored `work/v2-verification/`. They contain no uploaded visitor CVs or API keys.

- [Initial map](/workspace/deliverables/career-studio-v2/initial-map.png)
- [Exact English refinement](/workspace/deliverables/career-studio-v2/english-refined-map.png)
- [Chinese refinement](/workspace/deliverables/career-studio-v2/chinese-refined-map.png)
- [Alternate coordinated theme](/workspace/deliverables/career-studio-v2/alternate-theme-map.png)
- [Mobile map](/workspace/deliverables/career-studio-v2/mobile-map.png)
- [Downloaded PNG](/workspace/deliverables/career-studio-v2/my-pm-career-dna.png)
- [Live verification](/workspace/deliverables/career-studio-v2/live-verification.json)
