from factory_twin.simple_line import simulate_scenario


def compare_scenarios(scenarios):
    """Run scenarios and return one metrics row per scenario."""
    rows = []

    for scenario in scenarios:
        metrics = simulate_scenario(scenario)
        rows.append(
            {
                "scenario": scenario.name,
                "machine": scenario.machine.name,
                "process_time": scenario.machine.process_time,
                **metrics,
            }
        )

    return rows
