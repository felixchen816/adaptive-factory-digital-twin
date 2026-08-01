def build_markdown_report(rows, best):
    lines = [
        "# Simple Line Scenario Report",
        "",
        "## Recommendation",
        "",
        f"Best scenario: {best['scenario']}",
        "",
        "## Scenario Results",
        "",
        "| Scenario | Machine | Status | Throughput/hr | Demand/hr | Capacity/hr | Capacity Gap/hr | Avg Queue | Max Queue | Explanation | Recommendation |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]

    for row in rows:
        lines.append(
            f"| {row['scenario']} | {row['machine']} | {row['line_status']} | "
            f"{row['throughput_per_hour']} | {row['demand_per_hour']} | "
            f"{row['capacity_per_hour']} | {row['capacity_gap_per_hour']} | "
            f"{row['average_queue_length']} | {row['max_queue_length']} | "
            f"{row['explanation']} | "
            f"{row['recommendation']} |"
        )

    lines.append("")
    return "\n".join(lines)
