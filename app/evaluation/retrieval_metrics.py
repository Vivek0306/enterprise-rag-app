
def _validate_inputs(
    retrieved_ids: list[str],
    relevant_ids: list[str],
    k: int | None = None,
) -> None:
    if not relevant_ids:
        raise ValueError("relevant_ids cannot be empty")

    if k is not None and k <= 0:
        raise ValueError("k must be greater than zero")


def precision_at_k(
    retrieved_ids: list[str],
    relevant_ids: list[str],
    k: int,
) -> float:
    _validate_inputs(retrieved_ids, relevant_ids, k)

    retrieved_top_k = retrieved_ids[:k]
    relevant_set = set(relevant_ids)

    relevant_retrieved = sum(
        1 for chunk_id in set(retrieved_top_k)
        if chunk_id in relevant_set
    )

    return relevant_retrieved / k


def recall_at_k(
    retrieved_ids: list[str],
    relevant_ids: list[str],
    k: int,
) -> float:
    _validate_inputs(retrieved_ids, relevant_ids, k)

    retrieved_top_k = set(retrieved_ids[:k])
    relevant_set = set(relevant_ids)

    relevant_retrieved = len(retrieved_top_k & relevant_set)

    return relevant_retrieved / len(relevant_set)


def reciprocal_rank(
    retrieved_ids: list[str],
    relevant_ids: list[str],
) -> float:
    _validate_inputs(retrieved_ids, relevant_ids)

    relevant_set = set(relevant_ids)

    for rank, chunk_id in enumerate(retrieved_ids, start=1):
        if chunk_id in relevant_set:
            return 1 / rank

    return 0.0


def hit_rate_at_k(
    retrieved_ids: list[str],
    relevant_ids: list[str],
    k: int,
) -> float:
    _validate_inputs(retrieved_ids, relevant_ids, k)

    retrieved_top_k = set(retrieved_ids[:k])
    relevant_set = set(relevant_ids)

    return float(bool(retrieved_top_k & relevant_set))
