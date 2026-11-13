import pytest

from app.ingestion.chunker import chunk_pages
from app.ingestion.extractor import ExtractedPage

def test_chunking_creates_chunks():

    page = ExtractedPage(
        page_number=1,
        text= (
            "Employees receive annual leave.\n\n"
            "Managers approve leave requests.\n\n"
            "Employees receive sick leave."
        ),
    )

    chunks = chunk_pages(
        pages=[page],
        chunk_size=10,
        overlap=2,
    )

    assert len(chunks) > 0
    assert all(chunk.content.strip() for chunk in chunks)


def test_chunk_size_is_never_exceeded():
    page = ExtractedPage(
        page_number=1,
        text=(
            " ".join(["word"] * 18)
            + "\n\n"
            + " ".join(["next"] * 9)
        ),
    )

    chunks = chunk_pages(
        pages=[page],
        chunk_size=20,
        overlap=2,
    )

    for chunk in chunks:
        assert chunk.token_count <= 20


def test_empty_pages_return_empty_chunks():
    page = ExtractedPage(
        page_number=1,
        text=(
            "           "
        ),
    )
    chunks = chunk_pages(
        pages=[page],
        chunk_size=10,
        overlap=2,
    )

    assert chunks == []

def test_page_numbers_are_preserved():
    pages = [
        ExtractedPage(
            page_number=1,
            text="Annual leave policy details.",
        ),
        ExtractedPage(
            page_number=2,
            text="Sick leave policy details.",
        ),
    ]

    chunks = chunk_pages(
        pages=pages,
        chunk_size=20,
        overlap=3,
    )

    assert chunks[0].page_number == 1
    assert chunks[1].page_number == 2


def test_invalid_overlap_raises_error():
    page = ExtractedPage(
        page_number=1,
        text="Annual leave policy details.",
    )

    with pytest.raises(ValueError):
        chunk_pages(
            pages=[page],
            chunk_size=10,
            overlap=15,
        )