
from sqlalchemy.orm import Session

from app.database.models import DocumentChunk
from app.embeddings.embedder import generate_embeddings, generate_embedding


def search_similar_chunks(
    db: Session,
    query: str,
    top_k: int = 5,
) -> list[tuple[DocumentChunk, float]]:

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")
    
    query_embedding = generate_embedding(query)

    distance = DocumentChunk.embedding.cosine_distance(
        query_embedding
    )

    results = (
        db.query(
            DocumentChunk,
            distance.label("distance"),
        )
        .filter(DocumentChunk.embedding.is_not(None))
        .order_by(distance.asc())
        .limit(top_k)
        .all()
    )

    return [
        (chunk, float(distance_score))
        for chunk, distance_score in results
    ]
