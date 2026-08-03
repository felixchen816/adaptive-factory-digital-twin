import pytest
from factory_twin.line_analysis import (
    find_queue_bottleneck,
    explain_queue_bottleneck,
    recommend_line_action,
)


def test_three_stage_queue_bottleneck():
    metrics = {"cutter": 0, "press": 41, "inspector": 0}

    # Verify bottleneck detection
    assert find_queue_bottleneck(metrics) == "press"

    # Verify explanation text
    explanation = explain_queue_bottleneck(metrics)
    assert "press" in explanation
    assert "accumulating the largest queue" in explanation

    # Verify recommendation options
    rec = recommend_line_action(metrics)
    assert "Improve press capacity" in rec
    assert "reduce press process time" in rec
    assert "add parallel press capacity" in rec
    assert "reduce arrivals" in rec


def test_empty_or_zero_queues():
    zero_metrics = {"cutter": 0, "press": 0, "inspector": 0}
    assert find_queue_bottleneck(zero_metrics) == "none"
    assert "No queue bottleneck" in explain_queue_bottleneck(zero_metrics)
    assert "operating smoothly" in recommend_line_action(zero_metrics)

    empty_metrics = {}
    assert find_queue_bottleneck(empty_metrics) == "none"


def test_nested_metrics_dictionary():
    nested_metrics = {
        "cutter": {"queue_length": 2},
        "press": {"queue_length": 15},
        "inspector": {"queue_length": 1},
    }
    assert find_queue_bottleneck(nested_metrics) == "press"
    assert "press is accumulating the largest queue" in explain_queue_bottleneck(nested_metrics)