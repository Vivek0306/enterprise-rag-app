from ollama import embeddings
from sqlalchemy.orm import Session

from app.database.models import Document, DocumentChunk
from app.ingestion.chunker import DocumentChunk as ChunkData


def update_document_embeddings(
        db: Session,
        document_id,
        embeddings: list[list[float]],
        embedding_model: str,
) -> int:
    try:
        chunks = (
            db.query(DocumentChunk)\
            .filter(DocumentChunk.document_id == document_id)\
            .order_by(DocumentChunk.chunk_index)\
            .all()
        )

        if not chunks:
            raise ValueError(f"No chunks found for document ID: {document_id}")


        if len(chunks) != len(embeddings):
            raise ValueError(
                f"Number of embeddings ({len(embeddings)}) does not match number of chunks ({len(chunks)})."
            )

        for embedding in embeddings:
            if len(embedding) != 1024:
                raise ValueError(
                    f"Expected embedding dimension of 1024, but got {len(embedding)}."
                )

        for chunk, embedding in zip(chunks, embeddings):
            chunk.embedding = embedding
            chunk.embedding_model = embedding_model

        db.commit()

        return len(chunks)

        
    except Exception:
        db.rollback()
        raise


def save_document(
        db: Session,
        filename: str, 
        source_path: str,
        file_type: str,
        checksum: str,
        chunks: list[ChunkData],
        embeddings: list[list[float]],
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

        if len(chunks) != len(embeddings):
            raise ValueError("Chunk count and embedding count do not match.")

        if any(len(embedding) != 1024 for embedding in embeddings):
            raise ValueError("All embeddings must have 1024 dimensions.")

        document = Document(
            filename=filename,
            source_path=source_path,
            file_type=file_type,
            checksum=checksum,
            metadata_json=metadata or {},
        )

        db.add(document)

        db.flush()


        for chunk, embedding in zip(chunks, embeddings):
            db_chunk = DocumentChunk(
                document_id = document.id,
                chunk_index = chunk.chunk_index,
                content = chunk.content,
                page_number = chunk.page_number,
                token_count = None,
                embedding = embedding,
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

def get_document_by_checksum(db: Session, checksum: str) -> Document | None:
    return db.query(Document).filter(Document.checksum == checksum).first()