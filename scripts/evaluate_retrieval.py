
import json
from pathlib import Path

from app.database.connection import SessionLocal

from app.retrieval.vector_search import search_similar_chunks
from app.retrieval.keyword_search import search_keyword_chunks
from app.retrieval.hybrid_search import hybrid_search

from app.evaluation.retrieval_metrics import (
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
    hit_rate_at_k,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data" / "evaluation" / "retrieval_dataset.json"

TOP_K = 5

RETRIEVAL_STRATEGIES = {
    "Vector Search": search_similar_chunks,
    "Keyword Search": search_keyword_chunks,
    "Hybrid Search": hybrid_search,
}



def load_evaluation_dataset() -> list[dict]:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Evaluation dataset not found: {DATASET_PATH}"
        )

    with DATASET_PATH.open("r", encoding="utf-8") as file:
        dataset = json.load(file)

    if not isinstance(dataset, list) or not dataset:
        raise ValueError("Evaluation dataset must be a non-empty list.")

    for item in dataset:
        if not item.get("question") or not item.get("relevant_chunk_ids"):
            raise ValueError(f"Invalid evaluation entry: {item}")

    return dataset


def evaluate_strategy(db, dataset, search_function):
    scores = {
        "precision_at_5": [],
        "recall_at_5": [],
        "mrr": [],
        "hit_rate_at_5": [],
    }

    for item in dataset:
        question = item["question"]
        relevant_ids = item["relevant_chunk_ids"]

        results = search_function(
            db,
            question,
            top_k=TOP_K,
        )

        retrieved_ids = [
            str(chunk.id)
            for chunk, score in results
        ]

        scores["precision_at_5"].append(
            precision_at_k(retrieved_ids, relevant_ids, TOP_K)
        )

        scores["recall_at_5"].append(
            recall_at_k(retrieved_ids, relevant_ids, TOP_K)
        )

        scores["mrr"].append(
            reciprocal_rank(retrieved_ids, relevant_ids)
        )

        scores["hit_rate_at_5"].append(
            hit_rate_at_k(retrieved_ids, relevant_ids, TOP_K)
        )

    return {
        metric: sum(values) / len(values)
        for metric, values in scores.items()
    }



def main():
    dataset = load_evaluation_dataset()

    print(f"Loaded {len(dataset)} evaluation questions.")
    print(f"Evaluating with TOP_K = {TOP_K}\n")

    with SessionLocal() as db:
        for strategy_name, search_function in RETRIEVAL_STRATEGIES.items():
            metrics = evaluate_strategy(
                db,
                dataset,
                search_function,
            )

            print(f"\n{strategy_name}")
            print("-" * 45)

            for metric, value in metrics.items():
                print(f"{metric:<20}: {value:.4f}")


if __name__ == "__main__":
    main()
