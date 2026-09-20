"""Run the portfolio-readiness verification checks for the project."""

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON = REPO_ROOT / ".venv" / "bin" / "python"

GENERATED_ARTIFACTS = [
    "simple_line_results.csv",
    "simple_line_report.md",
    "multi_stage_results.json",
    "multi_stage_report.md",
    "multi_stage_history.csv",
    "multi_stage_queue_chart.svg",
    "factory_dashboard.html",
]

TESLA_SCENARIO_ARTIFACTS = [
    "tesla_fremont_model3y_results.json",
    "tesla_fremont_model3y_report.md",
    "tesla_fremont_model3y_history.csv",
    "tesla_fremont_model3y_queue_chart.svg",
    "tesla_fremont_model3y_dashboard.html",
    "tesla_fremont_dynamic_results.json",
    "tesla_fremont_dynamic_report.md",
    "tesla_fremont_dynamic_history.csv",
    "tesla_fremont_dynamic_queue_chart.svg",
    "tesla_fremont_dynamic_dashboard.html",
]


def main():
    """Run tests, compile checks, demo generation, and artifact inspections."""
    python = _python_executable()

    _run([python, "-m", "pytest", "-q"])
    _run([python, "-m", "compileall", "-q", "src", "tests", "examples"])
    _run([python, "examples/run_simple_line.py"])
    _run_real_factory_scenario(python)
    _run_dynamic_factory_scenario(python)

    _verify_artifacts_exist()
    _verify_multi_stage_results()
    _verify_report()
    _verify_dashboard()
    _verify_real_factory_scenario()
    _verify_dynamic_factory_scenario()

    print("Project verification passed.")


def _python_executable():
    if PYTHON.exists():
        return str(PYTHON)
    return sys.executable


def _run(command):
    print(f"Running: {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def _run_real_factory_scenario(python):
    _run(
        [
            python,
            "examples/run_simple_line.py",
            "--multi-stage-config",
            "examples/tesla_fremont_model3y_scenario.json",
            "--multi-stage-json",
            "tesla_fremont_model3y_results.json",
            "--multi-stage-report",
            "tesla_fremont_model3y_report.md",
            "--multi-stage-history-csv",
            "tesla_fremont_model3y_history.csv",
            "--multi-stage-chart-svg",
            "tesla_fremont_model3y_queue_chart.svg",
            "--dashboard-html",
            "tesla_fremont_model3y_dashboard.html",
        ]
    )


def _run_dynamic_factory_scenario(python):
    _run(
        [
            python,
            "examples/run_simple_line.py",
            "--multi-stage-config",
            "examples/tesla_fremont_dynamic_scenario.json",
            "--multi-stage-json",
            "tesla_fremont_dynamic_results.json",
            "--multi-stage-report",
            "tesla_fremont_dynamic_report.md",
            "--multi-stage-history-csv",
            "tesla_fremont_dynamic_history.csv",
            "--multi-stage-chart-svg",
            "tesla_fremont_dynamic_queue_chart.svg",
            "--dashboard-html",
            "tesla_fremont_dynamic_dashboard.html",
        ]
    )


def _verify_artifacts_exist():
    missing = [
        artifact
        for artifact in GENERATED_ARTIFACTS + TESLA_SCENARIO_ARTIFACTS
        if not (REPO_ROOT / artifact).exists()
    ]
    if missing:
        raise AssertionError(f"Missing generated artifacts: {', '.join(missing)}")


def _verify_multi_stage_results():
    path = REPO_ROOT / "multi_stage_results.json"
    metrics = json.loads(path.read_text(encoding="utf-8"))

    required_keys = [
        "completed",
        "arrivals",
        "final_queue_lengths",
        "queue_history",
        "completed_history",
        "queue_bottleneck",
        "recommendation",
        "best_improvement",
    ]
    missing = [key for key in required_keys if key not in metrics]
    if missing:
        raise AssertionError(f"Missing JSON keys: {', '.join(missing)}")

    if not metrics["queue_history"]:
        raise AssertionError("Queue history should not be empty.")
    if not metrics["completed_history"]:
        raise AssertionError("Completed history should not be empty.")
    if not metrics["recommendation"]:
        raise AssertionError("Recommendation should not be empty.")


def _verify_report():
    text = (REPO_ROOT / "multi_stage_report.md").read_text(encoding="utf-8")
    required_text = [
        "# Multi-Stage Production Line Report",
        "## Case Study",
        "## Scenario Results",
        "## Ranked Improvement Options",
        "## Queue Trend Charts",
        "Decision logic prioritized completion rate first",
    ]
    _require_text(text, required_text, "multi_stage_report.md")


def _verify_dashboard():
    text = (REPO_ROOT / "factory_dashboard.html").read_text(encoding="utf-8")
    required_text = [
        "Adaptive Factory Digital Twin",
        "Decision Snapshot",
        "Selected scenario",
        "Primary bottleneck",
        "Recommended action",
        "Executive Summary",
        "Model Assumptions",
        "Limitations",
        "Scenario Comparison",
        "Recommended Improvements",
        "Best Scenario Total WIP",
        "Best Scenario Throughput",
        "Per-Stage Queue Charts",
    ]
    _require_text(text, required_text, "factory_dashboard.html")


def _verify_real_factory_scenario():
    metrics_path = REPO_ROOT / "tesla_fremont_model3y_results.json"
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    annualized_output = metrics["throughput_per_hour"] * 24 * 365
    target_output = 550000
    relative_error = abs(annualized_output - target_output) / target_output

    if metrics["scenario"] != "tesla fremont model 3/y public-capacity baseline":
        raise AssertionError("Tesla Fremont scenario export used the wrong scenario.")
    if relative_error >= 0.01:
        raise AssertionError(
            "Tesla Fremont annualized output is not within 1% of 550,000."
        )
    if len(metrics["queue_history"]) != 10080:
        raise AssertionError("Tesla Fremont queue history should cover seven days.")

    report = (REPO_ROOT / "tesla_fremont_model3y_report.md").read_text(
        encoding="utf-8"
    )
    dashboard = (REPO_ROOT / "tesla_fremont_model3y_dashboard.html").read_text(
        encoding="utf-8"
    )
    _require_text(
        report,
        [
            "tesla fremont model 3/y public-capacity baseline",
            "## Case Study",
            "## Ranked Improvement Options",
        ],
        "tesla_fremont_model3y_report.md",
    )
    _require_text(
        dashboard,
        [
            "Decision Snapshot",
            "tesla fremont model 3/y public-capacity baseline",
            "Recommended Improvements",
        ],
        "tesla_fremont_model3y_dashboard.html",
    )


def _verify_dynamic_factory_scenario():
    metrics_path = REPO_ROOT / "tesla_fremont_dynamic_results.json"
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    arrival_rates = {
        row["arrivals"]
        for row in metrics["arrival_history"]
    }
    paint_queues = [
        row["paint shop"]
        for row in metrics["queue_history"]
    ]

    if metrics["scenario"] != "tesla fremont dynamic surge and failure case":
        raise AssertionError("Dynamic Tesla scenario export used the wrong scenario.")
    if len(arrival_rates) < 4:
        raise AssertionError("Dynamic Tesla scenario should include multiple arrival rates.")
    if max(paint_queues) - min(paint_queues) < 30:
        raise AssertionError("Dynamic Tesla scenario should create varied paint queues.")
    if metrics["downtime_events"]["rear underbody casting"] != 10:
        raise AssertionError("Dynamic Tesla scenario should include casting downtime.")
    if metrics["downtime_events"]["final assembly and end-of-line test"] != 5:
        raise AssertionError("Dynamic Tesla scenario should include final assembly downtime.")

    history_header = (REPO_ROOT / "tesla_fremont_dynamic_history.csv").read_text(
        encoding="utf-8"
    ).splitlines()[0]
    _require_text(
        history_header,
        ["arrivals", "cumulative_arrivals"],
        "tesla_fremont_dynamic_history.csv",
    )
    _require_text(
        (REPO_ROOT / "tesla_fremont_dynamic_dashboard.html").read_text(
            encoding="utf-8"
        ),
        [
            "tesla fremont dynamic surge and failure case",
            "Decision Snapshot",
            "paint shop",
        ],
        "tesla_fremont_dynamic_dashboard.html",
    )


def _require_text(text, required_text, artifact_name):
    missing = [needle for needle in required_text if needle not in text]
    if missing:
        raise AssertionError(
            f"{artifact_name} is missing expected text: {', '.join(missing)}"
        )


if __name__ == "__main__":
    main()
