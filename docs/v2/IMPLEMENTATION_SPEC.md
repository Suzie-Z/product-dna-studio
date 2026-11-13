# Career DNA V2
## Complete Product Redesign & Engineering Rebuild Specification

### Instructions for Codex

You are responsible for comprehensively rebuilding the existing Career DNA application into a focused, stable, visually distinctive, AI-powered career reflection experience.

**Work within the existing repository. Do not create a separate project or application.**

This is a major product and architectural rebuild, not a collection of incremental UI fixes.

You are authorised to redesign the existing pages, replace poorly structured components, simplify the architecture, remove obsolete features, and rewrite the core workflow.

However, preserve the original repository, existing production deployment, brand identity, and valuable design assets.

Create a dedicated Git branch for the rebuild. Do not directly overwrite the existing working version or deploy V2 to production without approval.

The new implementation should become the replacement for the current Career DNA experience once validated.

---

# PART 1: PRODUCT VISION

## 1.1 What Is Career DNA?

Career DNA is an AI-powered professional self-discovery experience.

Its purpose is to help people rediscover the value of their professional journey, understand the strengths they have developed, and feel inspired by how their experiences have shaped them.

**Career DNA is NOT:**

- A resume builder.
- A resume rewriting tool.
- A LinkedIn profile generator.
- A job matching platform.
- A traditional career assessment.
- A generic AI motivational tool.

It should not simply reformat a CV or produce a list of professional skills.

Instead, Career DNA must help users view their entire professional journey from a higher perspective.

### Core Product Promise

**Discover the strengths behind your story.**

### The Three Desired Outcomes

**Clarity**

Help users understand how their seemingly separate career experiences connect.

**Recognition**

Help users recognise capabilities and achievements they may have overlooked.

**Inspiration**

Help users feel genuinely proud of their development and more confident about their future.

The product should create an experience of personal recognition rather than simply generating a professional report.

---

# PART 2: USER EXPERIENCE AND MVP SCOPE

## 2.1 Simplify the Entire User Journey

The MVP should follow one clear workflow:

**Upload CV → Extract Experience → Generate Career Intelligence → Visualise Career Journey → Reveal My Career DNA**

No complicated onboarding.

No unnecessary questionnaires.

No multiple input modes.

No additional features that distract from the core experience.

## 2.2 One Input Method Only

The homepage should provide only one primary input:

**Upload Your CV**

Supported formats:

- PDF
- DOCX

Remove the following from the V2 interface and associated application logic:

- LinkedIn profile input.
- LinkedIn URL import.
- Manual career history input.
- Long free-text input.
- Multiple alternative onboarding modes.
- Unnecessary input configuration.

Do not merely hide these features while retaining their obsolete state management and dependencies.

Safely remove obsolete code after confirming it is not required elsewhere.

The upload experience should support drag-and-drop, file selection, validation, clear loading states, and retry behaviour.

## 2.3 Lightweight Review

After parsing the CV, the system may present a simple review of extracted career information.

Display:

- Company.
- Role.
- Employment period.
- Career stage order.

Allow users to correct material extraction errors.

Do not create a complicated form.

Where extraction confidence is high, keep the review lightweight and allow users to continue immediately.

---

# PART 3: CAREER INTELLIGENCE ENGINE

## 3.1 Highest Priority

**The quality of career analysis is the single most important feature of this application.**

Visual design must amplify meaningful insight, not compensate for superficial analysis.

The AI should transform individual career experiences into evidence-backed, higher-order professional capabilities.

The output must resemble the level of professional self-awareness found in thoughtfully written senior professional profiles, without copying LinkedIn language or relying on generic corporate jargon.

Build the analysis in three layers.

## 3.2 Layer One: Experience Extraction

Identify factual information from the uploaded CV:

- Companies and organisations.
- Job titles.
- Employment periods.
- Industries and domains.
- Products and services.
- Responsibilities.
- Technical expertise.
- Leadership responsibilities.
- Cross-functional collaboration.
- Business outcomes.
- Measurable achievements.

Maintain traceability to the source CV.

Do not invent information.

If dates or information are missing, handle uncertainty explicitly.

## 3.3 Layer Two: Capability Synthesis

Move beyond individual activities and identify the professional capabilities they demonstrate.

For example:

| Individual Experience | Higher-Order Capability |
|---|---|
| Developed messaging safety features | Trust & Safety Product Leadership |
| Collaborated closely with engineering | Technical Product Leadership |
| Introduced AI-powered tools | Applied AI & Product Innovation |
| Managed international stakeholders | Global Cross-functional Leadership |
| Improved performance through experimentation | Data-driven Product Strategy |
| Led major cross-team initiatives | Strategic Execution & Organisational Influence |

These examples are illustrative and must not be hardcoded as the only possible outputs.

The system must support multiple professions and industries.

Identify recurring capabilities across career stages.

Distinguish between:

- Domain expertise.
- Transferable capabilities.
- Leadership maturity.
- Strategic thinking.
- Technical understanding.
- Commercial impact.
- Problem-solving patterns.
- Professional adaptability.

Focus on the capabilities a person has accumulated, rather than merely listing what they have done.

### Avoid Generic AI Summaries

Unacceptable:

"You are a highly skilled, innovative and passionate professional."

Better:

"Across different roles, you have repeatedly bridged technical complexity and practical business outcomes, developing a distinctive ability to translate emerging technologies into scalable products."

But only generate such a statement when the CV provides supporting evidence.

## 3.4 Layer Three: Career Pattern Recognition

Analyse how the user's professional journey has evolved.

Identify patterns such as:

- Increasing responsibility.
- Development of strategic leadership.
- Growing technical or domain depth.
- Transition across industries.
- Recurring problem-solving strengths.
- Connections between different career chapters.
- Distinctive combinations of expertise.
- Evolution from hands-on delivery to broader influence, where supported.

Do not assume every career follows a linear promotion path.

Career changes, lateral moves, entrepreneurial work, and multidisciplinary experience may also represent meaningful development.

The analysis should help users recognise a coherent story behind their experiences.

## 3.5 Layer Four: Personalised Career Reflection

Translate the analysis into a concise, emotionally intelligent reflection.

The tone should be:

- Warm.
- Thoughtful.
- Encouraging.
- Insightful.
- Professional.
- Grounded in actual experience.

Avoid excessive praise and generic motivational language.

The objective is for the user to feel:

"I hadn't realised these experiences were connected."

And:

"I have developed more valuable strengths than I previously recognised."

### Narrative Quality

The reflection should be personalised enough that it would not naturally apply to hundreds of unrelated CVs.

A strong reflection should reference meaningful patterns rather than repeat job titles.

Do not invent achievements, seniority, or future career potential as established facts.

---

# PART 4: AI OUTPUT STRUCTURE

Build a stable, validated, structured output schema.

The AI analysis should produce:

## A. Career Stages

For each significant career chapter:

- Company.
- Role.
- Period.
- Professional domain.
- Up to four higher-order capability labels.
- Short explanation of what this stage contributed.
- Supporting CV evidence.
- Suggested visual theme.

## B. Overall Professional Identity

One concise positioning statement describing the user's distinctive professional identity.

This should synthesise the entire career, not simply repeat their most recent title.

## C. Core Career DNA

Identify approximately three to five defining professional capabilities.

Each should include:

- A concise title.
- A meaningful explanation.
- Supporting evidence from the career history.

Avoid duplicates and overlapping concepts.

## D. Career Evolution

A short narrative explaining how the user's capabilities developed across different career stages.

## E. Personal Recognition

An uplifting, evidence-grounded conclusion that helps the user recognise the value of their journey.

### Technical Requirements

Use a structured JSON schema with runtime validation.

Keep AI content generation independent from frontend rendering.

Support graceful handling of incomplete or invalid responses.

Do not rely on brittle string parsing of unstructured model responses.

---

# PART 5: THREE-SCREEN PRODUCT DESIGN

## Screen 1: Discover Your Career DNA

### Purpose

Create a welcoming, minimal entry into professional self-discovery.

### Content

Main title:

**Discover Your Career DNA**

Supporting statement:

"Your journey has shaped who you are today. Discover the strengths behind your story."

Primary action:

**Upload Your CV**

### Design

- Premium and minimal.
- Calm, welcoming colour palette.
- Clear central alignment.
- Elegant typography.
- One obvious primary action.
- No unnecessary UI elements.
- Fully responsive.

Do not overwhelm users with instructions or decorative content.

Provide a concise privacy statement regarding document handling.

---

## Screen 2: Your Career Journey

### Purpose

Visualise the user's professional evolution as a memorable and meaningful journey.

The core concept is a connected world of distinctive floating islands.

Each island represents a career chapter.

The user should visually understand how their professional journey developed over time.

### Information Display

Each island should show:

- Company or career stage.
- Job title.
- Employment period.
- Up to four higher-order capability labels.

Supporting details may be expandable.

Do not overcrowd the islands with text.

Do not simply display lists of projects or raw CV responsibilities.

### Narrative

Each island should communicate how a particular career stage contributed to the user's accumulated strengths.

The overall journey should feel connected and purposeful.

---

# PART 6: CRITICAL VISUAL REQUIREMENT

## ONE WORLD, DISTINCT ISLANDS

**This requirement is essential and must be implemented correctly.**

Visual consistency does NOT mean using one identical island template and repeatedly changing its colour or icons.

Every island must belong to one cohesive artistic universe, while having its own distinctive visual identity.

Imagine different locations within the same beautifully designed animated world.

They share an artistic language, but not identical geography, architecture, composition, or silhouette.

### 6.1 What Must Remain Consistent

All islands should share:

- The same illustration style.
- The same isometric camera perspective.
- Compatible 3D depth and proportions.
- Consistent lighting direction.
- Similar shadow treatment.
- Consistent material rendering.
- Compatible surface textures.
- Harmonious colour treatment.
- Consistent illustration quality.
- Cohesive visual sophistication.

Preferred overall direction:

**Soft 3D / Isometric / Whimsical Miniature Worlds**

The visual environment should feel warm, imaginative, premium, and polished.

### 6.2 What Must Be Different

Individual islands should meaningfully vary in:

- Shape and silhouette.
- Terrain and elevation.
- Architectural structures.
- Landscape features.
- Spatial composition.
- Professional objects and symbols.
- Environmental elements.
- Colour palette.
- Pathways and bridges.
- Decorative details.

**Do not create visual variety merely by recolouring identical assets.**

### 6.3 Professional Visual Themes

Examples include:

**Engineering**

Mechanical architecture, systems, technical structures, industrial environments.

**AI & Technology**

Futuristic laboratories, intelligent networks, connected structures.

**Product Management**

Connected platforms, modular environments, bridges between different systems.

**Creative & Design**

Art studios, imaginative architecture, gardens, creative structures.

**Consulting & Strategy**

Strategic environments, observatories, elevated viewpoints.

**Leadership**

Interconnected communities, towers, gathering spaces, structures symbolising influence and coordination.

These examples are starting points, not fixed templates.

The visual engine should adapt to different career domains.

Avoid stereotypes and repetitive symbolism.

### 6.4 Visual Composition Standards

- Every island must be fully visible.
- Avoid cropped clouds and cut-off decorative elements.
- Maintain balanced spacing.
- Keep each island visually distinct.
- Maintain logical pathway connections.
- Ensure career labels remain readable.
- Avoid visual overlap.
- Preserve proper alignment and scaling.
- Support desktop and mobile layouts.

No island should look like an accidental duplicate of another.

### 6.5 Visual Asset Strategy

Do not require a huge library of manually pre-generated island images.

Implement a modular visual system capable of dynamically mapping career themes to suitable visual components.

The architecture should support future AI image generation.

For the MVP, use reliable assets and frontend composition where appropriate.

If the existing rendering method cannot achieve distinct island structures while maintaining consistent artistic quality, explain the limitation and implement a more suitable approach.

**Do not pretend CSS colour changes or icon substitutions satisfy the island diversity requirement.**

---

# PART 7: MY CAREER DNA PAGE

## 7.1 Purpose

This is the emotional and intellectual destination of the experience.

The page should synthesise the user's entire professional journey into a clear, distinctive professional identity.

## 7.2 Page Structure

### A. Professional Identity

A short, insightful description of the user's professional positioning.

### B. My Core Career DNA

Three to five meaningful core strengths.

Each strength should be concise, evidence-backed, and clearly differentiated.

### C. The Story Behind My Strengths

A brief reflection showing how the strengths emerged across different career chapters.

### D. A Moment of Recognition

A thoughtful closing statement recognising the value of the user's journey.

Avoid long generic motivational paragraphs.

Keep the presentation emotionally resonant but elegant.

## 7.3 Visual Direction

- Continue the same artistic universe as the Career Journey.
- Use consistent typography and colours.
- Centre the main title and DNA visual identity.
- Maintain balanced spacing between the title and central visual.
- Use strong visual hierarchy.
- Avoid unnecessary decorations.
- Ensure the page looks polished on mobile and desktop.

Make the result suitable for saving, reviewing, or sharing in a later product iteration.

---

# PART 8: VISUAL GENERATION ARCHITECTURE

Separate visual decisions from visual rendering.

### Career Intelligence Engine

Determines:

- Professional domains.
- Career-stage themes.
- Capability labels.
- Meaningful narrative elements.

### Visual Design Engine

Maps the structured career data to:

- Island types.
- Environmental structures.
- Colours.
- Professional symbols.
- Visual motifs.
- Pathway composition.

### Frontend Renderer

Handles:

- Text.
- Layout.
- Responsive behaviour.
- Navigation.
- Interactions.
- Labels.
- Positioning.
- Animation.

### Optional Image Generation

Design the architecture so that a dedicated image-generation model may be added later for personalised island artwork.

Do not require real-time image generation to complete the MVP.

Do not place editable text, labels, or interactive components inside generated image assets.

Prioritise consistency, visual distinctiveness, and performance.

---

# PART 9: ENGINEERING REBUILD

## 9.1 Audit Before Rewriting

Inspect the current codebase and identify:

- Obsolete features.
- Fragile state management.
- Coupled components.
- Duplicate functionality.
- Unnecessary dependencies.
- Existing rendering bugs.
- Parsing issues.
- AI integration problems.
- Reusable visual components.

Do not assume the existing architecture is worth preserving.

## 9.2 Rebuild the Core Modules

Create clean separation between:

1. CV Upload & Parsing.
2. Career Experience Extraction.
3. Career Intelligence Analysis.
4. Structured Career Data.
5. Visual Design Mapping.
6. Career Journey Rendering.
7. My Career DNA Rendering.
8. Validation and Error Handling.

Prefer straightforward, maintainable code over unnecessary abstractions.

## 9.3 Remove Old Complexity

Remove obsolete multi-input workflows and associated dependencies.

Do not maintain two competing application architectures.

Do not introduce new features beyond the defined MVP.

## 9.4 Security

Uploaded CVs contain personal information.

Ensure:

- Secure file processing.
- No exposure of API keys.
- No unnecessary retention of CV documents.
- No sensitive information in application logs.
- Clear data handling rules.
- Safe handling of untrusted document contents.

---

# PART 10: TESTING AND QUALITY ASSURANCE

The new V2 must have reliable automated tests.

Test:

- PDF uploads.
- DOCX uploads.
- Invalid files.
- Missing data.
- Unreadable CVs.
- Multiple jobs at the same company.
- Career breaks.
- Overlapping employment periods.
- Career changes across industries.
- Capability synthesis.
- Evidence attribution.
- Invalid AI responses.
- Loading and retry states.
- Duplicate requests.
- Desktop responsiveness.
- Mobile responsiveness.
- Island layout and overflow.
- Broken visual assets.
- Complete end-to-end user journeys.

Use multiple synthetic CVs across different professions.

Do not optimise only for Product Management.

### AI Quality Testing

Evaluate whether generated outputs are:

- Evidence-based.
- Professionally credible.
- Distinctive.
- Insightful.
- Concise.
- Emotionally appropriate.
- Free of generic corporate buzzwords.

Include a check that each important capability claim is supported by CV evidence.

### Visual Quality Testing

Test whether:

- Islands belong to one artistic universe.
- Islands have genuinely different silhouettes and compositions.
- Colours remain harmonious.
- Visual objects are not cropped.
- Labels are readable.
- All layouts are responsive.

---

# PART 11: MVP SUCCESS CRITERIA

Career DNA V2 is ready when:

1. A user can upload a CV with minimal friction.
2. The CV is accurately parsed.
3. AI identifies meaningful higher-order capabilities.
4. The generated narrative reveals patterns across the user's career.
5. The Career Journey accurately represents career stages.
6. Each island is visually distinctive yet stylistically consistent.
7. My Career DNA feels personal, credible, and encouraging.
8. The application works reliably without recurring critical bugs.
9. The complete experience works on desktop and mobile.
10. The user can understand their professional identity more clearly after completing the journey.

The product should prioritise:

**Career Intelligence Quality > Career Clarity > Emotional Resonance > Visual Quality > Additional Features**

---

# PART 12: IMPLEMENTATION PLAN

Implement the rebuild in the following order.

### Phase 1: Repository Audit

Review the existing implementation and identify technical debt, reusable components, and required changes.

### Phase 2: Clean V2 Architecture

Create the new application structure within the existing repository.

Simplify the input workflow.

### Phase 3: Career Intelligence Engine

Implement experience extraction, capability synthesis, career pattern recognition, and personalised narrative generation.

### Phase 4: Core UI

Implement the upload screen and the structured analysis flow.

### Phase 5: Career Journey Visualisation

Implement the connected island experience using the one-world, distinct-islands design principle.

### Phase 6: My Career DNA

Implement the professional identity, core capabilities, career narrative, and recognition sections.

### Phase 7: QA and Stabilisation

Run comprehensive automated tests, visual reviews, and regression testing.

Fix identified issues before considering the rebuild complete.

---

# PART 13: CODEx EXECUTION DIRECTIVE

Please begin implementing this rebuild in the existing repository.

Do not create an unrelated new application.

Do not continue patching V1 incrementally.

Treat this specification as the new product and architecture baseline.

You may replace existing pages and components where necessary.

Preserve useful assets and validated design patterns.

Start by examining the existing repository and creating a safe V2 working branch.

Then proceed through the implementation stages.

Use sensible technical defaults, maintain clean code, and run tests throughout.

Do not repeatedly interrupt implementation for minor design decisions.

Only request input when a decision has material consequences for product scope, security, deployment, or irreversible data changes.

After implementation, provide:

1. A summary of the architectural changes.
2. The main components replaced or retained.
3. A description of the new AI Career Intelligence pipeline.
4. Screenshots of all three screens.
5. Screenshots demonstrating at least three visually distinct islands in one consistent artistic style.
6. Automated test results.
7. Known limitations.
8. Instructions for local testing and preview.

Do not claim completion for functionality that has not been implemented or verified.

Do not deploy to production without approval.

## FINAL PRODUCT PRINCIPLE

**One simple input. One meaningful journey. One distinctive Career DNA.**

Career DNA should not merely tell people what they have done.

It should help them recognise what their experiences have made them capable of becoming.

Build an experience that transforms professional history into clarity, recognition, and inspiration.