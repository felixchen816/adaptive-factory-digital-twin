from factory_twin.comparison import compare_scenarios
from factory_twin.machine import Machine
from factory_twin.scenario import Scenario


def test_compare_scenarios_returns_one_row_per_scenario():
    scenarios = [
        Scenario(
            name="balanced line",
            minutes=60,
            arrival_rate=1,
            machine=Machine(name="standard cutter", process_time=1),
        ),
        Scenario(
            name="overloaded line",
            minutes=60,
            arrival_rate=1,
            machine=Machine(name="slow press", process_time=3),
        ),
    ]

    rows = compare_scenarios(scenarios)

    assert len(rows) == 2


def test_compare_scenarios_includes_identity_and_metrics():
    scenario = Scenario(
        name="overloaded line",
        minutes=60,
        arrival_rate=1,
        machine=Machine(name="slow press", process_time=3),
    )

    row = compare_scenarios([scenario])[0]

    assert row["scenario"] == "overloaded line"
    assert row["machine"] == "slow press"
    assert row["process_time"] == 3
    assert row["completed"] == 20
    assert row["throughput_per_hour"] == 20.0
    assert row["average_queue_length"] == 20.0
    assert row["max_queue_length"] == 40
    assert row["utilization"] == 1.0
    assert row["queue_growth_rate"] == 40
    assert row["line_status"] == "overloaded"
    assert row["explanation"] == (
        "Backlog is growing because arrivals exceed effective processing capacity."
    )
