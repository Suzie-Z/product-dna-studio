"""Synthetic CVs and deterministic transport fixtures. Never used by production."""

import copy, io, json
from docx import Document
from reportlab.pdfgen.canvas import Canvas

PROFILES = {
    "technology": [
        (
            "Northstar Labs",
            "Software Engineer",
            "2017–2020",
            "engineering",
            "Designed service interfaces and investigated reliability failures with engineering partners.",
            "Systems Reliability",
            "Turns failure investigation into dependable technical interfaces.",
        ),
        (
            "Harbour Tools",
            "Platform Product Manager",
            "2020–2023",
            "product",
            "Owned reusable capability requirements and balanced extensibility against implementation cost.",
            "Platform Trade-off Judgement",
            "Balances reusable capability boundaries with delivery constraints.",
        ),
        (
            "Orchid Research",
            "Applied AI Product Manager",
            "2023–present",
            "technology",
            "Built evaluation cases for model boundaries and used failure analysis to set release requirements.",
            "Evidence-led AI Decisions",
            "Uses evaluation cases and model limitations to shape release decisions.",
        ),
    ],
    "education": [
        (
            "Willow School",
            "Classroom Teacher",
            "2018–2021",
            "education",
            "Adapted lesson plans using formative assessment and collaborated with families on learning barriers.",
            "Responsive Learning Design",
            "Adapts learning activities to evidence of individual understanding.",
        ),
        (
            "Willow School",
            "Curriculum Coordinator",
            "2020–2023",
            "education",
            "Coordinated teachers to develop shared assessment rubrics and review inclusive classroom materials.",
            "Collaborative Curriculum Design",
            "Builds shared learning standards while keeping individual needs visible.",
        ),
        (
            "Meadow Library",
            "Learning Programme Designer",
            None,
            "creative",
            "Developed community workshops with librarians and tested accessible materials with adult learners.",
            "Accessible Programme Design",
            "Uses learner feedback to make community learning more accessible.",
        ),
    ],
    "healthcare": [
        (
            "Cedar Hospital",
            "Registered Nurse",
            "2015–2019",
            "healthcare",
            "Followed documented care protocols and coordinated handovers with multidisciplinary clinical teams.",
            "Reliable Care Coordination",
            "Makes shared care information usable across clinical handovers.",
        ),
        (
            "Career break",
            "Family Care Break",
            "2019–2021",
            "general",
            "Paused paid employment for family care between clinical roles.",
            "Professional Adaptability",
            "Navigates a documented transition without assuming uninterrupted progression.",
        ),
        (
            "Oak Clinic",
            "Quality Improvement Coordinator",
            "2021–present",
            "operations",
            "Reviewed handover incidents and co-designed checklist trials with nursing and administrative colleagues.",
            "Practical Quality Improvement",
            "Turns incident patterns into testable changes in care workflows.",
        ),
    ],
    "creative": [
        (
            "Studio Kite",
            "Visual Designer",
            "2019–2022",
            "creative",
            "Tested visual hierarchy with readers and developed accessible print layouts with editorial teams.",
            "Audience-centred Design",
            "Uses reader feedback to clarify visual communication.",
        ),
        (
            "Independent",
            "Design Consultant",
            "2022–present",
            "strategy",
            "Translated client briefs into design criteria and facilitated trade-off reviews with small business owners.",
            "Creative Problem Framing",
            "Turns ambiguous briefs into shared criteria for design decisions.",
        ),
    ],
    "finance": [
        (
            "River Cooperative",
            "Financial Analyst",
            "2018–2020",
            "finance",
            "Compared cash-flow scenarios and documented assumptions for quarterly investment reviews.",
            "Scenario-based Judgement",
            "Makes uncertainty explicit through decision-relevant financial scenarios.",
        ),
        (
            "River Cooperative",
            "Operations Analyst",
            "2020–present",
            "operations",
            "Mapped reconciliation exceptions and worked with operations to test controls before wider adoption.",
            "Operational Control Design",
            "Connects exception patterns with proportionate operational controls.",
        ),
    ],
    "multilingual": [
        (
            "Shan Hai",
            "Researcher",
            None,
            "science",
            "研究实验方法，记录不确定性，并与团队复核分析结果。",
            "Evidence Evaluation",
            "Makes experimental uncertainty visible in collaborative analysis.",
        )
    ],
}


def cv_text(profile="technology"):
    lines = [
        "SYNTHETIC CAREER CV — " + profile,
        "contact@example.test",
        "Phone: +61 400 000 000",
    ]
    for company, role, period, domain, quote, title, explanation in PROFILES[profile]:
        lines += [f"{company} | {role} | {period or 'Period not provided'}", quote]
    return "\n".join(lines)


def pdf_bytes(profile="technology", text=None):
    buffer = io.BytesIO()
    c = Canvas(buffer)
    for i, line in enumerate((text or cv_text(profile)).splitlines()):
        c.drawString(36, 800 - i * 26, line)
    c.save()
    return buffer.getvalue()


def docx_bytes(profile="technology", text=None):
    doc = Document()
    for line in (text or cv_text(profile)).splitlines():
        doc.add_paragraph(line)
    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


def extraction(profile="technology"):
    stages = []
    for i, (company, role, period, domain, quote, title, explanation) in enumerate(
        PROFILES[profile], 1
    ):
        stages.append(
            {
                "id": f"s{i}",
                "company": company,
                "role": role,
                "period": period,
                "kind": "career_break"
                if role == "Family Care Break"
                else "independent"
                if company == "Independent"
                else "employment",
                "domain": domain,
                "header_quote": f"{company} | {role} | {period or 'Period not provided'}",
                "facts": [
                    {
                        "id": f"f{i}",
                        "claim": quote
                        if profile != "multilingual"
                        else "Reviewed experimental uncertainty with the research team.",
                        "kind": "responsibility",
                        "quote": quote,
                    }
                ],
                "uncertainty": "The CV does not provide a period for this chapter."
                if period is None
                else None,
            }
        )
    return {
        "status": "ready",
        "stages": stages,
        "note": "Some roles overlap; the periods have been kept as written."
        if profile == "education"
        else None,
    }


def analysis(profile="technology"):
    rows = PROFILES[profile]
    ids = [f"f{i}" for i in range(1, len(rows) + 1)]
    descriptions = {
        "technology": (
            "Connecting technical reliability, platform judgement and evidence-led AI decisions.",
            "The work shifts from investigating service failures to defining reusable capabilities and evaluating model boundaries. Across these settings, technical evidence informs practical decisions.",
            "A connecting strength is making complex systems easier to judge: interfaces, capability boundaries and release requirements each turn uncertainty into a clearer decision.",
        ),
        "education": (
            "Making learning more accessible through feedback and shared design.",
            "Classroom assessment, shared curriculum work and community workshops each use learner needs to guide design. The later library chapter has no dates, so its chronological position remains uncertain.",
            "Your work connects individual learning barriers with changes other educators can use—a contribution that stretches beyond any single classroom.",
        ),
        "healthcare": (
            "Connecting reliable care coordination with practical quality improvement.",
            "Clinical handovers and later checklist trials both centre on making care information usable across teams. The documented family-care break is a separate chapter, not a claim of linear promotion.",
            "Your experience shows care in the details: shared information and small, tested workflow changes can make collaboration more dependable.",
        ),
        "creative": (
            "Turning audience needs and ambiguous briefs into clear design decisions.",
            "Reader testing and client criteria connect through a consistent practice: making communication decisions explicit enough to review together.",
            "The thread is more than producing visuals: you help people agree what a design needs to accomplish.",
        ),
        "finance": (
            "Connecting financial uncertainty with practical operational controls.",
            "Scenario assumptions and reconciliation exceptions reveal a shared habit of making risks visible before decisions are scaled.",
            "You repeatedly turn uncertainty into something colleagues can examine and test, rather than hide behind a confident-looking answer.",
        ),
        "multilingual": (
            "Making experimental uncertainty visible through collaborative review.",
            "The available chapter connects research methods, uncertainty documentation and team review. There is not enough evidence to describe a broader chronological evolution.",
            "The evidence highlights a careful research habit: documenting what is uncertain so the team can examine it together.",
        ),
    }
    identity, evolution, recognition = descriptions[profile]
    return {
        "stage_insights": [
            {
                "stage_id": f"s{i}",
                "capabilities": [{"label": row[5], "fact_ids": [f"f{i}"]}],
                "contribution": {"text": row[6], "fact_ids": [f"f{i}"]},
                "theme": row[3],
            }
            for i, row in enumerate(rows, 1)
        ],
        "identity": {"text": identity, "fact_ids": ids},
        "core_dna": [
            {
                "id": f"k{i}",
                "title": row[5],
                "category": "problem_solving" if i == 1 else "transferable",
                "explanation": row[6],
                "fact_ids": [f"f{i}"],
            }
            for i, row in enumerate(rows, 1)
        ],
        "evolution": {"text": evolution, "fact_ids": ids},
        "recognition": {"text": recognition, "fact_ids": ids},
    }


def model_transport(path, payload, timeout=90):
    if path == "moderations":
        return {"results": [{"flagged": False}]}
    data = json.loads(payload["input"][-1]["content"])
    if "cv_text" in data:
        profile = next(
            (
                p
                for p in PROFILES
                if "SYNTHETIC CAREER CV" in data["cv_text"]
                and p in data["cv_text"].splitlines()[0]
            ),
            "technology",
        )
        value = extraction(profile)
    else:
        company = data["reviewed_stages"][0]["company"]
        profile = next(
            (p for p, rows in PROFILES.items() if rows[0][0] == company), "technology"
        )
        value = analysis(profile)
    return {
        "status": "completed",
        "model": payload["model"],
        "output": [
            {
                "type": "message",
                "content": [{"type": "output_text", "text": json.dumps(value)}],
            }
        ],
        "usage": {"input_tokens": 100, "output_tokens": 200},
    }


def complete(profile="technology"):
    return {
        "schema_version": "2.0",
        "stages": extraction(profile)["stages"],
        **analysis(profile),
        "review_corrected": False,
    }
