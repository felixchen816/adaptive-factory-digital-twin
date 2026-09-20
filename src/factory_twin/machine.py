from dataclasses import dataclass


@dataclass(frozen=True)
class Machine:
    """A production resource that processes one part at a fixed interval."""

    name: str
    process_time: float
    parallel_units: int = 1
    downtime_minutes: tuple = ()
    process_time_schedule: tuple = ()

    def __post_init__(self):
        if not self.name:
            raise ValueError("machine name must not be empty")
        if self.process_time <= 0:
            raise ValueError("machine process_time must be positive")
        if not isinstance(self.parallel_units, int) or self.parallel_units <= 0:
            raise ValueError("machine parallel_units must be positive")
        if not _is_non_negative_integer_tuple(self.downtime_minutes):
            raise ValueError(
                "machine downtime_minutes must be non-negative integers"
            )
        if not _is_schedule_tuple(self.process_time_schedule):
            raise ValueError(
                "machine process_time_schedule must contain valid schedule windows"
            )


def _is_non_negative_integer_tuple(values):
    if not isinstance(values, tuple):
        return False
    return all(
        isinstance(value, int) and not isinstance(value, bool) and value >= 0
        for value in values
    )


def _is_schedule_tuple(values):
    if not isinstance(values, tuple):
        return False

    for window in values:
        if not isinstance(window, dict):
            return False
        start = window.get("start")
        end = window.get("end")
        value = window.get("value")
        if not isinstance(start, int) or isinstance(start, bool) or start < 0:
            return False
        if not isinstance(end, int) or isinstance(end, bool) or end <= start:
            return False
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
            return False
    return True
