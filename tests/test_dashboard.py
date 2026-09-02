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
                {"minute": 0, "press": 0},
                {"minute": 1, "press": 5},
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
            "queue_history": [],
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


def test_write_dashboard_html_creates_file(tmp_path):
    output_path = tmp_path / "dashboard.html"

    write_dashboard_html(sample_rows(), sample_rows()[1], output_path)

    assert output_path.exists()
    assert "Scenario Comparison" in output_path.read_text(encoding="utf-8")
