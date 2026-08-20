from __future__ import annotations

from typing import Optional, Sequence

try:
    from .machine import Machine
except ImportError:  # pragma: no cover
    from factory_twin.machine import Machine


class ProductionLine:
    """Represents a production line composed of machines."""

    def __init__(
        self,
        line_name: str = "production line",
        machines: Optional[Sequence[Machine]] = None,
    ) -> None:
        if machines is None and not isinstance(line_name, str):
            machines = line_name
            line_name = "production line"

        if not isinstance(line_name, str) or not line_name.strip():
            raise ValueError("line_name must be a non-empty string.")

        machine_list = list(machines or [])
        if not machine_list:
            raise ValueError("ProductionLine must contain at least one machine.")

        self.line_name = line_name.strip()
        self.name = self.line_name
        self.machines = machine_list
        self.bottleneck_machine = self._find_bottleneck_machine()
        self.bottleneck = self.bottleneck_machine
        self.slowest_machine = self.bottleneck_machine
        self.critical_machine = self.bottleneck_machine
        self.bottleneck_process_time = self._get_process_time(self.bottleneck_machine)
        self.capacity_per_hour = self._get_capacity_per_hour(self.bottleneck_machine)
        self.capacity = self.capacity_per_hour
        self.line_capacity = self.capacity_per_hour

    def _find_bottleneck_machine(self) -> Machine:
        return min(self.machines, key=self._get_capacity_per_hour)

    def _get_process_time(self, machine: Machine) -> float:
        process_time = getattr(machine, "process_time", None)
        if process_time is not None:
            return float(process_time)

        capacity = self._get_capacity_per_hour(machine)
        if capacity <= 0:
            raise ValueError("machine capacity must be greater than zero.")
        return 60.0 / capacity

    def _get_capacity_per_hour(self, machine: Machine) -> float:
        capacity = getattr(machine, "capacity", None)
        if capacity is not None:
            capacity = float(capacity)
            if capacity <= 0:
                raise ValueError("machine capacity must be greater than zero.")
            return capacity

        process_time = getattr(machine, "process_time", None)
        if process_time is None:
            raise ValueError("Each machine must define a process_time.")
        process_time = float(process_time)
        if process_time <= 0:
            raise ValueError("process_time must be greater than zero.")
        return self._get_parallel_units(machine) * 60.0 / process_time

    def _get_parallel_units(self, machine: Machine) -> int:
        parallel_units = getattr(machine, "parallel_units", 1)
        if not isinstance(parallel_units, int) or parallel_units <= 0:
            raise ValueError("machine parallel_units must be greater than zero.")
        return parallel_units

    def get_bottleneck(self) -> Machine:
        return self.bottleneck_machine

    def get_capacity(self) -> float:
        return self.capacity_per_hour


Line = ProductionLine
