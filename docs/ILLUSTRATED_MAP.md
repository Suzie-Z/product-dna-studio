# Simplified illustrated-map update

The user's latest instructions take priority over the attached design brief where they differ. The published flow is input → AI generation → download. There is no manual map editor, separate refinement/Make It Yours section, share-caption action, or format selection. Users change requirements in the original input and generate a new AI result. The story placeholder is empty; the visible label remains Write your story.

The attached brief supplies the illustration direction: a consistent soft lilac/teal two-band scene, floating shaded career islands, a purple bridge label, neutral toy-like career explorer with a symbolic work prop, and capability cards. The model selects profession-appropriate broad categories and higher-order strengths, not employers/project names. Both lists are now independently bounded at 1–4; sparse evidence is never padded to two or four.

The same escaped structured content renders as real selectable SVG text on the page and a fixed 3200×2008 PNG download. Phones use vertically stacked journey stages and full-width strength cards. Layout, palette and illustration grammar are controlled by code. Icons/accessories are symbolic and do not infer identity, gender or appearance. Arrows are drawn only when the source supports chronology. Brief English evidence notes are native SVG tooltips; raw resume quotes are never embedded in SVG or PNG.

The HTML logo attachment was a saved ChatGPT page without a usable embedded logo asset. The supplied inline AI/helix reference was prepared as a transparent logo asset and bundled in the self-contained frontend. The original saved HTML, including unrelated account/page metadata, is not published or committed.

Privacy copy is scoped to Career DNA Studio, with an AI processing policy link and the existing disclosure before Generate. Only the total completed-generation count is displayed; the app continues to expose no content storage or visitor tracking. The live counter already reports persistent storage; this release preserves the existing database connection and does not provision resources or change call limits.

Validation: 42 automated tests, including all 32 independent desktop/mobile 1–4 cardinality combinations, PDF/DOCX/TXT parsing, voice and fallback, clarification, original-input regeneration, XML escaping, overflow handling, counter behavior, and PNG download. Legacy backend refinement/review safety tests remain; those APIs are no longer exposed by the UI.

Repair feedback now names the exact English-copy field when validation fails, rather than a generic language error. If both bounded attempts fail, the API supplies only a safe rule/field diagnostic, never submitted text or model copy. The page preserves the input and shows the existing short retry message. No content logging was introduced.

Generation now uses a per-request citation schema whose allowed alternatives pair each exact source excerpt with its real source ID. Bounded excerpts are distributed across the source, then selected by the model; citations cannot be freely rewritten or attached to another source under constrained decoding. The existing independent literal-quote, reference and safety checks still run afterward.

A real mixed-source regeneration exposed a quote assigned to the wrong source. The citation-schema change addresses that decoding failure directly; it does not relax literal-evidence validation, fabricate a substitute quote, or silently fill slots. Browser verification is rerun against the deployed API after the repair.
