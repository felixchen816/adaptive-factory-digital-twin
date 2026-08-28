# Week 4 Reflection

Date: 2026-08-28

## What I Built

- Added planned downtime so machines can skip processing during maintenance or failure minutes.
- Added queue and completed-part time-series history to the simulator output.
- Exported the time-series history to CSV so the project has chart-ready data.
- Added value-aware improvement scoring with estimated value and net value.
- Added matching-scenario checks so recommendations can be compared against scenario results that already exist.
- Added text-based queue trend charts to the Markdown report.

## What Changed In The Project

The project is now less like a single simulation script and more like a small analysis workflow. It can simulate a line, explain the queue bottleneck, rank improvement actions, compare those actions against scenarios, and generate data that can be charted later.

## What Felt Important

- Time-series data matters because final totals hide how a queue developed.
- Downtime makes the model more realistic without making the code too complicated.
- Matching recommendations to existing scenarios makes the tool more practical: the report can point to a scenario that already tests the recommended change.
- Text charts are not a replacement for real visualization, but they make the Markdown report easier to scan.

## What Still Needs Work

- Downtime is deterministic and manually scheduled.
- Costs and values are still simple numeric scores, not real equipment, labor, or revenue data.
- The charting is text-based; a future version should generate actual throughput and WIP charts.

## Next Goal

Turn the current report into a stronger decision artifact by adding graphical charts, richer cost assumptions, and clearer scenario-level executive summaries.
