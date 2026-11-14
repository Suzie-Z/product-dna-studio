# Original Experience Refinement — published

14 November 2026 (Australia/Sydney).

[Open the website](https://product-dna-studio-preview.onrender.com/?v=599bf51)

Application commit: 599bf51061b44b6a8db280ecdec47b6e87944d73.
Recoverable checkpoint: checkpoint-original-before-full-refinement-a532d5d → a532d5d0e67e76f2a5561c30d22f917b893cf3fa.
Review branch: pm-original-refinement.

## Delivered changes

### Refine

- Removed voice, recording, permissions, transcription states/module and audio API routes. No replacement speech service.
- Removed visible conversation history and version-number parsing from instructions. Each opening has an empty textarea. The current selected accepted map is the context; explicit version selection and Undo remain.
- Kept the approved title/subtitle and X in a non-scrolling header. Only the body scrolls; the X has no underline.
- Apply disables immediately, prevents duplicates and shows a real-operation spinner with a qualified estimate. No fake countdown. Processing remains active through validation, fitting and export preparation.
- Required blank edits receive inline validation, without Yes/No proposals. Failure preserves input and the current map. Success commits the candidate, clears input, closes the modal and returns to the map.
- Prepared candidate rendering before committing the version; cancellation cannot replace the current map with a late response.
- Added bounded keyword leaf paths, such as /strengths/k1/methods/0/label, preserving siblings and evidence.
- Added UI-to-schema section definitions: conclusion means the /superpower summary ribbon, while the theme, Recognition and Possibilities are distinct targets. This fixed an unnecessary clarification found in a real model test.
- Ordinary text edits retain platform choice, icons, palette, background, character, order and unrelated content. A separate full-generation action remains.

### Original map and reading experience

- Integrated the dynamic Personal DNA Theme as a secondary pill within the title container, including bounded mobile wrapping.
- Enforced one platform shape per map at component level, even when legacy overrides contain different shapes. Stage colors vary orange/blue/teal/purple; silhouette, structure, perspective and details stay consistent. Different original platform styles remain possible between maps.
- Retained light horizontal connections and added subtle glowing curves into Shaped My PM DNA. Removed chronological arrow decorations.
- Preserved the capability-card system and maximum four categories, with fewer when evidence warrants. No empty placeholder tags.
- Added a rounded gradient concluding-insight ribbon and subtle symbolic mark, with the studio footer secondary.
- Kept original rounded fonts, brand, character/icon atlases, pastel palettes, desktop 16:9 composition and one 3200×1800 outlined-font PNG. No image model is called.
- Kept the homepage and its single-line brand statement.
- Renamed the optional reflection to Your Next Chapter, with the requested subtitle and exactly two subsections: Recognition and Possibilities to Explore.
- Removed the redundant My Product DNA heading/sentence.
- Next Chapter and Supporting Evidence share aligned widths, margins, padding, lavender surfaces, corner radii and chevrons. Both start collapsed and open independently.
- Preserved source attribution, inferred-strength distinctions and evidence notes. Prior non-PM experience is not relabelled as PM work.
- Strengthened PM editorial guidance for recurring judgement, constraints, trade-offs, distinctive themes and synthesis rather than task lists. No new profession categories, scores or job matching.

## Actual model and endpoint

Refinement model ID: **gpt-6-sol**.
Endpoint: **POST https://api.openai.com/v1/responses**.

The running backend queried the active project's model list and confirmed that exact identifier before configuration changed. Only OPENAI_REFINEMENT_MODEL was updated, by merging with existing variables. No substitute to gpt-6.1-sol or another model was made.

Initial understanding and capability synthesis retain gpt-6-astra. API key, quotas, trial settings, plans and database connection were not changed or retrieved.

The non-secret /api/refinement-model endpoint reports supported Sol identifiers and configured selection. Health checks remain fast and do not query the model list.

## Changed components/files

| Files | Purpose |
|---|---|
| preview/studio.js | Text-only state, empty sessions, no chat log, loading lifecycle, atomic candidate commit |
| preview/studio.template.html, studio.css, copy.json | Fixed modal header/body, one textarea, progress/errors and matching reading panels |
| preview/poster.js | Integrated header, uniform platform shape, stage colors, convergence glow and summary ribbon |
| preview/index.html | Rebuilt production bundle |
| semantic_refinement.py, refinement_validation.py | Stable leaf patches, section aliases and required-field validation |
| career_ai.py, career_reflection.py | Validation and evidence-led editorial guidance |
| ai_server.py, model_config.py | Removed audio routes/metadata; safe model capability discovery |
| voice_input.py | Removed obsolete implementation |
| Dockerfile, .dockerignore | Package validation module; omit voice |
| tests/test_original_refinement.py and updated existing tests | New acceptance cases and replacement of superseded voice/mixed-platform assertions |
| docs/original-refinement, README.md, docs/DEPLOYED.md | Request, verification and publication record |

## Automated verification

**119 unique relevant checks passed:** a 115-test regression suite in 107.476 seconds, plus three later model/scope/removed-route checks and one added conclusion-target regression. The later scope fix also passed 23 related contracts; overlapping invocations are not added to the unique count.

Coverage includes actual PDF/DOCX browser parsing, PM scope, strict schemas, literal evidence validation, multiple PM evidence fixtures/source isolation, no more than four categories, retries, versions, counters, desktop/mobile/zoom, measured text/illustration collisions, all original platform families, unknown assets, one export and outlined fonts.

New acceptance cases verify exact tag replacement with siblings/proof retained; blank instruction/model-patch validation without confirmation; failure/retry/cancellation; empty newly opened input; no voice/history nodes; real pending spinner and disabled Apply; fixed title/subtitle/X on a short narrow viewport; independent matching reading panels; uniform platforms despite conflicting overrides; header/summary/convergence components; exact model reporting without aliasing; removed audio endpoints; and evidence isolation across Growth, Platform and AI PM examples.

Python compilation, JavaScript syntax and Git whitespace checks passed.

## Real GPT-6 Sol verification

With synthetic PM evidence, the real API accepted:

1. Change Launch requirements to Design for lasting value: only /strengths/k1/methods/0/label changed. Server elapsed 5.95 seconds.
2. Make only the conclusion less generic: only /superpower changed, and the first edit remained intact. Server elapsed 3.32 seconds.

A clear-description request returned HTTP 422 / required_field_blank, without a Yes/No prompt.

An earlier conclusion request produced an unnecessary clarification. UI section-name mapping was added and tested; the same instruction then succeeded on the already accepted map. There were three real refinement requests in total, including that clarification. Public response metadata does not expose tokens or billed cost; no cost estimate is asserted.

Public creation total remained **5 before and 5 after** the final real verification. Refinement requests do not add generation counts.

The recorded real responses were replayed through the actual frontend: both updates appeared in the SVG, the next input began empty, the modal closed after success and visual state stayed unchanged. The initial map was a synthetic fixture, not a fresh initial-generation quality benchmark.

## Deployment verification

Both application deployments are confirmed live at commit 599bf51061b44b6a8db280ecdec47b6e87944d73:

- API srv-dbpflmjrjlhs73fps3kg: dep-dbs4ah6k1f9s7387vuk0.
- Frontend srv-dbpf7to8v5cc73e3jtfg: dep-dbs4chu7bikc73eilic0.

The served HTML matched the tested bundle:
db6435f006b6b2acd5a045da234ac5169a1cc8fdd8208ac7f11ebe82c51f473b.

Existing Render services and URLs were reused. No new resource, plan, CV database or paid image service was added.

## Screenshots, blocks and limits

The delivery gallery includes the four-card map, matching reading sections, mobile map/modal, the real Sol-refined synthetic example and actual single PNG download.

- The brief references a sixth screenshot, but that image was not newly supplied with this turn. Explicit written layout rules and the existing original assets were used. Exact pixel-level comparison against that particular image is not claimed.
- Initial screenshot maps are synthetic fixtures. The two real Sol edits are verified; subjective first-generation quality was not freshly benchmarked across real personal CVs. Source references establish provenance, not independent career certification.
- Chromium and responsive viewports were tested; comprehensive Safari/physical-device/accessibility certification was not performed.
- Existing browser CDN parsers, OCR limitations, temporary session/replay memory and provider processing policies remain. CVs/maps are not written to the app database.
- Cancel prevents late UI replacement but cannot guarantee cancellation/billing avoidance of an already-running provider request.
- Required-field validation is conservative; model interpretation remains fallible. Failure retains the accepted map. Visual changes require the explicit full-generation action.
