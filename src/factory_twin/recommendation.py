def recommend_action(row):
    """Return a practical next action for a simulated line status."""
    status = row["line_status"]

    if status == "overloaded":
        return "Increase capacity, reduce process time, or lower arrivals to stop backlog growth."
    if status == "underused":
        return "Reallocate capacity or increase demand so the machine is not sitting idle."
    if status == "stable":
        return "Keep the current setup and monitor queue growth over time."

    raise ValueError(f"unknown line status: {status}")
