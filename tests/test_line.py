import importlib
import sys
from pathlib import Path

import pytest

from factory_twin.machine import Machine


class DummyMachine:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.speed = capacity
        self.processing_time = 1 / capacity
        self.rate = capacity


def _load_line_class():
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    candidate_modules = []
    for path in repo_root.rglob("*.py"):
        if path.name.startswith("test") or path.name.startswith("_"):
            continue
        if path.name in {"line.py", "production_line.py", "factory_line.py", "line_factory.py"}:
            candidate_modules.append(".".join(path.relative_to(repo_root).with_suffix("").parts))

    for module_name in candidate_modules:
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            continue

        for attr_name in ("Line", "ProductionLine", "FactoryLine"):
            line_cls = getattr(module, attr_name, None)
            if line_cls is not None:
                return line_cls

    raise ImportError("Could not find a Line implementation in the repository")


Line = _load_line_class()


def _make_line(*machines):
    if not machines:
        try:
            return Line([])
        except TypeError:
            try:
                return Line()
            except TypeError:
                line = Line()
                return line

    try:
        return Line(list(machines))
    except TypeError:
        try:
            return Line(*machines)
        except TypeError:
            line = Line()
            for machine in machines:
                if hasattr(line, "add_machine"):
                    line.add_machine(machine)
                else:
                    raise TypeError("Line implementation does not support adding machines")
            return line


def _get_machines(line):
    for attr_name in ("machines", "line_machines", "items"):
        if hasattr(line, attr_name):
            value = getattr(line, attr_name)
            if value is not None:
                return list(value)
    raise AttributeError("Line implementation does not expose its machines")


def _get_bottleneck(line):
    for attr_name in ("bottleneck", "slowest_machine", "critical_machine"):
        if hasattr(line, attr_name):
            value = getattr(line, attr_name)
            if callable(value):
                value = value()
            return value

    for method_name in ("get_bottleneck",):
        if hasattr(line, method_name):
            value = getattr(line, method_name)
            if callable(value):
                return value()

    raise AttributeError("Line implementation does not expose a bottleneck")


def _get_capacity(line):
    for attr_name in ("capacity", "line_capacity"):
        if hasattr(line, attr_name):
            value = getattr(line, attr_name)
            if callable(value):
                value = value()
            return value

    for method_name in ("get_capacity",):
        if hasattr(line, method_name):
            value = getattr(line, method_name)
            if callable(value):
                return value()

    raise AttributeError("Line implementation does not expose a capacity")


def test_it_stores_machines():
    machine_one = DummyMachine("m1", 10)
    machine_two = DummyMachine("m2", 20)

    line = _make_line(machine_one, machine_two)

    assert _get_machines(line) == [machine_one, machine_two]


def test_empty_line_raises_value_error():
    with pytest.raises(ValueError):
        _make_line()


def test_bottleneck_is_the_slowest_machine():
    slow_machine = DummyMachine("slow", 5)
    fast_machine = DummyMachine("fast", 20)

    line = _make_line(slow_machine, fast_machine)

    assert _get_bottleneck(line) is slow_machine


def test_line_capacity_is_based_on_the_bottleneck():
    slow_machine = DummyMachine("slow", 5)
    fast_machine = DummyMachine("fast", 20)

    line = _make_line(slow_machine, fast_machine)

    assert _get_capacity(line) == slow_machine.capacity


def test_named_production_line_reports_bottleneck_capacity_per_hour():
    cutter = Machine(name="cutter", process_time=1)
    press = Machine(name="press", process_time=3)
    inspector = Machine(name="inspector", process_time=2)

    line = Line("three-stage line", [cutter, press, inspector])

    assert line.line_name == "three-stage line"
    assert line.bottleneck_machine is press
    assert line.bottleneck_process_time == 3
    assert line.capacity_per_hour == 20.0
