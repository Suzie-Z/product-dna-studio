# Career Studio V2 — Complete Product & Technical Implementation Specification

**Project:** Career Studio – PM Career DNA  
**Scope:** Full V2 enhancement of the existing application  
**Priority:** Career Intelligence, AI Model Upgrade, Conversational Refinement, Dynamic Visual Design and UX Reliability

## Overall Objective

Upgrade the existing Career Studio into a high-quality AI-powered experience that helps Product Managers discover, visualise, refine and share their professional Career DNA.

The product must not simply convert CV content into a decorative infographic. It should intelligently identify a user's underlying professional strengths, summarise them at the appropriate level, and produce a distinctive visual representation that users can continuously improve through natural-language conversation.

**This is an enhancement of the existing application, not a rebuild.**

Please inspect the codebase, current model configuration, rendering architecture and existing functionality before implementing changes.

Preserve the established brand identity and landing-page experience.

---

# 1. Product Positioning & Naming

## 1.1 Product Scope: Product Managers First

Career Studio V2 should focus specifically on Product Managers.

This is an intentional product-quality decision. We want to produce reliable, insightful PM career interpretations before expanding to other professions.

Support different PM backgrounds, including:

- Consumer Product Management
- AI / ML Product Management
- Platform and Infrastructure Product Management
- Trust & Safety Product Management
- Growth Product Management
- Enterprise / B2B Product Management
- Technical Product Management
- Product professionals with earlier experience in engineering, consulting, business, operations or other disciplines

Recognise relevant transferable skills without incorrectly labelling every previous role as a PM position.

Do not expand the product to all career types during this release.

## 1.2 Naming Standards

Use the following user-facing terminology consistently.

| Location | Text |
|---|---|
| Brand | Career Studio |
| Landing page headline | Discover Your PM Career DNA |
| Landing page CTA | Explore My Career DNA |
| Input section heading | Explore My PM Career |
| CV upload action | Upload CV |
| Input placeholder | Tell me about your career journey... |
| Initial primary action | Generate |
| Initial loading state | Analysing... |
| Result heading | My PM Career DNA |
| Refinement action | Refine My DNA |
| Refinement loading state | Updating... |
| Export action | Download DNA Map |
| Public counter | XX PM Career DNA Maps Created |

Naming principles:

- **PM Career DNA** is the core product concept.
- **DNA Map** describes the visual output.
- Do not overuse "Map" in major headings.
- Do not call the generated output "Recall".
- Keep the naming short, natural and consistent.

Preserve internal identifiers where possible. Do not introduce unnecessary breaking changes solely for naming.

---

# 2. Preserve the Existing Landing Page

**Critical requirement: Do not redesign or remove the current landing-page experience.**

The landing page is an important trust-building and discovery experience.

Preserve its:

- Existing layout
- Logo
- Visual branding
- Animations
- Overall composition
- Exploration-first interaction

The first screen should introduce the experience, not immediately request personal career information.

### Expected User Journey

1. User opens Career Studio.
2. User sees the existing branded landing page.
3. User clicks **Explore My Career DNA**.
4. The page smoothly scrolls or navigates to the career input section.
5. User uploads a CV and/or describes their experience.
6. User clicks Generate.
7. The system analyses their background.
8. A personalised PM Career DNA visualisation is produced.
9. User can refine, restore, compare versions and download the result.

**Do not place the CV upload as the primary first-screen experience.**

---

# 3. Career Input Experience

## 3.1 Layout

After clicking the landing-page CTA, show a simple, centred input experience.

Structure:

**Explore My PM Career**

Upload CV

Small privacy reassurance

Upload confirmation, if applicable

OR / AND

Unified career journey input composer

Generate

Avoid excessive instructions, explanatory paragraphs and unnecessary labels.

## 3.2 CV Upload

Provide a prominent **Upload CV** action.

Support common document formats such as PDF, DOC and DOCX, subject to reliable parser support.

After successful upload:

- Display a green checkmark.
- Display the filename, such as ✓ Resume.pdf.
- Allow users to remove or replace the uploaded file.
- Do not display a CV preview.
- Do not reproduce CV contents anywhere in the visible interface.
- Preserve the information needed for generation and refinement during the active session.

### Privacy Message

Use concise wording such as:

"Your CV is only used to create your PM Career DNA."

Only use an absolute statement such as "Your CV won't be saved" after verifying that no persistent storage occurs across the application and external processing services.

Do not make privacy promises that the implementation cannot support.

## 3.3 Unified Text and Voice Input

Use a single ChatGPT-style composer.

Placeholder:

**Tell me about your career journey...**

Users should be able to:

- Type their career experiences.
- Use the microphone inside the same composer.
- Stop or interrupt voice recording.
- Start subsequent recordings.
- Edit the transcribed text.
- Combine typed content and voice transcription.
- Add additional context to an uploaded CV.

Do not create separate text and voice boxes.

The CV and composer should work independently or together.

A CV alone must be sufficient to trigger generation.

A meaningful text or voice description alone must also be sufficient.

## 3.4 Multilingual Input

Accept user input in languages supported by the configured models.

At minimum, test:

- English
- Mandarin Chinese
- Mixed English and Mandarin
- Common PM and technical vocabulary

Do not force English as the speech-recognition language.

Users should be able to give generation or refinement instructions in Chinese, English or a mixture of both.

Preserve the intended meaning of the original input.

**All final Career DNA content must be in English.**

This includes:

- Headings
- Capability names
- Career categories
- Descriptions
- Supporting explanations
- Visual labels

Do not add language selectors or instructional text telling users what language to use.

### Voice Interface Priority

Keep the existing voice recording interface for now.

Do not prioritise redesigning its responsiveness or animation in this release.

Focus first on multilingual transcription quality and correct integration with the career analysis pipeline.

Use a compatible multilingual transcription model where appropriate.

---

# 4. Mandatory AI Model Upgrade

**The Career Intelligence model upgrade is part of this V2 release, not a future optional enhancement.**

The application previously moved from GPT-5 Mini to GPT-5.

Please audit the current implementation and confirm which actual model is being called.

We want to evaluate and migrate the career understanding and text-generation stages to the strongest suitable GPT-6 model available through the project's API access.

## 4.1 Preferred Quality-First Configuration

Preferred candidate:

`gpt-6-astra`

Use it for:

- CV reading and interpretation
- Career experience extraction
- PM capability extraction
- Career summarisation
- Natural-language refinement

Keep these as logically separate processing stages even if they initially use the same model.

Verify that the exact model ID is available, supported by the SDK, and accessible to the current API project before deploying.

If unavailable, identify the blocker and compare suitable supported alternatives. Do not silently substitute GPT-5.

## 4.2 Cost and Performance Benchmarking

Compare the quality-first candidate with:

`gpt-6.1-sol`

Use representative PM CVs and real refinement instructions.

Evaluate:

- Factual understanding
- Professional capability abstraction
- Summary quality
- Unsupported claims
- Refinement accuracy
- Structured output reliability
- Latency
- API cost

Start by prioritising quality.

Optimise cost only after confirming that quality remains acceptable.

## 4.3 Model Responsibilities

Maintain separate configurable stages:

| Stage | Preferred Configuration |
|---|---|
| CV Interpretation | GPT-6 Astra |
| Career Extraction | GPT-6 Astra |
| Capability Summarisation | GPT-6 Astra |
| Refinement Interpretation | GPT-6 Astra |
| Voice Transcription | Compatible multilingual transcription model |
| Image Generation | Retain existing service initially |
| Text and Layout Rendering | Deterministic application renderer |

Do not use the image-generation model to independently interpret the career history.

## 4.4 Environment Configuration

Inspect existing environment variable names before changes.

Suggested configuration structure:

`OPENAI_CAREER_MODEL=gpt-6-astra`

`OPENAI_SUMMARY_MODEL=gpt-6-astra`

`OPENAI_REFINEMENT_MODEL=gpt-6-astra`

`OPENAI_TRANSCRIPTION_MODEL=<verified-supported-model>`

`OPENAI_IMAGE_MODEL=<existing-model>`

These are proposed variable names, not assumed existing variables.

Ensure the code reads the actual configured names correctly.

Do not expose API keys in frontend code or logs.

Do not ask the user to change production environment variables before checking code compatibility.

Verify the final model IDs using successful real API calls.

---

# 5. Separate Career Intelligence from Visual Generation

**Critical architectural requirement.**

The application should not depend on a single image model to understand a CV, derive professional capabilities, create summaries and render the final map.

Implement a structured multi-stage process.

## Stage A – Input Processing

Combine:

- Uploaded CV text
- Typed career description
- Voice transcription
- Additional user-provided context

Extract factual career information.

Preserve technical terminology and relevant achievements.

Avoid duplicate information.

## Stage B – Career Intelligence

Analyse:

- Professional roles
- Responsibilities
- Scope of ownership
- Technical capabilities
- Business capabilities
- Product domains
- Career progression
- Demonstrated impact

Distinguish documented facts, explicit user statements and AI-inferred capabilities.

## Stage C – Capability Summarisation

Translate detailed experience into concise, higher-level PM capabilities.

Avoid simply reproducing projects, job titles or operational tasks.

## Stage D – Structured Career DNA

Produce validated structured JSON containing:

- Career history
- Experience domains
- Core PM capabilities
- Supporting evidence
- Primary categories
- Summaries and labels
- Visual metadata
- Version information

This structured representation becomes the single source of truth.

## Stage E – Visual Rendering

Generate the final visual from the structured data.

Use programmatic layout where possible for:

- Text
- Icons
- Typography
- Labels
- Positioning
- Spacing
- Card layout
- Alignment

Use an image model for artistic assets only where necessary.

The image model must not independently rewrite factual career content.

This separation is essential for accurate summaries, visual consistency and targeted editing.

---

# 6. Improve PM Capability Extraction

**Current problem: The AI extracts details at too low a level.**

The output frequently highlights individual tasks instead of broader PM capabilities.

This reduces the perceived seniority and impact of the user's career profile.

## 6.1 Required Interpretation Hierarchy

### Level 1 – Career Domain

Examples:

- Trust & Safety PM
- AI Product
- Platform Product
- Growth Product

### Level 2 – High-Level Capability

Examples:

- Safety Framework Development
- 0-to-1 Product Infrastructure
- Scalable Risk Governance
- AI Product Strategy
- Platform Capability Development
- Product Growth Experimentation
- Cross-functional Product Leadership

### Level 3 – Supporting Projects and Evidence

Examples:

- Minor protection
- High-risk report routing
- Individual reporting workflows
- Specific safety features
- Technical integrations
- Model evaluation projects

**The main visual should prioritise Level 2.**

Level 3 should support the claims rather than dominate the map.

## 6.2 Trust & Safety PM Example

Current output:

**Trust & Safety PM**
- Minor protection
- High-risk report routing

The user has clarified that their work includes:

- Building safety frameworks
- Creating safety pipelines from zero to one

Better summary:

**Trust & Safety PM**
- Safety Framework Development
- 0-to-1 Safety Pipelines & Infrastructure

Other capability labels may be considered if supported by actual evidence.

Do not force these exact labels onto every user.

## 6.3 General Abstraction Rules

Prioritise:

- Strategic contribution
- Systems thinking
- Framework development
- Zero-to-one product creation
- Platform and infrastructure building
- Cross-functional leadership
- Risk and governance capability
- Business value
- Product outcomes
- Technical complexity where relevant

Do not fabricate business outcomes or metrics.

Distinguish ownership from participation.

Avoid repetitive generic buzzwords.

The goal is a meaningful professional capability summary, not a list of CV bullet points.

## 6.4 Category Limits

Use up to four primary PM capability categories.

Fewer than four is acceptable.

Do not create additional categories solely to fill the design.

Avoid overlapping categories.

Keep the primary labels concise.

Preserve detailed supporting evidence separately.

---

# 7. Flexible Natural-Language Understanding

**Core principle: Flexible by Default, Strict on Safety and Factual Integrity.**

The system should behave like an intelligent PM career analysis collaborator, not a rigid template editor.

## Generation

Understand user inputs semantically.

Accept:

- Informal language
- Imperfect grammar
- Different languages
- Incomplete sentences
- Career corrections
- Additional context
- Broad requests for emphasis

## Refinement

Accept both high-level and specific editing instructions.

Users should not need to know internal field names or exact data structure.

Examples:

- "Make my AI experience more prominent."
- "These two categories overlap."
- "Focus more on the frameworks I built."
- "Change the two lines under Trust & Safety."
- "Keep the design unchanged."
- "Make it sound more strategic."
- "Highlight my zero-to-one experience."

Infer reasonable editing intent from the active map and conversation context.

Ask for clarification only when genuinely needed.

Do not reject a valid request simply because it differs from a predefined template.

## User Corrections

Allow users to add or correct their own professional information.

Treat explicit corrections as new user-provided source information.

Do not reject them merely because they are absent from the original CV.

However, never fabricate measurable achievements, companies, responsibilities or unsupported career claims.

---

# 8. Conversational Map Refinement

**This is a core feature of Career Studio V2.**

The first generated result must be editable through natural language.

## 8.1 User Journey

1. Generate initial PM Career DNA.
2. Review the map.
3. Return to the existing composer.
4. Type or speak a modification request.
5. Click **Refine My DNA**.
6. The system updates the selected version.
7. The revised result appears automatically.

The user may repeat the process.

Reuse the same composer.

Do not introduce a separate complex editing interface.

## 8.2 Required Editing Behaviour

The model must:

1. Identify the selected map version.
2. Understand the requested change.
3. Locate the correct section or category.
4. Apply a targeted update.
5. Preserve unrelated content.
6. Validate the resulting structure.
7. Create a new version.
8. Re-render the map.

Do not regenerate the entire career interpretation from scratch for every small edit.

## 8.3 Critical Existing Bug

The system previously rejected:

"Please update the ones under Trust and Safety PM for Version 1. We should summarise the key points for Trust and Safety PM because I constructed safety frameworks and created safety pipelines from 0 to 1."

The application returned:

"That edit could not be verified. Try a smaller, more specific change."

**This request is valid and must be supported.**

### Expected Interpretation

- Version: Version 1
- Section: My PM Journey
- Category: Trust & Safety PM
- Target: Two supporting descriptions beneath that category

Expected updated text:

**Trust & Safety PM**
- Safety Framework Development
- 0-to-1 Safety Pipelines & Infrastructure

Unrelated sections and visual elements should remain unchanged.

## 8.4 Reliable Structured Editing

Use stable IDs and structured data.

Implement:

- Semantic target resolution
- Structured patch generation
- Schema validation
- Targeted updates
- Version creation
- Safe re-rendering

Do not depend on exact matching of visible text.

Do not reject an instruction just because the model reformulates it.

Do not use overly restrictive verification that prevents valid semantic updates.

If a patch is structurally invalid, attempt internal repair.

If a request is genuinely ambiguous, ask for clarification.

If an update fails, preserve the previous successful map.

Report the actual root cause of the existing failure.

---

# 9. Version History & Restoration

Implement version history for successful map generations and refinements.

Example:

- Version 1: Initial map
- Version 2: Updated Trust & Safety description
- Version 3: Revised AI capability summary

Users must be able to:

- Select an earlier version.
- View the selected version.
- Restore it.
- Continue refining from it.

Never overwrite the original version when applying edits.

Failed changes must not corrupt saved versions.

Use session-scoped storage or another privacy-conscious approach with clear retention behaviour.

Refinements and restoration should not increase the public map creation counter.

---

# 10. Dynamic Visual Design System

**Critical design principle: Consistent Design Language, Flexible Visual Expression.**

The original reference illustration defines the overall aesthetic, not a fixed template.

We want each user's PM Career DNA to feel individual and distinctive.

Do not force every map to use identical purple colours, icons, decorations or arrangements.

## 10.1 Preserve the Design Language

Maintain:

- Friendly, playful visual identity
- Rounded typography
- Soft dimensional illustrations
- Floating islands
- Subtle shadows
- Balanced composition
- Clear information hierarchy
- Polished, approachable appearance

Avoid generic corporate dashboards and unrelated infographic styles.

## 10.2 Flexible Colour Palettes

**Purple is not mandatory.**

Allow coordinated pastel themes such as:

- Lavender, pink and peach
- Sky blue, mint and turquoise
- Coral, cream and gold
- Soft green, teal and blue
- Lilac, periwinkle and yellow

Use coherent colour roles.

All icons, islands, cards and decorative elements must work together within the selected palette.

Maintain readable contrast.

Do not randomly assign unrelated colours to every element.

## 10.3 Dynamic Icon Selection

Do not use the same fixed icons for every map.

Choose icons based on the user's actual PM domains and capabilities.

Examples:

| Capability | Potential Icons |
|---|---|
| AI Product | AI chip, network, brain |
| Growth Product | Rocket, growth chart |
| Platform Product | Layers, modular systems |
| Trust & Safety | Shield, lock, framework |
| Product Strategy | Compass, roadmap |
| Data & Insights | Chart, magnifying glass |
| Customer Experience | People, interaction |
| Zero-to-one Building | Building blocks, construction |
| Technical Leadership | Gears, architecture |

These are suggestions, not fixed rules.

Use varied, semantically appropriate icons.

Maintain consistent illustration style within the map.

Ensure that every icon is complete and correctly proportioned.

## 10.4 Remove the Two Upper-Corner Clouds

The current map has two decorative cloud groups positioned near the left and right edges of the upper section.

They are partially clipped and look visually disconnected.

**Preferred solution: Remove both clouds.**

If retaining decorative clouds in future variations, they must be:

- Fully visible
- Properly integrated
- Appropriately spaced
- Visually balanced

Do not add decorative objects merely to fill space.

## 10.5 Fix Title and Logo Alignment

The title:

**My PM Career DNA**

must be horizontally centred relative to the full canvas.

The DNA logo should be closer to the title.

Requirements:

- Centre the title.
- Reduce the gap between title and logo.
- Treat title and logo as one visually balanced header group.
- Avoid the logo pushing the title away from the centre.
- Preserve correct alignment across different canvas sizes.
- Use reliable layout constraints instead of arbitrary pixel positioning.

## 10.6 Flexible Visual Structure

Preserve the main information flow:

**My PM Journey → Shaped My PM DNA**

However, the detailed layout may adapt to the content.

Allow variation in:

- Career-domain count
- Capability-card count
- Floating-island positioning
- Icon arrangements
- Decorative elements
- Card widths
- Spacing
- Supporting illustrations

Do not force empty categories into a map.

Do not overcrowd a map with extensive content.

Use content-aware layout rules.

## 10.7 Visual Completeness

Every visual element must remain fully inside the intended output canvas.

This includes:

- Icons
- Islands
- Clouds
- Characters
- Cards
- Text
- Decorative graphics

Avoid:

- Cropped icons
- Cut-off clouds
- Overlapping text
- Misaligned elements
- Inconsistent margins
- Decorative elements obstructing content

Use safe margins and correct layout constraints.

Do not simply shrink the entire composition to compensate for clipping.

Fix the underlying layout.

## 10.8 Typography

Match the playful, rounded typography of the approved reference image.

Maintain:

- Readability
- Consistency
- Clear hierarchy
- Appropriate spacing
- Professional polish

Render critical text programmatically wherever possible.

Do not rely on the image model to generate all text.

## 10.9 Controlled Visual Variation

Different users' maps should feel related but not identical.

Support controlled variation in:

- Palette
- Icons
- Illustration choices
- Layout composition
- Decorative elements

Keep consistent:

- Typography system
- Visual quality
- Information hierarchy
- Component styling
- Shadow treatment
- Overall brand personality

## 10.10 Visual Stability During Refinement

For text-only refinements, preserve the current map's:

- Palette
- Icons
- General layout
- Decorative elements
- Typography

Do not randomly redesign the map after each user correction.

Only change visual elements when explicitly requested or genuinely required by the updated content.

---

# 11. Generation & Refinement Waiting Experience

## 11.1 Initial Generation

When Generate is clicked:

- Immediately display **Analysing...**
- Disable duplicate submissions.
- Preserve user input.
- Show a clear waiting state.
- Automatically display the finished result when ready.
- Smoothly scroll to the results area.

The user should not have to search manually for the generated map.

## 11.2 Expected Waiting Time

Measure actual generation latency.

If real performance supports it, use:

"This usually takes about 1–2 minutes."

Do not display arbitrary estimates.

If reliable data is not yet available, use a neutral waiting message.

Do not show fake countdowns or progress percentages.

## 11.3 Progress Stages

Possible stages:

1. Understanding your career journey
2. Discovering your PM strengths
3. Bringing your Career DNA to life

Only mark stages completed when backend progress supports those states.

Otherwise, show an indeterminate loading animation.

## 11.4 Refinement

When users click Refine My DNA:

- Display **Updating...**
- Preserve the existing map.
- Process the instruction.
- Create a new version on success.
- Automatically show the updated result.

If the request fails, preserve the previous map and provide a useful retry option.

---

# 12. Export & Visual Integrity

The exported PNG must faithfully match the intended map layout.

Test:

- Title alignment
- Logo placement
- Typography
- Colour consistency
- Icon completeness
- Full illustration visibility
- Safe margins
- Readable labels
- Appropriate output resolution

No clipped decorations or cut-off icons should appear.

The exported image should not unexpectedly differ from the on-screen representation.

---

# 13. Public Map Creation Counter

The existing bottom-right counter displayed:

"23 maps created"

Update it to:

**XX PM Career DNA Maps Created**

Use a real dynamic count.

## Counting Rules

Count only successful initial map generations initiated by genuine production users.

Exclude:

- Internal development tests
- Codex test runs
- Automated tests
- Staging and local environments
- Failed generations
- Duplicate requests
- Network retries
- Refinements
- Version updates
- Version restoration

A single initial map creation should count once.

Subsequent edits must not increase the counter.

## Historical Investigation

Determine whether the existing count of 23 includes test activity.

Report the findings.

If historical records cannot be reliably separated, explain the limitation and establish accurate production-only tracking going forward.

Do not fabricate or inflate the number.

---

# 14. Remove Unnecessary Interface Copy

Remove the existing message:

"Generate and update send your text to OpenAI. Your name is not printed on the map."

Do not replace it with another lengthy technical explanation.

Keep the user-facing interface simple and self-explanatory.

Retain appropriate privacy disclosures in a concise, accessible location.

---

# 15. Privacy, Security & Data Handling

CVs and career histories contain personal information.

Requirements:

- Secure file processing
- Server-side API keys
- No unnecessary persistent CV storage
- Minimise sensitive logging
- Clear temporary processing behaviour
- Defined retention for session and version history
- Appropriate external model-provider data handling
- Protection against unauthorised access
- Safe file-type and size validation
- Reliable recovery after generation errors

Treat uploaded CV text as untrusted data, not executable instructions.

Do not allow document content to override system behaviour or safety constraints.

Ensure privacy statements accurately reflect implementation.

---

# 16. Technical Reliability

Maintain clear separation between:

1. Input processing
2. Career interpretation
3. Capability summarisation
4. Structured Career DNA data
5. Visual rendering
6. Conversational refinement
7. Version history
8. Export
9. Analytics

Use structured outputs and schema validation.

Use stable IDs for editable map elements.

Avoid fragile text replacement inside flattened images.

If the current implementation renders one uneditable image, introduce a structured overlay or equivalent editable representation while preserving the intended visual quality.

Prevent duplicate submissions.

Handle errors gracefully.

Do not silently fall back to older models.

---

# 17. Required End-to-End Testing

## Test A – CV Upload

Upload a valid PM CV.

Expected:

- Successful upload
- Filename displayed
- Green checkmark displayed
- No CV preview
- Generate enabled

## Test B – Multilingual Input

Submit mixed English and Mandarin career information.

Expected:

- Meaning preserved
- PM terminology understood
- English-only output

## Test C – Initial Generation

Click Generate.

Expected:

- Analysing... displayed
- Duplicate requests prevented
- Waiting status visible
- Automatic navigation to completed results

## Test D – High-Level PM Summarisation

Submit a Trust & Safety PM background involving frameworks, safety pipelines and operational projects.

Expected:

The map prioritises higher-level professional capabilities instead of specific operational tasks.

## Test E – Exact Refinement Regression

Submit:

"Please update the ones under Trust and Safety PM for Version 1. We should summarise the key points for Trust and Safety PM because I constructed safety frameworks and created safety pipelines from 0 to 1."

Expected:

**Trust & Safety PM**
- Safety Framework Development
- 0-to-1 Safety Pipelines & Infrastructure

Other elements remain unchanged.

A new version is created.

## Test F – Chinese Refinement

Submit:

"把 Trust & Safety PM 下面的描述改成更高层次的能力，突出我建设安全框架和从零到一搭建安全管线的经验，其他内容保持不变。"

Expected:

The correct fields are updated and the final text is in English.

## Test G – Version History

Generate Version 1, refine into Version 2, then restore Version 1.

Expected:

- Original preserved
- Correct version displayed
- Restoration successful
- No data corruption
- No additional creation count

## Test H – Visual Variety

Generate maps for multiple distinct PM profiles.

Expected:

- Different appropriate palettes
- Different contextual icons
- Varied compositions
- Consistent design language
- No identical-looking template repeated without reason

## Test I – Visual Layout

Check:

- Title centred
- DNA logo close to title
- Two upper-corner clouds removed
- All icons complete
- No clipped illustrations
- Compact content layout
- Consistent typography

## Test J – Refinement Visual Stability

Perform a text-only edit.

Expected:

Palette, layout, icons and decoration remain unchanged unless a necessary layout adjustment is required.

## Test K – PNG Export

Export the generated map.

Expected:

- Complete image
- No clipping
- Consistent spacing
- Readable text
- Accurate visual composition

## Test L – Creation Counter

Create one new map and refine it twice.

Expected:

Public count increases by exactly one.

## Test M – Model Verification

Run real API calls and confirm the actual model IDs used by:

- CV interpretation
- Summarisation
- Refinement
- Transcription
- Image generation

Do not rely on environment variable values alone as proof.

---

# 18. Implementation Priorities

## P0 – Critical

1. Audit existing architecture and model calls.
2. Upgrade Career Intelligence models.
3. Improve PM capability extraction.
4. Fix the existing refinement failure.
5. Ensure multilingual input and English-only output.
6. Implement reliable structured editing.
7. Preserve version history and data integrity.

## P1 – Core User Experience

1. Implement consistent naming.
2. Preserve the landing page.
3. Simplify the input section.
4. Improve Analysing and Updating states.
5. Automatically display completed results.
6. Improve version navigation.
7. Correct the creation counter.
8. Remove unnecessary interface copy.

## P2 – Dynamic Visual Design

1. Implement coordinated colour variation.
2. Introduce contextual icon selection.
3. Allow flexible content-aware layouts.
4. Remove problematic corner clouds.
5. Centre the title and logo.
6. Fix clipping and export margins.
7. Improve compactness and typography.
8. Preserve visual stability during refinement.

## P3 – Optimisation

1. Benchmark GPT-6 Astra against GPT-6.1 Sol.
2. Measure generation time.
3. Measure API costs.
4. Improve model efficiency where quality allows.
5. Optimise voice input responsiveness in a later iteration.

---

# 19. Final Deliverables from Codex

After implementation, provide:

1. Summary of implemented changes.
2. Current and previous model IDs for each processing stage.
3. Any required environment variable changes.
4. Confirmation of successful API model migration.
5. Root cause and fix for the failed Trust & Safety refinement.
6. Results of multilingual input testing.
7. Screenshots of initial and refined maps.
8. Examples of maps with different coordinated visual themes.
9. Confirmation that icons and illustrations are not clipped.
10. Confirmation that the title and logo are correctly centred.
11. Confirmation that version history and restoration work.
12. PNG export verification.
13. Public counter investigation findings.
14. Measured generation latency and approximate cost.
15. Any unresolved limitations.

## Final Implementation Instructions

**Please implement these requirements as one coherent Career Studio V2 upgrade.**

Do not rebuild the application or remove functioning features.

Inspect the existing repository first.

Keep the current landing-page experience intact.

Upgrade the career understanding and summarisation models, separate AI reasoning from visual generation, improve capability abstraction, and fix conversational refinement.

Evolve the current renderer into a flexible, content-aware visual design system that produces distinctive but stylistically consistent Career DNA maps.

Use the supplied reference images as design guidance.

Do not treat the reference artwork as a fixed colour palette or immutable layout template.

Test all critical user workflows before reporting completion.

If any requirement cannot be implemented reliably, explain the actual technical limitation rather than silently omitting it.

**The ultimate goal is a personalised PM Career DNA experience that feels intelligent, trustworthy, visually delightful and genuinely collaborative.**
