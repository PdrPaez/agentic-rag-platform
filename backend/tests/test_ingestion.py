import pytest

from app.rag.chunking import split_text
from app.services.document_ingestion import DocumentIngestionError, ingest_document


def test_split_text_respects_size_and_overlap() -> None:
    chunks = split_text("one two three four five six seven eight", chunk_size=20, chunk_overlap=5)

    assert len(chunks) > 1
    assert all(len(chunk) <= 20 for chunk in chunks)
    assert chunks[0].split()[-1] in chunks[1].split()


def test_ingest_markdown_extracts_safe_name_and_chunks() -> None:
    document = ingest_document("folder/guide.md", b"# Guide\n\nUseful content", chunk_size=10, chunk_overlap=2)

    assert document.name == "guide.md"
    assert document.source_type == "md"
    assert document.chunks
    assert "Useful" in " ".join(document.chunks)
    assert "content" in " ".join(document.chunks)


@pytest.mark.parametrize("filename", ["guide.docx", "guide.exe", "guide"])
def test_ingest_rejects_unsupported_types(filename: str) -> None:
    with pytest.raises(DocumentIngestionError, match="Unsupported document type"):
        ingest_document(filename, b"content")


def test_ingest_strips_upload_path_components() -> None:
    extracted = ingest_document("../../outside/guide.md", b"safe content")

    assert extracted.name == "guide.md"


def test_ingest_strips_windows_style_upload_path_components() -> None:
    extracted = ingest_document(r"C:\private\notes.txt", b"safe content")

    assert extracted.name == "notes.txt"


def test_ingest_rejects_empty_text() -> None:
    with pytest.raises(DocumentIngestionError, match="no extractable text"):
        ingest_document("empty.txt", b" \n\t")
