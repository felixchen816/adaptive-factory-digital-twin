# Simulation Tool Comparison

This project is a lightweight factory digital-twin prototype. It is not trying
to replace full simulation platforms. The goal is to show a clear engineering
workflow: define scenarios, run a deterministic model, compare bottlenecks,
recommend improvements, and export readable evidence.

## Compared Tools

### SimPy

SimPy is a Python discrete-event simulation framework. It is better suited for
general event-driven models where active entities compete for resources, wait,
resume, and trigger events. A future version of this project could move toward
SimPy if it needs true event scheduling, stochastic arrivals, or resource
contention beyond one queue per stage.

Reference: `https://pythonhosted.org/SimPy/`

### AnyLogic

AnyLogic is a commercial multimethod simulation platform used for logistics,
manufacturing, healthcare, supply chains, and related systems. It supports
discrete-event, agent-based, and system-dynamics approaches. Compared with this
project, AnyLogic is much more powerful for production-grade experiments,
animation, layout-driven modeling, and large scenario studies.

Reference: `https://www.anylogic.com/`

### FlexSim

FlexSim is a 3D discrete-event simulation package for modeling, analyzing, and
improving physical systems. It is stronger for detailed factory layouts,
material handling, animation, and stakeholder-facing visual validation.

Reference: `https://www.flexsim.com/`

## Where This Project Now Fits

The current project is intentionally smaller, but now includes enough
complexity to make queue behavior more realistic:

- multiple production stages
- parallel machine capacity
- scheduled machine downtime
- scheduled demand surges and demand lulls
- scheduled process-time slowdowns
- queue, completion, and arrival histories
- CSV, JSON, Markdown, SVG, and dashboard outputs

Those features make the model better for portfolio-level bottleneck analysis:
it can show how queues react to demand shocks, temporary failures, and slower
processing windows.

## Remaining Gap

The project still uses deterministic minute-by-minute simulation rather than a
full discrete-event engine. It does not yet include random distributions,
repair-time distributions, routing alternatives, operators, part families,
material handling travel time, or spatial layout. Those are the next logical
steps if the project needs to move closer to SimPy, AnyLogic, or FlexSim.
