# Career Studio: PM intelligence, session refinement and counting

This is an enhancement of the existing app. The hero, logo, animated background and illustrated map renderer are retained. Only the exploration CTA wording and downstream input/result flow change.

## Data and models

`OPENAI_CAREER_MODEL` overrides `OPENAI_MODEL`; when both are absent, `gpt-5-mini` remains the compatibility default. Never infer the deployed model from this default. The safe `/health` configuration reports the actual selected model. Authenticated `/api/internal/models` checks the active key's model list without disclosing it. Internal test harnesses may benchmark a listed model; public requests cannot select arbitrary models. Final observed model access, benchmarking and selection are recorded in DEPLOYED.md.

Python urllib calls `https://api.openai.com/v1/responses` with structured JSON schema, medium reasoning for interpretation/refinement and `store:false`. Moderation uses `/v1/moderations`. There is no OpenAI SDK and no runtime image-generation model. The local illustration assets, rounded fonts and deterministic SVG renderer remain the visual stage; the image never rewrites career claims. No image-model environment variable is necessary for this implementation.

The session document contains original source records, factual journey roles/quotes, supported or inferred capability categories, summaries, secondary practices with quotes, visual variant, version identifier, parent identifier and change summary. Maximum four independently evidenced roles and four capabilities. Prior engineering/consulting/data/operations roles retain truthful labels; they are not retroactively converted into PM jobs. A concrete product transition may be supported without claiming prior PM employment. Unrelated or aspirational-only material asks for more context.

## Input and refinement

CV parsing stays in the browser; files are not uploaded or saved. PDF, DOCX and TXT work; legacy binary DOC and scanned PDFs are explicitly unsupported because reliable parsing/OCR is unavailable. The UI shows filename/checkmark, removal and replacement, never a full CV preview. The source text remains in session memory.

One composer combines editable typing and final browser speech transcripts. Recording can stop, pause and resume. Browser support/recognition language varies; typing is always available. No separate transcript box or language selector. Real microphone capture remains a device/browser verification rather than a headless-test claim.

Initial `Generate` sends sources. After success, the same composer becomes an instruction entry point and the action is `Update My DNA Map`. Each update sends original/selected-version sources, the current structured map, base version and latest instruction. The API merges explicit changed-field paths and preserves unrelated values. An unsupported assertion or conflict can request clarification while keeping the selected map. Pure edits do not select new avatars/themes. A successful edit appends a session version; undo/selection restores its exact data, sources and visual configuration. Refining an older version creates a new serial version with that parent. The latest30 versions remain in page memory; refresh/navigation clears them. Combined source context remains bounded to22,000 characters and32 source records.

## Waiting, retries and privacy

The waiting animation is indeterminate. Elapsed time is real wall time, not a countdown or invented backend stage. At90 seconds, copy explains that input and previous versions are retained. Requests time out after five minutes on the client; cancellation stops waiting, not necessarily server work. Retry reuses the same logical request ID. A five-minute, bounded server-memory response cache prevents repeated model calls for completed retries; concurrent duplicates receive an in-progress response. It is cleared by timers and never written to disk. Payload fingerprints live only in this temporary cache. Existing model-attempt quota and two-request concurrency bound remain.

Keys remain server-only. No source, transcript or model text logging is introduced. `store:false` does not establish zero provider retention: OpenAI's published data controls describe abuse-monitoring retention and eligibility for additional controls. Privacy copy distinguishes app processing from provider and browser-speech policies. It does not promise that all providers save nothing.

## Public counter v2

The pre-existing counter was23 when investigated and release records confirm internal synthetic test generations were included. Date/integer aggregates cannot identify which entries were genuine production creations. The legacy table is preserved; it is not reset or relabelled as verified users.

V2 starts a separately labelled tracking period and excludes failed/clarification responses, refinements, downloads, local/staging environments and authenticated internal tests. `PUBLIC_COUNTER_ENV=production` is explicitly set only on the real API. `PM_INTERNAL_TEST_TOKEN` marks controlled production tests; it is generated server-side, merged into Render variables and never shipped to visitors. Requests without test identification are production traffic, not independently verified human/unique visitors. Anonymous counter logic cannot distinguish an undisclosed manual test or a bot from a visitor; no unique-user claim is made.

V2 stores daily integer totals, tracking start date and SHA-256 hashes of random request identifiers with assigned ordinal/time. Receipts contain no source/body hashes or personal content. They expire after48 hours and are deleted on the next counter access. PostgreSQL advisory locking makes insertion/deduplication/count assignment one transaction. Durable receipts prevent recounting retries even after response-cache loss or restart. The earlier date/count table remains untouched and its total is explicitly reported as unverified history. If the existing free database expires, persistent counting is unavailable; no new paid storage is created.

A restricted storage self-test verifies real PostgreSQL increment/deduplication under a force-rollback transaction, so synthetic tests cannot change the public count. Production model benchmarks and browser tests carry authenticated test markers. The counter is a creation count, not visitors, satisfaction or billing usage.

## Validation

73 automated tests cover the unified input, parser fallback, voice API pause/resume, targeted changes, versions/branch restoration, retry identity, preserved state on errors, public-vs-test counting, durable receipt semantics, model configuration/authentication, actual prior roles, provenance and existing map typography/collision/PNG checks. Real provider model access, five-profile benchmark, API cost estimates and the live browser flow are recorded after rollout. Model inference still requires editorial review; literal quotes prove provenance, not exhaustive semantic correctness.


Pure recognised theme/neutral-character requests take a deterministic visual-only path: career facts are copied unchanged, no career model is called, and no public creation count is added. The new presentation is versioned and can be undone. Mixed content/visual requests or arbitrary layout changes are not silently reinterpreted as permission to invent career capabilities.
