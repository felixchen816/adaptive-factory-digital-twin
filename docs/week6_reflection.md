# Week 6 Reflection

Date: 2026-09-02

## What I Built

- Added a static HTML dashboard UI for multi-stage scenario results.
- Connected the dashboard to the existing simulator, comparison rows, improvement planner, and SVG chart code.
- Added a CLI option for writing `factory_dashboard.html`.
- Updated tests so the dashboard must include summary metrics, scenario comparison, improvement recommendations, and embedded SVG charts.

## What Changed In The Project

The project now has a real UI layer. It is still generated from Python and does not require a web server, but it makes the project easier to open, scan, and explain from a browser.

## What Felt Important

- The dashboard uses the existing analysis pipeline instead of duplicating simulation logic.
- A static HTML file is enough for this stage because the project needs presentation clarity more than interactivity.
- The dashboard makes the system feel more complete: data, reports, charts, and a browser-readable interface now come from one run.

## What Still Needs Work

- The dashboard is static and does not let users edit scenarios directly.
- The SVG charts focus on queue trends, not full throughput or WIP breakdowns.
- The next useful UI step is adding forms or controls for changing scenario inputs.

## Next Goal

Add dashboard controls or a small scenario editor so users can change assumptions without editing JSON by hand.
