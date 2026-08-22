import json

from examples.run_simple_line import main


def test_example_accepts_config_and_output_paths(tmp_path):
    config_path = tmp_path / "scenarios.json"
    config_path.write_text(
        json.dumps(
            [
                {
                    "name": "custom baseline",
                    "minutes": 60,
                    "arrival_rate": 1.0,
                    "machines": [
                        {"name": "cutter", "process_time": 1},
                        {"name": "press", "process_time": 3},
                        {"name": "inspector", "process_time": 2},
                    ],
                }
            ]
        ),
        encoding="utf-8",
    )
    multi_stage_json = tmp_path / "multi_stage_results.json"
    multi_stage_report = tmp_path / "multi_stage_report.md"
    simple_csv = tmp_path / "simple_line_results.csv"
    simple_report = tmp_path / "simple_line_report.md"

    main(
        [
            "--multi-stage-config",
            str(config_path),
            "--multi-stage-json",
            str(multi_stage_json),
            "--multi-stage-report",
            str(multi_stage_report),
            "--simple-csv",
            str(simple_csv),
            "--simple-report",
            str(simple_report),
        ]
    )

    assert multi_stage_json.exists()
    assert multi_stage_report.exists()
    assert simple_csv.exists()
    assert simple_report.exists()
    assert "custom baseline" in multi_stage_report.read_text(encoding="utf-8")

    exported_metrics = json.loads(multi_stage_json.read_text(encoding="utf-8"))
    assert exported_metrics["best_improvement"]["target"] == "press"
    assert exported_metrics["best_improvement"]["completed_gain"] > 0
    assert len(exported_metrics["queue_history"]) == 60
    assert exported_metrics["completed_history"][-1]["completed"] == exported_metrics["completed"]
    assert exported_metrics["downtime_events"] == {
        "cutter": 0,
        "press": 0,
        "inspector": 0,
    }
