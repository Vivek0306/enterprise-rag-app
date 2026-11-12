
from app.database.connection import SessionLocal
from app.database.models import DocumentChunk
from app.embeddings.embedder import generate_embeddings
from app.ingestion.repository import update_document_embeddings

# Replace this with an existing document UUID from PostgreSQL.
DOCUMENT_ID = "7b52a737-0ab1-4a5f-9408-92e920bdc7c1"

db = SessionLocal()

try:
    chunks = (
        db.query(DocumentChunk)
        .filter(DocumentChunk.document_id == DOCUMENT_ID)
        .order_by(DocumentChunk.chunk_index)
        .all()
    )

    texts = [chunk.content for chunk in chunks]

    embeddings = generate_embeddings(texts)

    updated_count = update_document_embeddings(
        db=db,
        document_id=DOCUMENT_ID,
        embeddings=embeddings,
        embedding_model="bge-m3",
    )

    print("Updated chunks:", updated_count)

    # Verify stored embeddings.
    db.expire_all()

    saved_chunks = (
        db.query(DocumentChunk)
        .filter(DocumentChunk.document_id == DOCUMENT_ID)
        .all()
    )

    for chunk in saved_chunks:
        print(
            f"Chunk {chunk.chunk_index}: "
            f"embedding dimensions = {len(chunk.embedding)}"
        )

finally:
    db.close()
