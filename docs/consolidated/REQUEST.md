# Career DNA Studio — Consolidated Codex Implementation Specification

**Scope:** All requirements discussed since ~09:51 Sydney time, covering (A) homepage/privacy/font stability, (B) streamlined Refine My DNA, and (C) high-fidelity implementation of the approved Career DNA Map design. **This file supersedes the separate iteration instructions for these three workstreams.**

## 0. Mission, source of truth and boundaries

Implement improvements **in the current Career DNA Studio codebase**. Do not build a new app, revert to V2, add unrelated features, or substitute a static infographic for a functioning map. Preserve existing CV upload/analysis, PM career understanding, dynamically generated themes and capability cards, collapsible Your Next Chapter and Supporting Evidence, download/export, counters, and existing working fixes. Make a recoverable commit/checkpoint before changes. Inspect current architecture, components, fonts, image assets, API routes, state management, and export pipeline first.

**Approved visual source:** `APPROVED_VISUAL_REFERENCE.png` in this package. This is the image the user liked: warm, dimensional 3D pastel design with a sophisticated centred header, converging curved journey paths, complete explorer character, PM-related decorative props and polished lower summary. Treat it as the visual specification for the map, **not** a background image or content template. Do not hardcode the sample user's CV, `AI PM`, `Trust & Safety PM`, example card wording, or fixed stage/card counts.

**Priority ordering:** P0 preserve reliability and working flows; P1 Refine one-step workflow; P2 homepage/privacy and font stability; P3 visual map high-fidelity; P4 regression tests and actual screenshots. It is acceptable to implement in dependency order but complete all three workstreams.

## A. Homepage and privacy improvements

### A1. Privacy disclosure — concise, accurate, inline

Replace the two long general privacy paragraphs with **one concise paragraph**, preserving accurate disclosure of browser reading, service/OpenAI processing, short-lived memory, aggregate counts and technical records. Proposed copy (verify claims against actual implementation):

> Your CV is read in your browser and isn't saved by this app. Extracted text and your instructions are sent to our service and OpenAI to create and refine your DNA. Temporary results may remain in memory for up to 10 minutes. We retain aggregate usage counts and short-lived technical records for security and deduplication. OpenAI's processing and retention policies also apply.

Do not imply that CV data **never leaves the browser**: extracted text is sent to the service/OpenAI. Do not make claims unsupported by code. Retain the existing **Technical details** sub-section for specifics, including receipt expiry/limits and browser-handled download semantics, as applicable.

- Align `Privacy & Data` control **right**, with `Technical details` control on the same right edge, matching typography, spacing and chevron.
- Privacy section **collapsed by default**.
- Click expands **inline in normal document flow**, never a modal, overlay, tooltip or automatically opened floating popup.
- Keep Technical details nested within Privacy & Data if already so; ensure both controls work by keyboard and screen reader, with `aria-expanded`.
- Expanded content must not overlap or cause accidental horizontal overflow.
- Keep the concise reassurance under Upload CV, if already in use: **`Your CV file will not be saved, only read in your browser.`** Ensure the nearby full privacy disclosure makes the transmission of extracted text clear.

### A2. Remove redundant homepage CTA

Remove the **large gradient** `Explore My PM Career DNA →` button displayed above the upload section. **Keep** the section heading `Explore My PM Career DNA`, `Upload CV`, the privacy note, `PDF / DOCX / 5 MB`, and the primary `Discover My DNA` button. Remove the resultant excessive blank space; ensure no broken anchor/scroll action remains. Do not delete the real generation CTA.

### A3. Fix initial font flicker / page layout shift

User sees a brief wrong-font render followed by intended font, causing a small jump on load. Fix underlying causes, not with arbitrary timers:

1. Audit `@font-face`, stylesheet ordering, remote fonts, weight declarations, and hydration/client-only styles.
2. Preload critical final font files used by headline and hero/major UI; prefer project-compatible self-hosted WOFF2 and correct MIME/crossorigin.
3. Make typography-defining CSS available before first visible render; ensure weight mappings and metrics are correct and avoid synthesized weights.
4. Use suitable `font-display` and metric-compatible fallbacks, or a minimal font-readiness gating strategy only if warranted; avoid a prolonged blank page.
5. Check both CSS transitions and hydration reflow. Test cold load and cache-disabled reload on desktop/mobile.
6. Before exporting DNA map, ensure intended fonts and visual assets are ready.

**Acceptance:** no perceptible fallback-font flash, title resize, horizontal jump or layout shift; preserve good first meaningful render and all functionality.

## B. Refine My DNA — simple one-step text refinement

### B1. User-facing UI

Keep the existing `Refine My DNA` modal with title and approved subtitle:

> A small change can make it feel more like you. Your map's visual identity stays the same.

Use **one multiline text input**, a single `Apply Changes` button, and existing `Upload a New CV` action. Voice input is out of scope and should remain removed. Replace longer guidance with:

> Paste the sentence you'd like to change and tell us what to replace it with.

Do not show redundant `Tell us what you'd like to change` heading, prior successful edit history, AI chat bubbles or conversational transcripts. Keep the header/subtitle/close `X` sticky/fixed within the modal; content scrolls independently; remove extra decorative rule under `X`. Closing does not apply changes.

### B2. Remove clarification/questions completely

Remove the lavender question card **inside** the input area and the duplicate clarification text **below** the Apply button. No Yes/No prompts, no additional confirm action, and no follow-up chatbot question as part of normal refinement.

Current bad example: `Should I replace “Automated enforcement” under Trust & Safety PM or under Safety Systems Design?`

**Required flow:** user types instruction → clicks `Apply Changes` → AI interprets and validates → structured map patch commits → modal closes → revised real map visible. No intermediate user action.

### B3. Matching and patch semantics

For `Automated enforcement - design safety system`, interpret as replacement of `Automated enforcement` with a polished concise replacement such as `Design safety systems`, only if faithful to user intent. Identify existing occurrences from the current structured content.

- If the user **specifies a section/card**, update only that target.
- If the source text occurs in **multiple places** and they request a general text replacement without narrowing scope, update **all exact matching occurrences**; do not ask the user which one.
- If a target cannot be confidently identified, **do not guess**: keep modal open and show short inline validation error, e.g. `We couldn't identify the text to update. Please include the exact sentence you'd like to change.` This is an error, not a question bubble.
- Do not change the map's artwork, layout, islands, theme palette or unrelated text while refining content.
- Protect empty required fields: `This field can't be left blank. Please enter a replacement.` No suggested Yes/No alternatives.
- Use structured stable field IDs, current accepted map state and a validated patch. Do not accept a whole hallucinated new map from the model. Validate patch existence, editability, nonempty content, length, factual grounding, and scope; apply atomically.
- Refinement should use configured GPT-6 Sol only if an actual supported endpoint/model ID is available; verify configuration. Do not silently claim or substitute `GPT-6 Sol` if unavailable; report blocker. Preserve existing supported model integration where necessary pending explicit resolution.

### B4. Loading, success, failure

During the actual request, disable duplicate clicks and show a spinner/hourglass with `Applying your changes…`. Optional `This may take around 20–30 seconds` as estimate only; no fake countdown or arbitrary delay.

**Success:** patch applied to source of truth → regenerate/render the **same fixed visual composition** with updated text → clear input → close modal automatically → map in view. Do not leave historical messages in modal.

**Failure/validation:** do not commit partial changes; keep modal open, preserve the user's instruction, stop loading, re-enable Apply, show a single concise inline error. On next successful open, input begins empty. Several successful successive refinements must build on latest accepted map, without reverting prior patches.

### B5. Regression scenarios

- One exact-match replacement; two matching occurrences replaced together; section-specific one occurrence only.
- Blank required field rejected, no Yes/No dialog.
- Nonexistent target shows only inline error.
- Network/model error preserves original map and user input; retry possible.
- Reopen after success: empty input, previous map edit preserved.
- Modal scroll: header, subtitle and close `X` always visible.
- No microphone, extra conversation UI, repeated clarification message or duplicate question.

## C. High-fidelity map visual implementation

**Implementation goal:** make the actual dynamic web-rendered DNA map closely resemble `APPROVED_VISUAL_REFERENCE.png`. Reconstruct the reference's composition with reusable HTML/CSS/SVG and compatible assets; never paint a static screenshot beneath dynamic labels. Use the reference for art direction, **not** its sample career facts.

### C1. Art direction and layout

- Cohesive premium soft 3D pastel aesthetic: peach/ivory/lilac surfaces, warm gradients, refined shadows, subtle highlights, deeper dimensional PM illustrations; navy for primary text, softer purple for secondary.
- Avoid the previous flat rigid rectangular sections, monotone dark text, oversimplified horizontal lines and cropped character.
- Logical map near the reference's **4:3** composition; scaled responsively for display and exported at sufficient resolution. Keep all important assets within a safe inset margin (roughly 3–5%). Never clip character, easel, decorations, title, islands or callout. Test variable text lengths.
- Keep role and capability content dynamic and evidence-based; allow **variable journey stages (e.g. 2–5)** and **1–4 DNA cards**, without inventing slots to fill a fixed grid.

### C2. Header — visually engaging and balanced

- Left: original PM/DNA logo with a modest `PM Career Studio` brand lockup beside it. **Remove cramped brand footer below the map summary.**
- Main `My PM Career DNA` title: visually centred against the **whole canvas** (not just leftover flex width), eye-catching but readable. Use a subtle swoosh/gradient ribbon/glow and depth, avoiding mere stacked colour rectangles.
- Right: dynamic personal theme in a polished small pill, e.g. `AI Experiences, Built for Trust`. Can wrap appropriately at narrower sizes; never overlap title.
- Brand, heading and theme must all fit and appear coherent, even if generated personal thesis is long.

### C3. Journey — unified sculptural islands

- Retain chronological source-derived career stages with role titles and concise, accurate statements.
- All stages share **one identical island/platform silhouette**, perspective and rendering style; vary coordinated colours, and add small *semantically relevant* PM props: AI chip/evaluation flask for AI, shield/decision mechanism for safety, stacked architecture/workflow for platform, funnels/charts for growth or analytics only when supported by actual experience.
- Prefer reference's substantial floating, bowl-like dimensional islands and crystal/mountain accents, not paper-boat forms.
- Reuse a shared pedestal component plus colour variants, **not** different islands for every role.
- Use modest roadmap/dashboard/experiment/flow motifs around the journey, strategically placed with whitespace preserved.

### C4. Curved paths — must visibly converge into DNA hub

This is a **highest-priority visual change**. Prior map used almost parallel horizontal lines that failed to visibly show `Shaped My PM DNA`.

- Draw distinct, elegant, softly glowing **curved/ribbon paths** from the bottoms of journey islands into a **central convergence** physically touching/leading into `Shaped My PM DNA`.
- Match path hue to island colour (amber, blue, teal, etc.), with soft depth, dots/nodes and directional cues/arrow tips as useful; flow should read unambiguously from experience to DNA.
- Use responsive **computed SVG Bezier geometry** anchored to actual stage centres, adapted to different stage counts; avoid hardcoded coordinates that only fit the example.
- Keep curves behind textual content, do not obscure labels. No chaotic line tangle, excessive animation or simple three parallel stripes.
- Central hub is a luminous peach badge with `Shaped My PM DNA`, integrated between journey and cards.

### C5. Capability cards and full explorer character

- Use 1–4 dynamically generated, evidence-backed PM strengths. Elevate from narrow tasks to high-level, transferable capabilities; favour substantive/detailed CV evidence and, all else equal, recent experience. Avoid inventing outcomes. Do not hardcode example card names or summaries.
- Cards: consistent dimensional rounded borders, muted pastel gradient fills, gentle icon/shadow treatment, legible dark titles, lighter supporting descriptions, translucent evidence/tag capsules.
- Relevant prop icons should have **one coherent 3D illustration family**. Appropriate PM motifs include AI judgement, system diagrams, funnels, user interactions, safety shields, design flows, data insights. Never add an unsupported growth element merely as decoration for content.
- Explorer character: warm curly-haired, goggles, backpack, easel/board in reference style. **Full figure and props entirely visible**; face toward DNA cards; no cropping at any edge. On mobile, adapt placement/scale (or deliberately hide purely decorative character) rather than crop.
- Preserve readable line breaks and cards with consistent heights. Export must include all card text; prevent clipping even with long labels.

### C6. Bottom concluding insight

- Display dynamically generated insight in a prominent but not overwhelming glossy, softly glowing **wide rounded summary ribbon** below cards. Reference uses small spark accents and relevant PM ornaments near outer edges (e.g. charts/target/checklist).
- Leave generous breathing room above/below. Do not collide with capability cards. No cramped `PM Career Studio` footer; brand has moved to the logo/header.

### C7. Asset strategy

1. Inventory existing project 3D character, island and icon assets first, and reuse compatible artwork.
2. If required, produce a **coherent small family** of transparent-background assets matching the reference style; do not mix emoji, flat generic glyphs, photo cutouts and glossy 3D art.
3. Use CSS/SVG for scalable paths/panels and deterministic text. Avoid baking text into pictures. Source artwork should be separate, replaceable assets with safe intrinsic padding.
4. Ensure image/font asset readiness before map screenshot or PNG download.
5. If matching art assets cannot be generated in the coding environment, report what is blocked, implement available structural improvements and **do not claim** full visual fidelity.

## D. Shared implementation constraints and QA

- No full rewrite, no V2, no new career verticals, no hardcoded CV content, no detached static reference image used as the real map.
- Preserve `Upload CV` → `Discover My DNA` → map exploration → optional refinement → `Download`.
- Preserve existing expandable `Your Next Chapter` and `View Supporting Evidence` visual alignment, dynamic creation/download counters, and all privacy functionality.
- Successful text refinement must update the same dynamic map preview **and** exported image; no independent stale export version.
- Add or update tests for mobile/desktop layout, loading fonts, privacy disclosure, CTA removal, all Refine patch/error scenarios, 2/3/4/5 stage paths, 1–4 cards, overflow, safe artwork bounds, download image and counts.
- Compare a screenshot from the **actual running implementation** side-by-side with `APPROVED_VISUAL_REFERENCE.png` at approximately the same display size; mention intentional differences due to user-specific content. Do not present an AI mockup as implementation evidence.

## E. Required Codex final handoff

After implementing, provide:

1. Brief implementation summary grouped into A homepage/privacy/font, B Refine, C map visual design.
2. Files/components/assets modified, and whether any model integration is unavailable.
3. Test/QA results, including error handling and export checks.
4. Actual screenshots of the running page + generated map, not another concept graphic.
5. Any known differences from approved visual reference and outstanding blockers.

**Definition of done:** Site preserves working generation/download; privacy reads as one honest concise paragraph and collapses inline from a right-aligned control; duplicate Explore CTA is gone; font does not visually jump; Refine is one text box/one Apply with no clarification bubbles; changes apply atomically and close modal on success; high-fidelity map has premium centred title, brand near PM logo, matching islands, visible ribbon convergence, relevant illustrative props, fully visible inward-facing character, polished cards and uncluttered conclusion.
