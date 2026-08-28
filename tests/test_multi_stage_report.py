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
            "best_improvement": {
                "summary": "Improve press by reducing process time.",
                "completed_gain": 9,
                "benefit_per_cost": 4.5,
                "estimated_value": 45,
                "net_value": 43,
            },
            "matching_scenario": "faster press",
            "queue_history": [
                {"minute": 0, "press": 0},
                {"minute": 1, "press": 5},
            ],
            "improvement_options": [
                {
                    "rank": 1,
                    "option": "reduce process time",
                    "target": "press",
                    "cost": 2,
                    "completed_gain": 9,
                    "wip_reduction": 9,
                    "benefit_per_cost": 4.5,
                    "estimated_value": 45,
                    "net_value": 43,
                    "summary": "Improve press by reducing process time.",
                },
                {
                    "rank": 2,
                    "option": "add parallel capacity",
                    "target": "press",
                    "cost": 4,
                    "completed_gain": 9,
                    "wip_reduction": 9,
                    "benefit_per_cost": 2.25,
                    "estimated_value": 45,
                    "net_value": 41,
                    "summary": "Improve press by adding parallel capacity.",
                },
            ],
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
            "best_improvement": {
                "summary": "Improve press by adding parallel capacity.",
                "completed_gain": 6,
                "benefit_per_cost": 2.0,
                "estimated_value": 30,
                "net_value": 26,
            },
            "matching_scenario": None,
            "queue_history": [],
            "improvement_options": [],
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
    assert "Best Improvement" in report
    assert "Improve press by reducing process time." in report
    assert "## Ranked Improvement Options" in report
    assert "Matching Scenario" in report
    assert "| baseline | 1 | reduce process time | press | 2 | 9 | 9 | 4.50 | 45 | 43 |" in report
    assert "## Queue Trend Charts" in report
    assert "baseline - press" in report


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
            "best_improvement": {
                "summary": "Improve press by reducing process time.",
                "completed_gain": 9,
                "benefit_per_cost": 4.5,
                "estimated_value": 45,
                "net_value": 43,
            },
            "matching_scenario": "faster press",
            "queue_history": [
                {"minute": 0, "press": 0},
                {"minute": 1, "press": 5},
            ],
            "improvement_options": [
                {
                    "rank": 1,
                    "option": "reduce process time",
                    "target": "press",
                    "cost": 2,
                    "completed_gain": 9,
                    "wip_reduction": 9,
                    "benefit_per_cost": 4.5,
                    "estimated_value": 45,
                    "net_value": 43,
                    "summary": "Improve press by reducing process time.",
                }
            ],
        }
    ]

    report = build_multi_stage_report(rows, rows[0])

    assert "| Scenario | Completed | Arrivals | Completion Rate |" in report
    assert "| baseline | 19 | 60 |" in report
    assert "| 41 | 41 |" in report
    assert "| Improve press by reducing process time. | 9 | 4.50 |" in report
