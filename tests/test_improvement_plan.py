import pytest

from factory_twin.improvement_plan import (
    build_improvement_options,
    choose_best_improvement,
)
from factory_twin.line import ProductionLine
from factory_twin.machine import Machine


def test_build_improvement_options_targets_queue_bottleneck():
    line = ProductionLine(
        "baseline line",
        [
            Machine(name="cutter", process_time=1),
            Machine(name="press", process_time=3),
            Machine(name="inspector", process_time=2),
        ],
    )
    metrics = {
        "final_queue_lengths": {"cutter": 0, "press": 41, "inspector": 0},
        "completed": 19,
    }

    options = build_improvement_options(line, metrics)
    option_names = {option["option"] for option in options}

    assert option_names == {
        "reduce process time",
        "add parallel capacity",
        "reduce arrivals",
    }
    assert all(option["target"] == "press" for option in options)
    assert all(option["before_completed"] == 19 for option in options)


def test_best_improvement_prefers_highest_benefit_per_cost():
    line = ProductionLine(
        "baseline line",
        [
            Machine(name="cutter", process_time=1),
            Machine(name="press", process_time=3),
            Machine(name="inspector", process_time=2),
        ],
    )
    metrics = {
        "final_queue_lengths": {"cutter": 0, "press": 41, "inspector": 0},
        "completed": 19,
    }

    best = choose_best_improvement(build_improvement_options(line, metrics))

    assert best["option"] == "reduce process time"
    assert best["target"] == "press"
    assert best["after_completed"] > best["before_completed"]
    assert best["benefit_per_cost"] == pytest.approx(
        best["completed_gain"] / best["cost"]
    )


def test_build_improvement_options_handles_no_queue_bottleneck():
    line = ProductionLine(
        "no demand line",
        [
            Machine(name="cutter", process_time=1),
            Machine(name="press", process_time=3),
        ],
    )
    metrics = {
        "final_queue_lengths": {"cutter": 0, "press": 0},
        "completed": 0,
    }

    options = build_improvement_options(line, metrics)

    assert options == []
