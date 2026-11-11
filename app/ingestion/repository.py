from sqlalchemy.orm import Session

from app.database.models import Document, DocumentChunk
from app.ingestion.chunker import DocumentChunk as ChunkData


def save_document(
        db: Session,
        filename: str, 
        source_path: str,
        file_type: str,
        checksum: str,
        chunks: list[ChunkData],
        embedding_model: str,
        metadata: dict | None = None,
        ) -> Document:
    try:
        existing_document = (
            db.query(Document).filter(Document.checksum == checksum).first()
        )

        if existing_document:
            raise ValueError(f"Document already exists: {filename}")

        if not chunks:
            raise ValueError(f"Cannot save a document without chunks.")

        document = Document(
            filename=filename,
            source_path=source_path,
            file_type=file_type,
            checksum=checksum,
            metadata_json=metadata or {},
        )

        db.add(document)

        db.flush()


        for chunk in chunks:
            db_chunk = DocumentChunk(
                document_id = document.id,
                chunk_index = chunk.chunk_index,
                content = chunk.content,
                page_number = chunk.page_number,
                token_count = None,
                embedding = None,
                embedding_model = embedding_model,
                metadata_json = {
                    "word_count": chunk.token_count
                }
            )

            db.add(db_chunk)

        db.commit()

        db.refresh(document)

        return document
        
    except Exception:
        db.rollback()
        raise