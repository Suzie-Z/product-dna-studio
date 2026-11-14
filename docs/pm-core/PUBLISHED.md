# Original PM Career Studio core experience — published

Published 14 November 2026 (Australia/Sydney), following the user's explicit deployment request.

Live website: https://product-dna-studio-preview.onrender.com/?v=3a4a349
API: https://product-dna-studio-ai.onrender.com
Runtime commit: `3a4a3492b4e8cdd02b5de60b8f23d667e058a4b7`.

- API service `srv-dbpflmjrjlhs73fps3kg`: deploy `dep-dbs29djl550s73f8ferg`, confirmed **live**.
- Static service `srv-dbpf7to8v5cc73e3jtfg`: deploy `dep-dbs2a8m1egvs73cl4990`, confirmed **live**.
- Existing workspace: Suzie's AI World. Existing services, URLs, plans, API key/model variables, quotas and database were retained. No new resource or environment-variable mutation was made.
- Previous published runtime `717d3961f6246c5fc3332defe86763fde1f9ba18` and original source baseline `c065bdfccc5d37cf336b9e40acc62c8adfeab142` remain available for recovery. V2 remains an archived direction, not the published replacement.

## Verification

The existing **110-test** result is recorded in [implementation delivery](DELIVERY.md). Both current deployment statuses were confirmed through Render, and the real API `/health` returned ready with the existing `gpt-6-astra` extraction/synthesis/refinement configuration, `gpt-transcribe` voice configuration and no image-model request.

The served static bundle matched the tested local bundle byte for byte. SHA-256: `6ec0c70cfc4b85f6b1d8b8f897a870c982e3f18aa1f94e132a6ab95169f0b0c0`.

A real, non-generative API request to the new content-only refinement boundary returned the expected single clarification for a background-change request, without modifying a map or invoking a model. Browser checks then exercised the served frontend, actual DOCX parsing, the initially hidden chatbot, CV-only generation payload, one rendered map, on-demand Refine, and one PNG download. The browser's generation transport was mocked to avoid paid calls and artificial public creations. This is UI and deployment verification, **not a live new-prompt quality evaluation**. Chromium's environment CA trust differed from the shell's; the site was fetched with normal TLS verification using urllib and bridged into the browser for these checks. No certificate verification was disabled.

Public total remained **4 before and 4 after** verification. Legacy totals were not reset. No API key or test credential was retrieved, rotated or exposed.

Artifacts: `work/pm-core-live/report.json`, `live-cv-first.png`, `live-ui-map-mocked-content.png`, `live-ui-single-map.png`. All use synthetic evidence; no visitor CV was used.

## Experience

Open the website → Explore My PM Career DNA → Upload CV (PDF/DOCX) → Discover My DNA. Real user generation uses the retained server-side AI configuration. Refine My DNA opens the optional text/voice dialog after the map exists. A replacement CV starts a full new analysis; ordinary edits preserve presentation. Download still produces one PNG.

The free service can need time to wake up. Real generation quality, latency and provider billing for the new prompts were not measured in this deployment check. Existing parser/device/voice/provider-retention and session-memory limits continue to apply as documented in the implementation delivery.
