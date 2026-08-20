def simulate_production_line(line, minutes, arrival_rate):
    """
    Simulate a production line with one queue in front of each machine.

    Parts arrive at the first stage, move one stage at a time, and are counted
    as completed after the final stage.
    """
    if minutes < 0:
        raise ValueError("minutes must be non-negative")
    if arrival_rate < 0:
        raise ValueError("arrival_rate must be non-negative")

    machines = list(line.machines)
    queues = [0 for _ in machines]
    max_queue_lengths = [0 for _ in machines]
    completed = 0

    for minute in range(minutes):
        queues[0] += arrival_rate

        for stage_index in reversed(range(len(machines))):
            machine = machines[stage_index]
            process_time = _get_process_time(machine)
            parallel_units = _get_parallel_units(machine)

            if queues[stage_index] >= 1 and minute % process_time == 0:
                processed_parts = min(int(queues[stage_index]), parallel_units)
                queues[stage_index] -= processed_parts

                if stage_index == len(machines) - 1:
                    completed += processed_parts
                else:
                    queues[stage_index + 1] += processed_parts

        for stage_index, queue_length in enumerate(queues):
            max_queue_lengths[stage_index] = max(
                max_queue_lengths[stage_index],
                queue_length,
            )

    final_queue_lengths = _stage_dict(machines, queues)
    max_queue_lengths_by_stage = _stage_dict(machines, max_queue_lengths)

    return {
        "line": line.line_name,
        "completed": completed,
        "throughput_per_hour": completed * 60 / minutes if minutes else 0,
        "arrivals": arrival_rate * minutes,
        "demand_per_hour": arrival_rate * 60,
        "bottleneck_machine": line.bottleneck_machine.name,
        "bottleneck_process_time": line.bottleneck_process_time,
        "line_capacity_per_hour": line.capacity_per_hour,
        "final_queue_lengths": final_queue_lengths,
        "max_queue_lengths": max_queue_lengths_by_stage,
        "total_wip": sum(queues),
    }


def _get_process_time(machine):
    process_time = getattr(machine, "process_time", None)
    if process_time is None:
        raise ValueError("each machine must define a process_time")
    if process_time <= 0:
        raise ValueError("process_time must be positive")
    return process_time


def _get_parallel_units(machine):
    parallel_units = getattr(machine, "parallel_units", 1)
    if not isinstance(parallel_units, int) or parallel_units <= 0:
        raise ValueError("parallel_units must be positive")
    return parallel_units


def _stage_dict(machines, values):
    return {
        machine.name: value
        for machine, value in zip(machines, values)
    }
