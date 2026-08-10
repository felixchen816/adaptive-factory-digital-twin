import pytest

from factory_twin.multi_stage_decision import choose_best_multi_stage_scenario


def test_choose_best_multi_stage_scenario_prefers_highest_completion_rate():
    rows = [
        {
            "scenario": "more completed lower rate",
            "completion_rate": 0.8,
            "completed": 80,
            "total_wip": 10,
            "largest_max_queue": 10,
        },
        {
            "scenario": "fewer completed higher rate",
            "completion_rate": 0.9,
            "completed": 45,
            "total_wip": 20,
            "largest_max_queue": 20,
        },
    ]

    best = choose_best_multi_stage_scenario(rows)

    assert best["scenario"] == "fewer completed higher rate"


def test_choose_best_multi_stage_scenario_uses_completed_as_first_tie_breaker():
    rows = [
        {
            "scenario": "fewer completed",
            "completion_rate": 0.8,
            "completed": 20,
            "total_wip": 5,
            "largest_max_queue": 5,
        },
        {
            "scenario": "more completed",
            "completion_rate": 0.8,
            "completed": 28,
            "total_wip": 20,
            "largest_max_queue": 20,
        },
    ]

    best = choose_best_multi_stage_scenario(rows)

    assert best["scenario"] == "more completed"


def test_choose_best_multi_stage_scenario_uses_lower_wip_as_second_tie_breaker():
    rows = [
        {
            "scenario": "high wip",
            "completion_rate": 0.8,
            "completed": 28,
            "total_wip": 32,
            "largest_max_queue": 32,
        },
        {
            "scenario": "low wip",
            "completion_rate": 0.8,
            "completed": 28,
            "total_wip": 20,
            "largest_max_queue": 20,
        },
    ]

    best = choose_best_multi_stage_scenario(rows)

    assert best["scenario"] == "low wip"


def test_choose_best_multi_stage_scenario_uses_lowest_largest_max_queue_as_final_tie_breaker():
    rows = [
        {
            "scenario": "large queue",
            "completion_rate": 0.8,
            "completed": 28,
            "total_wip": 30,
            "largest_max_queue": 25,
        },
        {
            "scenario": "smaller largest queue",
            "completion_rate": 0.8,
            "completed": 28,
            "total_wip": 30,
            "largest_max_queue": 15,
        },
    ]

    best = choose_best_multi_stage_scenario(rows)

    assert best["scenario"] == "smaller largest queue"


def test_choose_best_multi_stage_scenario_rejects_empty_rows():
    with pytest.raises(ValueError):
        choose_best_multi_stage_scenario([])
