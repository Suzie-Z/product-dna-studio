# Career DNA Studio — Original Experience Refinement
## Complete Product, Content, Visual & UX Requirements for Codex

**Project:** Career DNA Studio / My PM Career DNA  
**Iteration:** Original Version — Content & Experience Refinement  
**Priority:** Restore consistency, simplify interactions, improve content quality and reliability.

---

# 1. Overall Direction — Do Not Rebuild

We are returning to the original Career DNA Studio product experience.

The previous V2 redesign is not the direction we want to pursue.

**Use the original version as the implementation baseline, while using the sixth attached screenshot as the approved visual reference for the generated Career DNA Map.**

The sixth screenshot represents the intended visual improvements, especially:

- The integrated title and personal DNA theme.
- Consistent journey island/platform design.
- Subtle glowing connections between the career journey and resulting DNA.
- A distinct "Shaped My PM DNA" transition.
- Four clean capability cards.
- A professionally highlighted concluding statement.

These are visual specifications, not instructions to hardcode the particular person's career content.

Do not rebuild the website from scratch.

Do not introduce a new design system.

Do not change unrelated functionality.

Preserve the original homepage design language, branding and overall experience.

Create a recoverable checkpoint before implementation.

---

# 2. Product Positioning & Target Users

Career DNA Studio is currently designed exclusively for Product Management professionals.

Target users include:

- Product Managers
- Senior Product Managers
- Product Leads
- Product Owners
- Experienced professionals transitioning between PM roles

Do not introduce support for unrelated career categories in this iteration.

## Core Product Purpose

Career DNA Studio is not a CV optimisation product.

It is a self-recognition and career reflection experience.

We want to help people who are actively job hunting rediscover the value of their professional journey.

**Emotional positioning:**

"A warm embrace from who you've become, to who you are today."

**Brand statement:**

"See the person that you have become. Be inspired by who you are."

The product should transform existing career experiences into a meaningful, personalised Product DNA Map.

It should help users recognise strengths they may not have articulated before.

The tone should be warm, thoughtful and encouraging, without generic flattery or unsupported claims.

---

# 3. Primary User Journey

Keep the user journey simple:

**Upload CV → Understand Experience → Generate DNA Map → Explore Map → Refine (Optional) → Download**

## 3.1 CV Upload

CV upload is the primary entry point.

Most target users are already job hunting and have an existing CV.

Requirements:

- Support PDF and DOCX uploads.
- Avoid unnecessary onboarding questions.
- Do not require a separate manual career history form.
- Extract career experience from the CV.
- Provide a clear loading state while the CV is being analysed.
- Do not permanently store original CV files.
- Allow CV replacement when users want a fresh analysis.
- Keep final generated output in English.

## 3.2 AI Understanding

Before generating the map, extract a structured understanding of:

- Career stages and professional transitions.
- PM domains and responsibilities.
- Core transferable capabilities.
- Demonstrated achievements and impact.
- Technical and business problem-solving experience.
- Cross-functional influence.
- Leadership and decision-making.
- Evidence supporting each inferred strength.

Avoid direct keyword matching or simply rewriting CV bullet points.

The analysis should distinguish:

1. What the user did.
2. What the user demonstrated.
3. What professional capability those experiences reveal.

---

# 4. Generated Career DNA Map — Visual Requirements

The sixth attached screenshot is the approved reference for this iteration.

Use it as a design target while preserving the original application's render architecture.

The map should remain personal and dynamically generated.

Do not hardcode the example content from the screenshot.

## 4.1 Main Header and Personal DNA Theme

The existing design has:

"My PM Career DNA"

And beneath it:

"AI Productisation with Guardrails"

The second phrase is valuable because it provides a high-level professional interpretation of the person.

It should be retained as a dynamically generated **Personal DNA Theme**.

### Required Change

Integrate the personal DNA theme into the main title area rather than leaving it isolated on a separate line.

Preferred layout:

**[PM Logo] | My PM Career DNA | [Personal DNA Theme]**

The personal DNA theme should appear as a smaller companion pill or subtitle within the same header container.

The main title must remain visually dominant.

The DNA theme should be secondary, but clearly connected.

### Content Requirements

The theme must:

- Represent the user's distinctive professional identity.
- Be concise and meaningful.
- Reflect recurring strengths across the CV.
- Be grounded in evidence.
- Avoid generic statements such as "Innovative Product Leader".
- Vary between users.

Example:

"AI Productisation with Guardrails"

This is a reference example, not a fixed label.

The title layout must also handle longer generated themes gracefully, including responsive wrapping when needed.

---

## 4.2 My PM Journey — Consistent Island Design

The upper section represents the professional journey.

Each journey stage includes:

- Role/category icon.
- Professional category or role title.
- One or two concise descriptions.
- A 3D island/platform element.

### Critical Visual Rule

**Every island/platform in the same generated map must use exactly the same base shape and design style.**

Only the colours should vary.

For example, if four career stages are generated:

- Stage 1: orange circular platform.
- Stage 2: blue circular platform.
- Stage 3: teal circular platform.
- Stage 4: purple circular platform.

All four must share:

- The same silhouette.
- The same platform structure.
- The same perspective.
- The same illustration style.
- Consistent dimensions.
- Consistent lighting treatment.
- Consistent depth and decorative details.

Do not generate different kinds of structures for each stage.

Do not mix a floating island, a layered block, a cloud platform and a futuristic circular disc in the same journey.

If a different platform style is selected for another user's map, it may be different from this reference, but all stages within that map must use the same selected style.

### Implementation Guidance

Use a single shared component or visual template for journey platforms.

Apply different colour variants instead of generating independent platform illustrations.

This must be enforced at the component/design level, not left to generative image prompting alone.

---

## 4.3 Journey Connections

Keep a subtle dotted or flowing line connecting the journey stages horizontally.

This represents career progression.

The connection should be:

- Light and elegant.
- Visually continuous.
- Non-intrusive.
- Consistent with the 3D pastel visual language.

Do not allow connector lines to overlap titles or body descriptions.

---

## 4.4 Connect Career Journey to Shaped My PM DNA

The previous reference design successfully used soft glowing connection lines between the career stages and the resulting DNA.

Reintroduce this visual relationship.

### Required Interaction Between Sections

Each journey platform should visually contribute toward the central:

**"Shaped My PM DNA"**

Use subtle flowing connector lines that originate near the platforms and converge toward the central DNA transition.

The design should convey:

**Your past experiences have shaped the professional strengths you carry today.**

Visual characteristics:

- Thin, softly glowing lines.
- Smooth curves.
- Low visual weight.
- Similar illustration style to the approved reference.
- Clearly visible without dominating the layout.

Avoid complex network diagrams.

Do not use arrows or heavy lines that make the experience look like an engineering architecture chart.

The goal is emotional and visual storytelling.

---

# 5. Shaped My PM DNA — Capability Cards

The second major section represents the professional capabilities developed throughout the career journey.

Keep the existing card-based design.

Generate a maximum of four capabilities.

Fewer than four is acceptable if the available CV evidence does not support four distinct strengths.

## 5.1 Capability Abstraction

Each capability should represent a meaningful, transferable PM strength.

Do not simply repeat:

- Past job titles.
- Employer names.
- Project names.
- Product feature names.
- Generic PM keywords.

For example:

CV evidence:
"Worked on multimodal model evaluations and model selection."

Weak output:
"Multimodal Evaluation"

Stronger output:
"AI Product Judgement"

Supporting description:
"Use evaluation to guide model selection and product trade-offs."

The capability name should reflect what the person has become good at, rather than simply what tasks they completed.

## 5.2 Card Structure

Each card should contain:

1. A meaningful icon.
2. A concise capability title.
3. A short supporting statement.
4. Two or three evidence-backed keywords or skill indicators, where available.

Keep card design consistent.

Allow icon, background colour and content to vary.

Maintain the approved soft pastel design language.

Make sure text fits correctly.

Avoid:
- Clipped text.
- Overlapping icons.
- Excessive word wrapping.
- Different card dimensions caused by content length.
- Empty placeholder tags.
- Unsupported skills added merely to fill the layout.

## 5.3 Content Quality

The result should communicate a professional identity that the user can recognise.

The goal is not to make everyone appear equally strong in the same four PM capabilities.

Different users should receive meaningfully different DNA results.

Do not force every user into a predefined archetype.

Use PM archetypes as conceptual guidance only, not as fixed output templates.

---

# 6. Career DNA Summary — Dedicated Highlight Section

The original generated map had a concluding statement displayed as plain text beneath the capability cards.

Example:

"Connect model evaluation, reusable capabilities and safety-conscious product delivery."

The content direction is acceptable, but the presentation is too weak.

This is an important concluding insight and should not look like an afterthought.

## Required Change

Introduce a dedicated, visually highlighted summary section.

Follow the sixth screenshot.

The summary should appear inside a:

- Rounded gradient banner.
- Decorative insight ribbon.
- Or similarly polished highlight component.

Include a subtle symbolic icon, such as a target or spark.

The conclusion should be visually intentional and integrated into the overall design.

### Content Rules

The concluding statement should:

- Connect the user's strongest capabilities.
- Communicate what makes their combination distinctive.
- Be concise.
- Feel like a personalised professional insight.
- Be generated from the user's actual Career DNA.
- Avoid repeating card descriptions verbatim.

Do not hardcode the example conclusion.

The footer "PM Career Studio" should remain visually secondary beneath the summary.

---

# 7. Recognition & Possible Directions — Redesign the Reading Experience

Retain the existing expandable category.

However, its current presentation feels like a generic information panel rather than a meaningful part of the Career DNA experience.

We want this to feel more like a personal discovery moment.

## 7.1 Section Identity

Keep the section optional and collapsible.

Introduce a warmer, more memorable concept.

**Preferred section name:**

"Your Next Chapter"

Optional descriptive subtitle:

"A little recognition of who you've become, and a glimpse of what could come next."

This section can have a subtle "Book of Possibilities" concept, inspired by the experience of opening a personal book of answers.

Do not make this look like a literal fortune-telling application.

It should remain credible, professional and grounded in the user's career experience.

An understated book, doorway, star or discovery illustration may be used.

Do not introduce an unrelated visual style.

## 7.2 Expand/Collapse Behaviour

The section must remain collapsed by default.

The user may open it if interested.

Use a clear arrow/chevron indicator.

The arrow should change direction when the section expands or collapses.

Preserve the existing simple click-to-expand interaction.

No additional modal or navigation page is required.

## 7.3 Content — Keep Only Two Sections

Inside the expanded panel, retain:

**A. Recognition**

A thoughtful acknowledgement of the person's accumulated strengths and professional journey.

It should recognise how their experiences connect and what they have demonstrated over time.

Example:

"Across NLP foundations, evaluation and moderation systems, you've repeatedly turned uncertain AI capabilities into dependable product decisions."

The language should feel reflective, warm and specific.

Avoid generic praise.

**B. Possibilities to Explore**

A thoughtful invitation to consider possible future directions.

These should emerge from demonstrated strengths and interests.

Avoid treating career possibilities as guaranteed recommendations.

Keep the tone open and empowering.

### Remove the Redundant Third Section

Delete the following heading and sentence entirely:

"My Product DNA"

"Your evidenced PM capabilities are highlighted in the map above."

This content is redundant because the map already presents the Product DNA.

Do not replace this sentence with another generic explanation.

Do not generate a repetitive "My Product DNA" subsection here.

## 7.4 Visual Treatment

Design the expanded content as an intentional independent panel.

Preferred direction:

- Soft lavender background.
- Rounded corners.
- Gentle spacing.
- Distinct headings.
- Comfortable reading width.
- Optional small thematic illustration.
- Warm, reflective presentation.

It should feel like an optional chapter of the Career DNA experience.

Do not turn it into another full-sized infographic.

---

# 8. View Supporting Evidence — Layout and Styling Fix

The current Supporting Evidence area is visually inconsistent with Recognition & Possible Directions.

Problems observed:

- Inconsistent horizontal alignment.
- Different panel widths.
- Different background treatments.
- Excessive empty space.
- One section looks like a lavender panel, while the other appears transparent or outlined.
- The expand/collapse trigger is placed awkwardly.

## 8.1 Alignment

Align "View Supporting Evidence" with "Your Next Chapter".

Both expandable sections should have:

- The same horizontal start position.
- The same maximum container width.
- The same outer margins.
- Consistent horizontal padding.
- Consistent vertical spacing.
- Matching chevron placement.

When collapsed, both section headers should remain visible and visually aligned.

## 8.2 Consistent Panel Design

Both expandable panels should use the same visual component style.

Recommended:

- Soft lavender background.
- Matching corner radius.
- Similar border treatment.
- Consistent heading typography.
- Consistent spacing.
- Matching expand/collapse behaviour.

Do not make one panel filled and the other transparent.

Reuse a shared expandable-panel component where practical.

## 8.3 Supporting Evidence Content

Preserve the existing supporting evidence functionality.

The purpose of this section is to demonstrate that the generated DNA is grounded in the CV.

It may include:

- Career experience.
- Source roles.
- Supporting achievements.
- Evidence for inferred PM capabilities.
- Explanations of career consolidation or categorisation.

Do not invent career transitions.

Do not mislabel non-PM work as PM experience.

Do not remove supporting evidence merely because it is not prominently displayed on the map.

The evidence should remain accessible to users who want to understand the analysis.

---

# 9. Result Page Layout

The result page should follow this order:

1. Generated Career DNA Map
2. Your Next Chapter (collapsible)
3. View Supporting Evidence (collapsible)
4. Result actions

Result actions:

**Primary:**
Download DNA Map

**Secondary:**
Refine My DNA

**Secondary:**
Generate a New Map

Keep the primary download action visually prominent.

The other actions should remain easy to discover without competing for attention.

Keep the page clean and consistent.

---

# 10. Refine My DNA — Simplify the Experience

The current refinement interaction is unnecessarily complicated and has introduced bugs.

We want to simplify it significantly.

**Refine My DNA must be a straightforward text-based instruction and apply workflow.**

Remove advanced conversation mechanisms that are unnecessary for this MVP.

## 10.1 Remove Voice Input

Remove voice input from Refine My DNA.

This includes:

- Microphone button.
- Voice recording.
- Speech recognition.
- Voice permission handling.
- Voice processing states.
- Related UI elements.

Voice input is not reliable enough in the current implementation.

Text input is sufficient for this iteration.

Do not replace it with another speech service.

## 10.2 Use GPT-6 Sol for Refinement Understanding

Use **GPT-6 Sol** as the intended model for understanding and interpreting the user's refinement instructions, provided the configured model endpoint actually supports it.

The model should understand natural-language instructions such as:

- "Change Launch requirements to Design for lasting value."
- "Make this capability sound more strategic."
- "I don't think this description accurately reflects my experience."
- "Replace this sentence with AI Product Judgement."
- "Please remove the emphasis on compliance."
- "Make the conclusion less generic."

The AI should identify:

1. What the user wants to change.
2. Which existing content field is targeted.
3. Whether the change is supported.
4. What the replacement should be.
5. Whether more clarification is genuinely required.

### Model Integration Requirement

Use the exact supported model identifier in the existing API configuration.

Do not assume that the display name "GPT-6 Sol" is itself a valid API model ID.

If GPT-6 Sol is not available in the current environment, do not silently substitute another model.

Keep model selection configurable and report the blocker clearly.

Use structured responses for refinement operations.

Avoid direct uncontrolled rewriting of the entire map.

---

# 11. Refine My DNA Modal — Header Behaviour

Preserve the modal header structure from the existing design.

Title:

**Refine My DNA**

Subtitle:

"A small change can make it feel more like you. Your map's visual identity stays the same."

This wording is approved.

## 11.1 Fixed Header

The modal header must remain fixed or sticky at the top of the modal.

The title, subtitle and close button must remain visible while the user scrolls through the content.

The close button must not disappear when scrolling.

The main content area should scroll independently.

## 11.2 Close Button

Keep the "X" close button in the top-right corner.

It must remain usable at all times.

Closing the modal should not accidentally apply changes.

## 11.3 Remove Unnecessary Divider

Remove the small extra horizontal line underneath or adjacent to the close button.

It serves no meaningful purpose and makes the header look visually untidy.

Do not remove the main modal boundary or necessary structural separation.

---

# 12. Refine Input — One Simple Text Area

The primary refinement interaction should have:

- One clearly labelled input area.
- A concise instruction.
- A multiline text field.
- One Apply Changes button.
- Inline validation and status feedback.

### Label

"Tell us what you'd like to change"

### Supporting Text

"Tell us what feels inaccurate, missing or too generic. For a more precise update, you can paste the exact sentence you'd like to change."

Users should be able to write natural-language instructions.

Do not force them to identify internal field names.

Do not require structured commands.

Do not introduce a complicated multi-step chat history interface.

### Important

Do not automatically include previously applied changes or earlier conversation history in the visible text area.

When a new refinement session starts, the input should be empty.

The current map content should be used as context behind the scenes.

Previously accepted content should remain part of the current map state, not be displayed as conversation history.

---

# 13. Refine Processing — Apply Changes

The Apply Changes interaction must be simple and predictable.

## 13.1 On Click

When a user clicks:

**Apply Changes**

Validate the instruction.

If valid, initiate the refinement operation.

While processing:

- Disable the Apply Changes button.
- Prevent duplicate submissions.
- Show a spinner or hourglass-style loading indicator.
- Display concise progress messaging.

Suggested loading message:

"Applying your changes…"

Optional supporting message:

"This may take around 20–30 seconds."

This is only an estimate. Do not imply a guaranteed completion time.

Do not display a fake timer.

The loading indicator should remain visible until the actual operation completes or fails.

## 13.2 Validation

If a requested change would leave a required field blank, do not apply it.

Show a clear inline message such as:

"This field can't be left blank. Please enter a replacement."

The user should remain in the same editing interface.

Preserve their input so they can revise it.

Do not open additional dialogs.

Do not ask Yes/No questions.

Do not offer automatic alternative replacements unless the user explicitly asks for suggestions.

### Remove the Current Yes/No Interaction

Delete the current behaviour where the application asks:

"The editor rejected leaving this field blank. Would you like [replacement] as a short replacement?"

Do not display this type of confirmation prompt.

Instead:

1. Display the validation error.
2. Allow the user to edit the original instruction.
3. Let them click Apply Changes again.

Keep the process deterministic.

## 13.3 Successful Apply

When the update succeeds:

1. Save the updated content in the current session state.
2. Update only the relevant content fields.
3. Confirm that the map reflects the accepted changes.
4. Clear the refinement input.
5. Close the Refine My DNA modal automatically.
6. Return the user to the updated DNA Map.

The user should immediately see the revised real output.

Do not keep the modal open with historical messages after success.

Do not require an additional confirmation click.

Optionally display a small, non-blocking success message:

"Your DNA Map has been updated."

If the updated map is below the viewport, return focus to the map or scroll it into view without unexpected jumps.

## 13.4 Failed Apply

If the operation fails:

- Keep the Refine modal open.
- Preserve the user's entered instruction.
- Do not modify the existing map.
- Do not clear the input.
- Re-enable Apply Changes.
- Display a visible error message.

Suggested copy:

"We couldn't apply your changes. Please try again."

For specific validation errors, explain the actual issue rather than displaying a generic failure.

Do not silently fail.

Do not leave the interface in a permanent loading state.

---

# 14. Refinement Editing Boundaries

Refinement is primarily for content adjustments.

Allowed changes include:

- Updating capability titles.
- Rewording descriptions.
- Changing evidence-backed keywords.
- Improving the personal DNA theme.
- Refining the concluding summary.
- Adjusting Recognition wording.
- Updating Possibilities to Explore.
- Correcting inaccurate descriptions.
- Changing emphasis within the existing career narrative.

### Not Allowed Through Text Refinement

- Changing island shapes.
- Rearranging the map layout.
- Changing the colour palette.
- Repositioning decorative elements.
- Altering the overall illustration style.
- Redesigning capability cards.
- Changing the page structure.

The user may generate a new map separately if a new visual result is desired.

### Technical Requirement

Keep content data and visual configuration separate.

A text refinement must not trigger a full visual redesign.

Use stable IDs to target specific text fields.

Update only the requested fields.

Preserve unrelated content.

Do not accidentally overwrite earlier accepted refinements.

---

# 15. Refinement Architecture

Use a reliable, structured update approach.

Recommended pipeline:

**User Instruction → GPT-6 Sol Interpretation → Validation → Targeted Content Patch → Updated Map**

The model should return a structured patch rather than an entire rewritten document.

Conceptual fields:

- target_section
- target_field_id
- operation
- replacement_text
- validation_status

The exact schema can follow existing project conventions.

## Safety and Consistency Checks

Before applying a patch:

- Confirm the target exists.
- Confirm the field is editable.
- Ensure required fields are not blank.
- Ensure the replacement fits the content constraints.
- Avoid unsupported factual claims.
- Preserve all unrelated fields.
- Prevent duplicate or conflicting updates.

Support multiple sequential refinement sessions.

Each new refinement should operate on the latest successfully applied map version.

Avoid relying on the visible chat history to reconstruct current state.

Use structured current-map state as the source of truth.

---

# 16. Preserve the Visual Map During Refinement

This is a critical requirement.

A text edit should not unexpectedly regenerate the whole illustration.

For example:

If a user requests:

"Change Launch requirements to Design for lasting value."

Then:

- Locate the specific skill tag.
- Replace only its text.
- Preserve card styling.
- Preserve card position.
- Preserve icons.
- Preserve journey platforms.
- Preserve other descriptions.
- Preserve the conclusion unless explicitly targeted.

If the exported map is currently generated as a flattened image, refactor the text rendering or composition process as necessary so deterministic targeted text updates are possible.

Do not rely on generating an entirely new image each time a sentence changes.

If the map must be re-exported after a content change, use the same fixed layout, assets and styles.

---

# 17. Generate a New Map

Keep the separate "Generate a New Map" action.

This should not be mixed with the Refine My DNA operation.

Users should be able to upload a new CV and start a fresh analysis.

A new CV should produce a new Career DNA interpretation.

A fresh generation may change:

- Journey stages.
- Capability categories.
- Personal DNA theme.
- Supporting descriptions.
- Recognition.
- Possibilities to Explore.
- Summary.

Keep the original visual design system consistent.

The product should not unpredictably switch between unrelated design styles.

---

# 18. Content and Visual Consistency Across the Entire Experience

The experience should use consistent:

- Rounded typography.
- Pastel colour language.
- Soft 3D illustrations.
- Component radii.
- Panel spacing.
- Button styles.
- Expand/collapse interactions.
- Hover and focus states.
- Error messaging.
- Responsive layout behaviour.

Avoid excessive decorative elements.

The visual style should support reflection and emotional engagement without reducing readability.

Do not sacrifice content accuracy to fit a predetermined visual template.

Do not generate placeholder content to make the screen look full.

---

# 19. Testing Requirements

Test the following scenarios before considering this iteration complete.

## A. Initial Generation

- Upload a PM CV.
- Confirm the CV is interpreted correctly.
- Confirm the correct career journey is generated.
- Confirm the DNA theme is dynamic.
- Confirm no more than four capabilities are produced.
- Confirm the map remains visually consistent.

## B. Map Visual Quality

- Journey platforms have the same shape.
- Different journey stages may use different colours.
- The connecting lines are visible and properly positioned.
- The summary is inside a highlighted banner.
- No card text is clipped.
- No decorative elements overlap content.
- The title and DNA theme fit within the header.
- The exported map retains the intended layout.

## C. Recognition & Evidence

- Both sections are collapsed by default.
- Both can be independently expanded.
- The "My Product DNA" redundant subsection is absent.
- Both expand/collapse controls are aligned.
- Both panels share the same styling.
- Supporting Evidence remains readable and factually grounded.

## D. Refine — Successful Update

Test:

"Change Launch requirements to Design for lasting value."

Expected:

- The correct field is identified.
- Only the relevant text changes.
- The UI shows processing.
- The map is updated successfully.
- The modal closes automatically.
- The latest map is visible.
- No previous refinement history remains in the input.

## E. Refine — Invalid Update

Test a request to clear a required field.

Expected:

- The request is rejected.
- No Yes/No choice appears.
- A concise validation message is shown.
- The user can revise the instruction.
- Apply Changes remains available after correction.
- No partial or invalid changes are committed.

## F. Refine — API Failure

Simulate a failed model or backend request.

Expected:

- The existing map remains unchanged.
- The modal stays open.
- User input is preserved.
- The loading indicator stops.
- An error is visible.
- The user may retry.

## G. Refine — Scrolling

Open the Refine modal and scroll to the bottom.

Expected:

- The title remains visible.
- The subtitle remains visible.
- The X button remains visible and clickable.
- Only the main content area scrolls.
- No redundant line appears under the close button.

## H. Multiple Refinements

Apply one successful change, reopen Refine, and apply another.

Expected:

- The first change is preserved.
- The input starts empty.
- The second instruction uses the latest map.
- Unrelated content remains unchanged.

## I. Responsive Layout

Verify desktop and mobile viewport behaviour.

Check:

- No horizontal overflow.
- No clipped modal header.
- All primary actions remain accessible.
- Expandable panel alignment remains consistent.
- Map preview scales appropriately.
- Exported map retains its intended aspect ratio.

---

# 20. Implementation Priorities

Implement in this order:

### P0 — Fix Refine Reliability

- Remove voice input.
- Configure GPT-6 Sol if supported.
- Simplify the input interaction.
- Remove Yes/No confirmations.
- Introduce proper validation.
- Add reliable processing feedback.
- Handle success and failure correctly.
- Clear the input and close the modal after successful updates.
- Keep the modal header and close button visible while scrolling.

### P1 — Improve Map Output

- Apply the sixth screenshot's approved layout details.
- Integrate the Personal DNA Theme into the title.
- Standardise journey platform shapes.
- Add journey-to-DNA connector lines.
- Give the conclusion a dedicated highlight banner.
- Improve output text fitting and readability.

### P2 — Improve Supporting Sections

- Rename and redesign Recognition & Possible Directions as an optional reflective experience.
- Remove the redundant My Product DNA subsection.
- Align Supporting Evidence with Recognition.
- Use consistent expandable panel styling.
- Preserve evidence accuracy.

### P3 — Refine AI Content Quality

- Strengthen PM-specific capability abstraction.
- Reduce generic capability names.
- Improve Recognition and future possibility statements.
- Make personal DNA themes more distinctive.
- Maintain evidence grounding.
- Test multiple distinct PM CVs.

---

# 21. Non-Goals

Do not implement the following in this iteration:

- A completely new V3 UI.
- New career categories beyond PM.
- Voice-based refinement.
- Live visual editing.
- Drag-and-drop island editing.
- New onboarding questionnaires.
- CV scoring.
- Job matching.
- Unnecessary confirmation dialogs.
- Complex refinement conversation history.
- Automatic visual redesign after text changes.

---

# 22. Final Acceptance Criteria

The iteration is complete only when:

1. The website retains the original Career DNA Studio identity.
2. The generated map follows the sixth attached reference.
3. A Personal DNA Theme appears cohesively within the main header.
4. All journey platforms use one consistent shape per map.
5. Journey stages visually connect to Shaped My PM DNA.
6. The concluding insight has a proper highlighted design.
7. Recognition and Possibilities to Explore remain available without redundant content.
8. Supporting Evidence is visually consistent with Recognition.
9. Refine My DNA supports text input only.
10. GPT-6 Sol is used for interpreting refinement instructions if supported and configured.
11. Invalid edits are rejected without Yes/No dialogs.
12. Apply Changes provides clear processing feedback.
13. Successful edits update the real map and close the modal.
14. Failed edits preserve input and leave the map unchanged.
15. The modal header and X button remain visible during scrolling.
16. Existing valid map content is preserved across successive refinements.
17. No unrelated visual or functional regressions are introduced.

---

# 23. Codex Execution Instructions

Please inspect the existing codebase before making changes.

Identify:

- The original Career DNA Studio implementation.
- The current map generation pipeline.
- The data schema for CV analysis and generated content.
- The image/map rendering mechanism.
- The Refine My DNA modal implementation.
- The backend/model endpoint currently used for refinement.
- The Recognition and Supporting Evidence components.

Reuse existing components wherever possible.

Create a recoverable checkpoint.

Implement the requested improvements incrementally, following the priorities above.

Do not interpret this specification as authorisation to redesign the entire application.

Do not hardcode example career descriptions from the screenshots into the production output.

After implementation, provide:

1. A concise summary of changed components and files.
2. The model identifier and endpoint actually used for refinement.
3. Any requirements blocked by the current environment.
4. Results of relevant functional and regression tests.
5. Confirmation that the original design and unrelated functionality remain intact.

**Final principle:**

We are not trying to make Career DNA Studio more complicated.

We are trying to make it feel more personal, intelligent, reliable and emotionally meaningful.

The ideal user reaction is:

"I had never quite described myself this way before, but this is exactly the professional I've become."