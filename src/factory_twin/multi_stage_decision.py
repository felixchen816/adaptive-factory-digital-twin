def choose_best_multi_stage_scenario(rows):
    """
    Choose the best multi-stage scenario from comparison rows.

    Selection priority:
    1. highest completion rate
    2. highest completed parts
    3. lowest total work in process
    4. lowest largest max queue
    """
    if not rows:
        raise ValueError("at least one scenario row is required")

    return max(rows, key=_scenario_score)


def _scenario_score(row):
    return (
        row["completion_rate"],
        row["completed"],
        -row["total_wip"],
        -_largest_max_queue(row),
    )


def _largest_max_queue(row):
    return row.get("largest_max_queue", 0)
