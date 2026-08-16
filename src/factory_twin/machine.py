from dataclasses import dataclass


@dataclass(frozen=True)
class Machine:
    """A production resource that processes one part at a fixed interval."""

    name: str
    process_time: float

    def __post_init__(self):
        if not self.name:
            raise ValueError("machine name must not be empty")
        if self.process_time <= 0:
            raise ValueError("machine process_time must be positive")
