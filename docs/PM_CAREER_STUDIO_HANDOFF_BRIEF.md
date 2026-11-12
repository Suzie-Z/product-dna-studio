# PM Career Studio — Codex Implementation Brief
**Version:** 1.0 | **Scope:** Copy + visual system + compact result layout + flexible conversational refinement + output quality.  
**Status:** Ready for repo inspection and implementation.  
**IMPORTANT:** This is a functional product specification, NOT a request to generate a one-off reference image. Implement working website features. Reference PNGs are inspiration / comparison fixtures, not pixel-exact pages or image assets to stretch into the UI.

## 0. READ FIRST / NON-NEGOTIABLE INSTRUCTIONS

1. **Inspect the actual repository before editing.** Identify framework, page components, AI endpoints/prompts, image generation, existing asset library, state and storage behavior, and current export mechanism. Return a short architecture and implementation plan before major changes. Do not claim any feature exists until verified.
2. **Preserve the existing functioning experience**, upload flow, career parsing, PM Journey → PM Career DNA logic, export/share pipeline, and user ability to edit a result. Do not undertake a wholesale rewrite.
3. **What the product is:** a warm, delightful professional self-recognition experience. Its emotional arc ends at **Recognition → Self-Discovery → Inspiration**. Do NOT introduce Growth, Future DNA, career coaching, action plans, skills gap reports or mentoring functions.
4. **What the product is not:** a skill graph, dense resume dump, map of all relationships, or a generic list of buzzwords. Synthesize at most 4 distinct high-level strengths, grounded in experience.
5. **Typography and readable text must be rendered as editable HTML/SVG (or a reliable canvas text layer), not baked into an AI-generated background.** AI can generate *decorative* assets only, not final text-bearing layouts.
6. **Design variation is mandatory**, but not unconstrained randomness: use structured, semantic, reproducible choices, a coherent visual family and collision/layout checks.
7. **Do not assert privacy behavior that code does not enforce.** Audit file upload handling, remote API processing, temporary storage, logs, analytics, provider retention, caches, database writes and export handling before displaying "Your CV won't be saved" or "we only count creations". Where it cannot be verified, use the fallback copy specified below and report required engineering work.

## 1. PRODUCT INTENT AND EMOTIONAL TONE

**Brand:** PM Career Studio (not just "Career Studio" on the landing logo; retain the established PM DNA logo where relevant).  
**Hero:** Discover Your **PM Career DNA**.  
**Product thought:** "See the person you've become. Be inspired by who you are."  
**Journey:** Recognition (my experience matters) → Self-Discovery (a deeper identity emerges) → Inspiration (my past self can encourage my present self).

Voice: warm, validating but not flattering, insightful rather than motivational clichés; easy, human and inviting. Do not use overly therapeutic, mystical, sentimental or self-congratulatory language. Avoid overlong copy. The app's analysis should feel like *understanding*, never like processing a data record.

## 2. FINAL UI COPY — USE THESE STRINGS

Implement these as a centralized copy dictionary / localization constants (easy for future editing). Preserve title case and punctuation.

| Location | Primary text | Supporting copy / behavior |
|---|---|---|
| Brand header | **PM Career Studio** | Existing brand mark; do not change underlying logo shape. |
| Hero eyebrow | **FOR PRODUCT MANAGERS** | Small uppercase. |
| Hero headline | **Discover Your PM Career DNA** | Two lines if needed; visually dominant. |
| Hero subtitle (preferred) | **See how far you've come. Be inspired by who you are.** | Short, centered, max two lines. Avoid old two-sentence wall of text. |
| Primary CTA | **Explore My PM Career DNA** | Maintain existing function. |
| Upload section title | **Explore My PM Career DNA** | Use consistent capitalization. |
| Upload button | **Upload CV** | Existing accepted file types and limit must reflect actual validation. |
| Upload privacy — only AFTER verified | **Your CV is used only to create this Career DNA and isn't saved.** | Must be truthful end-to-end, including third-party provider handling. |
| Upload privacy — safe fallback | **Your CV is used to generate your Career DNA. See how your information is handled.** | Link to accurate privacy disclosure; use this if code/retention unverified. |
| Optional personal context label | **What moments are you proud of?** | Mark clearly **Optional**. |
| Optional context placeholder | **Share a proud moment, a challenge you overcame, or a strength you'd love us to notice…** | Freely written input, can be blank; no forcing users to list skills. |
| Optional helper | **A little context can help us see the story behind your CV.** | Small, one line if space allows. |
| Analysis heading | **Reading your story…** | Replaces robotic "Analysing…" if desired; if keeping "Analysing…", supporting copy still must change. |
| Analysis subcopy | **Looking beyond your roles to discover the strengths that shaped you.** | Make the app feel attentive, not invasive. |
| Analysis timing | **This usually takes about 60–90 seconds.** | Show as estimate (NOT guarantee); based on measured performance, update when data exists. |
| Analysis cancel | **Cancel** | Must actually cancel request when possible, prevent stale completion, reset state. |
| Counter label | **PM Career DNAs Created** | Display count as e.g. "2 PM Career DNAs Created"; not "Maps", "Runs", "Records". |
| Counter privacy note — verified only | **We count creations, not your personal data.** | Requires verification that analytics collect only aggregate counts and necessary operational metadata is appropriately handled. |
| Counter feedback | **I'd love to hear what you discovered. Share your thoughts on my LinkedIn post.** | Actual post URL must be configurable; do not fabricate. If no URL available, show plain non-linked text or hide link. |
| Refine heading | **Make it feel more like you** | Retain existing action entry point. |
| Refine placeholder | **Paste what you'd like to change, or tell me in your own words…** | This must be an actual freeform editor, not a fixed keyword list. |
| Refine helper | **Try: “Shorten this insight”, “Try warmer colors”, or “Use different icons”.** | Examples are illustrative, never the only supported commands. |
| Refine actions | **Apply Changes** / **Undo** / **Try Again** | Must work; preserve original and previous versions. |

**Copy handling notes**
- User suggested "I'm reading you." It has intimacy, but could sound like personal surveillance in English. Prefer **Reading your story…** with supportive explanation.
- **Do not show elapsed time** as the main analysis message. Estimated duration reduces uncertainty better. An optional small accessible progress indicator is fine; never fake precise completion percentages.
- Do not show internal tracking migration dates or notes such as "New tracking since 2026-11-11; earlier totals included test runs" in customer-facing UI. Keep any tracking caveat in developer/admin documentation. Exclude test runs from public counts when feasible.
- "PM Career DNAs Created" is *aggregated creations*, not unique persons and not number of CVs stored. If count is approximate, label as such and avoid false precision.

## 3. VISUAL DESIGN: KEEP THE ORIGINAL PURPLE REFERENCE'S ART DIRECTION

### Reference priority
1. `references/01_original_purple_style_target.png` — **PRIMARY visual quality benchmark**: collectible/shareable game-like infographic, airy lavender atmosphere, polished 2.5D details, clean rhythm and readable cards.
2. `references/02_current_green_output_to_improve.png` — **NEGATIVE comparison for deficiencies**, not a strict style target: too blank/clinical in places, overly tall/boxy cards, large gaps between icons/labels/platforms, generic repeated assets, text overflow/filler, less intentional connection from journey to DNA.
3. `references/03_visual_variation_direction_board.png` — **IDEA BOARD** for multiple platform forms, icon families and compact layout. Not an exact layout or a new mandatory asset pack.
4. `references/04_copy_and_page_direction_board.png` — **IDEA BOARD** for new copy and page sections. Do not rasterize its text.

### Design language
- **Soft, luminous 2.5D / playful premium / whimsical miniature world**, not flat enterprise dashboards; no heavy neumorphic gray slabs.
- Airy background with restrained gradients, translucent edge highlights, gentle ambient shadow, pastel glow, rounded shapes; high-quality, publishable visual polish.
- **Theme may vary**: lavender (reference), mint, peach, sky, lilac-blue, etc. Do not freeze the entire app to purple. Each rendered result should feel harmonious within ONE chosen theme family. No random unrelated bright colors.
- White or near-white translucent rounded master panels; consistent radius and stroke weights, soft shadows, and clear content layering. Avoid over-nesting outlines (e.g., cards surrounded by 3–4 almost identical borders).
- Header **centered**: logo and "My PM Career DNA" form one compact aligned unit; don't leave a giant gap between mark and title. Include a compact subtitle only when it adds meaning.
- Decorative clouds/foliage should feel integrated. No awkward half-cut clouds at the left/right margins; crop only when intentional and visually natural, otherwise omit.
- Journey and DNA are distinct but visually connected by a subtle flowing light path or progression motif. The platform visual belongs close to its label, not separated by a huge empty region.
- **Content hierarchy:** identity / 2–4 career stages / 2–4 top strengths / concise specific evidence. Do not cram every extracted skill onto the card.

### Component structure
**Top band**: compact centered identity headline, optional one-line synthesized insight.  
**Journey band**: a horizontal progression of up to four summarized experience categories (not necessarily every company), each using icon → category title → up to 2 short evidence fragments → platform underneath, with a continuous pathway.  
**Transition**: small connective label "Shaped My PM DNA", visually tied to stages below; avoid a tall divider block.  
**DNA band**: 2–4 compact high-quality cards with dynamic icon, 2–5 word capability name, ONE high-impact description line, and a compact line or 2 of specific supporting evidence/tags; optional character/mascot positioned intentionally, never reducing text legibility.  
**Footer**: optional one-line identity summary, understated brand signature. Nothing more.

### Typography limits (adaptive, not hard truncation)
- Identity summary: ideally <= 12–16 words; never repeated verbatim in several sections.
- Journey category title: 1–3 words or one short phrase. Journey description: max 2 short lines total; prioritize meaning over exhaustive details.
- DNA card title: ideally 2–5 words. Card insight: ONE readable sentence, ideally <= 10–15 words; small evidence chips usually 2–4 items, or two compact lines.
- Tag terms may be separated by middle dots `·`, e.g. `Evaluation · Golden Sets · Data Construction · Use Cases`; use accessible wrapping, not cramped run-on text.
- **Never display engineering placeholders** such as "Regenerate for shorter wording" in public export. If content is long, re-summarize and then validate layout before displaying.
- Preserve meaningful technical specificity: golden sets, model capability evaluation, data construction, risk signals, governance frameworks, when supported by source data.

## 4. SEMANTIC VISUAL VARIETY: ISLANDS / PLATFORMS / PATHWAYS

Current defect: four identical colored rock disks with the same repeat icon family make results templated. Implement a **curated visual vocabulary** with at least 6 platform variations, 4 pathway treatments, and several semantic icon choices per category. Select variations according to user journey and capability meaning, not blind random sampling.

### Six platform archetypes (minimum)
1. **Floating Garden Island** — soft floating earth shelf, grass/flowers, warm/caring/community/people/customer experience.
2. **Crystal / Prism Platform** — faceted translucent crystal pedestal, AI, analytical rigor, evaluation, insights.
3. **Layered Modular Platform** — stacked slabs or blocks with precision edge lighting, reusable platforms, architecture, systems design.
4. **Stepped Quest Stage** — small rising steps/flags, growth across career stages, decision-making, leadership, progression (visual motif only; do NOT add growth planning features).
5. **Cloud / Nebula Platform** — weightless pastel cloud, exploration, discovery, creativity, experimentation.
6. **Circuit / Tech Podium** — subtle circuitry, illuminated rim, engineered products, automation, technology.
7. **Stone / Heritage Platform** (optional) — polished miniature stone with plants for governance, resilience, foundational practices.
8. **Waterfall Island** (optional) — moving/waterfall motif for data flow, interconnected systems, operational feedback.

**Dynamic selection:** define platform archetype metadata `{id, semantics, themePalette, shapeVariant, assetRef}`. Pick different but related platforms within a composition; prevent all 4 from having identical geometry. Visuals must remain small and aligned to a common baseline.

### Pathway families (minimum four)
- **Soft glowing ribbon** (default): thin warm light curve behind stage platforms.
- **Floating stepping stones**: short gentle arcs, progression naturally implied.
- **Constellation / dotted spark trail**: small luminous points with curved links.
- **Layered light streams**: thin flowing gradient ribbons converging toward DNA cards.

Pathways must never cross text or impair legibility. They connect the story, not act as the main subject.

### Icon family variety, still coherent
Instead of a single hardcoded `AI chip / Shield / Layer stack / People` set for every user, create a **semantic icon registry** with multiple alternatives and variants per concept. Examples:
- **AI / model understanding:** neural nodes, lab flask + microchips, prism with data pulse, model cube, robot avatar (only if relevant)
- **Evaluation:** magnifying glass over chart, checklist with signal bars, target with calibration ticks, benchmark dial, test tube with metric
- **Platform/system:** modular cubes, infrastructure layers, connected nodes, interlocking building blocks, scalable architecture frame
- **Trust/risk:** secure gate, safety compass, umbrella + shield, balanced scales, verification seal, protective ring
- **Data/insights:** signal waveform, magnifying glass + bars, funnel, data constellation, pattern lens
- **Strategy/commercial:** compass, decision tree, upward arrow with market bars, chess-piece metaphor (tasteful), market radar
- **Collaboration/people:** connected hands, team constellation, community circles, dialogue bubbles, bridge
- **Creative/0→1:** seed + spark, lightbulb + gear, prototyping toolkit, launch capsule

Select icon by a **specific capability**, not by arbitrary word matching or user job title alone. Use variant sets within one icon style family (rounded 2.5D with consistent lighting/perspective) to preserve cohesion; don't mix 3D clay, flat outline and photorealistic icons on the same page.

Icon and platform art can be created by approved image-generation API **as transparent decorative assets** or from a curated, licensed asset library. Do not regenerate entire page images to change icons. Prefer cache / deterministic asset identifiers, configurable seed, theme + semantics, user-facing regenerate affordance, and license/source traceability. Do not copy nonlicensed copyrighted art.

## 5. ONE-VIEWPORT RESULT PAGE / COMPACT LAYOUT

**Primary user request:** On desktop, the generated share result should appear as a single complete 16:9-ish composition without vertical scrolling. Optimize for common 1440×900 and 1366×768 viewports and export at 16:9. Use scale-responsive containers; don't simply set a global CSS `transform: scale(...)` that destroys legibility or hit targets.

Target desktop layout budget (guideline, adjust after measurement):
- Outer safe padding: 20–28px
- Header / identity: 10–14% of available result height
- Journey section: 36–40%
- Transition ribbon: 5–7%
- DNA section: 37–42%
- Footer / breathing room: <= 5%

Eliminate giant vertical whitespace between:
- Journey icon and journey label
- Journey label and platform/island
- Journey section and "Shaped My PM DNA"
- DNA icon and DNA card title
- Description and evidence chips

A compact page must **not** reduce copy to unreadable font sizes. Recommended desktop floor: body ~14px, fine metadata ~12px, headings much larger. For card text that cannot fit: prioritize semantic compression / re-summarization, reduce number of lines or rearrange card; do not hide meaning with CSS overflow or clipping. Implement measured layout constraints plus a content-length validator.

Responsive exceptions: mobile and narrow screens MAY scroll and stack. Do not compromise accessibility on mobile to enforce impossible one-screen constraints. Support browser zoom; no overlap at 125% zoom when reasonable.

**Export:** preserve visual hierarchy on PNG at 1920×1080 (or equivalent 16:9 with adequate pixel density); no cut-off icons, footer, island edges or text; all fonts loaded before capture. Add an automated full-page screenshot/regression check at 1440×900, 1366×768, and exported image size.

## 6. CHAT-STYLE REFINE — ACTUAL EDITING, NOT A FROZEN FORM

Current defect: refine relies on narrow canned instructions or changes text only. Replace or extend with an **open-ended conversational editing interface**. Users must be able to paste exact words, refer to an existing visual component, or describe desired changes naturally, analogous to chatting with a design collaborator.

### UX
- Heading: `Make it feel more like you`.
- Input: `Paste what you'd like to change, or tell me in your own words…`.
- Example suggestions should NOT restrict commands:
  - "Shorten the AI Judgment description to one line."
  - "Replace the shield icon with something that conveys protection without being a shield."
  - "Make the colors warmer; keep the text and layout unchanged."
  - "Use a different pathway style and more varied platforms."
  - "Rename 'Reusable Platform Design' to 'Systems Architecture', but keep the evidence."
  - "Make the page fit without scrolling, and keep all text readable."
  - "The third card sounds generic. Rewrite it using my actual evidence."
- Show updated preview after each apply. Allow follow-up turns, retry, undo and revert to original.
- Whenever user asks to edit only one element, preserve the others. Avoid regenerating the entire content/story unasked.

### AI edit implementation
1. Pass **current canonical structured document state**, **user's freeform instruction**, **relevant provenance/evidence**, **theme/asset manifest**, and **edit history** to a capable model.
2. Return a **typed structured patch** (JSON Patch or equivalent), not unchecked HTML/CSS or random regex replacements. Patch targets may include `copy`, `capabilities`, `evidence`, `layout`, `theme`, `iconKey`, `platformVariant`, `pathwayVariant`, `decorations`.
3. Use schema validation, source grounding and layout constraints to check patches. Never silently invent CV achievements. Reject or clarify ambiguous changes only when necessary.
4. Apply patch immutably to canonical state → re-render deterministic DOM/SVG → validate layout/export → show result.
5. Keep user-created edits across rerenders; support `Undo` and version history (session-only unless user explicitly saves a result).
6. Provide honest error handling if a requested variation cannot be generated; don't claim an edit succeeded when nothing changed.
7. **Color editing MUST be functional:** freeform requests such as "make it less purple", "more mint", "warmer peach", "higher contrast" should update a semantic theme token system (background, panels, journey, cards, icon highlights, pathway, text and shadows) while maintaining contrast. Do not only swap body background.
8. Icon/platform editing MUST be functional: can change one card or the whole set while maintaining consistent style.
9. Ensure plain conversational follow-ups work (e.g. "No, keep the icons, just soften the colors" refers to prior turn correctly).
10. Provide version-aware cancellation and in-flight request handling; don't let stale responses overwrite newer edits.

### Suggested canonical state (adapt to existing code)
```ts
interface CareerDnaDocument {
  identity: { title: string; summary?: string };
  journey: Array<{ id: string; category: string; snippets: string[]; iconKey: string; platformKey: string }>;
  capabilities: Array<{
    id: string; title: string; insight: string;
    evidenceTags: string[]; sourceRefs: string[];
    iconKey: string; cardStyleKey?: string;
  }>;
  visual: {
    themeKey: string; paletteOverrides?: Record<string, string>;
    pathwayKey: string; decorationKey?: string;
    mascotKey?: string; density: "compact" | "comfortable";
  };
  revision: number;
}
```

## 7. AI SYNTHESIS QUALITY / DOES NOT JUST PARROT RESUME

A well-composed card must have **identity + interpretable claim + evidence**:
- Generic / bad: `AI PM — LLM evaluation, experiments, prompts`.
- Better: `AI Product Judgment — Selects and evaluates model capabilities against real use cases, grounded in golden-set testing and experiment evidence.`

This example is illustrative; model must not ascribe golden-set ownership unless source supports it. Avoid repeating job titles as DNA categories by default. Do not force four strengths if evidence only supports two or three.

Desired synthesis workflow: evidence extraction → cross-project problem-solving patterns → high-level capability clustering → 2–4 distinct grounded insights → evidence-backed concise phrasing → quality validation → layout length validation. Keep a source span or evidence ID for each claim. No inflation of seniority, outcomes or technical ownership.

**Acceptance tests** should include different professional backgrounds, sparse vs detailed resumes, changing color only, icon changes only, targeted copy edits, multi-turn contradictory edits, missing asset fallback, missing source evidence, and long title compression without losing meaning.

## 8. PRIVACY / COUNTING / FEEDBACK

User preference: **no CV storage**, no personal-data collection for growth analytics, only total aggregate number of Career DNA creations to assess interest. This is a PRODUCT REQUIREMENT, not a verified implementation fact.

Engineering actions:
- Determine existing request path and any uploads on server, object storage, third-party model provider, logs, telemetry, support systems and DB.
- Design short-lived in-memory / temporary handling where possible; delete upload after processing, exclude CV text/content from application logs and analytics; handle failure/cancel paths.
- Document third-party provider processing and retention (cannot claim no retention if provider keeps it).
- Implement server-side aggregate creation counter, count successful user creations rather than local/test/debug runs; avoid storing unique session/user IDs unless needed for basic integrity/abuse prevention and disclosed. Clearly document exact behavior.
- Offer a **real** link to owner's LinkedIn feedback post when URL provided. Don't make up a link. No pop-up surveys needed.
- Only publish strong privacy claims once implementation and disclosure actually match. If not yet verified, show the safe fallback copy and create a blocking TODO.

## 9. ACCEPTANCE CHECKLIST — MUST PASS BEFORE MERGE

### Copy
- [ ] Header reads `PM Career Studio`; title reads `Discover Your PM Career DNA`.
- [ ] Hero subcopy is exactly the new short preferred version unless user explicitly overrides it.
- [ ] Analysis uses reading/story language and estimated time; **no elapsed timer as main message**.
- [ ] Counter reads `PM Career DNAs Created`; no `Maps`, `Runs`, `Records` or tracking migration text in public UI.
- [ ] Optional prompt encourages proud moments and is actually optional.
- [ ] No unverified privacy assurances.

### Visual
- [ ] Reference 01's airy, shareable, luminous 2.5D quality is noticeably reproduced in component styling (not copying exact pixels).
- [ ] At least six distinct platform archetypes and four pathway styles can be selected.
- [ ] Icons are semantic, varied and coherent; not always the same chip/shield/stacks/people set.
- [ ] Decorative elements are complete / intentionally cropped, no clipped half icons.
- [ ] Header centered and logo/title close; card borders consistent and not over-nested.
- [ ] No placeholder text in final result; evidence tags separate/scan-friendly.
- [ ] Journey icon/label/platform spacing and card icon/title/description spacing compact.
- [ ] Result fully fits default desktop viewport and 16:9 export without scroll or clipping; mobile allowed to scroll.

### Refine
- [ ] User can type *arbitrary natural language* and see a meaningful edit.
- [ ] Color, icon, pathway, platform and copy edits all work.
- [ ] Targeted edits preserve unrelated content.
- [ ] User can undo, retry and chain conversational changes.
- [ ] Output remains factual and supported after refine.

### Engineering deliverables
- [ ] Short pre-change architecture assessment and list of exact files to modify.
- [ ] Working implementation, not just mockups/prompts.
- [ ] Updated text/assets manifest; accessible contrast and interactions.
- [ ] Before/after screenshots for 1440×900, 1366×768, export and mobile.
- [ ] Tests for copy, visual variation, schema patching, privacy counters and overflow.
- [ ] Report of models/API costs/latency, whether decorative assets are generated and cached, and remaining limitations.

## 10. SEQUENCING / DELIVERY PRIORITY

**P0 — Must work first:** compact responsive layout + new copy + verified privacy fallback + refiner accepts open natural language and can really modify colors and specific content + clear provenance.

**P1 — Visual richness:** platform archetype library, pathway library, icon registry, deterministic selection, asset caching and visual variation controls.

**P2 — Quality and polish:** export regression, varied fixtures, model prompt/eval enhancements, cross-browser and accessibility checks.

**Please implement rather than proposing more fixed examples.** The goal is a general-purpose generation system able to adapt to different people's careers and user-directed visual edits while always producing a polished, readable, distinctive, emotionally resonant page.
