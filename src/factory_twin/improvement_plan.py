"""Improvement option scoring for multi-stage production lines."""

from factory_twin.line import ProductionLine
from factory_twin.line_analysis import find_queue_bottleneck
from factory_twin.machine import Machine
from factory_twin.multi_stage import simulate_production_line


def build_improvement_options(line, metrics, minutes=60, arrival_rate=1.0):
    """Build scored improvement options for the largest queue bottleneck."""
    final_queues = metrics.get("final_queue_lengths", {})
    if not final_queues or max(final_queues.values()) <= 0:
        return []

    target = find_queue_bottleneck(final_queues)
    if not target:
        return []

    before_completed = metrics["completed"]
    before_wip = sum(final_queues.values())
    options = []

    options.append(
        _score_option(
            option="reduce process time",
            target=target,
            cost=2,
            line=_line_with_machine_process_time(line, target, reduction=1),
            minutes=minutes,
            arrival_rate=arrival_rate,
            before_completed=before_completed,
            before_wip=before_wip,
            summary=f"Improve {target} by reducing process time.",
        )
    )
    options.append(
        _score_option(
            option="add parallel capacity",
            target=target,
            cost=4,
            line=_line_with_parallel_capacity(line, target),
            minutes=minutes,
            arrival_rate=arrival_rate,
            before_completed=before_completed,
            before_wip=before_wip,
            summary=f"Improve {target} by adding parallel capacity.",
        )
    )
    options.append(
        _score_option(
            option="reduce arrivals",
            target=target,
            cost=1,
            line=line,
            minutes=minutes,
            arrival_rate=arrival_rate * 0.8,
            before_completed=before_completed,
            before_wip=before_wip,
            summary=f"Reduce arrivals so {target} stops accumulating work.",
        )
    )

    return options


def choose_best_improvement(options):
    """Choose the highest payoff option from scored improvement options."""
    if not options:
        return None
    return max(
        options,
        key=lambda option: (
            option["benefit_per_cost"],
            option["completed_gain"],
            option["wip_reduction"],
        ),
    )


def _score_option(
    option,
    target,
    cost,
    line,
    minutes,
    arrival_rate,
    before_completed,
    before_wip,
    summary,
):
    after_metrics = simulate_production_line(line, minutes, arrival_rate)
    after_completed = after_metrics["completed"]
    after_wip = after_metrics["total_wip"]
    completed_gain = after_completed - before_completed
    wip_reduction = before_wip - after_wip

    return {
        "option": option,
        "target": target,
        "cost": cost,
        "before_completed": before_completed,
        "after_completed": after_completed,
        "completed_gain": completed_gain,
        "before_wip": before_wip,
        "after_wip": after_wip,
        "wip_reduction": wip_reduction,
        "benefit_per_cost": completed_gain / cost,
        "summary": summary,
    }


def _line_with_machine_process_time(line, target, reduction):
    machines = []
    for machine in line.machines:
        process_time = machine.process_time
        if machine.name == target:
            process_time = max(1, process_time - reduction)
        machines.append(Machine(name=machine.name, process_time=process_time))
    return ProductionLine(f"{line.name} with faster {target}", machines)


def _line_with_parallel_capacity(line, target):
    machines = []
    for machine in line.machines:
        process_time = machine.process_time
        if machine.name == target:
            process_time = max(1, process_time - 1)
        machines.append(Machine(name=machine.name, process_time=process_time))
    return ProductionLine(f"{line.name} with parallel {target}", machines)
