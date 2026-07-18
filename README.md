# Adaptive Factory Digital Twin

A small Python simulation project for modeling production systems, measuring
throughput, and identifying early bottleneck signals.

The project currently starts with a simple one-machine production line and will
grow into a configurable factory digital twin with machines, buffers, part
types, failures, routing, bottleneck detection, and improvement recommendations.

## Current Model

The current simulator models one machine, one queue, and one demand stream:

- parts arrive at a fixed rate each minute
- the machine completes one part every `process_time` minutes
- unfinished parts wait in a queue
- the simulator reports basic production metrics

## Current Metrics

The simulator currently reports:

- `completed`: total parts completed during the simulation
- `throughput_per_hour`: completed parts scaled to an hourly rate
- `average_queue_length`: average number of waiting parts over time
- `max_queue_length`: largest queue size reached during the run
- `utilization`: estimated fraction of simulated time the machine is busy
- `queue_growth_rate`: final queue length minus initial queue length, showing
  whether backlog is building up

## Run the Demo

```bash
PYTHONPATH=src python -m factory_twin.simple_line
```

Example output:

```text
completed: 20
throughput_per_hour: 20.0
average_queue_length: 20.0
max_queue_length: 40
utilization: 1.0
queue_growth_rate: 40
```

## Run Scenario Comparison

```bash
PYTHONPATH=src python examples/run_simple_line.py
```

The scenario comparison runs the same one-machine model under three operating
conditions:

- `balanced line`: one part arrives each minute and the machine processes one
  part each minute
- `overloaded line`: one part arrives each minute and the machine processes one
  part every three minutes
- `faster machine`: one part arrives each minute and the machine processes one
  part every two minutes

This makes it easier to compare how processing speed affects completed parts,
throughput, queue size, utilization, and backlog growth.

## Run Tests

```bash
PYTHONPATH=src pytest
```

## Why This Project Matters

Factory systems are not just about making one machine faster. Throughput depends
on arrivals, processing time, queues, capacity, utilization, and bottlenecks
across the whole system. This project is a small first step toward modeling
those interactions with code.

## Next Milestones

- Add configurable machines, buffers, part types, and routes.
- Export simulation metrics to CSV.
- Add bottleneck detection.
- Add charts for throughput, utilization, and queue length.
- Compare before/after scenarios for process improvements.
