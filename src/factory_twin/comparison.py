from factory_twin.bottleneck import explain_line_status
from factory_twin.simple_line import simulate_scenario


def compare_scenarios(scenarios):
    """Run scenarios and return one metrics row per scenario."""
    rows = []

    for scenario in scenarios:
        metrics = simulate_scenario(scenario)
        row = {
            "scenario": scenario.name,
            "machine": scenario.machine.name,
            "process_time": scenario.machine.process_time,
            **metrics,
        }
        row["explanation"] = explain_line_status(row)
        rows.append(row)

    return rows
