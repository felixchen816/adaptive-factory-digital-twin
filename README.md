# Adaptive Factory Digital Twin

This project is starting as a tiny production-line simulator and will grow into
a configurable factory digital twin for bottleneck detection, throughput
analysis, and improvement recommendations.

## Current Model

The first model has one machine, one queue, and one demand stream:

- parts arrive at a fixed rate each minute
- the machine completes one part every `process_time` minutes
- the simulator reports completed parts, hourly throughput, and average queue
  length

## Run the Demo

```bash
PYTHONPATH=src python -m factory_twin.simple_line
```

## Run Tests

```bash
PYTHONPATH=src pytest
```

## Next Milestones

- Add configurable machines, buffers, part types, and routes.
- Export simulation metrics to CSV.
- Add bottleneck detection.
- Add charts for throughput, utilization, and queue length.
