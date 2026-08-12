import json
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

    return [
        _build_multi_stage_scenario(scenario_definition)
        for scenario_definition in scenario_definitions
    ]


def _build_multi_stage_scenario(scenario_definition):
    name = scenario_definition.get("name")
    if not name:
        raise ValueError("scenario name is required")

    machine_definitions = scenario_definition.get("machines", [])
    if not machine_definitions:
        raise ValueError("scenario must define at least one machine")

    machines = [
        Machine(
            name=machine_definition["name"],
            process_time=machine_definition["process_time"],
        )
        for machine_definition in machine_definitions
    ]
    line = ProductionLine(name, machines)

    return MultiStageScenario(
        name=name,
        line=line,
        minutes=scenario_definition.get("minutes", 60),
        arrival_rate=scenario_definition.get("arrival_rate", 1.0),
    )
