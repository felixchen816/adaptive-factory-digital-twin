import pytest

from factory_twin.simple_line import simulate_line


def test_simulate_line_returns_basic_metrics():
    metrics = simulate_line(60, 1, 3)

    assert metrics["completed"] > 0
    assert metrics["throughput_per_hour"] == metrics["completed"]
    assert metrics["average_queue_length"] >= 0


def test_throughput_scales_to_hour():
    metrics = simulate_line(30, 1, 3)

    assert metrics["throughput_per_hour"] == metrics["completed"] * 2


def test_invalid_process_time_raises_error():
    with pytest.raises(ValueError):
        simulate_line(60, 1, 0)


def test_simulate_line_tracks_max_queue_length():
    metrics = simulate_line(60, 1, 3)
    assert metrics["max_queue_length"] == 40

