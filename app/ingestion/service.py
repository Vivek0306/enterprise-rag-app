from pathlib import Path
from sqlalchemy.orm import Session


from app.ingestion.file_handler import (
    validate_file,
    calculate_checksum,
    extract_file_metadata,
)

from app.ingestion.extractor import extract_document
from app.ingestion.chunker import chunk_pages
from app.embeddings.embedder import generate_embeddings
from app.ingestion.repository import save_document, update_document_embeddings, get_document_by_checksum




def ingest_document(
    file_path: str,
    db: Session,
):
    # 1. Validate file
    path = validate_file(file_path)

    # 2. Extract metadata
    file_metadata = extract_file_metadata(path)

    # 3. Check for existing document
    checksum = file_metadata["checksum"]
    existing_document = get_document_by_checksum(db, checksum)

    if existing_document:
        raise ValueError(f"A similar document already ingested with checksum. Document: {existing_document.source_path}")

    # 4. Extract text
    pages = extract_document(str(path))

    if not pages:
        raise ValueError("No extractable text found in document.")

    # 5. Generate chunks
    chunks = chunk_pages(
        pages=pages,
        chunk_size=250,
        overlap=40,
    )

    if not chunks:
        raise ValueError("Document did not produce any chunks.")

    # 6. Generate embeddings
    texts = [chunk.content for chunk in chunks]

    embeddings = generate_embeddings(texts)

    # 7. Persist document, chunks and embeddings
    document = save_document(
        db=db,
        filename=path.name,
        source_path=str(path.resolve()),
        file_type=path.suffix.lower(),
        checksum=checksum,
        chunks=chunks,
        embeddings=embeddings,
        embedding_model="bge-m3",
        metadata=file_metadata,
    )

    return {
        "document_id": str(document.id),
        "filename": document.filename,
        "total_chunks": len(chunks),
        "embedding_dimensions": len(embeddings[0]),
        "status": "completed",
    }