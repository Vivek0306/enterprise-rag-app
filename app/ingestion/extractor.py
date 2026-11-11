from pathlib import Path
from dataclasses import dataclass

from pypdf import PdfReader
from docx import Document as DocxDocument


@dataclass
class ExtractedPage:
    page_number: int
    text: str


def extract_pdf(path: Path) -> list[ExtractedPage]:
    reader = PdfReader(str(path))

    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        if text.strip():
            extracted_pages.append(
                ExtractedPage(
                    page_number=page_number,
                    text = text.strip()
                )
            )
    return extracted_pages


def extract_docx(path: Path) -> list[ExtractedPage]:
    document = DocxDocument(str(path))

    content = []
    
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            content.append(paragraph.text.strip())

    for table in document.tables:
        for row in table.rows:
            cells = [
                cell.text.strip() for cell in row.cells  
            ]
            content.append(" | ".join(cells))

    text = "\n\n".join(content)

    if not text.strip():
        return []

    return [ExtractedPage(page_number=1, text=text.strip())]

def extract_text(path: Path) -> list[ExtractedPage]:
    text = path.read_text(encoding="utf-8")

    if not text.strip():
        return []

    return [ExtractedPage(page_number=1, text=text.strip())]


def extract_document(path: Path) -> list[ExtractedPage]:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    if not path.is_file():
        raise ValueError(f"Expected a file, received: {path}")

    extension = path.suffix.lower()

    if extension == ".pdf":
        return extract_pdf(path)
    elif extension == ".docx":
        return extract_docx(path)
    elif extension == ".txt":
        return extract_text(path)
    else:
        raise ValueError(f"Unsupported file format: {extension}")