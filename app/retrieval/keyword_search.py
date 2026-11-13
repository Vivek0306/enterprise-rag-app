
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.models import DocumentChunk


def search_keyword_chunks(
    db: Session,
    query: str,
    top_k: int = 5,
) -> list[tuple[DocumentChunk, float]]:
    

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    search_query = func.websearch_to_tsquery(
        "english",
        query,
    )

    relevance = func.ts_rank(
        DocumentChunk.content_tsv,
        search_query,
    )

    results = (
        db.query(
            DocumentChunk,
            relevance.label("relevance"),
        )
        .filter(
            DocumentChunk.content_tsv.op("@@")(search_query)
        )
        .order_by(relevance.desc())
        .limit(top_k)
        .all()
    )

    return [
        (chunk, float(score))
        for chunk, score in results
    ]
