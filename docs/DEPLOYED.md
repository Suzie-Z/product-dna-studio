# Single-visible-result correction — 11 November 2026 (Australia/Sydney)

https://product-dna-studio-preview.onrender.com

- Frontend commit `4f10ae209759f1be412a8a28d07e18cb1b8ec704`, deploy `dep-dbpucd0u01pc73992fm0`: live.
- Confirmed the actual duplicate-output bug in the production browser: one visible SVG PLUS one visible export canvas. The global `canvas {display:block}` overrode the canvas `hidden` attribute. Previous SVG-count-only verification missed this. Those older one-result claims were incorrect.
- Export canvas is now detached from the DOM. Removed global canvas display rules and added an explicit hidden-attribute guard. Production rendering verification now reports one visible SVG root, zero DOM export canvases, zero visible export canvases. PNG download passed and phone resizing still leaves a single map. The API was not redeployed because the fix changes only frontend behavior.
- Four browser regression tests passed with the stronger absence-of-DOM-canvas assertions, CV/voice input, regeneration and PNG download checks. Production rendering verification uses a synthetic map fixture and does not claim a new real-provider generation test or increment production counts.
- A separate Codex PM correction handoff was prepared: actionable requirements, 24 character sprites, 24 internet-PM icons, 6 theme palettes, 15 PM role categories, reference-archetype mappings and both original reference images. The generated atlases have 256px native cells; crop and high-resolution use require the documented checks. These libraries and the PM-specific selection/semantic changes are prepared for integration, not claimed as already implemented on the live site.

See [Codex PM correction standard](CODEX_PM_CORRECTION_STANDARD.md).

---

# Reference-fidelity illustrated world — 11 November 2026 (Australia/Sydney)

https://product-dna-studio-preview.onrender.com

- Runtime commit `523b99f3dc3cfdc07c962051c52b4d07069335c9` is live on both services. API deploy: `dep-dbptll0ae00c73clk920`; static deploy: `dep-dbptma1srm7s738rkutg`. Served HTML matches the committed bundle exactly.
- Replaced the previous vector approximation with an actual local 3D illustration library: cheerful gender-neutral human chibi, sculpted rocky floating islands, glossy career symbols, clouds, greenery and flowers. Rebuilt the original two-band illustrated composition with glowing journey/bridge paths and dimensional capability cards. The original My Product DNA reference and full-result screenshots were reviewed side by side; desktop and phone screenshots are in ignored test artifacts.
- Each generation displays exactly one responsive map root, not desktop/mobile alternatives side by side. One Download button exports one 3200×2360 PNG. Actual illustration pixels survive PNG export. No square/portrait chooser, manual map editor, alternate second image or extra AI image call per visitor was introduced.
- Added the requested read-only View Full Journey, showing evidence and optional original context in browser memory. It causes no content persistence or API request and does not add another result.
- Strengthened job-family versus project-activity abstraction and transferable capability generation. Known activity headings and capabilities repeating journey headings receive bounded repair feedback. Evidence-grounded 1–4 independent counts and literal quote/source constraints remain.
- 43 automated tests passed across backend, parsing, voice fallback, regeneration, source safety, one-result rendering, read-only evidence, all 32 cardinality/layout combinations, counter behavior and PNG download. Production browser verification with real OpenAI calls passed generation, Chinese original-input regeneration, single PNG download, phone layout and evidence disclosure, with no browser errors.
- Final real synthetic-profile test returned Software Engineering, Platform Engineering and Data Analytics, with Systems & Platform Design, Reliability Analysis and Evaluation Judgement. These are interpretive categories derived from submitted test experience, not independently verified jobs or qualifications.
- Existing free compute, configured key, persistent aggregate counter, daily call limit and pilot date were retained. No infrastructure resources were created or changed. Total counts include verification generations; downloads do not increment them.

See [visual fidelity implementation](VISUAL_FIDELITY.md).

---

# Simplified illustrated-map update — 11 November 2026 (Australia/Sydney)

https://product-dna-studio-preview.onrender.com

- Frontend commit `2fa3400f1d9bd9e3c05a976203e4dedfee896f1a`, deploy `dep-dbpsr4bl550s738r44hg`: live. The served HTML matches the committed bundle byte for byte.
- API commit `6a8a3c4d910277dab89a927a235037b9154276a1`, deploy `dep-dbpsv01srm7s738pbbl0`: live.
- New supplied AI/helix logo design, empty story placeholder, shortened privacy copy, no format selector, no separate refinement section, no manual map editor. The result ends with one Download PNG button. Changes are requested through the original input and regenerated by AI.
- Controlled pastel SVG illustration: career islands, two-band composition, neutral toy explorer, selectable English text, stacked mobile layout, and fixed 3200×2008 PNG. Each list is independently 1–4 items based on evidence, not slot filling.
- 42 automated tests passed. All 32 desktop/mobile cardinality combinations passed along with CV parsing, voice fallback, clarification, regeneration, XML escaping, overflow handling, download and count tests. Legacy API safety tests remain covered, but there is no legacy editing UI.
- Real production browser checks passed: multilingual CV upload → grounded English map → PNG → Chinese requirements in original input → regeneration → stacked mobile preview. The final test produced 3 journey nodes and 3 strengths, with no browser errors. Download did not increment counts.
- A real mixed-source regeneration exposed an incorrectly paired citation. The final API constrains quote/source pairs to pre-extracted exact passages in its decoding schema; independent provenance/safety checks remain in place. Precise safe field feedback covers other bounded repairs. No input, output or quote logging was added.
- The existing free persistent counter was already active before this release. Its count survived deployments; total observed after verification was 5, including four successful synthetic test maps generated during this update. Counts include testing and do not represent unique visitors. Existing credentials, AI call limit and pilot schedule were preserved; no infrastructure resources were created or approved in this update.

See [design and implementation decisions](ILLUSTRATED_MAP.md) and [counter storage](ANONYMOUS_COUNTS.md).

---

# Published release — 11 November 2026 (Australia/Sydney)

Career DNA Studio is published on the existing URL:

https://product-dna-studio-preview.onrender.com

- Frontend deploy: `dep-dbppr12fngtc7383jdv0`, commit `1e9c7c0a80f742ea7aa4873acf6b65207552e453`.
- API deploy: `dep-dbpptg8ae00c73c9jja0`, commit `53e3b87ec449525ec616de35261a62ba64921004`.
- Both deployments reached `live`; the bundled frontend matches the release source. The API's additional change omits non-displayed empty date values from edited-export English review.
- PR #1 was merged. Existing free services and their server-side credentials were retained. No database, paid infrastructure, or public trial start date was added.

Production browser verification used synthetic professional text and real OpenAI calls. Sparse clarification, bounded generation, scoped conversational refinement, undo, direct editing, consented English/safety review, portrait PNG download, square layout and phone-width rendering all passed.

The first production check exposed empty date fields being treated as non-English during edited export review. The hotfix excludes those non-displayed values, adds a regression, and passed 29 backend tests. The full production browser flow then passed, including the previously blocked download. The earlier prepared release's 33-test and six-check reports remain in VERIFICATION.md as historical evidence.

This publication updates the app. The seven-day pilot clock still requires the owner's separate launch-date instruction.
