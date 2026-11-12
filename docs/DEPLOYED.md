# Career-fact validation patch — published12 November2026

Backend `db6dcf78f0aa7a6b557b0f68b2d06c6d9e9918b3` is live.96 automated tests and two real Astra generations passed. [Cause, fixes and verification](FACT_VALIDATION_FIX.md). Frontend, model selections and quota are unchanged.

---

# Refinement reliability patch — published12 November2026

[Live application](https://product-dna-studio-preview.onrender.com) · [verified changes and token costs](REFINEMENT_RELIABILITY_FIX.md). Runtime `0f5d51a72d30da9df0b05161abb175fb4513e8a4` is live on both services. Copied-text edits use field-scoped context; overlong copy is shortened before display. Real API and browser Refine → Version2 → PNG verification passed.

---

# Career Studio V2 — published 12 November 2026 (Australia/Sydney)

https://product-dna-studio-preview.onrender.com

Runtime `e21394da064010e4392ed84665533f7eb2e11d72` is live on the existing services. All three text stages now use `gpt-6-astra`; multilingual voice uses `gpt-transcribe`. The preserved landing, semantic refinement, version branching, visual variation and one PNG download were verified.86 automated tests and real provider/browser verification passed. The production counter remains1 and legacy23 is preserved; the existing10-attempt limit is unchanged.

See the [complete V2 release record](CAREER_STUDIO_V2_RELEASE.md) for actual model verification, latency/cost, the Trust & Safety regression, privacy, screenshots and limits. No further user configuration is required.

---

## Historical releases

# Career Studio architecture enhancement — published 11 November 2026 (Australia/Sydney)

https://product-dna-studio-preview.onrender.com

- Final runtime commit `eb8b4ebc1c6ea9be49534c5357fa2ce8f7108b67` is live on both existing services: API `dep-dbq5vgbm8hqs739ufeh0`, static frontend `dep-dbq5vijrjlhs73bblb00`. Served HTML matches the tested bundle exactly. No new hosting/database resources were created.
- Existing hero, logo, animations and map identity remain. The CTA is Explore My Career DNA; input is introduced below the landing page. Filename/checkmark CV upload and one editable text/voice composer replace full CV previews and separate transcript boxes. Generate and Update My DNA Map are the main actions. Speech supports stop/pause/resume where the browser supports recognition.
- Original sources, selected structured map, new instruction and version identifiers drive allowlisted targeted updates. Version selection, Undo and branching from an older version preserve sources and presentation. Recognised pure theme/neutral-character edits update presentation without a model call or career-content change. One selected map and one PNG remain.
- **Actual text model: `gpt-6.1-sol`**, confirmed by both non-secret live configuration and provider response metadata. New `OPENAI_CAREER_MODEL` takes precedence; original `OPENAI_MODEL=gpt-5`, key, quota, private database connection and trial schedule are retained. `PUBLIC_COUNTER_ENV=production` and a server-only `PM_INTERNAL_TEST_TOKEN` were added for accurate public-vs-test accounting. No secret is in the frontend. No user configuration is required for this release.
- **Runtime image model: none.** Visuals use the existing local illustrations, rounded fonts and deterministic SVG/glyph-outline PNG renderer. The active project lists `gpt-image-2.6-sunburst`, but no runtime image call was introduced. Career text is never rewritten by an image model. Provider transport is Python urllib against `/v1/responses` and `/v1/moderations`, with `store:false`.
- Seven real model benchmarks covered five synthetic PM backgrounds and paired Sol/Astra comparisons on AI PM and consulting-to-PM. Both preserved actual non-PM prior roles; no material category/factual benefit from Astra was observed in these two pairs. Sol’s five cases took18–28 seconds at approximately US$0.023–0.029 each; Astra pairs took30–37 seconds at US$0.143–0.155. Estimates include observed cache writes and reasoning/output tokens. All seven outputs passed desktop/mobile renderer checks after a long-highlight wrap regression was fixed. See [benchmark details](PM_MODEL_BENCHMARK.md).
- Complete real-provider browser flow passed: landing → filename-only CV plus Chinese notes → English initial map (23.55s, estimatedUS$0.033651) → wording-only title update (19.8s, estimatedUS$0.032511) → Undo/exact version restoration → pure-theme version (no model call) → one PNG → phone layout. The targeted update changed only `/strengths/k1/label`; every other field was equal. Provider model metadata reported `gpt-6.1-sol`. No foreground overlaps, duplicate DOM canvases, horizontal overflow, browser errors or local storage were found.
- Final deployed-code verification additionally used a Spanish-only CV with no English PM title or typed supplement. It produced an English map in about24 seconds and estimatedUS$0.027633. A controlled first-request HTTP failure preserved the CV; retry through the primary button sent exactly the same body/request ID. The single result and PNG passed desktop/mobile checks. Source/file parsing, voice API controls, error state and both retry controls are covered by74 automated tests.
- The old persistent total was **23**, confirmed through the API; release history proves it includes internal testing, while date/count-only rows cannot identify a reliable human subset. The legacy table remains untouched. V2 starts a visibly labelled new period at0, with authenticated test exclusion, production-only eligibility and atomic random-request receipt deduplication. Refinements/downloads/failures/clarifications do not count. After all real tests, public v2 remained0 and legacy remained23. A real PostgreSQL increment/replay self-test passed under force rollback, with no synthetic count persisted.
- Privacy copy now distinguishes temporary app/session processing from provider retention. Browser history is session-memory only; the server has a five-minute bounded response replay cache. Counter storage contains aggregates and expiring random-request receipt hashes/ordinals/timestamps, not CVs or maps. Receipt expiry is48 hours, with deletion on the next counter access. No source/body logging or new personal-data database was added.

Remaining boundaries: binary DOC and scanned PDFs need conversion/OCR; microphone recognition is browser/device-dependent and real capture is not claimed from headless mocks. The counter is anonymous successful server-ready creations, not unique humans or guaranteed downloads; undisclosed manual tests/bots cannot be independently identified. Source interpretation and the small benchmark are not independent fact certification. Existing process-memory provider quota and free-database expiry remain; no paid-plan change or durable billing cap was introduced.

See [requirements](CAREER_STUDIO_REQUIREMENTS.md), [architecture](CAREER_STUDIO_ARCHITECTURE.md), [limits](LIMITATIONS.md), [configuration](RENDER.md) and [model benchmark](PM_MODEL_BENCHMARK.md). Local synthetic artifacts: `/workspace/work/pm-session-live/`, `/workspace/work/pm-spanish-live/`, `/workspace/work/pm-model-benchmark/`.

---

# Reference-quality PM identity map — published 11 November 2026 (Australia/Sydney)

https://product-dna-studio-preview.onrender.com

- Runtime commit `b663c1f4bb631b74573d4c1859199a21ae3f8dfe` is live on both services: API deploy `dep-dbq3one7bikc73bv8sf0`, static deploy `dep-dbq3op8n74is739ktm40`. Served HTML matches the tested bundle exactly.
- [Delivery acceptance standard](PM_DNA_DELIVERY_STANDARD.md) defines challenge/differentiation, professional judgement, specific practices, evidence, rounded type and sample fidelity. Promotional samples must be actual downloads from this app. The runtime [editorial skill](../skills/pm-dna-editorial/SKILL.md) incorporates these requirements.
- New generations show one or two source-backed highlights per role. The compact role/highlights/date/island grouping replaces detached generic descriptions. Capability cards present Title Case strengths, judgement sentences and zero to three concrete practices; richly evidenced test profiles produced two or three per card. Sparse evidence remains sparse rather than being padded.
- Locally bundled Fredoka headings and Nunito body type replace Arial in the map. PNG exports use exact matching glyph outlines, avoiding image-font fallback. On-page SVG text remains selectable; one landscape output and one PNG remain. PNG dimensions are 3200×2100 without dates, 3200×2180 with dates.
- 61 automated tests passed, including highlight provenance and bounds, generic-practice rejection, font/glyph advance matching, outlined export, multilingual and old-map compatibility, real painted bounds in both layouts, cardinality/method-count combinations, CV/voice input, variants, generation/download and aggregate counts.
- Complete production browser flow passed with real OpenAI calls and synthetic rich PM experience: non-PM clarification without count → multilingual CV → English map → one PNG → Chinese requirements in original input → regeneration → phone layout. Both ready maps had two highlights for every supported role, two or three complementary practices per capability, and a concrete AI decision lens. Both desktop/mobile had one result, zero DOM export canvases, no foreground collisions, no horizontal mobile overflow or browser errors/local storage. Download retained variant and did not increment counts.
- Actual AI card: `AI Product Judgement` → `Judge model boundaries and de-risk product fit before rollout.` → `Model capability review`, `Golden-set evaluation`, `Failure analysis`. Platform card: `Balance reusable capabilities with reliability and extensibility.` with `Product contracts` / `System design reviews`. These are observations from the synthetic test input, not guaranteed claims about every visitor.
- Medium reasoning now supports the editorial generation in the same existing provider call; this can increase latency/token consumption. Existing model, server-side credentials, daily attempt quota, pilot date, free hosting and numeric-only persistent count are unchanged. No user content storage or extra editorial/image-model call was added. Test generations are included in totals.

Local synthetic verification: `/workspace/work/pm-reference-live/report.json`, `first-map.json`, `regenerated-map.json`, downloaded PNG and desktop/mobile screenshots. The PNG itself was visually reviewed for rounded typography, content density and hierarchy. These artifacts were not published as the owner's personal career claims.

---

# Compact, deeper PM DNA — published 11 November 2026 (Australia/Sydney)

https://product-dna-studio-preview.onrender.com

- Frontend and API commit `623f7e9664171474568796d65ae81a806fbf091c` are live. Static deploy `dep-dbq1s89srm7s7398kk20`; API deploy `dep-dbq1s62jnfac73erie00`. The live HTML matches the tested bundle byte for byte.
- Desktop map height reduced from 1290 to 1080 (about 16%); one downloadable PNG is now 3200×2160. Tightened role/icon/description/island spacing while keeping reserved dates and readable desktop/mobile copy.
- Runtime loads [PM editorial skill](../skills/pm-dna-editorial/SKILL.md). Cards now combine a capability title, decision-value sentence and zero to three concrete source-backed methods. No methods are added to fill slots. All labels pass display safety; each method has its own associated verbatim source quote. Selected named techniques require explicit mention or supported multilingual equivalent in their own quote. Citations establish provenance, not independent certification or exhaustive semantic verification.
- 56 automated test methods passed. New coverage includes method provenance, specialist-name grounding, multilingual evidence/English labels, older-map compatibility and 128 dated layout/card/method-count combinations. Actual foreground geometry, parsing, voice fallback, single-result/download, variants and counter checks remain covered.
- Complete production browser flow passed with synthetic PM experience and real OpenAI calls: non-PM clarification without count, multilingual CV upload, English map, one PNG download, Chinese requirements through original-input regeneration, changed avatar/theme, phone layout, no foreground collisions or browser errors/local storage. Downloads retain the variant and do not increment the persistent aggregate count.
- Real regenerated AI card: `AI product judgement` → `Assess model fit and failure modes for product use` → `Golden-set evaluation` / `Failure analysis`. Growth methods: `Funnel analysis`, `Controlled experiments`, `Root-cause analysis`. These came from the synthetic test CV, not an assertion about every visitor.
- Existing hosting plans, server-side credentials, quota and pilot schedule are unchanged. No input/output persistence, second image, manual editor or extra image-model call was introduced. Counts include verification generations.

See [implementation](PM_IMPLEMENTATION.md). Local synthetic screenshots, maps, PNG and report: `/workspace/work/pm-editorial-live/`.

---

# PM Career DNA — published integrated release — 11 November 2026 (Australia/Sydney)

https://product-dna-studio-preview.onrender.com

- Frontend commit `ccaf0f0b529aea02495b384c771adac081cc318c`, deploy `dep-dbq086u7bikc73bksovg`: live. Served self-contained HTML matches the committed bundle.
- API commit `437a42ed39eb6c31bd7e3337415c5a9cbe541f16`, deploy `dep-dbq0jtek1f9s73d8eedg`: live. A previous rollout timed out before process startup; retrying the same tested commit succeeded.
- PM-only branding, PM/DNA logo, actual PM role taxonomy, 24 neutral avatars, 24 product-scene icons and six theme palettes are integrated into the application. Earlier handoff-only descriptions below are historical.
- One visible SVG result; detached export canvas; one 3200×2580 `my-pm-career-dna.png`. New generation chooses a fresh avatar/theme; resize and download retain it. No manual editor, format selection or duplicate result.
- 49 automated test methods passed: 46 backend/browser tests plus three aggregate-counter tests. Coverage includes all 64 dated/undated desktop/mobile cardinality combinations, actual clipped foreground geometry, 24 avatar variants, six-theme rotation, PM scope, evidence, input parsing, voice fallback, regeneration and download.
- Complete production browser flow passed using synthetic PM experience and real OpenAI calls: non-PM clarification without count → multilingual CV → English PM map → PNG download → Chinese original-input changes → regeneration → phone layout. Result roles: Growth PM, Operations PM, Platform PM, AI PM. Capabilities: Growth experimentation, Workflow design, Platform systems thinking, AI product judgement. Desktop and mobile report no foreground collisions, one map, zero DOM export canvases, no horizontal mobile overflow and no browser errors/local storage.
- Date captions now require source-supported years/intervals; invalid optional captions are omitted instead of blocking valid maps. Role/capability provenance requirements remain strict.
- Existing free services, server-side credentials, persistent numeric aggregate counter, daily provider-attempt limit and pilot schedule are unchanged. Successful test generations are included in total counts; download does not increment them. No visitor CV/story/map storage was added.

See [implementation and limits](PM_IMPLEMENTATION.md). Local synthetic verification artifacts are in `/workspace/work/pm-live/report.json` and accompanying screenshots/PNG (not user data and not publicly published).

---

# Single-visible-result correction — 11 November 2026 (Australia/Sydney)

https://product-dna-studio-preview.onrender.com

- Frontend commit `4f10ae209759f1be412a8a28d07e18cb1b8ec704`, deploy `dep-dbpucd0u01pc73992fm0`: live.
- Confirmed the actual duplicate-output bug in the production browser: one visible SVG PLUS one visible export canvas. The global `canvas {display:block}` overrode the canvas `hidden` attribute. Previous SVG-count-only verification missed this. Those older one-result claims were incorrect.
- Export canvas is now detached from the DOM. Removed global canvas display rules and added an explicit hidden-attribute guard. Production rendering verification now reports one visible SVG root, zero DOM export canvases, zero visible export canvases. PNG download passed and phone resizing still leaves a single map. The API was not redeployed because the fix changes only frontend behavior.
- Four browser regression tests passed with the stronger absence-of-DOM-canvas assertions, CV/voice input, regeneration and PNG download checks. Production rendering verification uses a synthetic map fixture and does not claim a new real-provider generation test or increment production counts.
- A separate Codex PM correction handoff was prepared: actionable requirements, 24 character sprites, 24 internet-PM icons, 6 theme palettes, 15 PM role categories, reference-archetype mappings and both original reference images. The generated atlases have 256px native cells; crop and high-resolution use require the documented checks. These libraries and the PM-specific selection/semantic changes are prepared for integration, not claimed as already implemented on the live site.

See [Codex PM correction standard](CODEX_PM_CORRECTION_STANDARD.md).

---

# Reference-fidelity illustrated world — 11 November 2026 (Australia/Sydney)

https://product-dna-studio-preview.onrender.com

- Runtime commit `523b99f3dc3cfdc07c962051c52b4d07069335c9` is live on both services. API deploy: `dep-dbptll0ae00c73clk920`; static deploy: `dep-dbptma1srm7s738rkutg`. Served HTML matches the committed bundle exactly.
- Replaced the previous vector approximation with an actual local 3D illustration library: cheerful gender-neutral human chibi, sculpted rocky floating islands, glossy career symbols, clouds, greenery and flowers. Rebuilt the original two-band illustrated composition with glowing journey/bridge paths and dimensional capability cards. The original My Product DNA reference and full-result screenshots were reviewed side by side; desktop and phone screenshots are in ignored test artifacts.
- Each generation displays exactly one responsive map root, not desktop/mobile alternatives side by side. One Download button exports one 3200×2360 PNG. Actual illustration pixels survive PNG export. No square/portrait chooser, manual map editor, alternate second image or extra AI image call per visitor was introduced.
- Added the requested read-only View Full Journey, showing evidence and optional original context in browser memory. It causes no content persistence or API request and does not add another result.
- Strengthened job-family versus project-activity abstraction and transferable capability generation. Known activity headings and capabilities repeating journey headings receive bounded repair feedback. Evidence-grounded 1–4 independent counts and literal quote/source constraints remain.
- 43 automated tests passed across backend, parsing, voice fallback, regeneration, source safety, one-result rendering, read-only evidence, all 32 cardinality/layout combinations, counter behavior and PNG download. Production browser verification with real OpenAI calls passed generation, Chinese original-input regeneration, single PNG download, phone layout and evidence disclosure, with no browser errors.
- Final real synthetic-profile test returned Software Engineering, Platform Engineering and Data Analytics, with Systems & Platform Design, Reliability Analysis and Evaluation Judgement. These are interpretive categories derived from submitted test experience, not independently verified jobs or qualifications.
- Existing free compute, configured key, persistent aggregate counter, daily call limit and pilot date were retained. No infrastructure resources were created or changed. Total counts include verification generations; downloads do not increment them.

See [visual fidelity implementation](VISUAL_FIDELITY.md).

---

# Simplified illustrated-map update — 11 November 2026 (Australia/Sydney)

https://product-dna-studio-preview.onrender.com

- Frontend commit `2fa3400f1d9bd9e3c05a976203e4dedfee896f1a`, deploy `dep-dbpsr4bl550s738r44hg`: live. The served HTML matches the committed bundle byte for byte.
- API commit `6a8a3c4d910277dab89a927a235037b9154276a1`, deploy `dep-dbpsv01srm7s738pbbl0`: live.
- New supplied AI/helix logo design, empty story placeholder, shortened privacy copy, no format selector, no separate refinement section, no manual map editor. The result ends with one Download PNG button. Changes are requested through the original input and regenerated by AI.
- Controlled pastel SVG illustration: career islands, two-band composition, neutral toy explorer, selectable English text, stacked mobile layout, and fixed 3200×2008 PNG. Each list is independently 1–4 items based on evidence, not slot filling.
- 42 automated tests passed. All 32 desktop/mobile cardinality combinations passed along with CV parsing, voice fallback, clarification, regeneration, XML escaping, overflow handling, download and count tests. Legacy API safety tests remain covered, but there is no legacy editing UI.
- Real production browser checks passed: multilingual CV upload → grounded English map → PNG → Chinese requirements in original input → regeneration → stacked mobile preview. The final test produced 3 journey nodes and 3 strengths, with no browser errors. Download did not increment counts.
- A real mixed-source regeneration exposed an incorrectly paired citation. The final API constrains quote/source pairs to pre-extracted exact passages in its decoding schema; independent provenance/safety checks remain in place. Precise safe field feedback covers other bounded repairs. No input, output or quote logging was added.
- The existing free persistent counter was already active before this release. Its count survived deployments; total observed after verification was 5, including four successful synthetic test maps generated during this update. Counts include testing and do not represent unique visitors. Existing credentials, AI call limit and pilot schedule were preserved; no infrastructure resources were created or approved in this update.

See [design and implementation decisions](ILLUSTRATED_MAP.md) and [counter storage](ANONYMOUS_COUNTS.md).

---

# Published release — 11 November 2026 (Australia/Sydney)

Career DNA Studio is published on the existing URL:

https://product-dna-studio-preview.onrender.com

- Frontend deploy: `dep-dbppr12fngtc7383jdv0`, commit `1e9c7c0a80f742ea7aa4873acf6b65207552e453`.
- API deploy: `dep-dbpptg8ae00c73c9jja0`, commit `53e3b87ec449525ec616de35261a62ba64921004`.
- Both deployments reached `live`; the bundled frontend matches the release source. The API's additional change omits non-displayed empty date values from edited-export English review.
- PR #1 was merged. Existing free services and their server-side credentials were retained. No database, paid infrastructure, or public trial start date was added.

Production browser verification used synthetic professional text and real OpenAI calls. Sparse clarification, bounded generation, scoped conversational refinement, undo, direct editing, consented English/safety review, portrait PNG download, square layout and phone-width rendering all passed.

The first production check exposed empty date fields being treated as non-English during edited export review. The hotfix excludes those non-displayed values, adds a regression, and passed 29 backend tests. The full production browser flow then passed, including the previously blocked download. The earlier prepared release's 33-test and six-check reports remain in VERIFICATION.md as historical evidence.

This publication updates the app. The seven-day pilot clock still requires the owner's separate launch-date instruction.
