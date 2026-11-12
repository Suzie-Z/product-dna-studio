# Internal career-fact validation fix — 12 November 2026

The error `invalid_career_facts` means both bounded attempts to produce a valid internal fact ledger failed. It is not a judgement about a visitor's real career. The screenshot alone cannot identify the exact failed rule: visitor CVs/drafts are not retained or logged, and the older error did not expose the safe validation-field diagnostic.

Reproducible issues repaired:

- Internal facts reused poster-text rating rules, rejecting an evidenced evaluation ratio such as20/100. Expanding `%` into ` percent` before a240-character bounds check could also reject an originally valid-length claim. Internal numeric facts are now distinct from display-rating rules. Final poster safety/length checks remain unchanged.
- Citations were constrained to a freshly sampled sentence/fragment enum. Fact citations now accept bounded original-text passages associated with valid source IDs and independently verify their literal presence. Invented, empty and too-short quotes are still rejected.
- Ready responses with an empty optional question are normalised to null. Internal fact IDs are canonicalised; these IDs are not externally referenced map IDs, so incidental duplicate model keys no longer block generation.
- The bounded repair call now receives the rejected draft plus the precise safe field/rule feedback. Previously it received only feedback and could repeat the same invalid output. After a failed bounded repair, the API now retains a non-sensitive `validation_issue` for diagnosis and uses a clearer temporary-reading-error message.

The complete96-test regression suite passed before deployment. Six new cases cover original-text partial citations, quantitative facts, unchanged poster-rating protection, internal normalisation, rejection of fabricated/empty citations and non-English claims, and targeted repair with the rejected draft.

The specific historic visitor failure cannot be attributed to one of these issues without its original response diagnostic. No visitor CV was retrieved, no model or quota was changed, and no automatic model downgrade or ungrounded fallback was introduced.

Deployment and real-provider verification: backend runtime `db6dcf78f0aa7a6b557b0f68b2d06c6d9e9918b3`, Render deploy `dep-dbqop6psrm7s73di00cg`, reached `live`; health passed. The frontend was unchanged. Two actual Astra career→summary generations succeeded: English quantitative experience (40.48s) retained a20/100 evaluation ratio and60%→80% study results without inventing causality; mixed Mandarin/English platform-PM experience (44.73s) retained ownership boundaries and produced an English map. Both passed independent schema/evidence validation, required no fact repair, and carried internal-test markers. The public creation count did not change during these tests. Synthetic reports are under ignored `work/fact-validation-fix/` and `/workspace/deliverables/fact-validation-fix/`.
