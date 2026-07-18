from factory_twin.simple_line import simulate_line


SCENARIOS = [
    {
        "name": "balanced line",
        "minutes": 60,
        "arrival_rate": 1,
        "process_time": 1,
    },
    {
        "name": "overloaded line",
        "minutes": 60,
        "arrival_rate": 1,
        "process_time": 3,
    },
    {
        "name": "faster machine",
        "minutes": 60,
        "arrival_rate": 1,
        "process_time": 2,
    },
]


def main():
    for scenario in SCENARIOS:
        metrics = simulate_line(
            scenario["minutes"],
            scenario["arrival_rate"],
            scenario["process_time"],
        )

        print(f"\nScenario: {scenario['name']}")
        print(f"  completed: {metrics['completed']}")
        print(f"  throughput_per_hour: {metrics['throughput_per_hour']}")
        print(f"  average_queue_length: {metrics['average_queue_length']}")
        print(f"  max_queue_length: {metrics['max_queue_length']}")
        print(f"  utilization: {metrics['utilization']}")
        print(f"  queue_growth_rate: {metrics['queue_growth_rate']}")


if __name__ == "__main__":
    main()