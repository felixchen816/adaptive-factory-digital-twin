import pytest

from factory_twin.line import ProductionLine
from factory_twin.machine import Machine
from factory_twin.multi_stage import simulate_production_line


def make_three_stage_line():
    return ProductionLine(
        "three-stage line",
        [
            Machine("cutter", 1),
            Machine("press", 3),
            Machine("inspector", 2),
        ],
    )


def test_simulate_production_line_reports_line_identity_and_bottleneck():
    line = make_three_stage_line()

    metrics = simulate_production_line(line, 60, 1)

    assert metrics["line"] == "three-stage line"
    assert metrics["bottleneck_machine"] == "press"
    assert metrics["bottleneck_process_time"] == 3
    assert metrics["line_capacity_per_hour"] == 20.0


def test_simulate_production_line_counts_completed_parts():
    line = make_three_stage_line()

    metrics = simulate_production_line(line, 60, 1)

    assert metrics["completed"] > 0
    assert metrics["completed"] < metrics["arrivals"]
    assert metrics["throughput_per_hour"] == metrics["completed"]


def test_simulate_production_line_tracks_final_queue_lengths():
    line = make_three_stage_line()

    metrics = simulate_production_line(line, 60, 1)

    assert set(metrics["final_queue_lengths"]) == {"cutter", "press", "inspector"}
    assert metrics["final_queue_lengths"]["press"] > 0
    assert metrics["total_wip"] == sum(metrics["final_queue_lengths"].values())


def test_simulate_production_line_tracks_max_queue_lengths():
    line = make_three_stage_line()

    metrics = simulate_production_line(line, 60, 1)

    assert set(metrics["max_queue_lengths"]) == {"cutter", "press", "inspector"}
    assert metrics["max_queue_lengths"]["press"] >= metrics["final_queue_lengths"]["press"]


def test_parallel_stage_processes_multiple_parts_at_a_time():
    baseline = make_three_stage_line()
    parallel_press = ProductionLine(
        "parallel press line",
        [
            Machine("cutter", 1),
            Machine("press", 3, parallel_units=2),
            Machine("inspector", 2),
        ],
    )

    baseline_metrics = simulate_production_line(baseline, 60, 1)
    parallel_metrics = simulate_production_line(parallel_press, 60, 1)

    assert parallel_metrics["completed"] > baseline_metrics["completed"]
    assert (
        parallel_metrics["final_queue_lengths"]["press"]
        < baseline_metrics["final_queue_lengths"]["press"]
    )


def test_machine_downtime_reduces_completed_parts():
    baseline = make_three_stage_line()
    press_down = ProductionLine(
        "press downtime line",
        [
            Machine("cutter", 1),
            Machine("press", 3, downtime_minutes=(0, 3, 6, 9)),
            Machine("inspector", 2),
        ],
    )

    baseline_metrics = simulate_production_line(baseline, 60, 1)
    downtime_metrics = simulate_production_line(press_down, 60, 1)

    assert downtime_metrics["completed"] < baseline_metrics["completed"]
    assert downtime_metrics["downtime_events"]["press"] == 4


def test_simulation_returns_queue_and_completed_history():
    line = make_three_stage_line()

    metrics = simulate_production_line(line, 5, 1)

    assert len(metrics["queue_history"]) == 5
    assert len(metrics["completed_history"]) == 5
    assert set(metrics["queue_history"][0]) == {"minute", "cutter", "press", "inspector"}
    assert metrics["completed_history"][-1]["completed"] == metrics["completed"]


def test_simulate_production_line_rejects_invalid_inputs():
    line = make_three_stage_line()

    with pytest.raises(ValueError):
        simulate_production_line(line, -1, 1)

    with pytest.raises(ValueError):
        simulate_production_line(line, 60, -1)
