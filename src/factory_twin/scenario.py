from dataclasses import dataclass


@dataclass
class Scenario:
    """Inputs for a one-machine production-line simulation."""

    name: str
    minutes: int
    arrival_rate: int
    process_time: int
