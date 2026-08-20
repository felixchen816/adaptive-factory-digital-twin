from dataclasses import dataclass


@dataclass(frozen=True)
class Machine:
    """A production resource that processes one part at a fixed interval."""

    name: str
    process_time: float
    parallel_units: int = 1

    def __post_init__(self):
        if not self.name:
            raise ValueError("machine name must not be empty")
        if self.process_time <= 0:
            raise ValueError("machine process_time must be positive")
        if not isinstance(self.parallel_units, int) or self.parallel_units <= 0:
            raise ValueError("machine parallel_units must be positive")
