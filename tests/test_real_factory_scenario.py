from pathlib import Path

from factory_twin.config import load_multi_stage_scenarios
from factory_twin.multi_stage import simulate_production_line


REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = REPO_ROOT / "examples" / "tesla_fremont_model3y_scenario.json"


def test_tesla_fremont_scenario_loads_with_multiple_stages():
    scenarios = load_multi_stage_scenarios(SCENARIO_PATH)

    assert len(scenarios) == 1
    scenario = scenarios[0]
    assert scenario.name == "tesla fremont model 3/y public-capacity baseline"
    assert scenario.minutes == 10080
    assert len(scenario.line.machines) == 6
    assert scenario.arrival_rate > 1


def test_tesla_fremont_scenario_matches_public_capacity_scale():
    scenario = load_multi_stage_scenarios(SCENARIO_PATH)[0]

    metrics = simulate_production_line(
        scenario.line,
        scenario.minutes,
        scenario.arrival_rate,
    )

    annualized_output = metrics["throughput_per_hour"] * 24 * 365

    assert metrics["completed"] > 10000
    assert metrics["throughput_per_hour"] > 62
    assert abs(annualized_output - 550000) / 550000 < 0.01
    assert metrics["final_queue_lengths"]["blanking and stamping"] < 10
