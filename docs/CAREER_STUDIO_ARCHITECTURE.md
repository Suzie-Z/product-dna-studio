# Career Studio: PM intelligence, session refinement and counting

This is an enhancement of the existing app. The hero, logo, animated background and illustrated map renderer are retained. Only the exploration CTA wording and downstream input/result flow change.

## Data and models

Career interpretation/extraction uses `OPENAI_CAREER_MODEL`; capability summarisation uses `OPENAI_SUMMARY_MODEL`; semantic refinement uses `OPENAI_REFINEMENT_MODEL`. Unset stage-specific choices inherit the career selection. `OPENAI_CAREER_MODEL` overrides `OPENAI_MODEL`; when both are absent, `gpt-5-mini` remains the compatibility default. Never infer the deployed model from this default. The safe `/health` configuration reports the actual selected model. Authenticated `/api/internal/models` checks the active key's model list without disclosing it. Internal test harnesses may benchmark a listed model; public requests cannot select arbitrary models. Final observed model access, benchmarking and selection are recorded in DEPLOYED.md.

Python urllib calls `https://api.openai.com/v1/responses` with structured JSON schema, medium reasoning for interpretation/refinement and `store:false`. Moderation uses `/v1/moderations`. There is no OpenAI SDK and no runtime image-generation model. The local illustration assets, rounded fonts and deterministic SVG renderer remain the visual stage; the image never rewrites career claims. No image-model environment variable is necessary for this implementation.

The session document contains original source records, factual journey roles/quotes, supported or inferred capability categories, summaries, secondary practices with quotes, visual variant, version identifier, parent identifier and change summary. Maximum four independently evidenced roles and four capabilities. Prior engineering/consulting/data/operations roles retain truthful labels; they are not retroactively converted into PM jobs. A concrete product transition may be supported without claiming prior PM employment. Unrelated or aspirational-only material asks for more context.

## Input and refinement

CV parsing stays in the browser; files are not uploaded or saved. PDF, DOCX and TXT work; legacy binary DOC and scanned PDFs are explicitly unsupported because reliable parsing/OCR is unavailable. The UI shows filename/checkmark, removal and replacement, never a full CV preview. The source text remains in session memory.

One composer combines editable typing with server-transcribed microphone recordings. MediaRecorder sends a bounded audio blob to `/api/transcribe`; `OPENAI_TRANSCRIPTION_MODEL` defaults to `gpt-transcribe`. Input language is automatic; original English/Mandarin/mixed text remains editable. There is no separate transcript box or language selector. Audio stays in request/browser memory, and the provider applies its retention policies. Failed audio can be retried with the same random request ID or explicitly discarded. Navigation cancels pending capture/upload. Devices lacking MediaRecorder fall back to browser speech recognition, whose language support depends on the browser.

Initial `Generate` sends sources. After success, the same composer becomes an instruction entry point and the action is `Refine My DNA`. Each update sends original/selected-version sources, the current structured map, base version and latest instruction. The API merges explicit changed-field paths and preserves unrelated values. An unsupported assertion or conflict can request clarification while keeping the selected map. Content edits do not select new avatars/themes. A successful edit appends a session version; undo/selection restores its exact data, sources and visual configuration. Refining an older version creates a new serial version with that parent. The latest30 versions remain in page memory; refresh/navigation clears them. Combined source context remains bounded to22,000 characters and32 source records.

## Waiting, retries and privacy

The waiting animation is indeterminate. Elapsed time is real wall time, not a countdown or invented backend stage. At90 seconds, copy explains that input and previous versions are retained. Requests time out after eight minutes on the client; cancellation stops waiting, not necessarily server work. Retry reuses the same logical request ID. A ten-minute, bounded server-memory response cache prevents repeated model calls for completed retries; concurrent duplicates receive an in-progress response. It is cleared by timers and never written to disk. Payload fingerprints live only in this temporary cache. Existing model-attempt quota and two-request concurrency bound remain.

Keys remain server-only. No source, transcript or model text logging is introduced. `store:false` does not establish zero provider retention: OpenAI's published data controls describe abuse-monitoring retention and eligibility for additional controls. Privacy copy distinguishes app processing from provider and browser-speech policies. It does not promise that all providers save nothing.

## Public counter v2

The pre-existing counter was23 when investigated and release records confirm internal synthetic test generations were included. Date/integer aggregates cannot identify which entries were genuine production creations. The legacy table is preserved; it is not reset or relabelled as verified users.

V2 starts a separately labelled tracking period and excludes failed/clarification responses, refinements, downloads, local/staging environments and authenticated internal tests. `PUBLIC_COUNTER_ENV=production` is explicitly set only on the real API. `PM_INTERNAL_TEST_TOKEN` marks controlled production tests; it is generated server-side, merged into Render variables and never shipped to visitors. Requests without test identification are production traffic, not independently verified human/unique visitors. Anonymous counter logic cannot distinguish an undisclosed manual test or a bot from a visitor; no unique-user claim is made.

V2 stores daily integer totals, tracking start date and SHA-256 hashes of random request identifiers with assigned ordinal/time. Receipts contain no source/body hashes or personal content. They expire after48 hours and are deleted on the next counter access. PostgreSQL advisory locking makes insertion/deduplication/count assignment one transaction. Durable receipts prevent recounting retries even after response-cache loss or restart. The earlier date/count table remains untouched and its total is explicitly reported as unverified history. If the existing free database expires, persistent counting is unavailable; no new paid storage is created.

A restricted storage self-test verifies real PostgreSQL increment/deduplication under a force-rollback transaction, so synthetic tests cannot change the public count. Production model benchmarks and browser tests carry authenticated test markers. The counter is a creation count, not visitors, satisfaction or billing usage.

## Validation

86 automated tests cover the unified input, parser fallback, voice API pause/resume, targeted changes, versions/branch restoration, retry identity, preserved state on errors, public-vs-test counting, durable receipt semantics, model configuration/authentication, actual prior roles, provenance and existing map typography/collision/PNG checks. Real provider model access, five-profile benchmark, API cost estimates and the completed live browser flow are recorded in DEPLOYED.md. Model inference still requires editorial review; literal quotes prove provenance, not exhaustive semantic correctness.


Pure recognised theme/neutral-character requests take a deterministic visual-only path: career facts are copied unchanged, no career model is called, and no public creation count is added. The new presentation is versioned and can be undone. Mixed content/visual requests or arbitrary layout changes are not silently reinterpreted as permission to invent career capabilities.

The scope prefilter also recognises common actual PM titles in Spanish, Portuguese, French, German, Japanese, Korean, Arabic, Vietnamese and Russian, rather than requiring English titles in multilingual CVs. The model still assesses factual scope. Both Retry and the primary generation action reuse the pending logical request identifier until input changes.

## V2 fact and patch stages

Generation first extracts up to12 evidence-grounded facts in a separate structured request. A second, independently configured request consolidates those facts into1–4 actual roles and1–4 capabilities while still citing original source passages. Each stage gets at most one bounded repair. Higher-level demonstrated frameworks, zero-to-one infrastructure and difficult decision lenses take precedence over operational project names. A first-person factual correction adds source testimony; a requested credential does not prove it. No provider failure causes a silent model downgrade.

Refinement returns a typed change list using stable item IDs. Nested highlight edits replace the bounded highlights array, including each detail’s own literal source quote. The server attaches new detail evidence to its parent automatically and validates the merged map. It copies unrelated fields instead of accepting a rewritten full map. A phrase up to64 characters can express `0-to-1 Safety Pipelines & Infrastructure`; the renderer measures the actual text to reserve enough space. Explicit Version1 instructions select Version1 even if another version is visible. Each successful edit creates a new revision with that base as its parent.

The V2 renderer removes the two corner clouds, measures title width to centre it on the full canvas, and places the logo beside it. Sprite viewports preserve source aspect ratio without exposing adjacent atlas cells. Semantic icon selection, six coordinated themes,24 neutral avatars and left/right character layouts provide controlled variation. Text-only edits retain the exact variant. Map height responds to actual highlights/dates; PNG width remains3200 pixels and height is twice the measured1600-pixel-wide scene. One SVG and one downloadable PNG remain.

Public model-attempt quota remains10/day and is separate from authenticated internal verification (bounded40/day). Two-stage initial creation normally consumes two attempts; each refinement or recording consumes another, and repairs consume attempts too. Moderation is a separate safety service. These limits reset with the process and are not a durable billing cap. Public map counts measure successful initial creations only, not API attempts or unique visitors.
