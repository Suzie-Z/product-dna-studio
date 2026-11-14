# Original-version targeted iteration

Checkpoint: `checkpoint-before-targeted-iteration-6666eaf`. No rebuild, new career domains, model change, or quota change.

## Implementation

- `career_pipeline.py`: configurable relative priorities for evidence depth, PM relevance, ownership, impact, recency, duration and independently repeated evidence. Summary-stage instructions separate enduring capability, transferable decision value and concrete evidence tags. No extra model call or sample CV data added. Selection remains model judgement rather than a rigid word-count score.
- `preview/poster.js`: centered header group derived from component widths, narrower theme capsule, separated summary ribbon, compact card container, restrained category-related atlas decorations. Existing 24 character/icon atlas assets reused; new maps place the right-looking characters on the left. Existing accepted visual variants remain unchanged during text refinement. No image assets generated, whole-poster raster templates, or font redistribution added.
- `preview/copy.json`, `studio.template.html`, `studio.css`, `studio.js`: exact short CV assurance, shorter left-aligned detailed disclosure and technical details; concise Refine helper with accessible hidden label; removed repeated generic source labels while preserving substantive evidence; Download label and real metric display.
- `generation_counts.py`, `ai_server.py`: separate aggregate download total and hashed random request receipts; PostgreSQL transaction/advisory lock and unique receipt prevent duplicates for 48 hours. In-memory fallback is explicitly process-scoped. No CV or map content is stored in these tables. Existing creation counters are untouched. Failed reads omit downloads rather than inventing zero.
- `preview/index.html`: rebuilt self-contained production artifact.
- `tests/test_targeted_iteration.py`: concurrent receipt deduplication, unavailable-metric omission, invalid receipts, real HTTP endpoint, actual browser PNG handoff and responsive renderer checks.

A download means a successful PNG export handed to the browser by a user click, not confirmed filesystem persistence. Browsers cannot report whether the user ultimately saves the file. Preview/rerender/generation do not increment it. Delivery errors can undercount; they never block the image download.

## Privacy and model

CV binary parsing remains browser-side (PDF.js/Mammoth); no binary upload or persistent CV storage was introduced. Extracted source text and refinement instructions go to the backend/OpenAI. Retry results can remain in server memory for up to ten minutes. Browser state clears on refresh. Aggregate counters and 48-hour anonymous receipts are durable when the existing PostgreSQL URL is configured. Network rate limits use a short-lived hash in memory. OpenAI policies remain linked.

Configured production Refine model remains `gpt-6-sol`, Responses API; no aliases, substitution or quota increase. Generation model configuration is unchanged.

## Verification and artifacts

Original regression suite: 119 passing tests. New and affected browser/HTTP tests are recorded in the accompanying logs. Actual browser DOCX/PDF parsing, generation/refinement (mocked AI provider), undo, replacement CV, retries, modal cancellation, one PNG export, 1–4-stage/card geometry and mobile layouts are covered. Three contrasting PM evidence sets remain isolated in the evidence validation regression. This is not a claim of a fresh paid-model qualitative benchmark: no synthetic public generations were added to real creation totals.

Before/after map, privacy, mobile, reading panels, modal and 3200×1800 PNG captures are in `work/targeted-iteration/` and the downloadable review bundle. Before uses commit `6666eaf`; after uses the current runtime. Images use synthetic test evidence, never the owner's CV.

Limitations: the two supplied Markdown files refer to six reference images, but those images/reference directory were not attached. Reference 06 fidelity cannot be certified. Existing warm 3D assets were visually inspected and reused. Legacy right-side character variants are retained to avoid restyling accepted maps; newly generated maps use inward-facing placement. Live AI wording quality still benefits from human review across real CVs; evidence validation checks truth/structure, not guaranteed editorial excellence.
