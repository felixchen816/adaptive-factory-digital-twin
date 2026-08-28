from factory_twin.chart import build_queue_trend_chart


def test_build_queue_trend_chart_samples_history():
    queue_history = [
        {"minute": 0, "press": 0},
        {"minute": 1, "press": 3},
        {"minute": 2, "press": 6},
    ]

    chart = build_queue_trend_chart(queue_history, "press", width=6)

    assert "press queue trend" in chart
    assert "00 |" in chart
    assert "02 | ###### 6" in chart


def test_build_queue_trend_chart_handles_missing_history():
    chart = build_queue_trend_chart([], "press")

    assert chart == "No queue history available."
