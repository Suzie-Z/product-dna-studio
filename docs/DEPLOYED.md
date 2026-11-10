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
