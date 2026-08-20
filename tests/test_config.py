import json

import pytest

from factory_twin.config import load_multi_stage_scenarios


def test_load_multi_stage_scenarios_creates_scenario_objects(tmp_path):
    config_path = tmp_path / "scenarios.json"
    config_path.write_text(
        json.dumps(
            [
                {
                    "name": "baseline",
                    "minutes": 60,
                    "arrival_rate": 1.0,
                    "machines": [
                        {"name": "cutter", "process_time": 1},
                        {"name": "press", "process_time": 3},
                        {"name": "inspector", "process_time": 2},
                    ],
                }
            ]
        ),
        encoding="utf-8",
    )

    scenarios = load_multi_stage_scenarios(config_path)

    assert len(scenarios) == 1
    scenario = scenarios[0]
    assert scenario.name == "baseline"
    assert scenario.minutes == 60
    assert scenario.arrival_rate == 1.0
    assert scenario.improvement_costs == {}
    assert scenario.line.name == "baseline"
    assert [machine.name for machine in scenario.line.machines] == [
        "cutter",
        "press",
        "inspector",
    ]
    assert [machine.parallel_units for machine in scenario.line.machines] == [1, 1, 1]
    assert scenario.line.bottleneck_machine.name == "press"


def test_load_multi_stage_scenarios_loads_parallel_units(tmp_path):
    config_path = tmp_path / "scenarios.json"
    config_path.write_text(
        json.dumps(
            [
                {
                    "name": "parallel press",
                    "machines": [
                        {"name": "cutter", "process_time": 1},
                        {"name": "press", "process_time": 3, "parallel_units": 2},
                        {"name": "inspector", "process_time": 2},
                    ],
                }
            ]
        ),
        encoding="utf-8",
    )

    scenario = load_multi_stage_scenarios(config_path)[0]

    assert scenario.line.machines[1].parallel_units == 2
    assert scenario.line.bottleneck_machine.name == "inspector"


def test_load_multi_stage_scenarios_loads_improvement_costs(tmp_path):
    config_path = tmp_path / "scenarios.json"
    config_path.write_text(
        json.dumps(
            [
                {
                    "name": "baseline",
                    "machines": [{"name": "press", "process_time": 3}],
                    "improvement_costs": {
                        "reduce_process_time": 6,
                        "add_parallel_capacity": 2,
                        "reduce_arrivals": 1,
                    },
                }
            ]
        ),
        encoding="utf-8",
    )

    scenario = load_multi_stage_scenarios(config_path)[0]

    assert scenario.improvement_costs == {
        "reduce_process_time": 6,
        "add_parallel_capacity": 2,
        "reduce_arrivals": 1,
    }


def test_load_multi_stage_scenarios_rejects_missing_name(tmp_path):
    config_path = tmp_path / "scenarios.json"
    config_path.write_text(
        json.dumps(
            [
                {
                    "minutes": 60,
                    "arrival_rate": 1.0,
                    "machines": [{"name": "cutter", "process_time": 1}],
                }
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="scenario name is required"):
        load_multi_stage_scenarios(config_path)


def test_load_multi_stage_scenarios_rejects_empty_machine_list(tmp_path):
    config_path = tmp_path / "scenarios.json"
    config_path.write_text(
        json.dumps(
            [
                {
                    "name": "empty line",
                    "minutes": 60,
                    "arrival_rate": 1.0,
                    "machines": [],
                }
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="at least one machine"):
        load_multi_stage_scenarios(config_path)


def test_load_multi_stage_scenarios_rejects_non_list_config(tmp_path):
    config_path = tmp_path / "scenarios.json"
    config_path.write_text(json.dumps({"name": "baseline"}), encoding="utf-8")

    with pytest.raises(ValueError, match="scenario config must be a list"):
        load_multi_stage_scenarios(config_path)


def test_load_multi_stage_scenarios_rejects_non_object_scenario(tmp_path):
    config_path = tmp_path / "scenarios.json"
    config_path.write_text(json.dumps(["baseline"]), encoding="utf-8")

    with pytest.raises(ValueError, match="each scenario must be an object"):
        load_multi_stage_scenarios(config_path)


def test_load_multi_stage_scenarios_rejects_duplicate_scenario_names(tmp_path):
    config_path = tmp_path / "scenarios.json"
    config_path.write_text(
        json.dumps(
            [
                {
                    "name": "baseline",
                    "machines": [{"name": "cutter", "process_time": 1}],
                },
                {
                    "name": "baseline",
                    "machines": [{"name": "press", "process_time": 3}],
                },
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="duplicate scenario name: baseline"):
        load_multi_stage_scenarios(config_path)


def test_load_multi_stage_scenarios_rejects_negative_minutes(tmp_path):
    config_path = tmp_path / "scenarios.json"
    config_path.write_text(
        json.dumps(
            [
                {
                    "name": "bad minutes",
                    "minutes": -1,
                    "machines": [{"name": "cutter", "process_time": 1}],
                }
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="minutes must be non-negative"):
        load_multi_stage_scenarios(config_path)


def test_load_multi_stage_scenarios_rejects_negative_arrival_rate(tmp_path):
    config_path = tmp_path / "scenarios.json"
    config_path.write_text(
        json.dumps(
            [
                {
                    "name": "bad arrivals",
                    "arrival_rate": -1,
                    "machines": [{"name": "cutter", "process_time": 1}],
                }
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="arrival_rate must be non-negative"):
        load_multi_stage_scenarios(config_path)


def test_load_multi_stage_scenarios_rejects_missing_machine_name(tmp_path):
    config_path = tmp_path / "scenarios.json"
    config_path.write_text(
        json.dumps(
            [
                {
                    "name": "missing machine name",
                    "machines": [{"process_time": 1}],
                }
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="machine name is required"):
        load_multi_stage_scenarios(config_path)


def test_load_multi_stage_scenarios_rejects_missing_machine_process_time(tmp_path):
    config_path = tmp_path / "scenarios.json"
    config_path.write_text(
        json.dumps(
            [
                {
                    "name": "missing process time",
                    "machines": [{"name": "cutter"}],
                }
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="machine process_time is required"):
        load_multi_stage_scenarios(config_path)


def test_load_multi_stage_scenarios_rejects_non_positive_machine_process_time(tmp_path):
    config_path = tmp_path / "scenarios.json"
    config_path.write_text(
        json.dumps(
            [
                {
                    "name": "bad process time",
                    "machines": [{"name": "cutter", "process_time": 0}],
                }
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="machine process_time must be positive"):
        load_multi_stage_scenarios(config_path)


def test_load_multi_stage_scenarios_rejects_non_positive_parallel_units(tmp_path):
    config_path = tmp_path / "scenarios.json"
    config_path.write_text(
        json.dumps(
            [
                {
                    "name": "bad parallel units",
                    "machines": [
                        {
                            "name": "press",
                            "process_time": 3,
                            "parallel_units": 0,
                        }
                    ],
                }
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="machine parallel_units must be positive"):
        load_multi_stage_scenarios(config_path)


def test_load_multi_stage_scenarios_rejects_non_object_improvement_costs(tmp_path):
    config_path = tmp_path / "scenarios.json"
    config_path.write_text(
        json.dumps(
            [
                {
                    "name": "bad costs",
                    "machines": [{"name": "press", "process_time": 3}],
                    "improvement_costs": ["reduce_process_time"],
                }
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="improvement_costs must be an object"):
        load_multi_stage_scenarios(config_path)


def test_load_multi_stage_scenarios_rejects_non_positive_improvement_cost(tmp_path):
    config_path = tmp_path / "scenarios.json"
    config_path.write_text(
        json.dumps(
            [
                {
                    "name": "bad costs",
                    "machines": [{"name": "press", "process_time": 3}],
                    "improvement_costs": {"reduce_process_time": 0},
                }
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="improvement cost reduce_process_time must be positive",
    ):
        load_multi_stage_scenarios(config_path)
