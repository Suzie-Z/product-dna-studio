"""V2 typed contracts and source-backed runtime validation, independent of rendering."""

import re, unicodedata
from ai_transport import AppError

DOMAINS = [
    "engineering",
    "technology",
    "product",
    "creative",
    "strategy",
    "leadership",
    "healthcare",
    "education",
    "operations",
    "finance",
    "science",
    "general",
]
CATEGORIES = [
    "domain",
    "transferable",
    "leadership",
    "strategy",
    "technical",
    "commercial",
    "problem_solving",
    "adaptability",
]


def text(n, nullable=False):
    return {"type": ["string", "null"] if nullable else "string", "maxLength": n}


def arr(item, n=5, minimum=0):
    return {"type": "array", "items": item, "minItems": minimum, "maxItems": n}


def obj(props):
    return {
        "type": "object",
        "properties": props,
        "required": list(props),
        "additionalProperties": False,
    }


def enum(values):
    return {"type": "string", "enum": values}


def norm(s):
    return (
        re.sub(
            r"\s+",
            " ",
            unicodedata.normalize("NFKC", s)
            .replace("’", "'")
            .replace("–", "-")
            .replace("—", "-"),
        )
        .strip()
        .casefold()
    )


CONTACT = re.compile(
    r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|(?:https?://|www\.)\S+|(?<!\w)(?:\+?\d[\d ()-]{8,}\d)(?!\w)",
    re.I,
)


def redact(text):
    text = CONTACT.sub("[contact removed]", text)
    return re.sub(
        r"(?im)^\s*(?:address|date of birth|dob|passport|national id|phone|mobile)\s*[:：].*$",
        "[private detail removed]",
        text,
    )


def validate_shape(v, s, path="$"):
    typ = s["type"]
    types = typ if isinstance(typ, list) else [typ]
    if v is None and "null" in types:
        return
    if "string" in types:
        if (
            not isinstance(v, str)
            or len(v) > s.get("maxLength", 10000)
            or not v.strip()
            or re.search(r"[<>\x00-\x08\x0b\x0c\x0e-\x1f]", v)
        ):
            raise ValueError(path + ": invalid text")
    elif typ == "object":
        if not isinstance(v, dict) or set(v) != set(s["properties"]):
            raise ValueError(path + ": invalid fields")
        for k, p in s["properties"].items():
            validate_shape(v[k], p, path + "." + k)
    elif typ == "array":
        if (
            not isinstance(v, list)
            or not s.get("minItems", 0) <= len(v) <= s["maxItems"]
        ):
            raise ValueError(path + ": invalid length")
        for i, x in enumerate(v):
            validate_shape(x, s["items"], path + "[" + str(i) + "]")
    if "enum" in s and v not in s["enum"]:
        raise ValueError(path + ": invalid choice")


def english(v):
    # Proper nouns may be romanized; original-language source quotes stay untouched.
    if CONTACT.search(v) or any(
        c.isalpha() and "LATIN" not in unicodedata.name(c, "") for c in v
    ):
        raise ValueError("English-only public copy required")
    if re.search(r"\b(?:rockstar|visionary|world.class|superhuman)\b", v, re.I):
        raise ValueError("Unsupported promotional language")
    return v


FACT = obj(
    {
        "id": text(16),
        "claim": text(220),
        "kind": enum(
            [
                "responsibility",
                "technical",
                "leadership",
                "collaboration",
                "outcome",
                "achievement",
                "domain",
                "product",
            ]
        ),
        "quote": text(500),
    }
)
STAGE = obj(
    {
        "id": text(16),
        "company": text(90, True),
        "role": text(90),
        "period": text(55, True),
        "kind": enum(["employment", "independent", "education", "career_break"]),
        "domain": enum(DOMAINS),
        "header_quote": text(500),
        "facts": arr(FACT, 8, 1),
        "uncertainty": text(160, True),
    }
)
EXTRACTION = obj(
    {
        "status": enum(["ready", "insufficient"]),
        "stages": arr(STAGE, 12),
        "note": text(200, True),
    }
)


def refs():
    return arr(text(16), 12, 1)


def narrative(n):
    return obj({"text": text(n), "fact_ids": refs()})


ANALYSIS = obj(
    {
        "stage_insights": arr(
            obj(
                {
                    "stage_id": text(16),
                    "capabilities": arr(
                        obj({"label": text(42), "fact_ids": refs()}), 4, 1
                    ),
                    "contribution": narrative(220),
                    "theme": enum(DOMAINS),
                }
            ),
            12,
            1,
        ),
        "identity": narrative(150),
        "core_dna": arr(
            obj(
                {
                    "id": text(16),
                    "title": text(48),
                    "category": enum(CATEGORIES),
                    "explanation": text(230),
                    "fact_ids": refs(),
                }
            ),
            5,
            1,
        ),
        "evolution": narrative(420),
        "recognition": narrative(300),
    }
)


def validate_extraction(data, source):
    validate_shape(data, EXTRACTION)
    ids = set()
    facts = set()
    if data["status"] == "insufficient":
        if data["stages"] or not data["note"]:
            raise ValueError("Invalid insufficient extraction")
        english(data["note"])
        return data
    if not data["stages"]:
        raise ValueError("No career stages")
    for stage in data["stages"]:
        if not re.fullmatch(r"s[1-9]\d?", stage["id"]) or stage["id"] in ids:
            raise ValueError("Duplicate stage")
        ids.add(stage["id"])
        if len(norm(stage["header_quote"])) < 8 or norm(
            stage["header_quote"]
        ) not in norm(source):
            raise ValueError("Stage header not found in CV")
        for key in ["company", "role", "period", "uncertainty"]:
            if stage[key]:
                english(stage[key])
        for fact in stage["facts"]:
            if not re.fullmatch(r"f[1-9]\d{0,2}", fact["id"]) or fact["id"] in facts:
                raise ValueError("Duplicate fact")
            facts.add(fact["id"])
            english(fact["claim"])
            if len(norm(fact["quote"])) < 8 or norm(fact["quote"]) not in norm(source):
                raise ValueError("Fact quote not found in CV")
    if data["note"]:
        english(data["note"])
    return data


def validate_analysis(data, stages):
    validate_shape(data, ANALYSIS)
    facts = {f["id"] for s in stages for f in s["facts"]}
    stage_ids = {s["id"] for s in stages}

    def verify(item):
        r = item["fact_ids"]
        if len(set(r)) != len(r) or not set(r) <= facts:
            raise ValueError("Unsupported evidence reference")
        for k in ["text", "title", "label", "explanation"]:
            if k in item:
                english(item[k])

    if {s["stage_id"] for s in data["stage_insights"]} != stage_ids or len(
        data["stage_insights"]
    ) != len(stages):
        raise ValueError("Stages missing or repeated")
    for insight in data["stage_insights"]:
        local = {
            f["id"]
            for s in stages
            if s["id"] == insight["stage_id"]
            for f in s["facts"]
        }
        verify(insight["contribution"])
        for cap in insight["capabilities"]:
            verify(cap)
            if not set(cap["fact_ids"]) <= local:
                raise ValueError("Stage capability attributed to another stage")
        if not set(insight["contribution"]["fact_ids"]) <= local:
            raise ValueError("Stage contribution attributed to another stage")
    seen = set()
    labels = set()
    for cap in data["core_dna"]:
        verify(cap)
        if cap["id"] in seen or norm(cap["title"]) in labels:
            raise ValueError("Repeated capability")
        seen.add(cap["id"])
        labels.add(norm(cap["title"]))
    for key in ["identity", "evolution", "recognition"]:
        verify(data[key])
    return data
