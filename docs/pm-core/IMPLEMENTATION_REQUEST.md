# Career DNA Studio — Return to Original Version & Refine Core Experience

## 1. Product Direction

We are discontinuing the V2 design direction.

**Return to the original Career DNA Studio experience and improve it incrementally.**

Do not rebuild the product from scratch. Do not use V2 as the new design baseline.

Use the original version as the source of truth for:
- Overall visual identity
- Career DNA Map layout
- Island and pathway design
- Typography, colours and icons
- General page structure and emotional tone

Preserve the original experience wherever possible.

If the original version is available through Git history, an earlier commit, or an existing branch, inspect and restore that baseline before making changes.

Do not overwrite the original implementation without a recoverable backup.

## 2. Product Positioning

Career DNA Studio is designed specifically for people with Product Management experience, particularly Product Managers who are exploring their next career opportunity.

**Target users for this MVP:**
- Product Managers
- Senior Product Managers
- Product Leads
- Product Owners
- Experienced Product Management professionals

Do not expand the scope to engineering, design, operations, consulting, or other career categories in this iteration.

The product is not a resume builder, CV rewriting tool, job-matching platform, or traditional career assessment.

Its purpose is to help people recognise the value of the professional they have become.

Core emotional positioning:

**"A warm embrace from who you've become, to who you are today."**

Supporting brand statement:

"See the person that you have become. Be inspired by who you are."

The experience should feel:
- Warm
- Personal
- Reflective
- Encouraging
- Credible and grounded in real experience
- Thoughtful rather than overly celebratory

Avoid generic motivational statements or excessive AI-generated praise.

## 3. Primary User Journey

### Step 1 — Upload CV

The main entry point should be CV upload.

Assume users already have an existing CV, especially if they are actively job hunting.

Requirements:
- Provide a clear and prominent CV upload entry point.
- Support PDF and DOCX formats.
- Show upload and processing status.
- Allow users to replace their uploaded CV.
- Do not introduce a lengthy questionnaire.
- Do not require users to manually describe their career history before generating their Career DNA.
- Do not permanently store the uploaded CV.
- Process the CV securely and remove temporary files after processing.
- Make no unsupported privacy promises about external AI providers.

Keep the original homepage design and update only the components necessary to support this journey.

### Step 2 — Understand the CV

The AI should first understand the user's experience before generating any visual output.

Extract:
- Career progression
- Product domains
- Core PM capabilities
- Key responsibilities
- Demonstrated contributions
- Evidence of outcomes and impact
- Leadership and collaboration experience
- Repeated strengths across roles
- Transferable capabilities

Do not simply identify keywords and reproduce job descriptions.

The model must distinguish between:
1. What the user has done
2. What the user has demonstrated
3. What professional capability this represents

Only promote a capability when it is reasonably supported by the CV.

Do not invent accomplishments, seniority, metrics, or expertise.

### Step 3 — Generate Career DNA Map

Generate the Career DNA Map using the **original design system and layout**.

The existing map may still require some visual refinement, but visual redesign is not the priority of this iteration.

Focus primarily on the quality, clarity, hierarchy and emotional relevance of the generated content.

#### Recognition

Help users appreciate their professional journey.

Highlight the meaningful qualities demonstrated by their past experiences.

Avoid merely listing previous employers, job titles, projects, or tasks.

#### Self-Discovery / My Product DNA

Extract a maximum of four core PM capability categories.

Fewer than four is acceptable when the evidence does not support four distinct categories.

Each category should represent an elevated, transferable professional capability.

Examples include:
- Product Strategy & Vision
- Platform & Systems Thinking
- AI Product Leadership
- Customer & Product Discovery
- Data-informed Decision Making
- Cross-functional Product Leadership
- Product Execution at Scale
- Risk & Trust Product Thinking
- Growth & Experimentation

These are reference examples, not a fixed list to assign to every user.

Select the categories dynamically based on the individual's actual CV.

Use concise, sophisticated, natural English.

Every capability must be defensible using evidence from the CV.

The top-level category should communicate a professional strength, while the supporting text explains what makes that strength distinctive.

#### Aspiration

Reflect possible directions based on the user's demonstrated strengths.

Avoid prescribing a single career path.

Do not invent qualifications or suggest the user is suitable for senior roles without supporting evidence.

The goal is reflection and inspiration, not automated job matching.

### Step 4 — Explore the Result

Once the map has been generated, let the user explore and read it.

Preserve the existing map's visual style and interaction model.

Do not automatically open a chatbot.

The Career DNA Map remains the main experience.

Introduce a clearly visible but unobtrusive action:

**Refine My DNA**

### Step 5 — Refine My DNA

Only launch the chatbot when the user selects "Refine My DNA".

Do not show the chatbot during the initial CV upload or map generation.

The refinement chatbot should support two paths:

**Option A — Tell us what you'd like to change**

Allow users to provide feedback through:
- Text input
- Voice input with speech-to-text support, where supported

Users can describe what is inaccurate, missing, overemphasised, or poorly worded.

The assistant should interpret natural language instructions and identify the relevant content section.

Examples:
- "I think my strategic product experience is underrepresented."
- "Please make this description sound more senior."
- "This isn't really my strongest skill."
- "I want to highlight more of my AI product experience."
- "Can you make the wording less generic?"

The chatbot may gently suggest:

**"For a more precise update, you can paste the exact sentence you'd like to change."**

This is a helpful suggestion, not a requirement.

Users must be able to request changes without knowing the internal structure of the map.

**Option B — Upload a New CV**

Allow users to upload a replacement CV.

A newly uploaded CV should become the new source of truth.

Because this may significantly change the extracted career identity, the user should be informed that a new analysis and full content generation will occur.

### Step 6 — Update the Existing Map

For text-based refinement:

**Preserve the existing map layout and visual identity.**

Do not regenerate islands, icons, illustration styles, background, or colour themes.

Update only the relevant textual content and associated structured data.

The AI should:
1. Understand the feedback.
2. Locate the affected content block.
3. Review relevant evidence from the CV and current map.
4. Generate improved content.
5. Apply a targeted update.
6. Keep all unrelated content unchanged.

If feedback is ambiguous, ask one targeted follow-up question rather than modifying multiple sections.

Users should be able to refine the content multiple times.

Maintain the latest accepted version of the map within the session.

Use the most recently accepted content as the base for subsequent revisions.

## 4. Clear Editing Boundaries

### Supported

- Rewording descriptions
- Improving capability labels
- Correcting factual inaccuracies
- Adjusting emphasis
- Adding an evidence-supported capability
- Removing an irrelevant capability
- Refining Recognition or Aspiration language
- Replacing the CV and generating a new analysis

### Not Supported Within the Chatbot

- Dragging islands
- Repositioning icons
- Changing island shapes
- Editing background artwork
- Changing map layout
- Changing the design system
- Direct visual editing of individual elements

Text-based editing should not trigger visual regeneration.

If users request a new visual presentation, this should be handled through a separate explicit full-regeneration action, not treated as an ordinary text refinement.

## 5. Content Generation Architecture

Separate the experience into three logical layers.

### Layer A — CV Understanding

Produce a structured representation of the user's professional background with supporting evidence.

### Layer B — Career DNA Generation

Transform the structured professional information into:
- Recognition content
- My Product DNA capability categories
- Supporting descriptions
- Aspiration content

### Layer C — Map Rendering

Render the generated content using the existing original visual design.

Content should be stored separately from layout and visual configuration.

Prefer a stable content schema with section IDs and capability IDs so targeted refinements can safely update the relevant fields.

Refinement should operate primarily on Layer B, using Layer A for factual grounding.

It should not invoke a redesign or full visual regeneration.

For a new CV, rerun Layers A and B and render the output using the same original design system.

## 6. UX and Emotional Tone

The experience should feel like the product is genuinely discovering and recognising the user.

Avoid:
- Generic personality tests
- Long questionnaires
- Job-board language
- Resume scoring
- Empty motivational statements
- Exaggerated AI compliments
- Overly technical explanations of model processing

The interface should be calm, warm and thoughtful.

Do not overwhelm the user with multiple input options simultaneously.

Prioritise one clear action at each stage.

Use concise and natural English throughout the product.

## 7. Implementation Priorities

Implement in this order:

**P0 — Restore the original version**
- Re-establish the original interface and Career DNA Map.
- Remove the V2-only redesign changes.
- Preserve existing functionality wherever possible.

**P1 — Improve CV-based content generation**
- Stronger PM-specific capability abstraction.
- Better distinction between achievements and capabilities.
- More meaningful Recognition and Aspiration content.
- Evidence-grounded output.

**P2 — Introduce the refine experience**
- Refine My DNA entry point.
- On-demand chatbot.
- Text feedback.
- Targeted content updating.
- Replacement CV upload.

**P3 — Improve refinement robustness**
- Voice input where technically supported.
- Multiple consecutive refinements.
- Clear handling of ambiguous feedback.
- Stable content IDs.
- Prevention of unintended layout changes.

**P4 — Polish existing map experience**
- Content readability
- Text fitting
- Visual consistency
- Responsiveness
- Minor UI improvements within the original design language

## 8. Acceptance Criteria

This iteration is successful when:

1. The product visually resembles the original Career DNA Studio version, not V2.
2. A Product Manager can upload a CV and generate a Career DNA Map.
3. The result includes no more than four meaningful, transferable PM capabilities.
4. The output is more insightful than a summary of job titles and projects.
5. Recognition, Self-Discovery and Aspiration are distinguishable in purpose.
6. The chatbot appears only when the user chooses to refine.
7. A user can identify and revise a specific sentence or capability using natural language.
8. Editing text does not regenerate the visual map or change unrelated content.
9. A user can replace the CV and generate a new content result.
10. Uploaded CVs are not permanently retained by the application.
11. The original layout, illustration style and overall brand identity remain consistent.

## 9. Important Final Instruction

**This is a focused product-quality iteration, not a redesign.**

Do not introduce new visual concepts, map styles, career categories, onboarding questionnaires, or unrelated features.

Start by restoring the original version.

Then improve the intelligence and emotional quality of what Career DNA Studio generates.

The goal is for a Product Manager to look at the result and think:

**"I had never quite described myself this way before, but this is exactly the professional I've become."**