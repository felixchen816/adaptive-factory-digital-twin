from factory_twin.machine import Machine
from factory_twin.scenario import Scenario
from factory_twin.simple_line import simulate_scenario


SCENARIOS = [
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
    Scenario(
        name="faster machine",
        minutes=60,
        arrival_rate=1,
        machine=Machine(name="upgraded press", process_time=2),
    ),
]


def main():
    for scenario in SCENARIOS:
        metrics = simulate_scenario(scenario)

        print(f"\nScenario: {scenario.name}")
        print(f"  machine: {scenario.machine.name}")
        print(f"  process_time: {scenario.machine.process_time}")
        print(f"  completed: {metrics['completed']}")
        print(f"  throughput_per_hour: {metrics['throughput_per_hour']}")
        print(f"  average_queue_length: {metrics['average_queue_length']}")
        print(f"  max_queue_length: {metrics['max_queue_length']}")
        print(f"  utilization: {metrics['utilization']}")
        print(f"  queue_growth_rate: {metrics['queue_growth_rate']}")


if __name__ == "__main__":
    main()
