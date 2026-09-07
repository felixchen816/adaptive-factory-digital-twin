from factory_twin.chart import (
    build_completed_trend_svg,
    build_stage_queue_svgs,
    build_total_wip_svg,
    build_queue_trend_chart,
    build_queue_trend_svg,
    write_queue_trend_svg,
)


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


def test_build_queue_trend_svg_contains_line_chart():
    queue_history = [
        {"minute": 0, "press": 0},
        {"minute": 1, "press": 3},
        {"minute": 2, "press": 6},
    ]

    svg = build_queue_trend_svg(queue_history, "press")

    assert svg.startswith("<svg")
    assert "<polyline" in svg
    assert "press queue trend" in svg


def test_write_queue_trend_svg_creates_file(tmp_path):
    queue_history = [
        {"minute": 0, "press": 0},
        {"minute": 1, "press": 3},
    ]
    output_path = tmp_path / "queue.svg"

    write_queue_trend_svg(queue_history, "press", output_path)

    assert output_path.exists()
    assert "<svg" in output_path.read_text(encoding="utf-8")


def test_build_stage_queue_svgs_returns_one_chart_per_stage():
    queue_history = [
        {"minute": 0, "cutter": 0, "press": 1},
        {"minute": 1, "cutter": 0, "press": 2},
    ]

    charts = build_stage_queue_svgs(queue_history)

    assert set(charts) == {"cutter", "press"}
    assert "cutter queue trend" in charts["cutter"]
    assert "press queue trend" in charts["press"]


def test_build_total_wip_svg_sums_stage_queues():
    queue_history = [
        {"minute": 0, "cutter": 1, "press": 2},
        {"minute": 1, "cutter": 2, "press": 4},
    ]

    svg = build_total_wip_svg(queue_history)

    assert "Total WIP trend" in svg
    assert "<polyline" in svg


def test_build_completed_trend_svg_uses_completed_history():
    completed_history = [
        {"minute": 0, "completed": 0},
        {"minute": 1, "completed": 2},
    ]

    svg = build_completed_trend_svg(completed_history)

    assert "Completed parts trend" in svg
    assert "<polyline" in svg
