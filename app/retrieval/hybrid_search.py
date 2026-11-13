
from sqlalchemy.orm import Session

from app.database.models import DocumentChunk
from app.retrieval.vector_search import search_similar_chunks
from app.retrieval.keyword_search import search_keyword_chunks


def hybrid_search(
    db: Session,
    query: str,
    top_k: int = 5,
    rrf_k: int = 60,
) -> list[tuple[DocumentChunk, float]]:

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    if rrf_k <= 0:
        raise ValueError("rrf_k must be greater than zero.")
    
    vector_results = search_similar_chunks(
        db=db,
        query=query,
        top_k=top_k,
    )

    keyword_results = search_keyword_chunks(
        db=db,
        query=query,
        top_k=top_k,
    )

    fused_results = {}

    for rank, (chunk, _) in enumerate(vector_results, start=1):
        chunk_id = chunk.id

        if chunk_id not in fused_results:
            fused_results[chunk_id] = {
                "chunk": chunk,
                "score": 0.0,
            }

        fused_results[chunk_id]["score"] += (
            1.0 / (rrf_k + rank)
        )

    for rank, (chunk, _) in enumerate(keyword_results, start=1):
        chunk_id = chunk.id

        if chunk_id not in fused_results:
            fused_results[chunk_id] = {
                "chunk": chunk,
                "score": 0.0,
            }

        fused_results[chunk_id]["score"] += (
            1.0 / (rrf_k + rank)
        )

    ranked_results = sorted(
        fused_results.values(),
        key=lambda item: (
            -item["score"],
            str(item["chunk"].id),
        ),
    )

    return [
        (item["chunk"], item["score"])
        for item in ranked_results[:top_k]
    ]
