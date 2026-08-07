def build_multi_stage_report(rows, best):
    """Build a Markdown report for multi-stage scenario comparisons."""
    lines = [
        "# Multi-Stage Production Line Report",
        "",
        "## Recommendation",
        "",
        f"Best scenario: {best['scenario']}",
        "",
        "## Scenario Results",
        "",
        "| Scenario | Completed | Arrivals | Throughput/hr | Total WIP | Bottleneck Machine | Queue Bottleneck | Recommendation |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]

    for row in rows:
        lines.append(
            f"| {row['scenario']} | {row['completed']} | {row['arrivals']} | "
            f"{row['throughput_per_hour']} | {row['total_wip']} | "
            f"{row['bottleneck_machine']} | {row['queue_bottleneck']} | "
            f"{row['recommendation']} |"
        )

    lines.append("")
    return "\n".join(lines)
