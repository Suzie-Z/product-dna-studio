# Consolidated original-version iteration

Checkpoint: `checkpoint-before-consolidated-194c8bf`. This updates the existing original app; its API routes, CV parser, version state, generation pipeline, evidence validation, reading panels and anonymous metrics remain in place.

## A. Homepage, privacy and font stability

- Removed the redundant gradient Explore button and its scroll handler; upload and Discover are visible immediately below the existing section heading.
- Privacy is one honest paragraph, collapsed inline by default. Matching right-aligned summary controls expose Privacy & Data and nested Technical details; native keyboard behaviour and synchronized aria-expanded are retained.
- CV binary files are still parsed in-browser. Extracted text/instructions go to the service/OpenAI. Ten-minute retry memory, browser refresh clearing, aggregate metrics, 48-hour receipts, hashed in-memory network rate limits and browser download handoff semantics are disclosed. No new CV/map persistence was introduced.
- Converted the existing licensed fonts to small self-hosted WOFF2 assets (13/15 KB), embedded/preloaded in the production HTML. Typography CSS precedes paint. A font-readiness promise gates visibility only until local font decoding completes, with no timer or artificial delay. Map rendering/export reuse that readiness and the existing matching outline glyphs. OFL license files remain in assets.

## B. One-step content refinement

- One input, Apply Changes, optional replacement CV; fixed header/X and independently scrolling body. No clarification card or duplicate question text.
- Exact replacement resolves stable field IDs across all occurrences; explicit role/card scope narrows the update. Dash-separated copied text is supported. Incomplete duplicate patches are rejected/repaired internally and cannot partially commit.
- Unknown targets and unsupported edits return one inline error; the existing map and typed request remain. Blank required fields stay protected. Success clears/closes the modal and renders the new accepted version, including the export.
- Freeform semantic requests remain supported without requiring pasted text. New first-person testimony can still be retained when the map already reflects a correction. Visual requests receive an inline explanation to use full generation; they never re-style a content refinement.
- Production model configuration remains `gpt-6-sol` via the Responses API; no alias, fallback claim, key, quota or provider changes.

## C. Approved dynamic map

- Logical desktop canvas is now 1600×1200 (4:3), exporting one 3200×2400 PNG. SVG text remains selectable in preview and outlined accurately in export.
- Whole-canvas-centered title, header brand lockup and dynamic theme pill, soft gradient swoosh, coordinated rounded surfaces, full inward-facing explorer, consistent sculptural bowl islands, topic-related props and glossy summary ribbon. Removed the cramped brand footer.
- Computed color-matched Bezier ribbons start at every island and visibly meet the central DNA badge. Geometry supports 1–5 actual journey nodes and 1–4 evidenced capabilities; no padded slots. Five-stage support also updates server schema/order/link bounds.
- One newly generated isolated transparent explorer/easel asset (`preview/assets/pm-explorer-full.png`), inspected before integration. Existing 24-icon atlas, plant/world atlas, PM logo and licensed fonts are reused. The reference PNG exists only in documentation/review material; it is not a rendered background, layout raster or production image source.
- Mobile stacks the actual journey/cards and deliberately omits the decorative explorer rather than cropping it. Successive text changes preserve the accepted visual variant.

## Files

Runtime: `career_ai.py`, `semantic_refinement.py`, `preview/studio.template.html`, `studio.js`, `studio.css`, `poster.js`, `build_preview.py` and rebuilt `preview/index.html`. New assets: explorer PNG plus two WOFF2 derivatives. Regression expectations were updated only for explicitly superseded behaviour (4:3/export dimensions, five journey nodes, unified bowl geometry, inline errors replacing questions, removed CTA). `tests/test_consolidated.py` adds exact/scoped/duplicate/atomic replacement, actual HTTP/UI refinement, font readiness, privacy and all stage/card combinations.

## QA and review

The verified regression log is included in the review bundle. Coverage includes actual browser DOCX/PDF parsing, upload/generate, consecutive refinement, undo, replacement CV, errors/retries/cancellation, sticky modal, one PNG download and anonymous download metrics. New checks cover cold reload without visible fallback fonts, default-collapsed/right-aligned privacy, 2–5 stages × 1–4 cards, uniform silhouettes, path-to-hub anchors, safe art bounds and actual painted text overlap. Required-field and unknown-target failures preserve input and map.

Actual running-app screenshots show homepage, privacy, Refine desktop/mobile, two/three/five-stage maps, reading panels and the actual downloaded PNG. Before captures use commit `194c8bf` with the same synthetic three-role map data. The comparison gallery presents the approved image beside the actual renderer at matching displayed widths. Synthetic QA fixtures are used for deterministic visual comparison, not hardcoded into the product or presented as fresh AI synthesis.

## Remaining differences

The composition is a component reconstruction, not pixel-identical generated artwork: header wave sculpting, outer props and island surface detailing are simplified SVG/atlas elements. The full-body explorer currently uses one consistent pose; the older character atlas is retained in the repository. Mobile intentionally hides this decoration. Palette and copy can vary with a real person's accepted map. Evidence validators protect provenance/structure; they do not guarantee editorial excellence for every CV. Browser download delivery cannot prove final disk save; its disclosed metric remains a handoff count.
