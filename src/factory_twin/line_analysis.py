"""High-level analytics and decision helpers for factory production lines."""

from typing import Dict, Any


def find_queue_bottleneck(metrics: Dict[str, Any]) -> str:
    """Identify the station/machine with the largest accumulated queue length.

    Args:
        metrics: Dictionary mapping stage/machine names to queue lengths or metric dicts.
                 e.g. {"cutter": 0, "press": 41, "inspector": 0} or nested metrics.

    Returns:
        The name of the bottleneck station, or "none" if all queues are zero or metrics is empty.
    """
    if not metrics:
        return "none"

    # Extract numeric queue lengths whether metrics is dict[str, int] or dict[str, dict]
    queues = {}
    for key, val in metrics.items():
        if isinstance(val, dict):
            queues[key] = val.get("queue_length", val.get("queue", 0))
        else:
            queues[key] = val

    max_stage = max(queues, key=queues.get)
    if queues[max_stage] <= 0:
        return "none"

    return max_stage


def explain_queue_bottleneck(metrics: Dict[str, Any]) -> str:
    """Provide a human-readable explanation of the queue bottleneck.

    Args:
        metrics: Dictionary mapping stage/machine names to queue lengths.

    Returns:
        Explanation string explaining which station accumulated the largest queue.
    """
    bottleneck = find_queue_bottleneck(metrics)
    if bottleneck == "none":
        return "No queue bottleneck identified across the line."

    return f"The {bottleneck} is accumulating the largest queue."


def recommend_line_action(metrics: Dict[str, Any]) -> str:
    """Generate an actionable recommendation to resolve the queue bottleneck.

    Args:
        metrics: Dictionary mapping stage/machine names to queue lengths.

    Returns:
        Recommendation string proposing capacity, timing, or arrival adjustments.
    """
    bottleneck = find_queue_bottleneck(metrics)
    if bottleneck == "none":
        return "Line is operating smoothly with no significant queue accumulation."

    return (
        f"Improve {bottleneck} capacity, reduce {bottleneck} process time, "
        f"add parallel {bottleneck} capacity, or reduce arrivals."
    )