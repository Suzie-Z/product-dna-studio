# Career DNA Studio — Targeted UI & Content Refinements

## Objective

Please implement the following five improvements in the existing Career DNA Studio application.

This is an incremental refinement, not a redesign.

Preserve the existing visual identity, pastel colour palette, 3D illustrations, typography, page structure and all working functionality.

Use the five attached screenshots to identify the specific issues.

Do not modify unrelated components.

---

## 1. Privacy & Data — Consolidate Content and Remove Technical Details

**Reference: Attachment 2**

### Current Issues

The Privacy & Data section contains two blocks of information that partially overlap.

The second block is currently placed under a separate expandable section called "Technical details".

This creates unnecessary repetition and makes the privacy explanation feel overly technical.

### Required Changes

1. Merge the two privacy explanations into a single coherent paragraph.
2. Remove the "Technical details" heading, chevron and expandable section entirely.
3. Keep one "Privacy & Data" expandable section.
4. Keep the Privacy & Data trigger right-aligned.
5. Keep the section collapsed by default.
6. When expanded, display the consolidated explanation directly within the page, not in a modal or popup.
7. Preserve material disclosures about processing, temporary retention, anonymous counters and OpenAI.

### Suggested Copy

"Your CV is read in your browser and isn't saved by this app. Extracted text and your instructions are processed by our service and OpenAI to create and refine your DNA. Temporary results may remain in memory for up to 10 minutes. We retain aggregate usage counts and short-lived technical records for security and deduplication. OpenAI's processing and retention policies also apply."

Please verify this wording against the actual implementation before publishing.

If additional technical or retention details are necessary for accuracy, incorporate them concisely into the same paragraph rather than introducing another expandable subsection.

### Acceptance Criteria

- Only one Privacy & Data section exists.
- No Technical details subsection remains.
- The explanation is concise and non-repetitive.
- The disclosure remains accurate.
- The section works correctly on desktop and mobile.

---

## 2. Career DNA Header — Simplify the Title Area

**Reference: Attachment 3**

### Current Issues

The header currently contains:

- PM logo.
- PM Career Studio branding.
- My PM Career DNA title.
- A generated personal DNA theme on the right.

The right-side theme makes the header visually crowded.

The PM Career Studio branding is also too prominent and wraps onto two lines.

### Required Changes

#### 2.1 Remove the Right-Side Theme

Remove the generated theme pill from the far right of the header.

Example to remove:

"AI Experiences, Evaluation and Guardrails"

Do not replace it with another summary or explanatory label in the header.

This is a presentation-only change.

Do not delete the generated theme from the underlying content schema if it is required elsewhere.

#### 2.2 Adjust PM Career Studio Branding

Keep the PM logo on the left.

Place the text:

**PM Career Studio**

Immediately beside the logo.

Requirements:

- Display the text on one line.
- No wrapping.
- Use a smaller font size.
- Use a muted lavender or soft grey colour.
- Reduce opacity or visual prominence so it feels like a subtle watermark.
- Maintain comfortable spacing between the logo and text.

The branding should be visible but not compete with the main title.

#### 2.3 Main Title Alignment

Keep:

**My PM Career DNA**

Visually centred within the entire header, not merely centred in the remaining space after the logo.

The title should remain the strongest visual element.

Preserve the existing decorative underline if it fits the simplified composition.

### Acceptance Criteria

- The right-side generated theme is removed.
- PM Career Studio appears on one line beside the logo.
- Brand text has a subtle watermark-like appearance.
- The main title is properly centred.
- No text overlaps or wraps awkwardly.

---

## 3. My PM Journey — Content Prioritisation and Layout Improvements

**Reference: Attachment 1**

### 3.1 Fix Icon and Text Overlap

The decorative elements marked as issues 1 and 2 in the screenshot overlap or sit too close to journey text.

This includes role icons and additional PM-related decorative illustrations.

### Required Changes

- Ensure all icons remain inside their intended visual areas.
- Prevent icons from overlapping role titles and descriptions.
- Do not place decorative elements on top of text.
- Keep a consistent minimum spacing between icons, headings and descriptions.
- Adjust icon positioning dynamically according to the number of journey stages.
- Keep decorative elements secondary to readability.

Do not remove all PM-related illustrations. Reposition or resize them intelligently.

### 3.2 Prioritise Product Management Experience

The journey currently sometimes gives prominent space to non-PM roles.

For this MVP, the primary focus is Product Management.

**Prefer PM-related roles and experiences whenever enough relevant evidence is available.**

Examples of preferred experience categories:

- Product Management
- AI Product Management
- Platform Product Management
- Growth Product Management
- Trust & Safety Product Management
- Enterprise Product Management

Only include non-PM roles when there are insufficient relevant PM experiences or when an earlier role contributes materially to understanding the person's professional development.

Do not fabricate PM experience or relabel a genuinely non-PM role as a PM role.

### 3.3 Improve Journey Stage Prioritisation

The displayed journey stages should be selected based on the CV, rather than following a fixed list.

Prioritise experiences using the following signals:

**Primary — CV Coverage and Depth**

Experiences that receive more detailed coverage in the CV should generally receive higher priority.

Consider:

- Amount of relevant content.
- Number of responsibilities or achievements described.
- Depth of product ownership.
- Specificity of contributions.
- Strength of supporting evidence.

**Secondary — PM Relevance**

Prioritise experiences that demonstrate meaningful Product Management capabilities.

**Additional — Recency**

Give additional weight to more recent experiences when their relevance and supporting evidence are comparable.

**Additional — Recurring Themes**

Identify recurring strengths and frequently discussed capabilities across the CV.

Use these as evidence of professional identity rather than simply counting keywords.

### Important

These signals should inform a balanced selection, not a rigid formula.

Do not always display the most recent role first if it contributes little to the person's broader Product DNA.

Preserve the actual chronological order of selected career stages where the visual journey represents career progression.

Do not invent additional stages simply to fill the layout.

### 3.4 Reduce Excessive Text Spacing

The supporting descriptions below the journey titles currently have too much vertical spacing.

Requirements:

- Reduce unnecessary line gaps.
- Use consistent line-height.
- Group each role title and its supporting descriptions more closely.
- Maintain enough separation between different journey stages.
- Preserve readability at smaller screen sizes.

The goal is a more compact, visually balanced journey section without making the text cramped.

### Acceptance Criteria

- No icon overlaps any journey text.
- PM experience is prioritised.
- Stage selection reflects CV depth, evidence, relevance and recency.
- Non-PM roles are only included when justified.
- Text spacing is tighter and more consistent.
- Journey layout remains visually balanced.

---

## 4. Shaped My PM DNA — Improve Capability Card Spacing

**Reference: Attachment 4**

### Current Issue

The capability card content looks crowded.

In particular, the supporting skill/evidence area at the bottom of each card sits too close to the description above.

The visual separation between the descriptive sentence and the evidence tag container is insufficient.

### Required Changes

#### 4.1 Improve Internal Card Spacing

Each capability card should have a clear visual hierarchy:

1. Icon
2. Capability title
3. Supporting description
4. Evidence/skill container

Increase the spacing between the supporting description and the bottom evidence container.

Do not allow the two sections to visually collide.

Maintain consistent spacing across all cards, even when the descriptions have different lengths.

#### 4.2 Improve Evidence Container Layout

The bottom evidence container should:

- Have sufficient internal padding.
- Maintain comfortable spacing from the card edges.
- Avoid text touching its border.
- Avoid excessive crowding between evidence items.
- Use consistent typography and alignment across cards.

If evidence strings are long, allow controlled wrapping.

Do not truncate meaningful content unnecessarily.

#### 4.3 Improve Section-Level Spacing

Ensure there is comfortable vertical separation between the My PM Journey section, the central Shaped My PM DNA transition and the capability cards.

Avoid the appearance of one section pressing against another.

Preserve the visual flow from the journey into the DNA capabilities.

#### 4.4 Preserve the Design System

Do not redesign the cards.

Keep:

- Rounded card shapes.
- Soft pastel backgrounds.
- Existing 3D icons.
- Main typography.
- Current overall card structure.

This is a spacing and readability improvement.

### Acceptance Criteria

- Card descriptions and evidence containers do not collide.
- All evidence text remains readable.
- Card internal padding is consistent.
- Cards are visually balanced despite differing content lengths.
- The Journey and DNA sections have appropriate breathing room.

---

## 5. Refine My DNA — Remove Duplicate Loading Messages

**Reference: Attachment 5**

### Current Issue

During Apply Changes, the interface displays the same status multiple times.

For example:

- The button displays "Applying your changes..."
- A loading section repeats "Applying your changes..."
- Another line below repeats "Applying your changes..." again.

This feels redundant and makes the interface unnecessarily busy.

### Required Changes

Show only one primary loading status.

Preferred loading UI:

**Spinner icon**

**Applying your changes...**

"This may take around 20–30 seconds."

Use one compact loading indicator and one concise status message.

The 20–30 second duration is an estimate, not a guaranteed completion time.

### Button Behaviour

While processing:

- Disable Apply Changes.
- Prevent multiple submissions.
- Show a spinner or disabled button state.
- Do not repeat the loading message in multiple places.

The button may show a spinner without repeating the full status text.

### Remove Redundant Status

Remove the additional text-only loading message highlighted in red in Attachment 5.

Do not show separate duplicate status messages below the loading component.

### Preserve Existing Refine Behaviour

The existing successful refinement flow should remain:

1. User enters a text instruction.
2. User clicks Apply Changes.
3. The system displays one loading state.
4. The requested text change is applied.
5. The modal closes automatically after success.
6. The updated DNA Map becomes visible.

On failure:

- Keep the modal open.
- Preserve user input.
- Stop the loading state.
- Show one clear error message.
- Allow the user to retry.

Do not reintroduce clarification popups, Yes/No dialogs or visible conversation history.

### Acceptance Criteria

- Only one clear loading message appears.
- A spinner indicates active processing.
- No duplicate status text remains.
- Duplicate submissions are prevented.
- Success and failure behaviour remains unchanged.
- No regression in Refine My DNA functionality.

---

# 6. Implementation Boundaries

This iteration should only address the five areas described above.

Do not:

- Rebuild the application.
- Introduce a new visual system.
- Redesign the Career DNA Map.
- Change the CV upload workflow.
- Change the existing model configuration.
- Replace the map generation architecture.
- Hardcode sample career content.
- Change the download functionality.
- Modify existing working expand/collapse sections other than Privacy & Data.
- Reintroduce voice input or conversational confirmation flows.

Preserve existing data structures and API contracts unless a minimal change is necessary for the requested functionality.

---

# 7. Regression Testing

Before completion, verify:

### Privacy
- Single privacy explanation.
- No Technical details.
- Accurate data handling disclosures.
- Right-aligned, functional Privacy & Data control.

### Header
- Right-side theme removed.
- PM Career Studio is subtle and single-line.
- Main title remains centred.

### Journey
- Icons do not overlap text.
- PM roles take priority.
- CV evidence drives selection.
- Role descriptions have consistent spacing.

### DNA Cards
- Description and evidence areas are clearly separated.
- Evidence items fit.
- No clipping or overflow.
- Section spacing is balanced.

### Refine
- Exactly one loading state.
- No redundant status text.
- No duplicate requests.
- Successful updates remain functional.
- Failed updates preserve user input.

Test desktop and mobile layouts.

---

# 8. Expected Delivery from Codex

After implementing the changes, please provide:

1. A concise summary of changes.
2. A list of modified files.
3. Screenshots of the updated Header, Journey and DNA capability cards.
4. A screenshot of the simplified Privacy & Data section.
5. A screenshot of the Refine loading state.
6. Results of relevant regression tests.
7. Any unresolved issues or limitations.

**Final instruction:**

Focus on improving visual consistency, content relevance and UI clarity.

Make targeted changes only.

Preserve the warm, playful and professional visual identity of Career DNA Studio while making the overall experience cleaner, more polished and reliable.