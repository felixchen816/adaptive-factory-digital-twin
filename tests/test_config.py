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
    assert scenario.line.name == "baseline"
    assert [machine.name for machine in scenario.line.machines] == [
        "cutter",
        "press",
        "inspector",
    ]
    assert scenario.line.bottleneck_machine.name == "press"


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
