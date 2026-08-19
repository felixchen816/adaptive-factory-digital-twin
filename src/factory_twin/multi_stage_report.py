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

    lines.extend(
        [
            "",
            "## Ranked Improvement Options",
            "",
            "| Scenario | Rank | Option | Target | Cost | Completed Gain | WIP Reduction | Benefit/Cost |",
            "| --- | ---: | --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in rows:
        improvement_options = row.get("improvement_options") or []
        if not improvement_options:
            lines.append(
                f"| {row['scenario']} | 0 | No change needed. |  | 0 | 0 | 0 | 0 |"
            )
            continue

        for option in improvement_options:
            lines.append(
                f"| {row['scenario']} | {option['rank']} | "
                f"{option['option']} | {option['target']} | "
                f"{option['cost']} | {option['completed_gain']} | "
                f"{option['wip_reduction']} | "
                f"{_format_number(option['benefit_per_cost'])} |"
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
