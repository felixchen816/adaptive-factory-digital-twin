import pytest

from factory_twin.decision import choose_best_scenario


def test_choose_best_scenario_prefers_highest_non_overloaded_throughput():
    rows = [
        {
            "scenario": "overloaded",
            "throughput_per_hour": 100,
            "line_status": "overloaded",
        },
        {
            "scenario": "stable",
            "throughput_per_hour": 60,
            "line_status": "stable",
        },
        {
            "scenario": "underused",
            "throughput_per_hour": 10,
            "line_status": "underused",
        },
    ]

    best = choose_best_scenario(rows)

    assert best["scenario"] == "stable"


def test_choose_best_scenario_uses_overloaded_if_all_are_overloaded():
    rows = [
        {
            "scenario": "slow overloaded",
            "throughput_per_hour": 20,
            "line_status": "overloaded",
        },
        {
            "scenario": "fast overloaded",
            "throughput_per_hour": 40,
            "line_status": "overloaded",
        },
    ]

    best = choose_best_scenario(rows)

    assert best["scenario"] == "fast overloaded"


def test_choose_best_scenario_rejects_empty_rows():
    with pytest.raises(ValueError):
        choose_best_scenario([])
