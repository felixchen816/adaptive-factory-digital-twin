def choose_best_scenario(rows):
    """Choose the highest-throughput scenario while avoiding overloaded lines."""
    if not rows:
        raise ValueError("rows must not be empty")

    non_overloaded = [
        row for row in rows
        if row["line_status"] != "overloaded"
    ]
    candidates = non_overloaded if non_overloaded else rows

    return max(
        candidates,
        key=lambda row: row["throughput_per_hour"],
    )
