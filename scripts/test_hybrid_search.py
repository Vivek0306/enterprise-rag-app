from app.retrieval.hybrid_search import hybrid_search
from app.database.connection import SessionLocal

db = SessionLocal()

try:
    query = "How many annual leave days are employees entitled to?"

    results = hybrid_search(
        db=db,
        query=query,
        top_k=5,
        rrf_k=60,
    )

    print("\nHYBRID SEARCH RESULTS")
    print("=" * 60)

    for rank, (chunk, score) in enumerate(results, start=1):
        print(f"\nRank: {rank}")
        print(f"Document ID: {chunk.document_id}")
        print(f"Chunk index: {chunk.chunk_index}")
        print(f"RRF Score: {score:.4f}")
        print(f"Content: {chunk.content}")


finally:
    db.close()