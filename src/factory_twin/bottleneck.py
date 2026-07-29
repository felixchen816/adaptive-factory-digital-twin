def explain_line_status(row):
    """Return a plain-English explanation for a simulated line status."""
    status = row["line_status"]

    if status == "overloaded":
        return "Backlog is growing because arrivals exceed effective processing capacity."
    if status == "underused":
        return "The machine is underused because demand is too low for available capacity."
    if status == "stable":
        return "The line is stable because demand and processing capacity are balanced."

    raise ValueError(f"unknown line status: {status}")
