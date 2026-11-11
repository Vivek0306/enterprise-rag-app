from dataclasses import dataclass

from app.ingestion.extractor import ExtractedPage


@dataclass
class DocumentChunk:
    chunk_index: int
    content: str    
    page_number: int
    token_count: int

'''
def chunk_pages(pages: list[ExtractedPage], chunk_size: int = 250, overlap: int = 40) -> list[DocumentChunk]:
    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size")

    chunks = []
    chunk_index = 0

    for page in pages:
        words = page.text.split()

        start = 0

        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk_words = words[start: end]

            content = " ".join(chunk_words)

            chunks.append(
                DocumentChunk(
                    chunk_index=chunk_index,
                    content=content,
                    page_number=page.page_number,
                    token_count=len(chunk_words),
                )
            )
            chunk_index += 1

            if end == len(words):
                break

            start = end - overlap

    return chunks
'''

def chunk_pages(
    pages: list[ExtractedPage],
    chunk_size: int = 250,
    overlap: int = 40,
) -> list[DocumentChunk]:

    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Invalid overlap")

    chunks = []
    chunk_index = 0

    for page in pages:

        paragraphs = [
            paragraph.strip()
            for paragraph in page.text.split("\n\n")
            if paragraph.strip()
        ]

        current_words = []

        def save_current():

            nonlocal chunk_index, current_words

            if not current_words:
                return

            content = " ".join(current_words)

            chunks.append(
                DocumentChunk(
                    chunk_index=chunk_index,
                    content=content,
                    page_number=page.page_number,
                    token_count=len(current_words),
                )
            )

            chunk_index += 1

        for paragraph in paragraphs:

            words = paragraph.split()

            if not words:
                continue

            # Handle oversized paragraphs.
            if len(words) > chunk_size:

                save_current()
                current_words = []
                
                for part in split_long_paragraph(
                    paragraph,
                    chunk_size,
                    overlap,
                ):

                    chunks.append(
                        DocumentChunk(
                            chunk_index=chunk_index,
                            content=part,
                            page_number=page.page_number,
                            token_count=len(part.split()),
                        )
                    )

                    chunk_index += 1

                continue

            # Check whether the next paragraph fits.
            if len(current_words) + len(words) > chunk_size:

                save_current()

                overlap_size = min(overlap, chunk_size - len(words))

                # Preserve the configured overlap.
                current_words = (
                    current_words[-overlap_size:]
                    if overlap_size > 0
                    else []
                )

            current_words.extend(words)

        save_current()

    return chunks


def split_long_paragraph(paragraph: str, chunk_size: int, overlap: int) -> list[str]:
    words = paragraph.split()

    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))

        if end == len(words):
            break

        start = end - overlap

    return chunks