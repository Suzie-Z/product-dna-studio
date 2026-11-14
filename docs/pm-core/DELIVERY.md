# Original PM Career Studio — focused core iteration

14 November 2026 (Australia/Sydney).

V2 is discontinued as the product baseline. This implementation starts from original commit `c065bdfccc5d37cf336b9e40acc62c8adfeab142` on the dedicated `pm-core-experience` branch. The V2 branch remains recoverable as history. Existing production branches and Render services have not been updated.

## Delivered

- Restored the original homepage, rounded typography, palette library, map composition, islands, paths, character/icon artwork and single PNG export. `preview/poster.js`, `preview/pm-fonts.js`, `preview/pm-library.js`, `preview/visual-manifest.json` and the original asset files have no changes from the original baseline.
- Kept the product PM-specific. The initial flow is PDF/DOCX upload → readiness feedback → generation. No initial chatbot, questionnaire or manual career-history requirement. The original browser parsers, 5 MB / 15-page checks and replace/error behavior remain; TXT is no longer an offered upload format.
- Strengthened CV understanding to preserve actions, demonstrated judgement, ownership boundaries, constraints, trade-offs and recurring strengths. The existing structured fact ledger is Layer A; PM capability synthesis and reflections are Layer B; the original renderer is Layer C.
- Enforced the existing maximum of four distinct core PM capabilities, with no filling of unsupported slots. Prior non-PM roles can remain truthful context in a PM's CV; the application is not expanded to target those professions.
- Added separate evidence-linked **Recognition** and **Possibilities to Explore** text alongside the original map. They have stable section paths and reference supported map item IDs, which already carry literal CV evidence. New generation requires both sections. Aspiration rejects prescribed/guaranteed-role language and the prompt calls for conditional, grounded alternatives rather than seniority inflation or job matching.
- Added **Refine My DNA** as an on-demand dialog. It opens only after the user selects it, supports natural-language feedback and the retained voice controls, and offers an optional exact-sentence suggestion. It uses the selected latest accepted map, CV context and recent edit history; accepted versions and Undo remain available.
- Removed visual patch paths from ordinary refinement. Both explicit icon edits and icon changes smuggled through whole-item patches are rejected. Existing block ordering and unrelated text remain protected. The client also ignores presentation patches during content edits, preserving the selected palette, avatar, path, platform configuration and original template.
- Added a separate explicit **Generate a New Map** action. This reruns full analysis and can choose a fresh presentation from the existing original library. It is not an ordinary text refinement. A replacement CV is also explained as full analysis; the resulting request contains only that new CV and does not mix in the previous CV or chat sources. Closing an unaccepted replacement restores the current accepted CV.
- Preserved cancellation, retry idempotency, one selected map, one PNG download, PM scope checks, provider configuration, safety checks, anonymous counters and session-only content handling.

## Changed files

| Files | Purpose |
|---|---|
| `career_pipeline.py` | Stronger PM understanding and integrated grounded reflection output |
| `career_reflection.py` | New separate section schema, evidence links and bounded Aspiration validation |
| `career_ai.py`, `semantic_refinement.py` | Content-only scope, safe targeted section updates, icon/order guards |
| `preview/studio.template.html`, `studio.js`, `studio.css`, `copy.json` | CV-first entry, on-demand refinement, new-CV/full-generation boundaries, warm copy and supporting reflection reading |
| `preview/index.html`, `build_preview.py` | Rebuilt bundle; build mechanism is retained |
| `skills/pm-dna-editorial/SKILL.md` | Align editorial guidance with grounded aspiration and content-only edits |
| `Dockerfile`, `.dockerignore` | Include the new reflection module in the existing runtime package |
| `tests/*`, `test_ai.py` | Replace superseded multi-input/visual-edit acceptance cases and add focused core-flow regressions |
| `docs/pm-core/*`, `README.md` | Request record, verification and local instructions |

## Verification

**110 tests passed in 81.976 seconds** on the final runtime changes.

```sh
python build_preview.py
python -m unittest test_ai test_server tests.test_counts tests.test_session_architecture tests.test_v2 tests.test_fact_validation tests.test_handoff tests.test_e2e tests.test_handoff_browser tests.test_core_experience -q
```

The browser tests exercise the actual HTTP server, actual PDF/DOCX readers, original rendering/fonts and PNG download. Only provider transport is mocked. New checks cover initial chatbot absence, upload enabling generation, two consecutive edits against the accepted version, Undo, visual preservation, a replacement-CV full-generation request without old sources, visual-request clarification without a map update, retry with the exact same request, cancellation without a late version, mobile dialog overflow, voice unavailability fallback, reflection grounding and model attempts to change an icon through an array patch.

Retained original regression checks cover evidence validation/repair, protected credentials, bounded categories, parser typography, counter deduplication/test exclusion, selected-version semantics, original platform/path variants, responsive layout, clipping/collisions, outlined fonts and 3200×1800 single-image export. Old tests asserting initial manual history or ordinary visual editing were replaced because those behaviors are explicitly removed by the new request; original renderer checks remain.

Python compilation, JavaScript syntax and Git whitespace checks passed. The downloadable standalone example preview was also exercised through generation and on-demand text editing, confirming an unchanged visual configuration and no browser script errors.

## Privacy and scope

CVs are read in the browser; extracted text is sent to the API and OpenAI. The application does not write CVs/maps to the database. Short-lived server replay memory and browser session history remain; external model/browser-speech providers have their own policies. No unsupported zero-retention promise was added. Original documents are not uploaded to a document archive or retained as server temporary files in this flow.

Existing model variables, daily limits, production counter tables and deployment configuration are unchanged. Synthetic tests were authenticated as internal tests and do not increment production counts. No real provider credential is configured locally, and no production credential was retrieved.

## Limits and release status

- **Not deployed.** The current production site is unchanged. The dedicated branch is ready for review rather than a published replacement.
- **Real-model content quality is not yet verified.** The new prompts and structured contracts are implemented, but these tests do not establish actual model insight quality, latency, cost, semantic entailment or English fluency. Source links are provenance, not independent verification of a career. Live synthetic PM/CV evaluation is still required before release acceptance.
- Recognition and Aspiration are supporting on-page sections. The PNG intentionally retains the original map composition; these longer paragraphs are not inserted into the artwork or exported image.
- Adding/removing a capability reflows cards within the original template. It does not create new artwork or change the design system. Ordinary wording edits retain the existing visual state; the SVG is rerendered to show new text using the same assets.
- Scanned PDFs require OCR, legacy DOC requires conversion, and browser readers depend on the existing pinned CDN packages. Microphone capture is device/browser/permission dependent; physical-device audio recording was not verified here. The retained service/audio contracts and unavailable-voice fallback are tested.
- Cancel prevents late UI replacement but cannot guarantee cancellation/billing avoidance of an already-running provider request. Historical accepted versions, including prior CV context, remain in browser memory until leaving/refreshing; only the selected new-CV version uses the new source for subsequent edits.
- The standalone preview uses a synthetic PM CV and programmed example edits, with no real AI or document upload. It is an interaction/design review, not an analysis-quality benchmark.

## Local use

```sh
pip install -r requirements.txt -r requirements-dev.txt
python build_preview.py
python ai_server.py
```

Open `http://127.0.0.1:10000` on the machine running the server. Configure `OPENAI_API_KEY` securely in the server environment for real generation; do not put a key in chat, browser code or Git. Keep production counting disabled for local tests. Existing model variables select extraction, synthesis and refinement; none were changed by this iteration.

For a no-key design review, download `PM_Career_Studio_Original_Refined_Preview.html`, open it in a browser, select Explore → Load Example CV → Discover My DNA, then choose Refine My DNA. The example recognizes a label change such as “Rename the first capability to Product Judgement.” The actual application uses semantic model patches rather than this preview's fixed demonstration handler.
