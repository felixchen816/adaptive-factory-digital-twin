import pytest
from factory_twin.line import ProductionLine
from factory_twin.machine import Machine
from factory_twin.multi_stage_comparison import (
    MultiStageScenario,
    compare_multi_stage_scenarios,
)


@pytest.fixture
def sample_scenarios():
    baseline_line = ProductionLine(
        "baseline line",
        [
            Machine(name="cutter", process_time=1),
            Machine(name="press", process_time=3),
            Machine(name="inspector", process_time=2),
        ],
    )

    faster_press_line = ProductionLine(
        "faster press line",
        [
            Machine(name="cutter", process_time=1),
            Machine(name="press", process_time=2),
            Machine(name="inspector", process_time=2),
        ],
    )

    # Fast cutter and press so parts flow freely to the slow inspector
    slow_inspector_line = ProductionLine(
        "slow inspector line",
        [
            Machine(name="cutter", process_time=1),
            Machine(name="press", process_time=1),
            Machine(name="inspector", process_time=4),
        ],
    )

    return [
        MultiStageScenario(
            name="baseline",
            line=baseline_line,
            minutes=60,
            arrival_rate=1.0,
        ),
        MultiStageScenario(
            name="faster press",
            line=faster_press_line,
            minutes=60,
            arrival_rate=1.0,
        ),
        MultiStageScenario(
            name="slow inspector",
            line=slow_inspector_line,
            minutes=60,
            arrival_rate=1.0,
        ),
        MultiStageScenario(
            name="lower demand",
            line=baseline_line,
            minutes=60,
            arrival_rate=0.5,
        ),
    ]


def test_compare_multi_stage_scenarios_behavior(sample_scenarios):
    results = compare_multi_stage_scenarios(sample_scenarios)
    res_map = {r["scenario"]: r for r in results}

    # Baseline queue bottleneck is press
    assert res_map["baseline"]["queue_bottleneck"] == "press"

    # Faster press completes more than baseline
    assert res_map["faster press"]["completed"] > res_map["baseline"]["completed"]

    # Slow inspector shifts queue bottleneck toward inspector
    assert res_map["slow inspector"]["queue_bottleneck"] == "inspector"

    # Lower demand reduces total WIP relative to baseline
    assert res_map["lower demand"]["total_wip"] < res_map["baseline"]["total_wip"]


def test_result_keys(sample_scenarios):
    results = compare_multi_stage_scenarios(sample_scenarios)
    expected_keys = {
        "scenario",
        "completed",
        "arrivals",
        "throughput_per_hour",
        "bottleneck_machine",
        "line_capacity_per_hour",
        "final_queue_lengths",
        "max_queue_lengths",
        "queue_bottleneck",
        "total_wip",
        "largest_final_queue",
        "largest_max_queue",
        "wip_per_completed_part",
        "completion_rate",
        "explanation",
        "recommendation",
    }
    for row in results:
        assert expected_keys.issubset(row.keys())


def test_summary_metrics_are_added_to_rows(sample_scenarios):
    results = compare_multi_stage_scenarios(sample_scenarios)
    baseline = {row["scenario"]: row for row in results}["baseline"]

    assert baseline["largest_final_queue"] == 41
    assert baseline["largest_max_queue"] == 41
    assert baseline["completion_rate"] == pytest.approx(19 / 60)
    assert baseline["wip_per_completed_part"] == pytest.approx(41 / 19)


def test_summary_metrics_handle_zero_completed_parts():
    line = ProductionLine(
        "no demand line",
        [
            Machine(name="cutter", process_time=1),
            Machine(name="press", process_time=3),
        ],
    )
    scenarios = [
        MultiStageScenario(
            name="no demand",
            line=line,
            minutes=60,
            arrival_rate=0,
        )
    ]

    row = compare_multi_stage_scenarios(scenarios)[0]

    assert row["completed"] == 0
    assert row["arrivals"] == 0
    assert row["completion_rate"] == 0
    assert row["wip_per_completed_part"] == 0
