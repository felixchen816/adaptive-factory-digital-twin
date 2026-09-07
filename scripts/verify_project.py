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


def main():
    """Run tests, compile checks, demo generation, and artifact inspections."""
    python = _python_executable()

    _run([python, "-m", "pytest", "-q"])
    _run([python, "-m", "compileall", "-q", "src", "tests", "examples"])
    _run([python, "examples/run_simple_line.py"])

    _verify_artifacts_exist()
    _verify_multi_stage_results()
    _verify_report()
    _verify_dashboard()

    print("Project verification passed.")


def _python_executable():
    if PYTHON.exists():
        return str(PYTHON)
    return sys.executable


def _run(command):
    print(f"Running: {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def _verify_artifacts_exist():
    missing = [
        artifact
        for artifact in GENERATED_ARTIFACTS
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


def _require_text(text, required_text, artifact_name):
    missing = [needle for needle in required_text if needle not in text]
    if missing:
        raise AssertionError(
            f"{artifact_name} is missing expected text: {', '.join(missing)}"
        )


if __name__ == "__main__":
    main()
