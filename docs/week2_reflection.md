# Week 2 Reflection

Date: 2026-08-05

## What I Built

- Expanded the project from a one-machine simulator into a multi-stage production line model.
- Added internal queues for each stage and measured completed parts, WIP, bottleneck capacity, final queues, and max queues.
- Added bottleneck analysis that explains which stage is accumulating work and recommends an improvement.
- Added JSON export and multi-stage scenario comparison so different line designs can be evaluated side by side.
- Added project configuration so tests can run with plain `pytest` without manually setting `PYTHONPATH`.

## What Felt Energizing

- The most interesting part was seeing queues move through a real system instead of only reading one machine's output.
- Bottleneck diagnosis felt useful because it turned raw simulation numbers into an engineering decision.
- Comparing scenarios made the project feel more like a decision-support tool than a coding exercise.

## What Felt Confusing

- Imports and test setup were easy to trip over before the project had pytest path configuration.
- Multi-stage timing is more subtle than the simple simulator because stage order and pipeline delay affect completed parts.
- It is important to distinguish the machine with lowest capacity from the queue with the largest accumulated backlog.

## What Felt Boring

- Some CSV/JSON/export plumbing felt less exciting than the simulation logic, but it makes the project easier to demo and review.

## What This Suggests About Major Direction

- Applied Math: optimization, queues, and modeling still fit well.
- Applied Science: this project is starting to connect math, code, and physical systems.
- MAE / Robotics: production lines, bottlenecks, and staged processes are relevant to automation and manufacturing.
- ECE / Computer Engineering: less central so far, but simulation software and future controls/robotics work could connect.
- Data Science: metrics, comparisons, and reports are useful, but the most energizing part is the system model.
- Systems / Operations: this is currently the strongest fit because the work centers on throughput, WIP, bottlenecks, and improvement decisions.

## Next Week Goal

Turn multi-stage comparisons into stronger decision support: choose the best scenario automatically, generate a multi-stage Markdown report, and update the README so the project is easy to understand from GitHub.
