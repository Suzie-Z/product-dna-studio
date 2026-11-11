> The referenced asset paths are inside the downloadable kit. Download: https://raw.githubusercontent.com/Suzie-Z/product-dna-studio/9bf27e577d9dd54a20d894eaa81578bf18f61f04/downloads/Career_DNA_Codex_Correction_Kit.zip

# Codex note — PM Career DNA, product managers only

## Decision / 本轮范围决定

The first version targets internet/technology product managers only. The product name is **PM Career DNA**. Do not build or generate a generic career DNA experience for other professions in this release. We will consider other careers only after the PM experience is sufficiently refined and validated.

“Product” means product-management roles, not every profession involved in building products. Do not describe engineers, designers, analysts, consultants, chefs, teachers or other professionals as target personas for V1 merely because some skills transfer to product work.

本版只服务互联网/科技产品经理。先把 PM 的经历归纳、能力映射、图形质量、内容准确性和使用流程打磨好，再考虑其他职业。这不是“支持所有职业，再默认给他们套 PM 模板”。

## PM role experience → PM capability

My PM Journey must describe the types of PM roles evidenced by the user's experience: Growth PM, Platform PM, Operations PM, AI PM, Data PM, Trust & Safety PM, B2B / Enterprise PM, AI Enablement PM and other approved PM types in role-taxonomy.json.

- Upper section = actual PM role types, responsibilities and supported chronology.
- Lower section = independently evidenced transferable PM capabilities.
- Examples: Platform PM → Systems & Platform Design; AI PM → AI Product Judgement; Growth PM → Growth Experimentation / Data-Informed Decisions.
- Do not substitute broad areas such as Product Development, Business Consulting or project activities for PM role types.
- A Growth Hacker role can keep its actual source title; do not invent the title Growth PM.
- Non-PM prior experience may support a PM user's capabilities, but cannot be relabelled as a PM job without PM responsibility evidence.
- If the input contains only non-PM experience, ask one focused question for PM roles/responsibilities. Do not produce a generic non-PM map and do not fabricate a transition into PM.
- Independently select 1–4 role nodes and 1–4 capabilities based on evidence; never fill slots.

## Visible naming — replace the generic Career DNA identity

Use the following user-visible strings consistently:

| Surface | Required text |
| --- | --- |
| Product name, page title, header, footer, metadata | PM Career DNA |
| Hero | Discover Your PM Career DNA |
| Input step | Share Your PM Journey |
| Generate button | Generate My PM Career DNA |
| Output title | My PM Career DNA |
| Journey section | My PM Journey |
| Capability section | Shape My PM DNA |
| Read-only evidence | View Full PM Journey |
| Download action | Download PNG |
| Download filename | my-pm-career-dna.png |
| Accessible map label | Your PM Career DNA map |

Update visible loading messages, errors, empty states, consent/privacy copy, browser titles, social metadata and export branding as well. Preserve the actual privacy policy and processing disclosure; only update the product name where necessary.

Do NOT do a blind global text replacement across source identifiers, API endpoints, file paths, environment variables, original CV text or historical reference images. Internal compatibility names such as career_ai.py and /api/career-dna/* can remain while the user-facing brand changes. The canonical word is Career, not Korea.

## PM DNA logo

Use `brand/pm-career-dna-logo-white.png`: one PM monogram integrated with a DNA helix, primarily blue/teal, white background, restrained lavender/amber accents. The letters are PM, replacing the previous AI mark. Do not show old AI and new PM logos together as competing identities.

Use it in the site header and output branding. Inspect actual legibility at header size and in the exported PNG. This is raster logo artwork; do not claim it is an SVG/vector master. Any favicon/small-size adaptation should preserve the same mark rather than introduce another logo design.

## Existing designed resources in this package

- 24 fictional gender-neutral human PM avatar sprites, with one consistent warm-apricot cartoon skin material. Variation is hairstyle, outfit colour, glasses, pose, expression and work tools; no skin/gender differentiation.
- 24 PM-scene icons: growth, conversion, platform, API, operations, AI, analytics, experimentation, trust & safety, user insight, strategy, roadmap, UX, commerce, mobile, SaaS, enterprise, content, marketplace, recommendation, monetization, collaboration, delivery, automation.
- 6 theme palettes and 15 PM functional-role categories, with manifest IDs, sprite coordinates and evidence-qualified role-to-capability hints.
- Both original reference images for composition and product-role art direction.
- White-background avatar overview for review, plus a transparent production atlas for composition. Never show an asset atlas as a user's final PM Career DNA output.

The library covers the listed common PM contexts; it is not a claim to exhaust every possible product discipline. Atlas cells are 256px native. Validate transparent edges, crop safety, small-size clarity and intended export size before production use. Additional high-resolution assets may need separate refinement.

## Non-negotiable output behaviour

Exactly ONE visible complete My PM Career DNA result and ONE PNG per download. Replace the old result during regeneration. Keep the export canvas detached from the DOM. Do not rely on hidden attributes overridden by display styles.

No overlapping foreground content: character, work props, career icons, text, islands and capability cards need independent safe regions. Decorative environment must not cover them. Preserve the original premium illustrated world; no robot or flat icon shortcuts.

Select one avatar_id and one theme_id for each new generation. Preview, responsive changes, evidence disclosure and export reuse those exact IDs. Themes must include blue, green, yellow, coral and teal options rather than every map being purple. Do not infer appearance or personality from CVs.

Multilingual input, English-only map output, literal citation validation, no invented roles/capabilities, no resume/map persistence, aggregate generation counts and the existing call limit remain in force. This scope change does not authorize new tracking, storage, paid infrastructure or higher limits.

## Delivery gate

1. A real PM profile yields PM role types mapped to distinct supported capabilities.
2. A non-PM-only profile asks for PM context rather than producing a non-PM or fabricated PM map.
3. No generic Career DNA or old AI-logo branding remains in the visible app/export; historical references and user-submitted text are exempt.
4. Exactly one complete result is visible after generation, regeneration, resizing, evidence disclosure and download; one click downloads one correctly branded PNG.
5. PM-themed assets and varied approved themes are actually integrated, not merely delivered as files.
6. Desktop, mobile and exported PNG are visually inspected against both reference images, including overlap and text-fit checks.

## Integration status

This note, PM logo and resource kit are a Codex handoff. They do not by themselves mean the live website has already been renamed, narrowed to PM or connected to the new avatar/theme library. The duplicate-canvas fix was deployed separately. Implement and verify the above changes before reporting the PM rebrand complete.
