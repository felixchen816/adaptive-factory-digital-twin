import pytest

from factory_twin.machine import Machine
from factory_twin.scenario import Scenario
from factory_twin.simple_line import simulate_line
from factory_twin.simple_line import simulate_machine_line
from factory_twin.simple_line import simulate_scenario


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


def test_simulate_line_tracks_utilization():
    metrics = simulate_line(60, 1, 3)
    assert metrics["utilization"] == 1.0


def test_simulate_line_tracks_queue_growth_rate():
    metrics = simulate_line(60, 1, 3)
    assert metrics["queue_growth_rate"] == 40


def test_scenario_stores_simulation_inputs():
    machine = Machine(name="press", process_time=3)
    scenario = Scenario(
        name="overloaded line",
        minutes=60,
        arrival_rate=1,
        machine=machine,
    )

    assert scenario.name == "overloaded line"
    assert scenario.minutes == 60
    assert scenario.arrival_rate == 1
    assert scenario.machine == machine
    assert scenario.process_time == 3


def test_simulate_scenario_matches_simulate_line():
    machine = Machine(name="press", process_time=3)
    scenario = Scenario(
        name="overloaded line",
        minutes=60,
        arrival_rate=1,
        machine=machine,
    )

    assert simulate_scenario(scenario) == simulate_line(60, 1, 3)


def test_machine_stores_name_and_process_time():
    machine = Machine(name="press", process_time=3)

    assert machine.name == "press"
    assert machine.process_time == 3


def test_machine_rejects_invalid_process_time():
    with pytest.raises(ValueError):
        Machine(name="press", process_time=0)


def test_simulate_machine_line_matches_simulate_line():
    machine = Machine(name="press", process_time=3)

    assert simulate_machine_line(60, 1, machine) == simulate_line(60, 1, 3)


def test_classifies_overloaded_line():
    metrics = simulate_line(60, 1, 3)
    assert metrics["line_status"] == "overloaded"


def test_classifies_stable_line():
    metrics = simulate_line(60, 1, 1)
    assert metrics["line_status"] == "stable"


def test_classifies_underused_line():
    metrics = simulate_line(60, 0, 1)
    assert metrics["line_status"] == "underused"
