def simulate_production_line(line, minutes, arrival_rate, arrival_schedule=()):
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
    downtime_events = {machine.name: 0 for machine in machines}
    queue_history = []
    completed_history = []
    arrival_history = []
    completed = 0
    arrivals = 0

    for minute in range(minutes):
        minute_arrivals = _scheduled_value(arrival_rate, arrival_schedule, minute)
        if minute_arrivals < 0:
            raise ValueError("arrival rates must be non-negative")
        arrivals += minute_arrivals
        queues[0] += minute_arrivals

        for stage_index in reversed(range(len(machines))):
            machine = machines[stage_index]
            process_time = _get_process_time(machine, minute)
            parallel_units = _get_parallel_units(machine)
            if _is_down(machine, minute):
                downtime_events[machine.name] += 1
                continue

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
        queue_history.append(_history_row(minute, machines, queues))
        completed_history.append(
            {
                "minute": minute,
                "completed": completed,
            }
        )
        arrival_history.append(
            {
                "minute": minute,
                "arrivals": minute_arrivals,
                "cumulative_arrivals": arrivals,
            }
        )

    final_queue_lengths = _stage_dict(machines, queues)
    max_queue_lengths_by_stage = _stage_dict(machines, max_queue_lengths)

    return {
        "line": line.line_name,
        "completed": completed,
        "throughput_per_hour": completed * 60 / minutes if minutes else 0,
        "arrivals": arrivals,
        "demand_per_hour": arrivals * 60 / minutes if minutes else 0,
        "bottleneck_machine": line.bottleneck_machine.name,
        "bottleneck_process_time": line.bottleneck_process_time,
        "line_capacity_per_hour": line.capacity_per_hour,
        "final_queue_lengths": final_queue_lengths,
        "max_queue_lengths": max_queue_lengths_by_stage,
        "total_wip": sum(queues),
        "downtime_events": downtime_events,
        "queue_history": queue_history,
        "completed_history": completed_history,
        "arrival_history": arrival_history,
    }


def _get_process_time(machine, minute=0):
    process_time = getattr(machine, "process_time", None)
    if process_time is None:
        raise ValueError("each machine must define a process_time")
    process_time = _scheduled_value(
        process_time,
        getattr(machine, "process_time_schedule", ()),
        minute,
    )
    if process_time <= 0:
        raise ValueError("process_time must be positive")
    return process_time


def _scheduled_value(default_value, schedule, minute):
    for window in schedule or ():
        if window["start"] <= minute < window["end"]:
            return window["value"]
    return default_value


def _get_parallel_units(machine):
    parallel_units = getattr(machine, "parallel_units", 1)
    if not isinstance(parallel_units, int) or parallel_units <= 0:
        raise ValueError("parallel_units must be positive")
    return parallel_units


def _is_down(machine, minute):
    return minute in getattr(machine, "downtime_minutes", ())


def _stage_dict(machines, values):
    return {
        machine.name: value
        for machine, value in zip(machines, values)
    }


def _history_row(minute, machines, queues):
    row = {"minute": minute}
    row.update(_stage_dict(machines, queues))
    return row
