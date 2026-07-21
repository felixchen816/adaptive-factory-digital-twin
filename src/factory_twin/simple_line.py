from factory_twin.machine import Machine
from factory_twin.scenario import Scenario


def simulate_line(minutes, arrival_rate, process_time):
    """
    Simulate a one-machine production line.

    Args:
        minutes: Number of minutes to simulate.
        arrival_rate: Parts arriving per minute.
        process_time: Minutes between processing each part.

    Returns:
        Dictionary with completed parts, queue metrics, throughput, and utilization.
    """
    if minutes < 0:
        raise ValueError("minutes must be non-negative")
    if arrival_rate < 0:
        raise ValueError("arrival_rate must be non-negative")
    if process_time <= 0:
        raise ValueError("process_time must be positive")

    queue = 0
    completed = 0
    queue_lengths = []
    max_queue = 0
    initial_queue = queue

    for minute in range(minutes):
        queue += arrival_rate

        if queue > 0 and minute % process_time == 0:
            queue -= 1
            completed += 1

        max_queue = max(max_queue, queue)
        queue_lengths.append(queue)

    average_queue = sum(queue_lengths) / len(queue_lengths) if queue_lengths else 0
    throughput_per_hour = completed * 60 / minutes if minutes else 0
    busy_minutes = min(completed * process_time, minutes)
    utilization = busy_minutes / minutes if minutes else 0
    queue_growth_rate = queue - initial_queue

    return {
        "completed": completed,
        "throughput_per_hour": throughput_per_hour,
        "average_queue_length": average_queue,
        "max_queue_length": max_queue,
        "utilization": utilization,
        "queue_growth_rate": queue_growth_rate,
    }


def simulate_scenario(scenario: Scenario):
    return simulate_line(
        scenario.minutes,
        scenario.arrival_rate,
        scenario.process_time,
    )


def simulate_machine_line(minutes, arrival_rate, machine: Machine):
    return simulate_line(minutes, arrival_rate, machine.process_time)


if __name__ == "__main__":
    metrics = simulate_scenario(
        Scenario(
            name="overloaded line",
            minutes=60,
            arrival_rate=1,
            process_time=3,
        )
    )
    print("completed:", metrics["completed"])
    print("throughput_per_hour:", metrics["throughput_per_hour"])
    print("average_queue_length:", metrics["average_queue_length"])
    print("max_queue_length:", metrics["max_queue_length"])
    print("utilization:", metrics["utilization"])
    print("queue_growth_rate:", metrics["queue_growth_rate"])
