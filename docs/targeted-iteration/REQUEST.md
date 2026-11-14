# Career DNA Studio — Targeted Iteration Requirements (Nov 2026)

## 0. Instructions to Codex

Implement this as an **incremental refinement of the current original-version experience**, not a V2/V3 rebuild. Inspect the existing repository, identify the relevant components, preserve existing routes/state and previously approved fixes, and create a recoverable checkpoint before modifying code. **The six images in `references/` are user-supplied visual references, not production-ready sliced UI assets.** Do not rasterize an entire map screenshot as the product output; generated text must remain dynamic and the composition editable in code.

Scope: Product Management careers only. CV upload -> personalised PM Career DNA map -> optional Your Next Chapter / Supporting Evidence -> download or text-only Refine. Preserve previously agreed features: evidence grounding, a maximum of four DNA categories (fewer if warranted), consistent platform silhouettes within each map, subtle journey-to-DNA connections, and reliable targeted text edits without re-styling the map.

## 1. DNA capability generation: abstract above individual tasks (highest priority)

**Problem:** Current capability card descriptions are too specific and task-oriented. They read like a single CV bullet rather than a transferable Product Management strength.

**Required content hierarchy:**
1. **Capability label:** a broadly useful yet distinctive PM capability/domain (e.g. *AI Product Judgement*, *Context-Aware Interaction Design*, *Scalable Platform Design*, *Growth Experimentation*).
2. **One-sentence description:** what type of product decisions, approach or value the person brings; no single test, feature, project or employer-specific incident.
3. **Evidence tags:** short, CV-grounded techniques, skills or work patterns; specific projects only if they meaningfully substantiate the broader capability.

Reference `01_ai_judgement_current.png`:
- Current body: “Test competing model approaches against product and risk needs.” — too narrowly anchored to one type of task.
- Desired level, **example, not hardcoded output**: “Understand AI use cases, evaluate capabilities and make informed product decisions.”
- The idea in Chinese is “深入理解使用场景，全面进行数据测评” — elevate this to product-level AI evaluation/judgement, not literal phrasing about a single test.

Reference `02_emotion_aware_current.png`:
- Keep the person's differentiating domain if supported, but lift the emphasis to interaction/product experience design rather than a checklist of features.
- **Example** title: *Context-Aware Interaction Design* or *Emotion-Aware Interaction Design*.
- **Example** body: “Design experiences that respond to user context, intent and emotional signals.”
- Tags such as user profiling and emotion recognition may appear as supporting evidence, not become the entire identity.

**Candidate experience selection and ranking:**
- Weight the **depth and amount of meaningful description in the CV**: longer, richer coverage often signals greater personal relevance, but avoid rewarding verbosity alone.
- Weight **recency**: favour more recent sustained work where evidence strength is comparable.
- Weight **duration, ownership, actual impact, repeated evidence across roles, and PM relevance**.
- Prefer well-evidenced, substantial experiences that users will recognise as part of their own professional identity.
- Do not automatically privilege the last job, the fanciest company or a technical buzzword.
- Cover diverse capabilities only if there is genuine evidence; do not force four.
- Never fabricate outcomes, qualifications, user research, experiments, adoption, metrics or skills.
- Do not turn small or historical non-PM experiences into major PM claims.

**Suggested design approach:** Have the analysis stage produce evidence-linked candidate capabilities, with rationale and prioritisation attributes, then select and abstract into the final map. Keep the scoring heuristic configurable rather than baking in rigid word-count thresholds. Use consistent structured output and unit tests demonstrating (a) nuanced abstraction and (b) priority of substantive, recent evidence.

## 2. CV privacy one-liner — exact requested replacement

Replace the currently displayed long sentence and link:

`Your CV is used to generate your Career DNA. See how your information is handled.`

with exactly:

**`Your CV file will not be saved, only read in your browser.`**

This is the short UI copy requested, not a licence to misstate data practices. Verify whether CV files are indeed processed in-browser and not saved; if the implementation differs, fix it to support this statement or raise a blocker rather than claiming something false. Retain a separate, accessible detailed Privacy & Data disclosure. The detailed disclosure should explicitly acknowledge that extracted text and editing instructions may be transmitted to the server and OpenAI, and that temporary in-memory retention or aggregate analytics may occur according to the real implementation. Do not imply that no CV-derived data leaves the browser.

## 3. Privacy & Data expandable disclosure — shorten and align

Reference `03_privacy_current.png`: the text is very long, visually dense and has awkward line breaks.

- Keep Privacy & Data collapsible and readable.
- Use a compact left-aligned container, reasonable maximum width, consistent line-height and 2–3 short paragraphs or compact bullets.
- Do not center-align long prose or force arbitrary line breaks.
- Retain materially important details: CV file is read locally (if verified); extracted CV text/instructions go to backend/OpenAI for generation/refinement; server results may remain temporarily in memory for retries (current implementation says up to 10 minutes); browser refresh clears session state (if true); no persistent app database storage of CV files/maps (if true); aggregate counts and anonymous request receipts for deduplication (currently 48h expiry) and short-lived hashed network identifier for rate limits (if true); OpenAI has its own processing/retention policies.
- **Suggested compact copy (verify against implementation before use):**
  “Your CV file is read in your browser and isn't saved by this app. To create or refine your DNA, extracted text and your instructions are sent to our service and OpenAI. Temporary results may be held in memory for up to 10 minutes for retries; refreshing clears your browser session.\n\nWe don't store CV files or maps in our app database. We keep aggregate creation/download counts and short-lived anonymous technical records for deduplication and abuse prevention. OpenAI's processing and retention policies also apply.”
- If exact TTLs and data categories are still important, show them in a small secondary “Technical details” disclosure or compact final sentence; do not quietly remove material disclosures.

## 4. Map styling: richer visual narrative, not a new visual system

Reference `04_map_current_annotated.png` (user marks **1** = header, **2** = footer insight); reference `06_preferred_character_style.png` for **character and decorative asset style**. User strongly prefers the cute, polished 3D cartoon characters and small contextual illustrations shown in reference 06.

### 4A. Header (marked 1)
- Visually center the **whole header composition** within the map: PM logo + large `My PM Career DNA` title + personalised DNA theme. The current header reads as spread out and unbalanced.
- Make the main title the visual anchor; the theme appears in a smaller adjoining capsule or elegantly integrated subheading. Use flex/grid composition that is mathematically balanced rather than manually offset.
- No arbitrary red “1” markup in final output (annotation only).
- Handle theme length responsively without clipping or awkward breaks.

### 4B. Bottom highlighted summary (marked 2)
- Retain the bottom concluding insight as a **special, celebratory highlight**, not a plain line of text.
- Give it its own well-spaced banner/ribbon/capsule with a subtle conceptual icon and tasteful gradient or shadow.
- **Add clear vertical breathing room between the DNA card container and this summary.** Current banner almost touches the preceding section.
- Ensure the banner sits cleanly above the `PM Career Studio` footer with ample margins.
- No arbitrary red “2” markup in final output.

### 4C. Character placement and orientation
- Make the illustrated character **face / look inward toward the DNA cards and text**. If placed at far right, character should face left; if at far left, face right.
- Do not rotate the entire image with text/logo/details if that mirrors words on the laptop or clothing; use a facing-correct asset or appropriately redrawn variant.
- Avoid awkward empty space and keep character secondary to the card content.
- Reuse approved character asset/style before creating new characters.

### 4D. Richer decoration using content-related motifs
Make the map feel more alive and content-specific without creating distracting clutter:
- **Analytics/Data:** funnel, subtle chart, magnifier, signal markers, experiment dots.
- **Growth:** upward line chart, activation funnel, branching paths, progress markers.
- **AI:** chip, model nodes, small evaluation symbols, luminous connections.
- **Platform:** modular blocks, stacked layers, architecture links.
- **Trust & Safety:** shield, check, balanced controls, protection motif.
- **Interaction/UX:** conversation bubbles, feedback loops, journey paths, expressive cues.
Use these selectively based on actual generated categories and CV evidence. Consistent icon geometry (soft, rounded 3D miniature objects), scale, shadow, visual language and palette.

**Do not** introduce every decorative motif in each map. No unrelated decorative clutter. No mixing of flat emojis, photorealism and 3D clay graphics. Prefer coded vector/shape decoration or reusable existing assets where practical.

### 4E. Color and typography
- Enrich the coordinated palette with subtle peach, blush, mint, aqua, sky blue, lilac and soft yellow, all consistent with the current map.
- Maintain high contrast on core titles and important body copy.
- De-emphasise metadata, helper copy and secondary labels using softer gray-purple tones. **Do not render every single line in equally heavy near-black.**
- Maintain accessible readability; do not make important text too pale.
- Refine weight, spacing and layout hierarchy; not everything needs bold.
- Keep cards legible at the actual exported resolution.

### 4F. Journey and connection design
- Maintain the hard rule: **every platform/pedestal in the same map uses the SAME geometry and illustration style; only theme colors vary.**
- Improve the current oversimplified horizontal connections by introducing elegant, gently curved/woven luminous paths, small milestones, progression details or layered routes — inspired by the preferred visuals.
- Keep connections consistent, subtle and behind the content. Journey stages should visibly feed into `Shaped My PM DNA` without crossing content.
- Connectors should preserve sensible meaning: career stages contribute to current capabilities. Avoid complex spaghetti diagrams.
- Make sure coherent connection geometry works for 2, 3 and 4 stages, not just the example count.

### 4G. Layout integrity
- Do not stretch character/graphics.
- Avoid clipped text, card overlap and imbalanced spacing.
- Use componentised assets/layout, not one flattened screenshot that cannot update text.
- Test responsive preview plus PNG export (and any other existing download format) for consistent layout.

## 5. The two expandable sections: approved, leave alignment intact

Reference `05_sections_alignment_approved.png` shows `Your Next Chapter` and `View Supporting Evidence` **already aligned correctly**.
- This issue is **resolved**. Do not redesign or inadvertently regress their horizontal alignment, width, paddings, margins, background colour or toggle behaviour.
- Preserve two independent collapsible sections and their common visual styling.
- Preserve their placement beneath the map and above primary page actions.

## 6. Supporting Evidence: remove repetitive source labels

Inside `View Supporting Evidence`, remove repeated generic text **`Evidence: Career source`** that appears on every career row.
- Keep actual evidence descriptions and source mapping intact.
- If a specific traceable reference is available and meaningful, it can remain in a discreet form; don't repeat a useless placeholder label in every row.
- Do not remove the underlying evidence or grounding logic.

## 7. Refine My DNA: simpler instructions

Delete the redundant standalone label:

`Tell us what you’d like to change`

Replace the long helper text:

`Tell us what feels inaccurate, missing or too generic. For a more precise update, you can paste the exact sentence you'd like to change.`

with shorter, action-oriented English, recommended:

**`Paste the sentence you'd like to change and tell us what to replace it with.`**

This is *guidance*, not a requirement: still accept natural-language requests without an exact pasted sentence, and use the model to resolve the target. Do not add new steps or additional forms.

Preserve prior approved Refine behaviour:
- Text only (no microphone/voice input).
- Use configured GPT-6 Sol only where endpoint/model ID is genuinely supported; do not invent an API identifier or silently substitute.
- No historical edit transcript clutter inside the modal.
- Sticky modal header: `Refine My DNA`, subtitle, always-available X; remove redundant tiny divider near X.
- One instruction input and one Apply Changes button.
- Spinner/loading; estimated 20–30 sec only as approximate copy, never a fake countdown.
- Invalid blank required fields produce a simple inline error, **no Yes/No confirmation**.
- On success: update only requested text, clear input, close modal, show the updated real map.
- On failure: keep modal open/input intact, show clear error, allow retry, don't mutate map.
- Never regenerate the entire visual style for a targeted text edit.

## 8. Creation and download metrics; shorter Download label

Current text example: `6 PM Career DNAs Created`.

Keep the creation count and add a **download count on the same line**, e.g.:

`6 PM Career DNAs Created  ·  3 Downloads`

Numbers above are **illustrative only**; query or use existing real counter data. Never display fabricated statistics.

- A download is an actual successful user-triggered export/download, not a map creation, preview, retry or automatic rerender.
- Avoid counting the same click multiple times due to concurrent requests/retries; use a reasonable idempotency approach consistent with existing anonymous counting architecture.
- If there is no durable download-count endpoint/storage, add the smallest privacy-preserving aggregate counter path consistent with existing architecture; do not repurpose creation count.
- Handle count retrieval failure gracefully: omit the unavailable download count rather than showing `0` falsely.
- Keep both counters aligned on one row at desktop widths, wrapping gracefully on mobile.
- Do not expose personal data and do not store CV/map content for this metric.

Rename the primary action button:

`Download DNA Map` → **`Download`**

Preserve its existing download behaviour and the correct exported file type.

## 9. Asset reuse and generation strategy

**Reference 06 is the preferred illustrative art direction.** It is a reference illustration, not a licence to insert the whole archetype poster in the product.

First reuse existing repository illustration assets if available. If additional assets are necessary, generate or create a small *cohesive asset family* in the same warm rounded 3D style, for example:
- Inward-facing character variant(s), with transparent backgrounds.
- Small reusable icons for data funnel, growth curve, AI chip, modular platform, shield and interaction design.
- Small path nodes, leaves/bushes, glows and decorative cues.

All assets in the map must match each other in perspective, lighting, stroke/shadow treatment, scale and palette. Make variants themeable by category; do not create random art styles per card. Use transparent assets or SVG where appropriate; do not bake dynamic words into illustrations. Preserve fonts' licensing; don't distribute raw font files.

A new asset pack is **not required just to implement layout/text changes**. If suitable reusable assets already exist, do not generate redundant images. The bundled reference images here are visual guidance; Codex should prefer existing source assets and create missing ones only when genuinely necessary.

## 10. Explicit non-goals

No new end-to-end redesign. No V2. No voice recognition. No additional career domains. No hardcoded example CV content. No automatic rewriting of unrelated DNA fields. No expanded confirmation-dialog chains. No loss of already-fixed expandable panel alignment. No fake metric values or unsupported privacy assurances.

## 11. Acceptance criteria and regression tests

1. PM capabilities are professional abstractions, not task-by-task restatements.
2. Capability selection reflects evidence depth and recency while respecting relevance and truth.
3. Exact requested short CV one-liner appears, and is factually supported by implementation.
4. Detailed privacy disclosure is shorter and neatly laid out without hiding material facts.
5. Header is balanced and centered as one coherent group; dynamic theme fits.
6. Insight banner has its own highlighted styling and does not touch the DNA cards.
7. Character looks toward the map content; no mirrored text.
8. Decoration is contextual, consistent, restrained, and more varied than the current design.
9. Journey platform silhouettes are uniform within a map; connections are richer but clear.
10. `Your Next Chapter` and `View Supporting Evidence` remain correctly aligned and styled.
11. Repeated `Evidence: Career source` strings are absent, while substantive evidence is preserved.
12. Refine helper uses the concise replacement; no redundant label.
13. Text-only Refine success/failure/validation flows remain reliable; targeted changes preserve visuals.
14. Both real creation and download counts display together when available; mobile remains responsive.
15. Primary button reads `Download` and still downloads correctly.
16. Test at least 3 contrasting PM CVs (AI/safety, growth/analytics, enterprise/platform) to confirm each generates distinct, evidenced DNA and relevant decoration.
17. Inspect both live map and downloaded output for overflow/clipping/contrast/spacing problems.
18. Check prior fixed features for regressions before completion.

## 12. Implementation output requested from Codex

- Summarise changed files/components and why.
- State whether existing assets were reused or which new asset files were made.
- Name the actual model ID configured for Refine, or clearly state if unsupported.
- Confirm the real privacy processing/retention behaviour before publishing the short assurance.
- Explain how the download count is sourced and deduplicated.
- Report build/test results and any known limitations.
- Provide before/after screenshots for the map header, footer insight, and privacy section.

**North star:** The output should feel like a warm, visually rich, evidence-grounded recognition of a PM's enduring strengths. Better content and coherent detail matter more than gratuitous new features.
