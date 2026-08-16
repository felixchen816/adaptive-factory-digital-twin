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
        "| Scenario | Completed | Arrivals | Completion Rate | Throughput/hr | Total WIP | Largest Final Queue | Largest Max Queue | WIP/Completed | Bottleneck Machine | Queue Bottleneck | Recommendation | Best Improvement | Completed Gain | Benefit/Cost |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | ---: | ---: |",
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
            f"{row['recommendation']} | "
            f"{_improvement_summary(row)} | {_improvement_gain(row)} | "
            f"{_format_number(_improvement_benefit_per_cost(row))} |"
        )

    lines.append("")
    return "\n".join(lines)


def _format_number(value):
    if isinstance(value, float):
        return f"{value:.2f}"
    return value


def _improvement_summary(row):
    best_improvement = row.get("best_improvement")
    if not best_improvement:
        return "No change needed."
    return best_improvement["summary"]


def _improvement_gain(row):
    best_improvement = row.get("best_improvement")
    if not best_improvement:
        return 0
    return best_improvement["completed_gain"]


def _improvement_benefit_per_cost(row):
    best_improvement = row.get("best_improvement")
    if not best_improvement:
        return 0
    return best_improvement["benefit_per_cost"]
