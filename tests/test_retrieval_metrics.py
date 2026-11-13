
import pytest

from app.evaluation.retrieval_metrics import (
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
    hit_rate_at_k,
)


def test_precision_at_k():
    assert precision_at_k(
        ["A", "B", "C", "D"],
        ["B", "D"],
        3,
    ) == pytest.approx(1 / 3)


def test_recall_at_k():
    assert recall_at_k(
        ["A", "B", "C", "D"],
        ["B", "D"],
        3,
    ) == pytest.approx(0.5)


def test_reciprocal_rank():
    assert reciprocal_rank(
        ["A", "B", "C"],
        ["B"],
    ) == pytest.approx(0.5)


def test_reciprocal_rank_when_no_relevant_result():
    assert reciprocal_rank(
        ["A", "B", "C"],
        ["D"],
    ) == 0.0


def test_hit_rate_at_k():
    assert hit_rate_at_k(
        ["A", "B", "C"],
        ["B"],
        3,
    ) == 1.0


def test_empty_relevant_ids():
    with pytest.raises(ValueError):
        precision_at_k(["A", "B"], [], 2)


def test_invalid_k():
    with pytest.raises(ValueError):
        precision_at_k(["A", "B"], ["A"], 0)
