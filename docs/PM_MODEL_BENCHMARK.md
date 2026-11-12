# Career Studio V2: verified models and quality benchmark

Observed 12 November 2026, Australia/Sydney. This V2 record supersedes the earlier Sol-default recommendation below.

The existing live text default before V2 was `gpt-6.1-sol`, rather than an inferred GPT-5 default. V2 uses independently configured `gpt-6-astra` for fact extraction, capability summarisation and conversational refinement. All candidate access checks and real calls use the active Render API project; no OpenAI key is retrieved or shipped to the browser. No SDK is used: the adapter calls the structured Responses API directly.

| Profile | Model | Complete two-stage time (s) | Estimated USD | Truthful roles |
| --- | --- | ---: | ---: | --- |
| ai_ml_pm | gpt-6-astra | 39.27 | 0.184638 | AI PM |
| ai_ml_pm | gpt-6.1-sol | 37.87 | 0.036201 | AI PM |
| consulting_to_pm | gpt-6-astra | 50.66 | 0.211673 | Business Consultant, Commerce PM |
| consulting_to_pm | gpt-6.1-sol | 31.01 | 0.037109 | Business Consultant, Commerce PM |
| engineering_to_pm | gpt-6-astra | 41.51 | 0.205635 | Software Engineer, Technical PM |
| platform_pm | gpt-6-astra | 28.49 | 0.166552 | Platform PM |
| traditional_pm | gpt-6-astra | 40.90 | 0.175705 | Generalist PM |

Each generation actually called both `career` and `summary` stages; provider response metadata confirmed the requested model on both calls. No validation repair was required in these seven cases. Astra took28.49–50.66 seconds (median40.9) and approximately US$0.167–0.212 for the five synthetic profiles. Sol’s two paired cases took31.01–37.87 seconds and approximately US$0.036–0.037. All seven together were approximately US$1.017513. These are two-stage costs and should not be compared as if they were the former single-call pipeline.

The paired outputs were both grounded and professionally specific. Astra exposed model limits/failure modes and commercial assumption review clearly; Sol retained comparable evidence and methods. This small sample does not establish universal Astra superiority. The release follows the user’s explicit quality-first Astra preference; it does not silently optimise back to Sol.

AI example from Astra: **AI Product Judgement** → “Judge real-world model fit against capability limits and failure modes.” → Golden-set evaluation / Failure analysis / Use-case comparison. Platform example: “Balance interface stability, reliability and extensibility across shared capabilities.” Actual engineering and consulting roles remained Software Engineer and Business Consultant before their PM transitions. No invented quantified outcome was observed.

Both candidates passed schema, literal evidence, English-display and all desktop/mobile render checks. Citations verify provenance, not exhaustive semantic accuracy or certification. Synthetic test markers excluded all seven initial creations from the public counter: it remained1; historical23 remained unverified and unchanged.

Current standard rates verified against official pricing: Astra US$10 input / US$50 output / US$1 cached read per million tokens; Sol US$2 / US$10 / US$0.10. Observed cache writes are included at1.25× ordinary input for30-minute retention and2.5× for12-hour retention. Estimates include output reasoning tokens but exclude taxes and hosting. Provider load, CV length, cache state and repairs change costs and latency.

Speech uses verified `gpt-transcribe` at the documented US$0.0045/minute. Synthetic Mandarin, English and code-switched Mandarin/English recordings all returned editable original-language transcripts. The mixed transcript preserved both languages even though provider language metadata reported only `zh`; the application does not discard English or rely on that metadata to translate.

Official references retrieved and read on12 November: [pricing](https://developers.openai.com/api/docs/pricing), [Astra](https://developers.openai.com/api/docs/models/gpt-6-astra), [transcription](https://developers.openai.com/api/docs/models/gpt-transcribe). Raw synthetic metrics: `work/v2-verification/benchmark/` (ignored from Git).

---

## Historical V1 benchmark — retained for comparison
# Model access and PM interpretation benchmark

Observed against the active Render API project on 11 November 2026 (Australia/Sydney). Synthetic professional inputs only; every request carried the authenticated internal-test marker and left the public creation count unchanged.

Before this update, the actual selected model was `gpt-5` via `OPENAI_MODEL`. The active key lists `gpt-6.1-sol`, `gpt-6-astra` and `gpt-image-2.6-sunburst`; both text candidates were also validated by actual structured Responses calls. Runtime visual generation remains SVG/local assets, so the image-model ID is `null` and there is no image API charge per map.

| Profile | Model | Wall time (s) | Estimated USD | Observed roles |
| --- | --- | ---: | ---: | --- |
| traditional_pm | gpt-6.1-sol | 22.59 | 0.023401 | Generalist PM |
| engineering_to_pm | gpt-6.1-sol | 27.91 | 0.027658 | Software Engineer, Technical PM |
| ai_ml_pm | gpt-6.1-sol | 20.85 | 0.025284 | AI PM |
| platform_pm | gpt-6.1-sol | 18.37 | 0.023164 | Platform PM |
| consulting_to_pm | gpt-6.1-sol | 27.54 | 0.029038 | Business Consultant, Commerce PM |
| ai_ml_pm | gpt-6-astra | 36.89 | 0.14273 | AI PM |
| consulting_to_pm | gpt-6-astra | 30.01 | 0.154705 | Business Consultant, Commerce PM |

## Decision

Use `OPENAI_CAREER_MODEL=gpt-6.1-sol` as the dedicated career interpretation/refinement default, retaining the original `OPENAI_MODEL=gpt-5` fallback rather than overwriting it. Two paired examples (AI PM and consulting-to-PM) showed similar supported categories and concrete methods with no material factual/category improvement from Astra in this small sample. Astra was slower and about five to six times as expensive. This is a limited benchmark, not proof that Astra never improves harder CVs. No automatic expensive-model fallback is enabled.

Sol handled all five backgrounds with one or two relevant capabilities rather than filling four slots. Engineering retained `Software Engineer` before `Technical PM`; consulting retained `Business Consultant` before `Commerce PM`. Both candidates retained the consulting role in the paired case. No fabricated quantitative outcomes were observed. Original citations, role/method references and English display checks passed independently.

The AI case produced `AI Product Judgement` plus a distinct risk/release lens. Its concrete methods included Golden-set evaluation, Failure analysis and Use-case comparison. The consulting case distinguished conversion/checkout prioritisation from commercial assumptions and unit economics. Editorial review found the paired models largely equivalent for these examples; outputs are interpretive and not independent proof of a person’s competence.

## Pricing and measurement

Estimates include ordinary input, cached reads, observed cache writes and all output tokens (including reasoning), using standard current rates: Sol US$2 input / US$10 output / US$0.10 cached input per million tokens; Astra US$10 / US$50 / US$1. Default30-minute cache writes cost1.25× input, and12-hour writes2.5×. These are token-based estimates, not invoices; they exclude hosting, taxes and unrelated service charges. Seven benchmark generations together were approximately US$0.42598.

Sol’s five cases took18–28 seconds (median about23 seconds) and cost approximately US$0.023–0.029 each in this run. Complex CVs, provider load, cache state and bounded repairs change latency/cost. No universal timing promise or fake progress percentage is shown.

Official references retrieved and read: [Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol), [Astra](https://developers.openai.com/api/docs/models/gpt-6-astra), [pricing](https://developers.openai.com/api/docs/pricing), [cache pricing](https://developers.openai.com/api/docs/guides/prompt-caching), [provider retention](https://developers.openai.com/api/docs/guides/your-data).

Local raw synthetic responses/token metrics: `/workspace/work/pm-model-benchmark/`. The single long mobile role-highlight phrase found in Astra output is covered by an adaptive two-line layout regression. All seven outputs passed live desktop/mobile renderer checks; the completed browser flow and final Spanish-only CV/retry verification are recorded in DEPLOYED.md.
