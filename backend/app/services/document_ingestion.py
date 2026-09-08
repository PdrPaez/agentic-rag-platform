from dataclasses import dataclass
from io import BytesIO
from pathlib import PurePath

from pypdf import PdfReader

from app.rag.chunking import split_text

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}


class DocumentIngestionError(ValueError):
    """Raised when an uploaded document cannot be safely ingested."""


@dataclass(frozen=True)
class ExtractedDocument:
    name: str
    source_type: str
    text: str
    chunks: list[str]


def ingest_document(
    filename: str,
    content: bytes,
    *,
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> ExtractedDocument:
    extension = PurePath(filename).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise DocumentIngestionError("Unsupported document type. Use .txt, .md, or .pdf")
    if not content:
        raise DocumentIngestionError("The document is empty")

    try:
        text = _extract_text(extension, content)
    except Exception as exc:
        raise DocumentIngestionError("The document text could not be extracted") from exc

    if not text.strip():
        raise DocumentIngestionError("The document contains no extractable text")
    chunks = split_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return ExtractedDocument(
        name=PurePath(filename).name,
        source_type=extension.removeprefix("."),
        text=text,
        chunks=chunks,
    )


def _extract_text(extension: str, content: bytes) -> str:
    if extension in {".txt", ".md"}:
        return content.decode("utf-8")
    reader = PdfReader(BytesIO(content))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

