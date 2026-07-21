from dataclasses import dataclass

from factory_twin.machine import Machine


@dataclass
class Scenario:
    """Inputs for a one-machine production-line simulation."""

    name: str
    minutes: int
    arrival_rate: int
    machine: Machine

    @property
    def process_time(self):
        return self.machine.process_time
