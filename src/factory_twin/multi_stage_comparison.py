"""Multi-stage scenario comparison tools for production line configurations."""

from dataclasses import dataclass, field
from typing import Sequence

from factory_twin.line import ProductionLine
from factory_twin.line_analysis import (
    explain_queue_bottleneck,
    find_queue_bottleneck,
    recommend_line_action,
)
from factory_twin.improvement_plan import (
    build_improvement_options,
    choose_best_improvement,
)
from factory_twin.multi_stage import simulate_production_line


@dataclass
class MultiStageScenario:
    """Configuration for a multi-stage line simulation scenario."""

    name: str
    line: ProductionLine
    minutes: int = 60
    arrival_rate: float = 1.0
    improvement_costs: dict = field(default_factory=dict)


def compare_multi_stage_scenarios(
    scenarios: Sequence[MultiStageScenario],
):
    """Simulate multiple multi-stage production line scenarios and return comparison metrics.

    Args:
        scenarios: List of MultiStageScenario instances to run.

    Returns:
        List of result dictionaries containing performance metrics for each scenario.
    """
    rows = []
    for scenario in scenarios:
        metrics = simulate_production_line(
            scenario.line,
            scenario.minutes,
            scenario.arrival_rate,
        )

        final_queues = metrics.get("final_queue_lengths", {})
        max_queues = metrics["max_queue_lengths"]
        queue_bottleneck = find_queue_bottleneck(final_queues)
        explanation = explain_queue_bottleneck(final_queues)
        recommendation = recommend_line_action(final_queues)
        improvement_options = build_improvement_options(
            scenario.line,
            metrics,
            scenario.minutes,
            scenario.arrival_rate,
            scenario.improvement_costs,
        )
        best_improvement = choose_best_improvement(improvement_options)

        completed = metrics["completed"]
        arrivals = metrics["arrivals"]
        total_wip = sum(final_queues.values())
        largest_final_queue = _largest_queue(final_queues)
        largest_max_queue = _largest_queue(max_queues)

        row = {
            "scenario": scenario.name,
            "completed": completed,
            "arrivals": arrivals,
            "throughput_per_hour": metrics["throughput_per_hour"],
            "bottleneck_machine": metrics["bottleneck_machine"],
            "line_capacity_per_hour": metrics["line_capacity_per_hour"],
            "final_queue_lengths": final_queues,
            "max_queue_lengths": max_queues,
            "queue_bottleneck": queue_bottleneck,
            "total_wip": total_wip,
            "largest_final_queue": largest_final_queue,
            "largest_max_queue": largest_max_queue,
            "wip_per_completed_part": _safe_divide(total_wip, completed),
            "completion_rate": _safe_divide(completed, arrivals),
            "explanation": explanation,
            "recommendation": recommendation,
            "improvement_options": improvement_options,
            "best_improvement": best_improvement,
        }
        rows.append(row)

    return rows


def _largest_queue(queue_lengths):
    if not queue_lengths:
        return 0
    return max(queue_lengths.values())


def _safe_divide(numerator, denominator):
    if denominator == 0:
        return 0
    return numerator / denominator
