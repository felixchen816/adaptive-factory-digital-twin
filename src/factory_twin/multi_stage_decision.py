def choose_best_multi_stage_scenario(rows):
    """
    Choose the best multi-stage scenario from comparison rows.

    Selection priority:
    1. highest completed parts
    2. lowest total work in process
    3. lowest largest queue
    """
    if not rows:
        raise ValueError("at least one scenario row is required")

    return max(rows, key=_scenario_score)


def _scenario_score(row):
    return (
        row["completed"],
        -row["total_wip"],
        -_largest_queue(row),
    )


def _largest_queue(row):
    queue_lengths = row.get("max_queue_lengths", {})
    if not queue_lengths:
        return 0
    return max(queue_lengths.values())
