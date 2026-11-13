
from app.database.connection import SessionLocal
from app.retrieval.vector_search import search_similar_chunks

db = SessionLocal()

try:
    query = "How many annual leave days are employees entitled to?"

    results = search_similar_chunks(
        db=db,
        query=query,
        top_k=5,
    )

    print("\nVECTOR SEARCH RESULTS")
    print("=" * 60)

    for rank, (chunk, distance) in enumerate(results, start=1):
        print(f"\nRank: {rank}")
        print(f"Document ID: {chunk.document_id}")
        print(f"Chunk index: {chunk.chunk_index}")
        print(f"Cosine distance: {distance:.4f}")
        print(f"Content: {chunk.content}")

finally:
    db.close()
