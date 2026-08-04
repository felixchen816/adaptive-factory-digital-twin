"""Export tools for factory twin simulation data and metrics."""

import json
from pathlib import Path
from typing import Any, Dict, List, Union


def write_rows_to_csv(rows: List[Dict[str, Any]], output_path: Union[str, Path]) -> None:
    """Write scenario results list to a CSV file."""
    if not rows:
        return

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(rows[0].keys())
    with open(output_path, "w", encoding="utf-8") as f:
        # Header
        f.write(",".join(fieldnames) + "\n")
        # Data rows
        for row in rows:
            line = ",".join(str(row.get(field, "")) for field in fieldnames)
            f.write(line + "\n")


def write_metrics_to_json(metrics: Dict[str, Any], output_path: Union[str, Path]) -> None:
    """Write multi-stage simulation metrics dictionary to a formatted JSON file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)