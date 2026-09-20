# Tesla Fremont Model 3/Y Case Study

## Product And Factory

Product: Tesla Model 3 / Model Y vehicles.

Factory: Tesla Fremont Factory, Fremont, California.

This case was chosen because public filings and investor materials provide more
production information than many factories. Tesla's 2024 Form 10-K lists
California Model 3 / Model Y production as active. Tesla investor updates list
California Model 3 / Model Y installed annual capacity at more than 550,000
vehicles.

## Public Data Used

Sources checked:

- Tesla Investor Relations quarterly update page:
  `https://ir.tesla.com/`
- Tesla 2024 Form 10-K:
  `https://www.sec.gov/Archives/edgar/data/1318605/000162828025003063/tsla-20241231.htm`
- Tesla Fremont Factory process descriptions:
  `https://en.wikipedia.org/wiki/Tesla_Fremont_Factory`

Key public facts used:

- California produces Model 3 / Model Y vehicles.
- Published installed annual capacity for California Model 3 / Model Y is more
  than 550,000 vehicles.
- Public process descriptions identify major factory areas such as stamping,
  casting, body construction, paint, battery / drive-unit installation, final
  assembly, and end-of-line work.

## Capacity Conversion

The scenario uses 550,000 vehicles per year as the calibration target. Because
the public number is listed as "more than" 550,000, this model treats 550,000 as
a conservative lower-bound target.

```text
550,000 vehicles/year
/ 365 days/year
= 1,506.85 vehicles/day

1,506.85 vehicles/day
/ 24 hours/day
= 62.79 vehicles/hour

62.79 vehicles/hour
/ 60 minutes/hour
= 1.046 vehicles/minute
```

The simulator scenario therefore uses:

```text
arrival_rate = 1.0464231354642313 vehicles/minute
minutes = 10080
```

The 10,080-minute run represents seven continuous production days. A longer run
reduces distortion from initial pipeline fill in a multi-stage line.

The repository also includes a shorter stress scenario:

```text
examples/tesla_fremont_dynamic_scenario.json
```

That scenario keeps the same factory stage map but adds:

- morning and late-day demand surges
- a midday demand lull
- a temporary casting outage
- a temporary paint-shop slowdown
- a final-assembly downtime window

It is designed to produce more varied queue histories than the calibrated
baseline, so the dashboard charts show queue buildup and recovery instead of
only smooth linear growth.

## Modeled Stages

The real factory is much more complex than this model. The scenario compresses
the vehicle flow into six major stages:

1. blanking and stamping
2. rear underbody casting
3. body shop welding
4. paint shop
5. battery and drive-unit marriage
6. final assembly and end-of-line test

Most stages are modeled as effective batch processes with `process_time = 10`
minutes and `parallel_units = 11`, giving an effective capacity of about
66 vehicles/hour per stage. This is close to the public lower-bound target of
62.79 vehicles/hour while staying inside the simulator's integer parallel-unit
model.

Blanking and stamping is modeled with higher effective capacity because public
factory descriptions indicate stamping is a high-throughput upstream operation,
and the line-level bottleneck should be closer to the downstream vehicle-flow
stages rather than sheet-metal blanking.

## Validation Result

Running the scenario with:

```bash
.venv/bin/python examples/run_simple_line.py \
  --multi-stage-config examples/tesla_fremont_model3y_scenario.json \
  --multi-stage-json tesla_fremont_model3y_results.json \
  --multi-stage-report tesla_fremont_model3y_report.md \
  --multi-stage-history-csv tesla_fremont_model3y_history.csv \
  --multi-stage-chart-svg tesla_fremont_model3y_queue_chart.svg \
  --dashboard-html tesla_fremont_model3y_dashboard.html
```

Expected scale:

- public target: about 62.79 vehicles/hour
- simulator result: about 62.45 vehicles/hour over seven days
- annualized simulator output: about 547,031 vehicles/year
- difference from 550,000 target: about -0.54%

That is close enough for a first-order digital twin scenario. The model is not
claiming to reproduce Tesla's exact station-level engineering. It validates the
factory-scale throughput against public data and gives the simulator a realistic
multi-machine benchmark.

## Model Limits

- The real Fremont factory has many parallel lines, buffers, subassemblies, and
  quality loops that are not fully represented.
- Public data does not expose exact station cycle times, labor allocation, or
  downtime by area.
- The simulator currently uses deterministic arrivals and integer parallel
  units, so process times are effective approximations rather than measured
  station cycle times.
- The public capacity number combines Model 3 and Model Y, so the scenario
  models the combined product family rather than a single trim.
