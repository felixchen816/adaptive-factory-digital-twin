# Adaptive Factory Digital Twin

A Python simulation project for modeling production systems, measuring
throughput, finding bottlenecks, and comparing improvement scenarios.

The project started as a one-machine queue simulator and now includes a
multi-stage production line with internal queues, bottleneck diagnosis,
scenario comparison, JSON export, and Markdown reporting.

## One-Machine Simulator

The one-machine model represents a simple production line with one demand
stream, one queue, and one machine.

Each scenario defines:

- scenario name
- simulation length in minutes
- arrival rate in parts per minute
- machine name and `process_time`

The simulator reports:

- `completed`: total completed parts
- `throughput_per_hour`: completed parts scaled to an hourly rate
- `demand_per_hour`: arriving parts per hour
- `capacity_per_hour`: theoretical machine capacity per hour
- `capacity_gap_per_hour`: capacity minus demand
- `average_queue_length`: average waiting queue length
- `max_queue_length`: largest queue reached
- `utilization`: estimated machine busy fraction
- `queue_growth_rate`: final queue minus starting queue
- `line_status`: `stable`, `overloaded`, or `underused`
- `explanation`: plain-English status explanation
- `recommendation`: practical next action

## Multi-Stage Production Line

The multi-stage model represents a line with multiple machines and one queue in
front of each machine.

Example line:

```text
cutter -> press -> inspector
```

Each machine has a `process_time`. The slowest-capacity machine becomes the
line-level `bottleneck_machine`.

For the example line:

```text
cutter: 1 minute per part
press: 3 minutes per part
inspector: 2 minutes per part
```

The bottleneck machine is `press`, with a capacity of `20.0` parts/hour.

## Bottleneck Analysis

The project tracks two related bottleneck ideas:

- `bottleneck_machine`: the machine with the lowest theoretical capacity
- `queue_bottleneck`: the stage with the largest accumulated queue

These are not always the same. A machine can be theoretically slow, while the
largest queue can reveal where work is actually piling up during a specific
simulation.

Important multi-stage metrics:

- `final_queue_lengths`: queue length at each stage after the simulation
- `max_queue_lengths`: largest queue reached at each stage
- `total_wip`: total work in process left in the line
- `line_capacity_per_hour`: capacity of the bottleneck machine
- `recommendation`: action such as improving a stage, reducing process time,
  adding parallel capacity, or reducing arrivals

## Scenario Comparison

The demo compares multiple multi-stage scenarios:

- `baseline`: cutter 1, press 3, inspector 2
- `faster press`: cutter 1, press 2, inspector 2
- `slow inspector`: cutter 1, press 1, inspector 4
- `lower demand`: baseline line with lower arrival rate

Each comparison row includes:

- scenario name
- completed parts
- arrivals
- throughput per hour
- bottleneck machine
- queue bottleneck
- total WIP
- recommendation

The best multi-stage scenario is selected by:

1. highest completion rate
2. highest completed parts as a tie-breaker
3. lowest total WIP as the next tie-breaker
4. lowest largest max queue as the final tie-breaker

## Reports and Exports

The demo generates these local output files:

- `simple_line_results.csv`
- `simple_line_report.md`
- `multi_stage_results.json`
- `multi_stage_report.md`

These files are ignored by git because they are generated artifacts.

## Run the Demo

From the repository root:

```bash
.venv/bin/python examples/run_simple_line.py
```

The demo prints one-machine metrics, multi-stage queue behavior, scenario
comparison results, and the selected best multi-stage scenario.

It also writes the CSV, JSON, and Markdown report files listed above.

To use a different multi-stage scenario file or output location:

```bash
.venv/bin/python examples/run_simple_line.py \
  --multi-stage-config examples/multi_stage_scenarios.json \
  --multi-stage-json multi_stage_results.json \
  --multi-stage-report multi_stage_report.md
```

## Run Tests

```bash
.venv/bin/python -m pytest
```

The project uses `pyproject.toml` to add `src` to the pytest import path, so
manual `PYTHONPATH=src` setup is no longer needed for tests.

## Project Structure

```text
src/factory_twin/
  simple_line.py              one-machine simulator
  machine.py                  machine model
  scenario.py                 one-machine scenario model
  comparison.py               one-machine comparison helper
  decision.py                 one-machine best-scenario selector
  report.py                   one-machine Markdown report
  line.py                     multi-stage production line model
  multi_stage.py              multi-stage queue simulator
  line_analysis.py            queue bottleneck analysis
  multi_stage_comparison.py   multi-stage scenario comparison
  multi_stage_decision.py     multi-stage best-scenario selector
  multi_stage_report.py       multi-stage Markdown report
  config.py                   JSON scenario loading
  export.py                   CSV and JSON export helpers
```

## Roadmap

Next steps:

- add summary metrics such as completion rate and largest queue
- improve best-scenario scoring with completion rate
- add richer multi-stage report columns
- model parallel machines at one stage
- add machine downtime or failure events
- add charts for throughput, WIP, and queue growth
- add validation for richer scenario input files

## Why This Project Matters

Factory performance depends on more than one machine running fast. Throughput,
capacity, WIP, queues, bottlenecks, and demand all interact. This project is a
small but growing digital twin for testing those interactions with code and
turning simulation output into operational decisions.
