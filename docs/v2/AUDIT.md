# V2 architecture audit — 13 November 2026 (Australia/Sydney)

Branch: career-dna-v2-rebuild. Production stays on its existing branches and deployment. No production deployment is authorized for V2.

The previous active application couples PM-only validation, multi-source input, browser/CDN parsing, voice capture, versioned refinement and poster fitting. Its PM gate and career-role taxonomy prevent cross-profession use. The historical standalone SQLite/admin server persists submissions, contradicting the current product's data-handling model. Keeping these as competing entry points would be misleading.

Replace the active server/UI/analysis workflow. Retain model selection conventions, provider transport protections, anonymous count tables, expiring idempotent request memory, bundled rounded fonts, source-controlled brand assets and useful historical design references. Remove obsolete voice/refinement/manual onboarding from the active runtime, not merely from view. V1 remains available through Git history and unchanged production branches.

New boundaries: bounded PDF/DOCX parser → expiring extraction session → validated factual stages → reviewed company/role/period/order → structured capability/pattern/reflection analysis → semantic visual plan → independent journey and DNA renderers. No model output is HTML. No future-potential claims, demographic inference or career-ranking scores.

Document limits: 5 MB, 15 PDF pages, 32,000 extracted characters, bounded DOCX ZIP expansion, isolated parser CPU/memory/wall limits. Unsupported scans receive OCR guidance, not fabricated content. Source and analysis data remain in browser/process memory for at most ten minutes; provider processing is separately disclosed. Existing counters store no document content. Preview does not count production creations.

QA will use several synthetic professions and real document bytes, with mocked provider transport explicitly distinguished from a live model evaluation. No credential is configured in this cloud environment. No production key will be retrieved for an unapproved preview.
