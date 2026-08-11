from factory_twin.multi_stage_report import build_multi_stage_report


def test_build_multi_stage_report_contains_recommendation_and_results():
    rows = [
        {
            "scenario": "baseline",
            "completed": 19,
            "arrivals": 60,
            "completion_rate": 19 / 60,
            "throughput_per_hour": 19.0,
            "total_wip": 41,
            "largest_final_queue": 41,
            "largest_max_queue": 41,
            "wip_per_completed_part": 41 / 19,
            "bottleneck_machine": "press",
            "queue_bottleneck": "press",
            "recommendation": "Improve press capacity.",
        },
        {
            "scenario": "faster press",
            "completed": 28,
            "arrivals": 60,
            "completion_rate": 28 / 60,
            "throughput_per_hour": 28.0,
            "total_wip": 32,
            "largest_final_queue": 31,
            "largest_max_queue": 32,
            "wip_per_completed_part": 32 / 28,
            "bottleneck_machine": "press",
            "queue_bottleneck": "press",
            "recommendation": "Monitor queue growth.",
        },
    ]

    report = build_multi_stage_report(rows, rows[1])

    assert "# Multi-Stage Production Line Report" in report
    assert "Best scenario: faster press" in report
    assert "baseline" in report
    assert "faster press" in report
    assert "Completion Rate" in report
    assert "Largest Max Queue" in report
    assert "0.47" in report
    assert "Queue Bottleneck" in report
    assert "Improve press capacity." in report


def test_build_multi_stage_report_formats_markdown_table():
    rows = [
        {
            "scenario": "baseline",
            "completed": 19,
            "arrivals": 60,
            "completion_rate": 19 / 60,
            "throughput_per_hour": 19.0,
            "total_wip": 41,
            "largest_final_queue": 41,
            "largest_max_queue": 41,
            "wip_per_completed_part": 41 / 19,
            "bottleneck_machine": "press",
            "queue_bottleneck": "press",
            "recommendation": "Improve press capacity.",
        }
    ]

    report = build_multi_stage_report(rows, rows[0])

    assert "| Scenario | Completed | Arrivals | Completion Rate |" in report
    assert "| baseline | 19 | 60 |" in report
    assert "| 41 | 41 |" in report
