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
        "| Scenario | Completed | Arrivals | Completion Rate | Throughput/hr | Total WIP | Largest Final Queue | Largest Max Queue | WIP/Completed | Bottleneck Machine | Queue Bottleneck | Recommendation |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]

    for row in rows:
        lines.append(
            f"| {row['scenario']} | {row['completed']} | {row['arrivals']} | "
            f"{_format_number(row['completion_rate'])} | "
            f"{_format_number(row['throughput_per_hour'])} | "
            f"{row['total_wip']} | {row['largest_final_queue']} | "
            f"{row['largest_max_queue']} | "
            f"{_format_number(row['wip_per_completed_part'])} | "
            f"{row['bottleneck_machine']} | {row['queue_bottleneck']} | "
            f"{row['recommendation']} |"
        )

    lines.append("")
    return "\n".join(lines)


def _format_number(value):
    if isinstance(value, float):
        return f"{value:.2f}"
    return value
