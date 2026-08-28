"""Small text chart helpers for simulation reports."""


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
