"""Export tools for factory twin simulation data and metrics."""

import csv
import json
from pathlib import Path


def write_rows_to_csv(rows, output_path):
    """Write comparison rows to a CSV file."""
    if not rows:
        return

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = rows[0].keys()

    with open(output_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_metrics_to_json(metrics, output_path):
    """Write multi-stage simulation metrics dictionary to a formatted JSON file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(metrics, json_file, indent=4)


def write_time_series_to_csv(queue_history, completed_history, output_path):
    """Write queue and completed histories to a single CSV file."""
    if not queue_history:
        return

    completed_by_minute = {
        row["minute"]: row["completed"]
        for row in completed_history
    }
    rows = []
    for queue_row in queue_history:
        row = dict(queue_row)
        row["completed"] = completed_by_minute.get(row["minute"], 0)
        rows.append(row)

    write_rows_to_csv(rows, output_path)
