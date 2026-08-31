"""Small chart helpers for simulation reports."""

from html import escape
from pathlib import Path


def build_queue_trend_chart(queue_history, stage, width=24):
    """Build a compact ASCII bar chart for one stage queue over time."""
    if not queue_history:
        return "No queue history available."

    values = [
        row.get(stage, 0)
        for row in queue_history
    ]
    max_value = max(values)
    lines = [f"{stage} queue trend"]

    for row in _sample_rows(queue_history):
        minute = row["minute"]
        value = row.get(stage, 0)
        bar = _bar(value, max_value, width)
        lines.append(f"{minute:02d} | {bar} {value}")

    return "\n".join(lines)


def _sample_rows(rows, max_rows=8):
    if len(rows) <= max_rows:
        return rows

    step = (len(rows) - 1) / (max_rows - 1)
    sampled_indexes = [
        round(index * step)
        for index in range(max_rows)
    ]
    return [
        rows[index]
        for index in sampled_indexes
    ]


def _bar(value, max_value, width):
    if max_value <= 0:
        return ""

    bar_width = round(value / max_value * width)
    return "#" * bar_width


def build_queue_trend_svg(queue_history, stage, width=640, height=320):
    """Build an SVG line chart for one stage queue over time."""
    if not queue_history:
        return _empty_svg("No queue history available.", width, height)

    values = [
        row.get(stage, 0)
        for row in queue_history
    ]
    max_value = max(values) or 1
    max_minute = max(row["minute"] for row in queue_history) or 1
    margin = 40
    chart_width = width - margin * 2
    chart_height = height - margin * 2

    points = []
    for row in queue_history:
        x = margin + row["minute"] / max_minute * chart_width
        y = height - margin - row.get(stage, 0) / max_value * chart_height
        points.append(f"{x:.1f},{y:.1f}")

    title = escape(f"{stage} queue trend")
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<rect width="100%" height="100%" fill="white"/>',
            f'<text x="{margin}" y="24" font-family="Arial" font-size="18">{title}</text>',
            f'<line x1="{margin}" y1="{height - margin}" x2="{width - margin}" y2="{height - margin}" stroke="#333"/>',
            f'<line x1="{margin}" y1="{margin}" x2="{margin}" y2="{height - margin}" stroke="#333"/>',
            f'<polyline fill="none" stroke="#2563eb" stroke-width="3" points="{" ".join(points)}"/>',
            f'<text x="{margin}" y="{height - 12}" font-family="Arial" font-size="12">minute</text>',
            f'<text x="8" y="{margin}" font-family="Arial" font-size="12">queue</text>',
            "</svg>",
        ]
    )


def write_queue_trend_svg(queue_history, stage, output_path):
    """Write an SVG queue trend chart to disk."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        build_queue_trend_svg(queue_history, stage),
        encoding="utf-8",
    )


def _empty_svg(message, width, height):
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '<rect width="100%" height="100%" fill="white"/>',
            f'<text x="24" y="40" font-family="Arial" font-size="16">{escape(message)}</text>',
            "</svg>",
        ]
    )
