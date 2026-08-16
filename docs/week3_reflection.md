# Week 3 Reflection

Date: 2026-08-17

## What I Built

- Added an improvement-planning layer for multi-stage production lines.
- Made the project estimate actions for the queue bottleneck: reduce process time, add parallel capacity, or reduce arrivals.
- Added benefit-per-cost scoring so the code can recommend a best next improvement instead of only reporting raw metrics.
- Wired the best improvement into multi-stage scenario comparison, Markdown reports, and the example demo output.
- Expanded tests so the new decision logic is covered before it becomes part of the demo.

## What Changed In The Project

The project is moving from simulation toward decision support. Earlier versions could answer, "What happened in this line?" The new version starts answering, "What should I try next?"

The current improvement scoring is intentionally simple. It estimates completed-part gain and divides by a simple cost score. That makes the recommendation easy to explain, but it is not a replacement for real engineering cost data yet.

## What Felt Important

- Separating simulation from improvement planning kept the code cleaner.
- The best improvement should be based on measured results, not only the theoretical slowest machine.
- Reports are more useful when they include an action, a target, and an estimated payoff.

## What Still Needs Work

- Parallel capacity is still approximated by a faster effective process time.
- Improvement costs are fixed scores, not real dollar, labor, or equipment costs.
- The simulator still uses fixed arrivals and deterministic processing.

## What This Suggests About Major Direction

- Applied Math and Operations still fit strongly because the work is about queues, constraints, scoring, and optimization.
- MAE / Robotics is still relevant because the project models staged physical production systems.
- Data Science is useful for reporting and comparison, but the core interest is still system behavior and improvement decisions.
- Computer Engineering could become more relevant later if the project adds controls, sensors, or real-time data.

## Next Goal

Make the improvement planner more realistic by allowing scenario-specific costs, modeling true parallel machines, or adding downtime events that force the recommendation logic to handle messier production behavior.
