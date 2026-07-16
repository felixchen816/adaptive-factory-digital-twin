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

## Run the Demo

```bash
PYTHONPATH=src python -m factory_twin.simple_line
```
