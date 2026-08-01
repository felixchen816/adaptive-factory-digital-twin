from pathlib import Path

from factory_twin.comparison import compare_scenarios
from factory_twin.decision import choose_best_scenario
from factory_twin.export import write_rows_to_csv
from factory_twin.line import ProductionLine
from factory_twin.machine import Machine
from factory_twin.report import build_markdown_report
from factory_twin.scenario import Scenario


REPO_ROOT = Path(__file__).resolve().parents[1]

THREE_STAGE_LINE = ProductionLine(
    "three-stage line",
    [
        Machine(name="cutter", process_time=1),
        Machine(name="press", process_time=3),
        Machine(name="inspector", process_time=2),
    ],
)

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
        name="three-stage line",
        minutes=60,
        arrival_rate=1,
        machine=THREE_STAGE_LINE.bottleneck_machine,
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
    print(
        f"Three-stage bottleneck: {THREE_STAGE_LINE.bottleneck_machine.name} "
        f"({THREE_STAGE_LINE.capacity_per_hour} parts/hour)"
    )

    for row in rows:
        print(f"\nScenario: {row['scenario']}")
        print(f"  machine: {row['machine']}")
        print(f"  process_time: {row['process_time']}")
        print(f"  completed: {row['completed']}")
        print(f"  throughput_per_hour: {row['throughput_per_hour']}")
        print(f"  demand_per_hour: {row['demand_per_hour']}")
        print(f"  capacity_per_hour: {row['capacity_per_hour']}")
        print(f"  capacity_gap_per_hour: {row['capacity_gap_per_hour']}")
        print(f"  average_queue_length: {row['average_queue_length']}")
        print(f"  max_queue_length: {row['max_queue_length']}")
        print(f"  utilization: {row['utilization']}")
        print(f"  queue_growth_rate: {row['queue_growth_rate']}")
        print(f"  line_status: {row['line_status']}")
        print(f"  explanation: {row['explanation']}")
        print(f"  recommendation: {row['recommendation']}")

    best = choose_best_scenario(rows)
    print(f"\nBest scenario: {best['scenario']}")

    csv_path = REPO_ROOT / "simple_line_results.csv"
    write_rows_to_csv(rows, csv_path)
    print("\nWrote results to simple_line_results.csv")

    report = build_markdown_report(rows, best)
    report_path = REPO_ROOT / "simple_line_report.md"
    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write(report)
    print("Wrote report to simple_line_report.md")


if __name__ == "__main__":
    main()
