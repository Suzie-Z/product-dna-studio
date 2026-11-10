# Career DNA release verification

Executed against the existing project's `career-dna-release` implementation. This is a prepared release, not a claim that the production URL has been updated.

## Automated checks

- 28 backend/HTTP contract tests: independent 1–5 cardinalities, single-strength acceptance, unknown/duplicate IDs, literal quote provenance, multilingual evidence, English/script/length bounds, contact redaction, neutral output rules, chronology fallback, controlled icons, clarification, consent, scoped patch merging, stable item order, unsupported credentials, edited-copy English review, safety rejection, bounded repair, provider errors/quotas, input bounds, and CORS.
- Four browser tests run against the real Python HTTP boundary. Only OpenAI transport is mocked: full clarification → generation → evidence review → consent → refinement → undo → direct edit → reviewed PNG workflow; actual PDF/DOCX parsing and mixed sources; upload failure/removal; microphone fallback and simulated Mandarin transcript; and mobile layout.
- Renderer checks exercise all **50** combinations: 1–5 journey nodes × 1–5 strengths × portrait/square. All natural-copy fixtures fit their allocated text boxes. A deliberately excessive string produces the explicit overflow fallback instead of clipping and blocks download.
- Actual PNG files are decoded to verify 2400×3000 portrait output; square preview is 2800×2800. Secret/source quotes are absent from the exported field set. Drafts and histories do not use localStorage.
- One legacy research-dashboard integration test remains passing; that service is not deployed by the current manifests.
- Node syntax checks, Python compilation, Render public JSON-schema validation for all three manifests, generated-bundle rebrand checks, patch whitespace checks, and a secret-pattern scan of tracked sources passed.

Runtime test dependencies and command lines are in the README. Tests do not require an OpenAI key unless the opt-in real-provider suite is selected.

## Real-model checks

The corrected live smoke run used the real configured OpenAI model (`gpt-5-mini`) with synthetic professional accounts, through the new local application code. No production service was reconfigured or redeployed.

| Check | Result |
| --- | --- |
| Chef input produces hospitality-specific, grounded content | Passed |
| Mandarin engineer input produces an English-only map in a real browser | Passed |
| Chinese refinement changes the requested title and preserves unrelated strengths/superpower | Passed |
| Real generated result downloads as a readable high-resolution PNG | Passed |
| Unsupported surgical credential prompts for evidence rather than being asserted | Passed (independent server gate) |
| Embedded source instructions cannot override the map task or expose the key | Passed |

The final run made five model response calls, including one bounded repair, with 7,917 input and 7,621 output tokens total. Generation/refinement cases took about 14–32 seconds in this run; these are observations, not promised response times. The newly added per-field language check on locally edited exports is covered by mocked contract/browser tests; it was not included in that real-provider run.

A preceding live run failed the required clarification behavior for an unsupported credential. This led to an independent server credential gate and regression tests, rather than relying only on prompt compliance. Subsequent corrected checks passed. Initial five-card visual review also found connector lines crossing upper cards; connector painting now occurs behind all cards and the corrected layouts were reviewed.

## Remaining manual/platform checks

- Real microphone hardware, microphone permission UX on individual devices, speech-service language accuracy, iOS/Safari and other browsers are not certified by a Chromium simulation.
- Profession specificity beyond the chef/engineer real examples is guided by the career-agnostic prompt and needs pilot review. Graduate, marketing, operations, very long histories, and source conflicts have contract/clarification safeguards, but were not all separately evaluated with the paid model.
- Render CLI/platform Blueprint planning is not run here (CLI is absent); manifests passed the current public JSON Schema. A matching Render plan and production smoke test remain deployment steps.
- Evidence checks do not independently establish employment, credentials, or the truth of user statements. See LIMITATIONS.md for quota persistence, provider retention, and semantic-review boundaries.
