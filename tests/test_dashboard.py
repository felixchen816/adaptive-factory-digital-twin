from factory_twin.dashboard import build_dashboard_html, write_dashboard_html


def sample_rows():
    return [
        {
            "scenario": "baseline",
            "completed": 19,
            "arrivals": 60,
            "completion_rate": 19 / 60,
            "throughput_per_hour": 19.0,
            "total_wip": 41,
            "queue_bottleneck": "press",
            "best_improvement": {
                "summary": "Improve press by reducing process time.",
                "completed_gain": 9,
                "benefit_per_cost": 4.5,
                "net_value": 43,
            },
            "matching_scenario": "faster press",
            "queue_history": [
                {"minute": 0, "cutter": 0, "press": 0},
                {"minute": 1, "cutter": 0, "press": 5},
            ],
            "completed_history": [
                {"minute": 0, "completed": 0},
                {"minute": 1, "completed": 1},
            ],
        },
        {
            "scenario": "faster press",
            "completed": 28,
            "arrivals": 60,
            "completion_rate": 28 / 60,
            "throughput_per_hour": 28.0,
            "total_wip": 32,
            "queue_bottleneck": "press",
            "best_improvement": None,
            "matching_scenario": None,
            "queue_history": [
                {"minute": 0, "cutter": 0, "press": 0},
                {"minute": 1, "cutter": 0, "press": 2},
            ],
            "completed_history": [
                {"minute": 0, "completed": 0},
                {"minute": 1, "completed": 2},
            ],
        },
    ]


def test_build_dashboard_html_contains_summary_and_chart():
    html = build_dashboard_html(sample_rows(), sample_rows()[1])

    assert "<!doctype html>" in html
    assert "Adaptive Factory Digital Twin" in html
    assert "Best Scenario" in html
    assert "faster press" in html
    assert "Improve press by reducing process time." in html
    assert "<svg" in html
    assert "Executive Summary" in html
    assert "Model Assumptions" in html
    assert "Arrivals use a fixed average rate" in html
    assert "Limitations" in html
    assert "deterministic" in html
    assert "Total WIP" in html
    assert "Completed parts trend" in html
    assert "Per-Stage Queue Charts" in html


def test_write_dashboard_html_creates_file(tmp_path):
    output_path = tmp_path / "dashboard.html"

    write_dashboard_html(sample_rows(), sample_rows()[1], output_path)

    assert output_path.exists()
    assert "Scenario Comparison" in output_path.read_text(encoding="utf-8")
