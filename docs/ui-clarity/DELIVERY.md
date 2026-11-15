# Targeted UI and content refinements

Recoverable checkpoint: `checkpoint-before-targeted-clarity-d66eec7`. This is an incremental update of the approved original app; no new design system, assets, API contracts, model settings, upload flow or download implementation.

## Changes

1. **Privacy:** one right-aligned, initially collapsed inline disclosure. Removed the nested Technical details element, toggle listener and styling. The single paragraph retains browser file parsing, extracted-text/instruction transmission to the service/OpenAI, ten-minute retry memory, refresh behaviour, database non-storage of CV/maps, aggregate counts, 48-hour receipt expiry/next-access cleanup, hashed network rate limits and browser-delivery download semantics. These statements match the existing implementation.
2. **Header:** removed the visible generated theme pill on desktop/mobile; kept `career_signature` in the schema, state and accessible map title. The main title is centered on the whole canvas. The PM logo retains a nearby single-line, smaller muted brand watermark and the decorative underline.
3. **Journey:** bounded edge decorations to a dedicated gutter. Four/five-node maps place role icons beside headings to avoid heading/section-label collisions; fewer nodes retain icons above. Supporting lines use measured single/two-line heights and smaller consistent gaps. Selection guidance in both existing AI stages prioritizes substantive CV coverage/depth, then PM relevance, supported recency and recurring professional themes. Non-PM work remains truthful and is included only when PM evidence is insufficient or earlier work materially explains development. Source order is preserved; selected chronological stages must retain actual chronology. This adds guidance, not rigid scoring, hardcoded role output or a new generation stage.
4. **Capabilities:** clearer icon/title/description hierarchy, increased description-to-evidence separation, padded evidence capsules and bounded wrapping for a long single evidence label. Card height increases slightly within the same 1600×1200 composition; all established card surfaces, fonts and illustrations remain. Desktop export remains one 3200×2400 PNG.
5. **Refine:** the disabled Apply Changes button keeps its label. Only the compact spinner/estimate component shows the loading message. The duplicate text status is cleared, and the full-page loader is hidden only while the Refine modal is open. Initial generation and automatic text fitting retain their existing visible progress. Existing success/close, error/retry/input preservation, stable visual variants and single-submission guards remain.

## Modified files

- `career_pipeline.py`: selection guidance and summary-stage priority context, using the same two configured stages and response schema.
- `preview/poster.js`: targeted header, role/decor positioning, measured spacing and evidence capsule layout.
- `preview/studio.template.html`: consolidated privacy paragraph and removal of nested disclosure.
- `preview/studio.js`: one Refine loading state and one privacy-toggle binding.
- `preview/studio.css`: remove obsolete nested-disclosure selectors only.
- `preview/index.html`: rebuilt production bundle.
- `tests/test_targeted_ui_clarity.py`: six new contracts/browser checks. Updated superseded theme/privacy assertions in `tests/test_e2e.py`, `tests/test_original_refinement.py`, `tests/test_consolidated.py`.
- This request/delivery record; release pointers in README and deployment documentation.

## Verification

- **139 regression tests passed** in the full run; **7 focused layout/content tests passed** after final brand-spacing adjustment.
- Browser coverage includes desktop/mobile, 2–5 journey stages, 1–4 cards, actual painted glyph/illustration bounds, 0–3 evidence labels, controlled wrapping without truncation, center alignment, retained underlying theme data, keyboard privacy toggle, default collapse, exactly one loading message and prevention of duplicate requests.
- Existing tests continue to cover actual DOCX/PDF parsing, generation/refinement, successive accepted edits, undo, replacement CV, network errors/retry/cancellation, required-field rejection, reading-panel alignment, PNG export and anonymous counters.
- Models remain unchanged: initial analysis `gpt-6-astra`, Refine `gpt-6-sol`. No new public synthetic generations or download counts were required for QA; browser flow tests run against the isolated local test service with mocked AI responses.

## Screenshots and limits

The review bundle contains actual browser screenshots: same-data map before/after, simplified header, journey, capability cards, privacy desktop/mobile, Refine loading, preserved-input error state and actual downloaded PNG. Synthetic evidence is used only for deterministic QA; it is not embedded in runtime output. Existing rounded 3D assets were reused; no illustration generation was performed.

No known functional blocker remains. Experience prioritization is model-guided rather than a deterministic CV ranking engine; the regression checks ensure the instructions reach both stages and preserve grounding/source structure, not a fresh paid-model quality benchmark across real CVs. Very long copy retains the existing semantic fitting/failure safeguards rather than being cut off.

## Published verification

Runtime `ec3e8323138b8a91361101d26e99c90bbd2de61c` is live on the existing Render services. Backend deploy: `dep-dbsme3jbc2fs73bvo1n0`; frontend deploy: `dep-dbsmeh61egvs73e9eadg`. The published bundle passed checks at 1440, 768, 390 and 320 pixels: no horizontal overflow, unchanged one-line hero statement, a single privacy paragraph, no visible theme pill, retained theme data and exactly one Refine loading message. The configured available Refine model remains `gpt-6-sol`; counters remain persistent. Live visual checks used synthetic map fixtures and intercepted pending refinement requests, creating no public synthetic generations or downloads.
