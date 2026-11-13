
from app.database.connection import SessionLocal
from app.retrieval.keyword_search import search_keyword_chunks

db = SessionLocal()

try:
    query = "annual leave"

    results = search_keyword_chunks(
        db=db,
        query=query,
        top_k=5,
    )

    print("\nKEYWORD SEARCH RESULTS")
    print("=" * 60)

    for rank, (chunk, relevance) in enumerate(results, start=1):
        print(f"\nRank: {rank}")
        print(f"Document ID: {chunk.document_id}")
        print(f"Chunk index: {chunk.chunk_index}")
        print(f"Relevance: {relevance:.4f}")
        print(f"Content: {chunk.content}")

finally:
    db.close()
