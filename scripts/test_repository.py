
import hashlib
import uuid

from app.database.connection import SessionLocal
from app.database.models import Document, DocumentChunk
from app.ingestion.chunker import chunk_pages
from app.ingestion.extractor import ExtractedPage
from app.ingestion.repository import save_document


db = SessionLocal()
document = None

try:
    # Generate a unique checksum for this test document.
    checksum = hashlib.sha256(
        str(uuid.uuid4()).encode()
    ).hexdigest()

    # Create sample chunks using our existing chunker.
    pages = [
        ExtractedPage(
            page_number=1,
            text=(
                "Employees receive annual leave.\n\n"
                "Managers approve leave requests.\n\n"
                "Employees receive sick leave."
            ),
        )
    ]

    chunks = chunk_pages(
        pages,
        chunk_size=10,
        overlap=2,
    )

    # Save the document and its chunks.
    document = save_document(
        db=db,
        filename="policy.txt",
        source_path="data/raw/policy.txt",
        file_type=".txt",
        checksum=checksum,
        chunks=chunks,
        embedding_model="bge-m3",
        metadata={"test": True},
    )

    print("Document saved:", document.id)

    # Verify that all chunks were persisted.
    saved_chunks = (
        db.query(DocumentChunk)
        .filter(DocumentChunk.document_id == document.id)
        .all()
    )

    print("Expected chunks:", len(chunks))
    print("Saved chunks:", len(saved_chunks))
    
    assert len(saved_chunks) == len(chunks)

    # Verify duplicate detection.
    try:
        save_document(
            db=db,
            filename="policy.txt",
            source_path="data/raw/policy.txt",
            file_type=".txt",
            checksum=checksum,
            chunks=chunks,
            embedding_model="bge-m3",
        )
        raise AssertionError("Duplicate was not detected")

    except ValueError as error:
        if "already exists" not in str(error):
            raise
        print("Duplicate detection: passed")

    print("Repository integration test passed!")

finally:
    # Remove test data so it doesn't pollute the database.
    # if document is not None:
    #     db.delete(document)
    #     db.commit()

    db.close()
