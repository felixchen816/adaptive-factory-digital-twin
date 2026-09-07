from factory_twin.chart import build_queue_trend_chart


def build_multi_stage_report(rows, best):
    """Build a Markdown report for multi-stage scenario comparisons."""
    lines = [
        "# Multi-Stage Production Line Report",
        "",
        "## Recommendation",
        "",
        f"Best scenario: {best['scenario']}",
        "",
        "## Case Study",
        "",
        _case_study(rows, best),
        "",
        "## Scenario Results",
        "",
        "| Scenario | Completed | Arrivals | Completion Rate | Throughput/hr | Total WIP | Largest Final Queue | Largest Max Queue | WIP/Completed | Bottleneck Machine | Queue Bottleneck | Recommendation | Best Improvement | Completed Gain | Benefit/Cost | Matching Scenario |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- | ---: | ---: | --- |",
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
            f"{_format_number(_improvement_benefit_per_cost(row))} | "
            f"{_matching_scenario(row)} |"
        )

    lines.extend(
        [
            "",
            "## Ranked Improvement Options",
            "",
            "| Scenario | Rank | Option | Target | Cost | Completed Gain | WIP Reduction | Benefit/Cost | Estimated Value | Net Value |",
            "| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in rows:
        improvement_options = row.get("improvement_options") or []
        if not improvement_options:
            lines.append(
                f"| {row['scenario']} | 0 | No change needed. |  | 0 | 0 | 0 | 0 | 0 | 0 |"
            )
            continue

        for option in improvement_options:
            lines.append(
                f"| {row['scenario']} | {option['rank']} | "
                f"{option['option']} | {option['target']} | "
                f"{option['cost']} | {option['completed_gain']} | "
                f"{option['wip_reduction']} | "
                f"{_format_number(option['benefit_per_cost'])} | "
                f"{_format_number(option.get('estimated_value', 0))} | "
                f"{_format_number(option.get('net_value', 0))} |"
            )

    lines.extend(
        [
            "",
            "## Queue Trend Charts",
            "",
        ]
    )
    for row in rows:
        lines.extend(
            [
                f"### {row['scenario']} - {row['queue_bottleneck']}",
                "",
                "```text",
                build_queue_trend_chart(
                    row.get("queue_history", []),
                    row["queue_bottleneck"],
                ),
                "```",
                "",
            ]
        )

    lines.append("")
    return "\n".join(lines)


def _format_number(value):
    if isinstance(value, float):
        return f"{value:.2f}"
    return value


def _case_study(rows, best):
    baseline = _baseline_row(rows) or rows[0]
    completed_gain = best["completed"] - baseline["completed"]
    wip_change = best["total_wip"] - baseline["total_wip"]
    bottleneck_change = _bottleneck_change(baseline, best)
    improvement = best.get("best_improvement") or {}
    improvement_summary = improvement.get("summary", "No additional improvement is needed.")

    return (
        f"Baseline completed {baseline['completed']} of {baseline['arrivals']} arrivals "
        f"with {_format_number(baseline['total_wip'])} total WIP and "
        f"{baseline['queue_bottleneck']} as the queue bottleneck. "
        f"The selected scenario, {best['scenario']}, completed {best['completed']} "
        f"of {best['arrivals']} arrivals with {_format_number(best['total_wip'])} "
        f"total WIP. That is a completed-part change of {completed_gain} and "
        f"a WIP change of {wip_change}. {bottleneck_change} "
        f"Decision logic prioritized completion rate first, then completed parts, "
        f"then lower WIP and lower peak queue. Recommended next action: "
        f"{improvement_summary}"
    )


def _baseline_row(rows):
    for row in rows:
        if row["scenario"].lower() == "baseline":
            return row
    return None


def _bottleneck_change(baseline, best):
    if baseline["queue_bottleneck"] == best["queue_bottleneck"]:
        return f"The queue bottleneck remained {best['queue_bottleneck']}."
    return (
        f"The queue bottleneck moved from {baseline['queue_bottleneck']} "
        f"to {best['queue_bottleneck']}."
    )


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


def _matching_scenario(row):
    return row.get("matching_scenario") or "None"
