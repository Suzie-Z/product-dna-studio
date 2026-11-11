# Reference-fidelity correction

This implements the latest Mandatory Visual Redesign, with the user's explicit override that each generation produces only one result and one downloadable file. No alternate design or second result image is produced. Desktop and phone layouts replace the same single SVG root in place; the hidden export canvas is not another visible result. The only export is a 3200×2360 PNG.

## Approved illustration library

`preview/assets/career-world-atlas.png` is a reusable transparent production atlas prepared from the original My Product DNA reference's art direction. It contains a cheerful, gender-neutral human chibi with expressive face and laptop, four genuinely dimensional illustrated rocky islands, fourteen glossy professional symbols, clouds, and greenery/flowers. The character is a fixed brand illustration, not a likeness inferred from a resume. An illustrated domain accessory changes symbolically using validated career context. No robots, emoji people, flat line-icon substitutes or plain disc platforms remain.

The atlas is bundled locally into the frontend and SVG export, not generated per visitor. Transparent source regions are reused through SVG viewports; application-rendered SVG text remains selectable, XML-escaped and editable only by regenerating AI content. User inputs never become artwork prompts or image URLs.

Reusable components in `preview/poster.js`: `CareerJourneyIsland`, `JourneyConnection`, `CareerCharacter`, `CapabilityCard`, `DecorativeBackground`, and `CareerDNAResult`. These preserve the reference's two-band world, dimensional pastel cards, overlapping character, luminous journey trail, glowing bridge connections, clouds and flowering greenery. Count changes adjust spacing rather than adding invented islands or capabilities.

## Content and evidence

The existing structured career analysis remains separate from rendering. Its job-family instructions now explicitly distinguish professional categories (e.g. Software Engineering or AI Product Management) from activities (e.g. Multimodal Evaluation or API Development). Known activity headings are rejected with targeted repair feedback. Strengths must be transferable capabilities; a strength repeating a journey heading is rejected. These safeguards supplement model judgment; they do not independently certify job history or every semantic inference. Each list remains 1–4 items based on actual evidence, never slot filling.

`View Full Journey` is a read-only, initially collapsed disclosure. It shows source-grounded categories, capability evidence, and optional original context from current browser memory. It introduces no manual map editing, content storage, additional image, or API call. Source quotes stay out of the image and export.

## Visual review and validation

The full result/page screenshots were captured in ignored test artifacts and compared side-by-side with the original reference. The human chibi, rock depth, glossy icons, floral environment, illuminated path, typography and two-section hierarchy were inspected. All 32 independent 1–4 node/card desktop/mobile layouts pass fitting checks. The browser flow checks that there is exactly one top-level map SVG after generation and after resizing, one human illustration, and one download button.

43 automated tests cover the updated bounds and label guards, exact citations, source parsing, microphone fallback, regeneration, read-only evidence, safe text rendering, counters and PNG download. The exported PNG's actual character artwork was checked as well as its dimensions; the illustration does not disappear during SVG rasterisation. Live OpenAI verification and deployed commit IDs are recorded in DEPLOYED.md after rollout.
