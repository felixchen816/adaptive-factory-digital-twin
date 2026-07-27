from factory_twin.comparison import compare_scenarios
from factory_twin.decision import choose_best_scenario
from factory_twin.export import write_rows_to_csv
from factory_twin.machine import Machine
from factory_twin.scenario import Scenario


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
    Scenario(
        name="underused line",
        minutes=60,
        arrival_rate=0,
        machine=Machine(name="idle cutter", process_time=1),
    ),
]


def main():
    rows = compare_scenarios(SCENARIOS)
    for row in rows:
        print(f"\nScenario: {row['scenario']}")
        print(f"  machine: {row['machine']}")
        print(f"  process_time: {row['process_time']}")
        print(f"  completed: {row['completed']}")
        print(f"  throughput_per_hour: {row['throughput_per_hour']}")
        print(f"  average_queue_length: {row['average_queue_length']}")
        print(f"  max_queue_length: {row['max_queue_length']}")
        print(f"  utilization: {row['utilization']}")
        print(f"  queue_growth_rate: {row['queue_growth_rate']}")
        print(f"  line_status: {row['line_status']}")

    best = choose_best_scenario(rows)
    print(f"\nBest scenario: {best['scenario']}")

    write_rows_to_csv(rows, "simple_line_results.csv")
    print("\nWrote results to simple_line_results.csv")


if __name__ == "__main__":
    main()
