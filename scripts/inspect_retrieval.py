
from scripts.evaluate_retrieval import (
    load_evaluation_dataset,
    TOP_K,
)

from app.database.connection import SessionLocal
from app.retrieval.vector_search import search_similar_chunks
from app.retrieval.keyword_search import search_keyword_chunks
from app.retrieval.hybrid_search import hybrid_search


STRATEGIES = {
    "Vector": search_similar_chunks,
    "Keyword": search_keyword_chunks,
    "Hybrid": hybrid_search,
}


def main():
    dataset = load_evaluation_dataset()

    with SessionLocal() as db:
        for item in dataset:
            question = item["question"]
            relevant_ids = set(item["relevant_chunk_ids"])

            print("\n" + "=" * 80)
            print(f"QUESTION: {question}")
            print("=" * 80)

            for name, search_function in STRATEGIES.items():
                results = search_function(
                    db,
                    question,
                    top_k=TOP_K,
                )

                print(f"\n{name} Search:")

                for rank, (chunk, score) in enumerate(
                    results, start=1
                ):
                    chunk_id = str(chunk.id)
                    is_relevant = chunk_id in relevant_ids

                    print(
                        f"Rank {rank} | "
                        f"Relevant: {is_relevant} | "
                        f"Score: {score:.4f} | "
                        f"Chunk: {chunk_id}"
                    )

                    print(
                        f"Content: {chunk.content[:180]}..."
                    )


if __name__ == "__main__":
    main()
