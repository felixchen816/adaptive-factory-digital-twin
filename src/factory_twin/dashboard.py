"""Static dashboard generation for factory twin scenario results."""

from html import escape
from pathlib import Path

from factory_twin.chart import (
    build_completed_trend_svg,
    build_stage_queue_svgs,
    build_total_wip_svg,
)


def build_dashboard_html(rows, best):
    """Build a self-contained HTML dashboard for multi-stage scenarios."""
    scenario_rows = list(rows)
    best_name = best["scenario"] if best else "None"
    total_scenarios = len(scenario_rows)
    best_completed = best.get("completed", 0) if best else 0
    best_wip = best.get("total_wip", 0) if best else 0

    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            "<title>Adaptive Factory Digital Twin</title>",
            f"<style>{_styles()}</style>",
            "</head>",
            "<body>",
            '<main class="shell">',
            '<section class="header">',
            "<div>",
            "<p>Factory Simulation Dashboard</p>",
            "<h1>Adaptive Factory Digital Twin</h1>",
            "</div>",
            f'<strong class="status">Best Scenario: {escape(best_name)}</strong>',
            "</section>",
            '<section class="metrics">',
            _metric("Scenarios", total_scenarios),
            _metric("Best Completed", best_completed),
            _metric("Best Total WIP", _format_number(best_wip)),
            _metric("Best Completion Rate", _format_percent(best.get("completion_rate", 0) if best else 0)),
            "</section>",
            '<section class="panel">',
            "<h2>Executive Summary</h2>",
            _executive_summary(scenario_rows, best),
            "</section>",
            '<section class="panel">',
            "<h2>Scenario Comparison</h2>",
            _comparison_table(scenario_rows),
            "</section>",
            '<section class="panel">',
            "<h2>Recommended Improvements</h2>",
            _improvement_table(scenario_rows),
            "</section>",
            '<section class="chart-grid">',
            _dashboard_chart(
                "Best Scenario Total WIP",
                build_total_wip_svg(best.get("queue_history", []) if best else [], 520, 260),
            ),
            _dashboard_chart(
                "Best Scenario Throughput",
                build_completed_trend_svg(
                    best.get("completed_history", []) if best else [],
                    520,
                    260,
                ),
            ),
            "</section>",
            '<section class="chart-grid">',
            *_chart_panels(scenario_rows),
            "</section>",
            '<section class="panel">',
            "<h2>Per-Stage Queue Charts</h2>",
            _stage_queue_charts(best),
            "</section>",
            "</main>",
            "</body>",
            "</html>",
        ]
    )


def write_dashboard_html(rows, best, output_path):
    """Write a self-contained HTML dashboard to disk."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_dashboard_html(rows, best), encoding="utf-8")


def _comparison_table(rows):
    body = []
    for row in rows:
        body.append(
            "<tr>"
            f"<td>{escape(row['scenario'])}</td>"
            f"<td>{row['completed']}</td>"
            f"<td>{_format_percent(row['completion_rate'])}</td>"
            f"<td>{_format_number(row['throughput_per_hour'])}</td>"
            f"<td>{_format_number(row['total_wip'])}</td>"
            f"<td>{escape(row['queue_bottleneck'])}</td>"
            "</tr>"
        )
    return (
        "<table>"
        "<thead><tr><th>Scenario</th><th>Completed</th><th>Completion</th>"
        "<th>Throughput/hr</th><th>Total WIP</th><th>Queue Bottleneck</th></tr></thead>"
        f"<tbody>{''.join(body)}</tbody>"
        "</table>"
    )


def _improvement_table(rows):
    body = []
    for row in rows:
        best_improvement = row.get("best_improvement") or {}
        body.append(
            "<tr>"
            f"<td>{escape(row['scenario'])}</td>"
            f"<td>{escape(best_improvement.get('summary', 'No change needed.'))}</td>"
            f"<td>{best_improvement.get('completed_gain', 0)}</td>"
            f"<td>{_format_number(best_improvement.get('benefit_per_cost', 0))}</td>"
            f"<td>{_format_number(best_improvement.get('net_value', 0))}</td>"
            f"<td>{escape(row.get('matching_scenario') or 'None')}</td>"
            "</tr>"
        )
    return (
        "<table>"
        "<thead><tr><th>Scenario</th><th>Best Improvement</th><th>Gain</th>"
        "<th>Benefit/Cost</th><th>Net Value</th><th>Matching Scenario</th></tr></thead>"
        f"<tbody>{''.join(body)}</tbody>"
        "</table>"
    )


def _chart_panels(rows):
    panels = []
    for row in rows:
        stage = row["queue_bottleneck"]
        svg = build_stage_queue_svgs(row.get("queue_history", [])).get(
            stage,
            "",
        )
        panels.append(
            '<section class="chart-panel">'
            f"<h2>{escape(row['scenario'])}</h2>"
            f"<p>{escape(stage)} queue trend</p>"
            f"{svg}"
            "</section>"
        )
    return panels


def _executive_summary(rows, best):
    if not best:
        return "<p>No scenario data available.</p>"

    best_improvement = best.get("best_improvement") or {}
    matching_count = sum(1 for row in rows if row.get("matching_scenario"))
    return (
        "<p>"
        f"The best scenario is <strong>{escape(best['scenario'])}</strong>, "
        f"with {_format_percent(best['completion_rate'])} completion, "
        f"{_format_number(best['throughput_per_hour'])} parts/hour, and "
        f"{_format_number(best['total_wip'])} total WIP. "
        f"The top follow-up action is {escape(best_improvement.get('summary', 'No change needed.'))} "
        f"{matching_count} scenario(s) already match a recommended improvement."
        "</p>"
    )


def _dashboard_chart(title, svg):
    return (
        '<section class="chart-panel">'
        f"<h2>{escape(title)}</h2>"
        f"{svg}"
        "</section>"
    )


def _stage_queue_charts(best):
    if not best:
        return "<p>No scenario data available.</p>"

    charts = build_stage_queue_svgs(best.get("queue_history", []))
    if not charts:
        return "<p>No queue history available.</p>"

    return "".join(
        '<section class="stage-chart">'
        f"<h3>{escape(stage)}</h3>"
        f"{svg}"
        "</section>"
        for stage, svg in charts.items()
    )


def _metric(label, value):
    return (
        '<div class="metric">'
        f"<span>{escape(str(label))}</span>"
        f"<strong>{escape(str(value))}</strong>"
        "</div>"
    )


def _format_number(value):
    if isinstance(value, float):
        return f"{value:.2f}"
    return value


def _format_percent(value):
    return f"{value * 100:.1f}%"


def _styles():
    return """
* { box-sizing: border-box; }
body {
  margin: 0;
  color: #182026;
  background: #f4f7f8;
  font-family: Arial, Helvetica, sans-serif;
}
.shell {
  width: min(1180px, calc(100% - 32px));
  margin: 0 auto;
  padding: 32px 0;
}
.header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
  padding: 24px 0;
  border-bottom: 2px solid #1f6f78;
}
.header p {
  margin: 0 0 8px;
  color: #6b7280;
  font-size: 14px;
  text-transform: uppercase;
}
h1 {
  margin: 0;
  font-size: 36px;
  line-height: 1.1;
}
h2 {
  margin: 0 0 16px;
  font-size: 20px;
}
.status {
  padding: 10px 12px;
  border: 1px solid #1f6f78;
  border-radius: 8px;
  color: #1f6f78;
  background: #ffffff;
}
.metrics {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin: 20px 0;
}
.metric,
.panel,
.chart-panel {
  border: 1px solid #d7dee2;
  border-radius: 8px;
  background: #ffffff;
}
.metric {
  padding: 16px;
}
.metric span {
  display: block;
  color: #667085;
  font-size: 13px;
}
.metric strong {
  display: block;
  margin-top: 8px;
  font-size: 24px;
}
.panel {
  margin-top: 16px;
  padding: 18px;
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th,
td {
  padding: 10px 8px;
  border-bottom: 1px solid #e5e7eb;
  text-align: left;
  vertical-align: top;
}
th {
  color: #45515c;
  font-size: 13px;
}
.chart-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  margin-top: 16px;
}
.chart-panel {
  padding: 18px;
}
.chart-panel p {
  margin: -8px 0 12px;
  color: #667085;
}
.chart-panel svg {
  width: 100%;
  height: auto;
}
.stage-chart {
  margin-top: 16px;
}
.stage-chart h3 {
  margin: 0 0 8px;
  font-size: 16px;
}
.stage-chart svg {
  width: 100%;
  height: auto;
}
@media (max-width: 820px) {
  .header {
    align-items: flex-start;
    flex-direction: column;
  }
  .metrics,
  .chart-grid {
    grid-template-columns: 1fr;
  }
  h1 {
    font-size: 28px;
  }
}
"""
