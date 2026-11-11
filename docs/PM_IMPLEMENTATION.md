# PM Career DNA — integrated release

This implements the user's accumulated PM-only requirements in the actual application. It is no longer only a design handoff.

- Visible app, metadata, generated-map headings, logo, footer, action labels and download name use PM Career DNA. Original CV text and internal API/file names are preserved.
- Ready maps contain 1–4 supported PM role types and independently 1–4 transferable capabilities. Journey labels use a closed PM-role enum, with Generalist PM for evidenced general product ownership and Growth Hacker only for supported adjacent experience. A source guard asks non-PM-only/aspirational users for actual PM experience without a provider call or generation count. Role classification remains interpretive; citations prove source provenance rather than independently certifying job history.
- Uniform warm-apricot, neutral fictional avatars are selected from the 24-character library, never inferred from names or demographics. Background removal was redone to eliminate the source atlas's visible grey tile haze.
- All 24 PM-scene icon sprites are integrated. Role icons use the approved role catalog; capability icons use validated allowlisted IDs. The reusable illustrated islands/clouds/foliage preserve the reference world.
- A shuffled six-theme bag ensures all approved themes are used once per six new results; a 24-avatar bag avoids repeating an avatar until the pool cycles. Selection is page-memory only. Each result has one stable variant reused for resize and export. There is no separate image-model call per visitor.
- One SVG map root is replaced on generation and responsive changes. The PNG canvas remains detached from the DOM. One download exports one `my-pm-career-dna.png` at 3200×2160.
- Foreground icons, role titles/descriptions/dates, islands, avatar, capability labels and descriptions have independent reserved bounds. Pairwise collision checks run in both layouts and block export on overlap. Text fitting has a readability floor; model copy bounds were tightened to match the slots. Decorative gardens are constrained to corner margins, with no extra icon stickers over the avatar.
- White webpage background and blue/teal brand actions; varied softly colored map backgrounds. No manual editing form, format chooser, duplicated preview or extra generation step was added.
- Sources/maps remain browser/request-memory data. Persistent storage still contains only aggregate date/count rows; credentials, daily provider-attempt quota and trial schedule are unchanged.

Validation: 56 automated test methods pass, including PM-vs-non-PM scope, aspirations/denials, provenance, all 64 dated/undated role/card/layout cardinalities with zero foreground collisions, actual clipped foreground bounds in the browser, all 24 avatar variants, six-theme rotation, stable export/resize variants, parsing, voice fallback, regeneration and one PNG. Both services are live. The complete production flow passed with real-provider generation, Chinese-input regeneration, phone rendering, one PNG download and persistent-count checks; see DEPLOYED.md.

Tradeoff: the static host's existing index-copy build is retained, so the self-contained HTML includes all local PNG illustration assets (approximately 11 MB). This avoids a new external image dependency and new hosting configuration; first load is larger. Atlas cells remain 256px native with soft illustration detail; output text is rendered crisply by the app, not baked into the raster assets.

Live verification found a mobile date row whose reserved height was shorter than its line height. The final layout reserves a readable date row, larger mobile body-copy areas, and adds all dated cardinalities as regressions. Rendering keeps the Generate action busy through raster preparation so rapid clicks cannot race an unfinished export surface. Functional PM-ownership guards also distinguish actual ownership from denied or aspirational ownership.

A real-provider draft also exposed an optional date caption rejected by general contact/rating heuristics. Dates now use a dedicated whitelist grammar and exact source-year/interval checks; unconfirmed optional captions are omitted instead of blocking an otherwise valid evidence-grounded map. Unsupported role/capability claims and citation mismatches still fail normally.


## Compact editorial release

`skills/pm-dna-editorial/SKILL.md` is loaded into the runtime generation prompt. It ranks demonstrated decisions, trade-offs and specific methods above generic responsibilities. Strength cards now pair a concise decision-value sentence with zero to three concrete method labels, each carrying an associated literal source quote. Named techniques such as Golden Sets, RCA and RAG require an explicit name or supported multilingual equivalent in that method's own quoted passage; the main provenance/safety checks remain in force. Citations establish provenance, not a complete proof of semantic entailment. There is no second model/image call for the editorial layer.

The desktop canvas is 1600×1080 (previously 1600×1290); the PNG is 3200×2160. This removes about 16% of the height while keeping readable type and reserved date slots. Capability cards use an inset methods area. No methods are fabricated to fill the area. Older maps without the additive methods field still render/validate, supporting independent frontend/API rollout. The mobile role rows are tighter and method text has its own readable bounds.

56 automated methods pass, including new method provenance, specialist-name grounding, English-only labels with Chinese evidence, legacy-map compatibility and all 128 dated zero-to-three-method/card/layout combinations. Existing dated/undated layouts, browser-painted bounds, generation, parsing, voice fallback, variants, single PNG and counts remain covered. Both services are live and the full real-provider browser flow passed; see DEPLOYED.md.
