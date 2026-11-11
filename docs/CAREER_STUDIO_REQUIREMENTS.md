# Career Studio – Complete Product & AI Architecture Requirements

## Project Objective

Refine the existing Career Studio into a high-quality, AI-powered PM Career DNA experience.

The product should help Product Managers understand, visualise, and refine their professional strengths through a distinctive and personalised Career DNA Map.

**Important: This is an enhancement of the existing application, not a rebuild.**

Preserve the current branding, landing page, and visual direction while implementing the following requirements.

---

# 1. Product Positioning: PM Career DNA

Career Studio should initially focus exclusively on Product Managers.

The reason is quality control. We want excellent PM career interpretation rather than inconsistent support across many professions.

### Requirements

- Position the experience around **PM Career DNA**.
- Optimise the AI specifically for Product Management experiences.
- Recognise transferable skills from engineering, consulting, business, data, AI, operations, and other backgrounds.
- Do not incorrectly reinterpret every previous job as a PM position.
- Distinguish actual professional experience from inferred capabilities.
- Never invent achievements or responsibilities not supported by the user's input.
- All final Career DNA content must be in English.

The product should extract the underlying professional capabilities, not simply repeat job titles or project names.

# 2. Preserve the Existing Landing Page

**Do not redesign the existing first-screen experience.**

Keep the existing:

- Visual design and branding.
- Main hero section.
- Logo and animations.
- Page composition.
- Primary CTA: **Explore My Career DNA**.

Clicking the CTA should smoothly scroll or navigate to the career input section below.

Do not show CV upload immediately upon visiting the website.

The intended experience is:

Landing Page → Explore My Career DNA → Career Input → Generation → Interactive DNA Map.

The landing page should first build curiosity and trust before requesting personal career information.

# 3. Career Input Experience

## Section Heading

**Explore My PM Career**

Use a clean, minimal, centre-aligned layout.

## CV Upload

Provide a prominent:

**Upload CV**

Support PDF, DOC and DOCX where reliable parsing is available.

Display a short privacy reassurance underneath.

Suggested wording:

"Your CV is only used to create your PM Career DNA Map."

Only add "and won't be saved" if the complete data-processing architecture, including external providers, supports that claim.

After uploading:

- Display a green checkmark.
- Display the filename, e.g. ✓ Resume.pdf.
- Allow file removal or replacement.
- Do not display the CV contents or a preview.
- Process the CV securely.
- Avoid persistent storage of original CV files, except where explicitly required and disclosed.

## Unified Text + Voice Composer

Below the upload section, use one ChatGPT-style composer.

Placeholder:

**Tell me about your career journey...**

Users should be able to:

- Type information directly.
- Record their voice through a microphone icon.
- Pause, stop, or resume voice recording.
- Transcribe speech into editable text.
- Combine transcribed speech with typed content.
- Correct or remove any part of the input.
- Add career information to supplement an uploaded CV.

Do not create separate text and voice input boxes.

Support multilingual input, but always produce the final Career DNA content in English.

No language selector or language-related instructional text is required.

## Generate

Use one primary CTA:

**Generate**

Enable it when either a valid CV or meaningful career input is present.

Both inputs may be combined but neither is individually mandatory.

Prevent duplicate submissions.

# 4. AI Architecture: Separate Career Intelligence from Visual Generation

**This is a critical architectural requirement.**

Do not rely on one image-generation model to independently understand the user's career, determine professional capabilities, and generate all visual content.

Implement a structured multi-stage workflow.

## Stage A: Career Intelligence

Recommended initial model:

`gpt-6.1-sol`

Evaluate `gpt-6-astra` as a higher-intelligence alternative for difficult CVs or when benchmarking shows meaningful improvements.

The Career Intelligence model should:

1. Read and interpret the uploaded CV.
2. Combine CV content with typed and transcribed career information.
3. Extract factual professional experiences.
4. Identify underlying product management capabilities.
5. Consolidate overlapping capabilities.
6. Select up to four high-level PM Career DNA categories.
7. Generate concise, meaningful English summaries.
8. Preserve evidence supporting each extracted category.
9. Return validated structured JSON.

### Important Categorisation Rules

- Maximum four main capability categories.
- Fewer than four is acceptable.
- Categories must be meaningful professional capability areas.
- Avoid generic buzzwords.
- Avoid repeating specific project names as category labels.
- Avoid unsupported career claims.
- Do not force overlapping skills into multiple categories.
- Differentiate strategic, technical, commercial, operational, and execution-related strengths when supported by evidence.
- Reflect individual career backgrounds rather than applying the same fixed categories to everyone.

For example, an engineering-to-PM candidate might have categories such as:

- Technical Product Leadership
- Platform & Systems Thinking
- Product Strategy
- Cross-functional Execution

These are examples only, not mandatory categories.

### Structured Output

Maintain a structured PM Career DNA representation containing:

- Original career facts and experiences.
- Inferred capabilities and supporting evidence.
- Selected top-level DNA categories.
- Category descriptions.
- Secondary skills and supporting details.
- Career timeline or role-level information where relevant.
- Visual presentation configuration.
- Current map version.

Use a defined JSON schema with validation.

The system should preserve this structured data across generation and refinement.

## Stage B: Visual Generation

Use the structured career data as the single source of truth for map content.

Prefer deterministic SVG, HTML/CSS, Canvas, or another suitable programmatic renderer for:

- Text labels.
- Font selection.
- Category placement.
- Spacing and alignment.
- Visual hierarchy.
- Interactive elements.

An image-generation model may be used for decorative illustrations, artistic assets, or backgrounds.

Evaluate a supported image model such as:

`gpt-image-2.6-sunburst`

Do not change the current image-generation provider or model unnecessarily if the existing service produces better results. Benchmark against the reference design first.

**The image model should not independently rewrite or reinterpret career content.**

This separation is intended to improve accuracy, visual consistency, and editability.

# 5. Career DNA Visual Design

I will provide the preferred visual reference image again.

Use this image as the design target.

## Visual Style

- Friendly, distinctive, creative, and polished.
- Playful or slightly rounded typography.
- More compact layout.
- Reduced excessive whitespace.
- Closer alignment between labels and associated visual elements.
- Consistent colour palette and graphic language.
- Clear, attractive visual hierarchy.
- Preserve the reference's illustrated DNA / island-inspired visual identity.

Do not replace the reference style with a generic infographic, dashboard, corporate flowchart, or unrelated diagram.

## Career DNA Content Presentation

- Show a maximum of four primary capabilities.
- Use concise category headings.
- Avoid overcrowding the map with text.
- Keep detailed source information accessible through expandable details, tooltips, or equivalent interactions.
- Use real career information, not fabricated project examples.
- Maintain the reference typography as closely as practical.

The final result must be visually coherent, readable, and suitable for downloading and sharing.

# 6. Conversational Map Refinement

**Users must be able to modify their generated Career DNA Map through natural language.**

The first generated result is not final.

## Expected User Journey

1. Generate the first Career DNA Map.
2. Review the result.
3. Return to the existing Career Journey composer.
4. Type or speak requested changes.
5. Click **Update My DNA Map**.
6. Receive an updated version of the existing map.

Users should be able to repeat this process multiple times.

## Example Instructions

- "Make my AI experience more prominent."
- "This category doesn't accurately reflect my strengths."
- "Replace Stakeholder Management with Technical Product Leadership."
- "Make the descriptions shorter."
- "Keep the existing layout but change this title."
- "Consolidate the two overlapping categories."

## Refinement Logic

Each refinement must use:

- The original career information.
- The existing structured Career DNA.
- The latest map version.
- The user's new instruction.

The system should identify the requested changes and preserve unrelated content.

**Do not regenerate the entire career interpretation from scratch for every revision.**

Apply targeted updates to the structured representation whenever possible.

Maintain visual consistency between versions.

Do not invent new capabilities when a user requests a purely visual change.

If a requested change conflicts with documented career facts, ask for clarification or distinguish user-provided corrections from existing evidence.

# 7. Map Version History

Implement lightweight version history.

Each successfully generated or refined map should have a version identifier:

Version 1, Version 2, Version 3, etc.

Users should be able to:

- View the latest map.
- Return to an earlier version.
- Continue refining a selected version.
- Avoid losing a preferred previous result.

At minimum, provide an **Undo / Restore Previous Version** capability.

Maintain version data in the active user session. Do not introduce persistent storage of personal career data without a clear retention policy and user disclosure.

# 8. Generation Waiting Experience

Provide a polished waiting state for both initial generation and refinement.

Suggested title:

**Creating Your PM Career DNA...**

Suggested progress stages:

1. Understanding your career journey
2. Discovering your PM strengths
3. Bringing your Career DNA to life

Only display actual completed steps when backend progress information is available.

Otherwise, use an indeterminate loading animation.

## Expected Time

Measure real generation performance first.

Display a realistic estimate such as:

"This usually takes about 1–2 minutes."

Only use this wording if supported by measured generation times.

Do not implement a fake countdown or fake progress percentage.

If generation takes longer than expected, update the status message without losing user data.

Prevent duplicate generation requests.

Provide a retry option if generation fails.

# 9. Public Generation Counter

Investigate the existing bottom-right counter.

Current display:

"23 maps created"

Change the format to:

**"23 PM Career DNA Maps Created"**

The number must be dynamically calculated.

## Counting Rules

- Count only successful initial map generations initiated by genuine production users.
- Exclude internal development testing.
- Exclude automated tests.
- Exclude staging and local environments.
- Exclude failed generations.
- Exclude retries of the same generation request.
- Exclude map refinements and version updates.

Each newly created map should count once.

Investigate whether the existing number 23 includes internal testing.

Do not silently reset, retain, or alter historical counts without determining their accuracy.

If historical data cannot be reliably separated, explain the limitation and establish accurate tracking from that point forward.

# 10. Privacy, Security and Data Handling

Career documents contain personal information and must be treated carefully.

Requirements:

- Keep API keys server-side.
- Never expose API keys to the browser.
- Use secure temporary file processing.
- Minimise collection and storage of CV information.
- Avoid logging CV contents, transcription text, or other personal data.
- Clearly distinguish temporary processing from persistent storage.
- Check the model provider's retention behaviour before making privacy claims.
- Clear temporary files and unnecessary data when no longer needed.
- Preserve session context sufficiently to support refinement and version history.

# 11. Model Configuration and Environment Variables

The current application reportedly uses GPT-5 after previously using GPT-5 Mini.

Please first inspect the existing implementation and identify:

- The actual text model currently being called.
- The actual image model currently being called.
- Where each model is configured.
- Whether model names are hardcoded or controlled through environment variables.
- The API endpoint and SDK currently being used.
- Whether the project's API key has access to the recommended models.

Do not assume that changing one environment variable updates every generation stage.

### Recommended Configuration

Use separate configuration entries, for example:

`OPENAI_CAREER_MODEL=gpt-6.1-sol`

`OPENAI_IMAGE_MODEL=gpt-image-2.6-sunburst`

Treat these as suggested variable names, not mandatory existing names.

The implementation must match the application's actual configuration structure.

Do not overwrite or remove existing environment variables without checking their dependencies.

Never print API keys or other secrets.

### Model Validation

Confirm model availability for the active API project.

Test:

- CV parsing and structured output.
- English-only career summaries.
- Image or visual generation.
- Incremental map refinement.
- Error handling and retries.

Provide the actual model IDs used after implementation.

# 12. Performance and Quality Validation

Test the application with several different PM profiles, including:

- Traditional product management.
- Engineering-to-product career transition.
- AI / ML product management.
- Technical platform product management.
- Business or consulting-to-product transition.

Evaluate:

- Factual accuracy.
- Capability categorisation.
- Quality of abstraction.
- Detection of overlapping skills.
- Unsupported claims.
- English-language quality.
- Visual layout consistency.
- Refinement accuracy.
- End-to-end generation time.
- Estimated API cost per map.

Compare GPT-6.1 Sol and GPT-6 Astra on a representative sample before selecting a more expensive default.

# 13. Acceptance Criteria

The work is complete when:

- [ ] The existing landing page and exploration CTA are preserved.
- [ ] The product is clearly PM-focused.
- [ ] CV upload is introduced only after entering the exploration flow.
- [ ] CV upload confirmation displays a filename and checkmark.
- [ ] Text and voice use the same input composer.
- [ ] Voice can be interrupted, resumed, and edited.
- [ ] The main initial action is "Generate".
- [ ] All generated career content is in English.
- [ ] Career Intelligence and visual rendering are separated.
- [ ] Structured PM Career DNA data is validated and reusable.
- [ ] Maximum four primary capability categories are displayed.
- [ ] The map follows the provided visual reference.
- [ ] Users can request changes using the existing composer.
- [ ] Map updates preserve unrelated content.
- [ ] Version history and restoration work.
- [ ] Generation has a clear waiting state with realistic timing.
- [ ] The public creation counter excludes tests and refinements.
- [ ] Model configuration is verified and documented.
- [ ] Privacy and data handling claims match actual behaviour.
- [ ] The complete workflow has been tested.

# 14. Implementation Instructions

Please follow these principles:

1. Inspect the existing codebase before making changes.
2. Preserve the current landing page and working functionality.
3. Implement the requirements within the existing application.
4. Prioritise career interpretation accuracy over visual complexity.
5. Keep model configuration modular and easy to change.
6. Avoid unnecessary infrastructure and dependencies.
7. Avoid exposing secrets or storing personal data unnecessarily.
8. Keep the user-facing interface minimal and intuitive.
9. Test both initial generation and natural-language refinement.
10. Do not report a requirement as complete unless it has been implemented and verified.

After implementation, provide:

- A concise summary of completed changes.
- The actual text and image model IDs.
- Any required environment variable updates.
- The investigation result for the existing counter.
- A demonstration of initial map generation.
- A demonstration of one map refinement.
- Any remaining limitations or unresolved issues.

**Please preserve the current application's identity while improving the intelligence, reliability, visual quality, and editability of the PM Career DNA experience.**
