import json
from numbers import Number
from pathlib import Path

from factory_twin.line import ProductionLine
from factory_twin.machine import Machine
from factory_twin.multi_stage_comparison import MultiStageScenario


def load_multi_stage_scenarios(path):
    """Load multi-stage scenario definitions from a JSON file."""
    with open(Path(path), encoding="utf-8") as config_file:
        scenario_definitions = json.load(config_file)

    if not isinstance(scenario_definitions, list):
        raise ValueError("scenario config must be a list")

    scenario_names = set()
    scenarios = []
    for scenario_definition in scenario_definitions:
        scenario = _build_multi_stage_scenario(scenario_definition)
        if scenario.name in scenario_names:
            raise ValueError(f"duplicate scenario name: {scenario.name}")
        scenario_names.add(scenario.name)
        scenarios.append(scenario)

    return scenarios


def _build_multi_stage_scenario(scenario_definition):
    if not isinstance(scenario_definition, dict):
        raise ValueError("each scenario must be an object")

    name = _required_non_empty_string(scenario_definition, "name", "scenario")
    minutes = _optional_non_negative_number(scenario_definition, "minutes", 60)
    arrival_rate = _optional_non_negative_number(
        scenario_definition,
        "arrival_rate",
        1.0,
    )

    machine_definitions = scenario_definition.get("machines", [])
    if not isinstance(machine_definitions, list) or not machine_definitions:
        raise ValueError("scenario must define at least one machine")

    machines = [
        _build_machine(machine_definition)
        for machine_definition in machine_definitions
    ]
    line = ProductionLine(name, machines)

    return MultiStageScenario(
        name=name,
        line=line,
        minutes=minutes,
        arrival_rate=arrival_rate,
    )


def _build_machine(machine_definition):
    if not isinstance(machine_definition, dict):
        raise ValueError("each machine must be an object")

    name = _required_non_empty_string(machine_definition, "name", "machine")
    process_time = _required_positive_number(
        machine_definition,
        "process_time",
        "machine",
    )
    return Machine(name=name, process_time=process_time)


def _required_non_empty_string(data, field_name, object_name):
    value = data.get(field_name)
    if not isinstance(value, str) or not value.strip():
        if object_name == "scenario" and field_name == "name":
            raise ValueError("scenario name is required")
        raise ValueError(f"{object_name} {field_name} is required")
    return value.strip()


def _optional_non_negative_number(data, field_name, default):
    if field_name not in data:
        return default

    value = data[field_name]
    if not _is_number(value) or value < 0:
        raise ValueError(f"{field_name} must be non-negative")
    return value


def _required_positive_number(data, field_name, object_name):
    if field_name not in data:
        raise ValueError(f"{object_name} {field_name} is required")

    value = data[field_name]
    if not _is_number(value) or value <= 0:
        raise ValueError(f"{object_name} {field_name} must be positive")
    return value


def _is_number(value):
    return isinstance(value, Number) and not isinstance(value, bool)
