# PM Career Studio handoff delivery

Published 12 November 2026 (Australia/Sydney).

Live application: https://product-dna-studio-preview.onrender.com
Runtime commit: `717d3961f6246c5fc3332defe86763fde1f9ba18`.
API deployment: `dep-dbqr2ndg1s2s73f5dj1g`; frontend: `dep-dbqr2ph42hec73ar6ud0`. Both verified live.

## Implemented in priority order

The original purple reference guided the rounded typography, luminous layered surfaces, compact journey-to-capability composition and coherent character/icon style. It is a design benchmark, not a flattened runtime background. All four references and both starting documents were reviewed before implementation.

1. Centralized warmer, shorter English copy. CV input works without additional story text; optional context remains optional. Loading explains the work and gives an evidence-based 60–120 second estimate.
2. A compact 1600×900 desktop composition with one selected result and one 3200×1800 PNG. The complete result and download controls fit at 1440×900 and 1366×768. Mobile stacks and scrolls. Rounded bundled fonts are retained and outlined for export.
3. A shared visual manifest provides six original SVG platform families, four pathways, six themes and the existing coherent 24-icon atlas. Semantics select defaults; stable IDs preserve choices through subsequent edits. Theme colors apply across surfaces and accents. Unknown asset IDs have safe fallbacks.
4. Freeform Refine accepts copy, colors, icons, platforms and supported layout changes in one conversation. Typed patches update only requested fields. Recent context, immutable versions, Undo and original-version restoration work. Cancellation prevents late responses from overwriting the selected version. A real test exposed and fixed a quoted-heading scoping bug: asking to rewrite the insight under a heading now edits its description rather than being mistaken for a rename.
5. Editorial guidance prioritizes evidenced challenges, judgement, trade-offs and concrete methods. Journey roles remain distinct from capability synthesis. Source-linked validation remains active; it does not invent achievements or fill all slots. Both journeys and strengths retain the 1–5 limit.
6. Privacy copy distinguishes browser processing, temporary server memory, provider processing and aggregate counting. Shareable exports use one selected map, embedded assets and outlined text. No raw CV/map is added to the database or logs by this implementation.

## Changed files

| Files | Purpose |
|---|---|
| `preview/copy.json` | Centralized product copy and optional feedback URL |
| `preview/visual-manifest.json`, `visual_catalog.py` | Shared semantic asset catalogue and validated visual patch paths |
| `preview/poster.js` | Compact responsive scene, platform/pathway drawing, theme controls and export layout |
| `preview/studio.js` | Conversational edits, immutable versions, cancellation, measured fitting and single export |
| `preview/studio.template.html`, `preview/studio.css` | Warm flow, optional input, privacy, responsive sizing and readable controls |
| `build_preview.py`, `preview/index.html` | Safe copy/manifest embedding and rebuilt self-contained frontend |
| `semantic_refinement.py`, `career_ai.py` | Scoped evidence-backed text/visual updates and conversation context |
| `skills/pm-dna-editorial/SKILL.md` | Challenge-led PM capability synthesis and compact editorial standards |
| `Dockerfile`, `.dockerignore` | Include the shared runtime catalogue in packaged builds |
| `tests/test_handoff.py`, `tests/test_handoff_browser.py`, existing V2/E2E tests | New regression coverage and updated expectations |
| `docs/PM_STUDIO_ARCHITECTURE.md`, `docs/PM_CAREER_STUDIO_HANDOFF_BRIEF.md`, this report | Architecture, requirement record and delivery evidence |

## Verification

**108 automated tests passed** on the final runtime, including evidence validation, typed patches, generation, counts, sessions, browser flows and exports.

Command:

```sh
python -m unittest test_ai test_server tests.test_counts tests.test_session_architecture tests.test_v2 tests.test_fact_validation tests.test_handoff tests.test_e2e tests.test_handoff_browser -q
```

Browser checks covered 1440×900, 1366×768, 1092×614 (125%-equivalent viewport) and 390×844. Geometry checks found no clipped fields or text collisions in tested fixtures. Tests covered unknown assets, mixed edits, quoted headings, contextual follow-ups, cancellation, Undo, original preservation beyond 30 versions and one outlined-font PNG. Packaged Python imports were also verified; a Docker deployment was not performed.

Live provider/browser validation used synthetic PM evidence and multilingual optional context. It exercised initial generation, five successful refinement versions, warmer colors without text changes, one specific icon change, a pathway/platform change, a context-dependent follow-up, and an evidence-grounded insight rewrite. Undo, restore original, responsive display and the actual PNG download passed. Unsupported circular placement/3D artwork produced an honest clarification and retained the existing result. No browser errors were observed. Public creations remained **3 before and 3 after**; authenticated tests were excluded, and legacy 23 was preserved.

The integration run was deliberately resumed rather than repeatedly billed: an earlier fresh generation completed in 105.22 seconds. After fixing the heading-scope bug, a successful completed initial request was replayed by its idempotent ID; its 9.68-second UI timing is **not fresh generation latency**. Successful final refinement turns took 5.69–18.14 seconds including UI/fitting. Rapid test edits reached the unchanged 8/minute network guard; the later real Try Again clarified the unsupported request and the remaining browser/export checks completed. No quota was raised. The recorded response estimates sum to approximately $1.182, including the replayed request's original usage; this is neither a new-charge total nor an invoice, and excludes earlier debugging runs. Actual billing depends on provider accounting and cache pricing.

Text model remains `gpt-6-astra`; transcription remains `gpt-transcribe`. This release does not call an image-generation model.

## Before and after

The `before/` and `after/` screenshots use the **same synthetic four-role/four-capability fixture**, same lilac theme and same avatar for a fair comparison.

- `before/result-1440.png` → `after/result-1440.png`
- `before/result-1366.png` → `after/result-1366.png`
- `before/result-390.png` → `after/result-390.png`
- `before/export.png` → `after/export.png`

Open `comparison.html` to switch viewports. `live/` contains the final real-provider screenshots, the actual downloaded `pm-career-dna.png` and the structured verification report. Live examples use synthetic evidence, not a visitor's CV. Raw request/response dumps are excluded from this delivery.

## Privacy and remaining limits

- CVs, maps and conversation text are not written to the application database. Browser session data and bounded server result/replay memory are temporary (up to ten minutes). Text and refinement instructions are processed by the backend and OpenAI; provider retention policies are separate. This is not a zero-retention claim.
- Persistent counts contain anonymous aggregates plus expiring random-request receipt metadata for deduplication. They count validated initial server creations, not unique people or confirmed downloads. Hosting operational metadata is separate from content storage.
- Layout editing is curated: density, mascot placement/visibility and approved visual assets. Arbitrary grids, freehand positioning and new custom artwork are not supported. The interface clarifies such requests.
- Cancel stops waiting and prevents stale commits; an already-running provider request may still complete and incur cost.
- Existing public **10 model attempts/day** and 8/minute network guard remain unchanged. Initial analysis and optional shortening may use multiple calls; ten attempts does not mean ten full visitor journeys. Internal verification uses separate authenticated limits. Shared proxies may share a network guard.
- No actual LinkedIn feedback URL was supplied, so that link stays hidden until configured in `copy.json`.
- Free Render cold starts and the existing free PostgreSQL 30-day lifetime remain. No paid plan or new service was created.
- Legacy DOC and scanned PDFs need conversion/OCR. Physical microphone capture, Safari-specific behavior and full WCAG certification are not claimed; Chromium flows, readable contrast, focus, reduced motion and effective zoom were checked.
- AI synthesis remains an interpretation of supplied evidence, not independent career verification. The asset catalogue is extensible; it is not an unlimited illustration generator.
