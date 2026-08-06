import pytest

from factory_twin.multi_stage_decision import choose_best_multi_stage_scenario


def test_choose_best_multi_stage_scenario_prefers_highest_completed():
    rows = [
        {
            "scenario": "baseline",
            "completed": 19,
            "total_wip": 41,
            "max_queue_lengths": {"press": 41},
        },
        {
            "scenario": "faster press",
            "completed": 28,
            "total_wip": 32,
            "max_queue_lengths": {"press": 32},
        },
    ]

    best = choose_best_multi_stage_scenario(rows)

    assert best["scenario"] == "faster press"


def test_choose_best_multi_stage_scenario_uses_lower_wip_as_tie_breaker():
    rows = [
        {
            "scenario": "high wip",
            "completed": 28,
            "total_wip": 32,
            "max_queue_lengths": {"press": 32},
        },
        {
            "scenario": "low wip",
            "completed": 28,
            "total_wip": 20,
            "max_queue_lengths": {"press": 20},
        },
    ]

    best = choose_best_multi_stage_scenario(rows)

    assert best["scenario"] == "low wip"


def test_choose_best_multi_stage_scenario_uses_lowest_largest_queue_as_final_tie_breaker():
    rows = [
        {
            "scenario": "large queue",
            "completed": 28,
            "total_wip": 30,
            "max_queue_lengths": {"press": 25, "inspector": 5},
        },
        {
            "scenario": "smaller largest queue",
            "completed": 28,
            "total_wip": 30,
            "max_queue_lengths": {"press": 15, "inspector": 15},
        },
    ]

    best = choose_best_multi_stage_scenario(rows)

    assert best["scenario"] == "smaller largest queue"


def test_choose_best_multi_stage_scenario_rejects_empty_rows():
    with pytest.raises(ValueError):
        choose_best_multi_stage_scenario([])
