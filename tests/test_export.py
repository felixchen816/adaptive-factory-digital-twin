import json
from pathlib import Path
from factory_twin.export import write_metrics_to_json, write_rows_to_csv


def test_write_metrics_to_json(tmp_path: Path):
    sample_metrics = {
        "line": "three-stage line",
        "completed": 19,
        "arrivals": 60,
        "throughput_per_hour": 19.0,
        "bottleneck_machine": "press",
        "line_capacity_per_hour": 20.0,
        "final_queue_lengths": {"cutter": 0, "press": 41, "inspector": 0},
        "max_queue_lengths": {"cutter": 0, "press": 41, "inspector": 1},
        "total_wip": 41,
        "queue_bottleneck": "press",
        "recommendation": "Improve press capacity, reduce press process time, add parallel press capacity, or reduce arrivals.",
    }

    json_file = tmp_path / "multi_stage_results.json"
    write_metrics_to_json(sample_metrics, json_file)

    assert json_file.exists()

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["line"] == "three-stage line"
    assert data["completed"] == 19
    assert data["queue_bottleneck"] == "press"
    assert data["final_queue_lengths"]["press"] == 41