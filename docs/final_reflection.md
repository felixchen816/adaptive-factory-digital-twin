# Final Reflection

This project started as a small production-line simulator and grew into a
decision-support prototype. The most important lesson was that a digital twin
is useful only when it connects model output to an operational choice. Counting
completed parts was a start, but the project became more meaningful when it
also tracked queues, WIP, bottlenecks, downtime, improvement options, and
scenario comparisons.

From an Applied Math perspective, the project shows how simple discrete-time
models can reveal system behavior. A small difference in process time can
create a large queue, and the best answer is not always the stage with the
largest theoretical capacity. The simulator makes those relationships visible
through measurable outputs instead of intuition alone.

From an Operations perspective, the main takeaway was that throughput and WIP
must be evaluated together. A scenario can complete more parts while still
leaving too much work trapped inside the line. Ranking scenarios by completion
rate, completed parts, total WIP, and peak queue creates a practical way to
choose between competing improvements.

From an MAE and Robotics perspective, the project connects to real automated
systems because every stage has constraints. Machines have capacity limits,
queues build when one stage outpaces the next, and downtime changes the
behavior of the whole line. Modeling those interactions is the first step
toward designing better automation cells, assembly lines, and robotic work
flows.

From a Data Science perspective, the project reinforced the value of clean
outputs. CSV and JSON exports make the simulation results reusable, while the
Markdown report and static dashboard make the same results easier to explain.
The dashboard is especially important because a reviewer can see the best
scenario, bottleneck, recommendation, assumptions, limitations, and charts in
one place.

The project is still intentionally limited. It uses deterministic arrivals,
simple downtime inputs, and cost scores instead of a full financial model. That
is acceptable for this stage because the goal is to demonstrate a clear
simulation workflow: define scenarios, run the model, compare outcomes, explain
bottlenecks, recommend improvements, and export evidence. A stronger future
version could add random arrivals, real cost estimates, sensitivity analysis,
and an interactive scenario editor.

The final result is a portfolio project that shows both coding growth and
systems thinking. It is not just a script that prints numbers; it is a small
analysis pipeline that turns manufacturing assumptions into evidence-backed
recommendations.
