import argparse
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from factory_twin.comparison import compare_scenarios
from factory_twin.config import load_multi_stage_scenarios
from factory_twin.decision import choose_best_scenario
from factory_twin.export import write_metrics_to_json, write_rows_to_csv
from factory_twin.line import ProductionLine
from factory_twin.line_analysis import (
    explain_queue_bottleneck,
    find_queue_bottleneck,
    recommend_line_action,
)
from factory_twin.machine import Machine
from factory_twin.multi_stage import simulate_production_line
from factory_twin.multi_stage_comparison import compare_multi_stage_scenarios
from factory_twin.multi_stage_decision import choose_best_multi_stage_scenario
from factory_twin.multi_stage_report import build_multi_stage_report
from factory_twin.report import build_markdown_report
from factory_twin.scenario import Scenario


THREE_STAGE_LINE = ProductionLine(
    "three-stage line",
    [
        Machine(name="cutter", process_time=1),
        Machine(name="press", process_time=3),
        Machine(name="inspector", process_time=2),
    ],
)

MULTI_STAGE_CONFIG_PATH = REPO_ROOT / "examples" / "multi_stage_scenarios.json"

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


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Run factory twin one-machine and multi-stage demos."
    )
    parser.add_argument(
        "--multi-stage-config",
        default=MULTI_STAGE_CONFIG_PATH,
        type=Path,
        help="Path to a multi-stage scenario JSON file.",
    )
    parser.add_argument(
        "--multi-stage-json",
        default=REPO_ROOT / "multi_stage_results.json",
        type=Path,
        help="Output path for multi-stage JSON metrics.",
    )
    parser.add_argument(
        "--multi-stage-report",
        default=REPO_ROOT / "multi_stage_report.md",
        type=Path,
        help="Output path for the multi-stage Markdown report.",
    )
    parser.add_argument(
        "--simple-csv",
        default=REPO_ROOT / "simple_line_results.csv",
        type=Path,
        help="Output path for one-machine scenario CSV results.",
    )
    parser.add_argument(
        "--simple-report",
        default=REPO_ROOT / "simple_line_report.md",
        type=Path,
        help="Output path for the one-machine Markdown report.",
    )
    args, _unknown_args = parser.parse_known_args(argv)
    return args


def main(argv=None):
    args = parse_args(argv)
    rows = compare_scenarios(SCENARIOS)
    multi_stage_metrics = simulate_production_line(THREE_STAGE_LINE, 60, 1)

    # Queue bottleneck analysis for multi-stage line
    final_queues = multi_stage_metrics["final_queue_lengths"]
    queue_bottleneck = find_queue_bottleneck(final_queues)
    queue_explanation = explain_queue_bottleneck(final_queues)
    line_recommendation = recommend_line_action(final_queues)

    print(
        f"Three-stage bottleneck: {THREE_STAGE_LINE.bottleneck_machine.name} "
        f"({THREE_STAGE_LINE.capacity_per_hour} parts/hour)"
    )
    print(f"Three-stage completed: {multi_stage_metrics['completed']}")
    print(f"Three-stage final queues: {multi_stage_metrics['final_queue_lengths']}")
    print(f"Three-stage max queues: {multi_stage_metrics['max_queue_lengths']}")
    print(f"Queue bottleneck: {queue_bottleneck}")
    print(f"Explanation: {queue_explanation}")
    print(f"Line recommendation: {line_recommendation}")

    # Print multi-stage comparison
    multi_stage_scenarios = load_multi_stage_scenarios(args.multi_stage_config)
    ms_rows = compare_multi_stage_scenarios(multi_stage_scenarios)
    print("\nMulti-stage scenario comparison")
    for row in ms_rows:
        print(
            f"{row['scenario']}: completed={row['completed']}, "
            f"completion_rate={row['completion_rate']:.2f}, "
            f"largest_queue={row['largest_final_queue']}, "
            f"bottleneck={row['queue_bottleneck']}, "
            f"total_wip={row['total_wip']}"
        )
    best_multi_stage = choose_best_multi_stage_scenario(ms_rows)
    print(f"Best multi-stage scenario: {best_multi_stage['scenario']}")

    multi_stage_report = build_multi_stage_report(ms_rows, best_multi_stage)
    with open(args.multi_stage_report, "w", encoding="utf-8") as report_file:
        report_file.write(multi_stage_report)
    print(f"Wrote report to {args.multi_stage_report.name}")

    # Build multi-stage export dictionary matching expected schema
    multi_stage_results = {
        "line": THREE_STAGE_LINE.name,
        "completed": multi_stage_metrics["completed"],
        "arrivals": multi_stage_metrics.get("arrivals", 60),
        "throughput_per_hour": float(multi_stage_metrics["completed"]),
        "bottleneck_machine": THREE_STAGE_LINE.bottleneck_machine.name,
        "line_capacity_per_hour": float(THREE_STAGE_LINE.capacity_per_hour),
        "final_queue_lengths": final_queues,
        "max_queue_lengths": multi_stage_metrics["max_queue_lengths"],
        "total_wip": sum(final_queues.values()),
        "queue_bottleneck": queue_bottleneck,
        "recommendation": line_recommendation,
    }

    # Save multi-stage results JSON
    write_metrics_to_json(multi_stage_results, args.multi_stage_json)
    print(f"\nWrote results to {args.multi_stage_json.name}")

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

    write_rows_to_csv(rows, args.simple_csv)
    print(f"\nWrote results to {args.simple_csv.name}")

    report = build_markdown_report(rows, best)
    with open(args.simple_report, "w", encoding="utf-8") as report_file:
        report_file.write(report)
    print(f"Wrote report to {args.simple_report.name}")


if __name__ == "__main__":
    main()
