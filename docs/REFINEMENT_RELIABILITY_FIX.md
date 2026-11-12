# Refinement reliability and automatic wording fit

Published12 November2026 (Australia/Sydney). Runtime `0f5d51a72d30da9df0b05161abb175fb4513e8a4` is live: API `dep-dbqo26jtqb8s739u3n60`, frontend `dep-dbqo28bbc2fs73dv56p0`. Public HTML matched the tested bundle; the API remains on Astra. No model, quota, database or hosting-plan change was made.

The composer now gives this English instruction after generation: `Example: Change “AI Product Judgement” to “Model Fit & Evaluation”. Copy the exact text, then say what you want instead. Long wording will be shortened to fit.` Users can keep refining in the original composer.

A unique copied phrase scopes the response schema to its matching field. The model receives that item and associated evidence instead of the full CV/map, and a compact edit prompt instead of the full generation/editorial prompt. Existing other fields are copied unchanged. Ambiguous or broad requests still use semantic patch interpretation; this is not a guarantee that arbitrary instructions always resolve correctly.

Two independently reproducible validation hazards were repaired. Old valid literal citations no longer have to appear in freshly sampled quote enums: source IDs are bounded and every returned quote is independently checked against the actual original text. Repeated edits also retain required detail citations and an original parent anchor within the six-quote bound, rather than failing merely because historical supporting quotes accumulated. The specific historical visitor request was not logged, so we do not claim to have recovered its exact rejected patch.

The frontend measures candidate maps on desktop and mobile before committing a version. Overflow triggers a bounded field-only wording-shortening request, preserving existing factual citations. It does not regenerate the career analysis or rewrite the entire map. Up to two fitting attempts are allowed; if they fail, the previous map and input remain available. Capability titles can use three reserved lines without colliding with icons/descriptions. The in-image `Regenerate for shorter wording` placeholder has been removed.

The complete89-test regression suite passed; a further repeated-proof-bound regression also passed, bringing coverage to90 tests. New checks cover copied-phrase scope, compact context, literal citations outside old excerpt enums, repeated edits and automatic shortening before display without another generation request. Existing full input/refinement/version/download, safety, count and layout tests passed.

Real authenticated production checks confirmed:

| Case | Provider input/output tokens | Wall time | Estimated USD | Result |
| --- | ---: | ---: | ---: | --- |
| Copied-title replacement |1274 /65 |6.78s |0.019168 | Only `/strengths/k1/label` changed to `Model Fit & Evaluation` |
| Automatic field shortening |1331 /107 |7.93s |0.021980 | Only the overlong title changed to `Model Fit Assessment` |

Both used actual `gpt-6-astra` responses; all other fields were exactly preserved. The controlled calls left the public creation count unchanged at2. These examples are not universal latency/cost promises. Refinement still uses tokens, while avoiding the two-stage full-generation pipeline. Optional fitting and bounded repair can add a small call; the existing daily attempt guard still applies.

A separate real public-site browser test loaded a recorded synthetic Version1, clicked Refine, submitted the copied-title replacement through the actual UI/API and displayed Version2. It preserved unrelated fields and the visual variant, showed one SVG with no overflow/error placeholder, downloaded one decodable PNG and passed desktop/mobile layout checks without browser errors. No visitor CV was used. Synthetic verification and screenshots are in ignored `work/refine-reliability/` and copied to `/workspace/deliverables/refine-reliability/`.
