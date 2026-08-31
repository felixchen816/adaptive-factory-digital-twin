# Week 5 Reflection

Date: 2026-08-31

## What I Built

- Added SVG queue chart generation for the default multi-stage queue bottleneck.
- Added a CLI output option for `multi_stage_queue_chart.svg`.
- Kept the existing text charts in the Markdown report while adding a standalone graphical artifact.
- Updated the README and ignored generated SVG chart output.

## What Changed In The Project

The project now produces three levels of output: raw JSON metrics, CSV time-series data, and human-readable reports/charts. That makes it easier to inspect results quickly, but also keeps the underlying data available for future analysis.

## What Felt Important

- SVG output is useful because it does not require extra plotting libraries.
- The chart is generated from the same `queue_history` data used by the report, so the visual output stays tied to simulator results.
- Keeping generated artifacts ignored by git prevents demo runs from creating noisy commits.

## What Still Needs Work

- The SVG chart currently focuses on one queue bottleneck, not every stage.
- The chart is intentionally simple and does not yet include legends, multiple lines, or throughput overlays.
- The next useful step is richer chart output, not a full frontend.

## Next Goal

Generate multiple SVG charts from one run: per-stage queue trends, total WIP, and completed-parts throughput.
