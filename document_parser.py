"""Untrusted documents are parsed in a disposable, resource-limited process."""

import io, multiprocessing, zipfile, xml.etree.ElementTree as ET
from ai_transport import AppError

MAX_BYTES = 5 * 1024 * 1024
MAX_TEXT = 32000


def parse_bytes(data, kind):
    if not data or len(data) > MAX_BYTES:
        raise ValueError("Choose a CV smaller than 5 MB.")
    if kind == "pdf":
        if not data.startswith(b"%PDF-"):
            raise ValueError("This file is not a valid PDF.")
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(data), strict=False)
        if reader.is_encrypted:
            raise ValueError("Upload an unlocked PDF.")
        if not 1 <= len(reader.pages) <= 15:
            raise ValueError("Choose a PDF with 1–15 pages.")
        chunks = []
        for page in reader.pages:
            chunks.append(page.extract_text() or "")
            if sum(map(len, chunks)) > MAX_TEXT:
                raise ValueError("Choose a shorter CV, up to 32,000 characters.")
        text = "\n".join(chunks)
    elif kind == "docx":
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                entries = z.infolist()
                if (
                    len(entries) > 512
                    or sum(x.file_size for x in entries) > 20 * 1024 * 1024
                    or any(
                        x.flag_bits & 1
                        or x.file_size > 8 * 1024 * 1024
                        or x.file_size > max(1, x.compress_size) * 1000
                        for x in entries
                    )
                ):
                    raise ValueError(
                        "This Word file expands beyond the safe reading limit."
                    )
                if (
                    "[Content_Types].xml" not in z.namelist()
                    or "word/document.xml" not in z.namelist()
                ):
                    raise ValueError("This file is not a valid DOCX.")
                chunks = []
                names = ["word/document.xml"] + sorted(
                    n
                    for n in z.namelist()
                    if n.startswith(("word/header", "word/footer"))
                    and n.endswith(".xml")
                )
                for name in names:
                    xml = z.read(name)
                    if (
                        b"\x00" in xml
                        or b"<!DOCTYPE" in xml.upper()
                        or b"<!ENTITY" in xml.upper()
                    ):
                        raise ValueError("This Word file contains unsupported XML.")
                    root = ET.fromstring(xml)
                    for para in root.iter(
                        "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"
                    ):
                        chunks.append(
                            " ".join(
                                x.text or ""
                                for x in para.iter(
                                    "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"
                                )
                            )
                        )
                text = "\n".join(chunks)
        except (zipfile.BadZipFile, KeyError, ET.ParseError):
            raise ValueError("This file is not a readable DOCX.") from None
    else:
        raise ValueError("Choose a PDF or DOCX file.")
    text = text.replace("\x00", "").strip()
    if len(text) > MAX_TEXT:
        raise ValueError("Choose a shorter CV, up to 32,000 characters.")
    if len(text) < 40 or sum(ch.isalpha() for ch in text) < 25:
        raise ValueError(
            "We could not find enough readable text. For a scanned PDF, run OCR and upload it again."
        )
    return text


def _worker(pipe, data, kind):
    try:
        import resource, logging

        resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
        resource.setrlimit(resource.RLIMIT_CPU, (8, 8))
        logging.disable(logging.CRITICAL)
        pipe.send({"text": parse_bytes(data, kind)})
    except ValueError as e:
        pipe.send({"error": str(e)})
    except Exception:
        pipe.send(
            {
                "error": "This CV could not be read safely. Try a fresh PDF or DOCX export."
            }
        )
    finally:
        pipe.close()


def parse_document(data, kind):
    if kind not in ("pdf", "docx"):
        raise AppError(415, "Choose a PDF or DOCX file.", "file_type")
    if not data or len(data) > MAX_BYTES:
        raise AppError(413, "Choose a CV smaller than 5 MB.", "file_size")
    ctx = multiprocessing.get_context("spawn")
    parent, child = ctx.Pipe(duplex=False)
    process = ctx.Process(target=_worker, args=(child, data, kind), daemon=True)
    process.start()
    child.close()
    try:
        if not parent.poll(12):
            raise AppError(
                422,
                "Reading this file took too long. Try a simpler PDF or DOCX export.",
                "parser_timeout",
            )
        try:
            result = parent.recv()
        except EOFError:
            raise AppError(
                422,
                "This file exceeded safe reading limits. Try a simpler export.",
                "parser_limit",
            ) from None
        if "error" in result:
            raise AppError(422, result["error"], "unreadable_cv")
        return result["text"]
    finally:
        parent.close()
        process.join(0.1)
        if process.is_alive():
            process.terminate()
            process.join(1)
