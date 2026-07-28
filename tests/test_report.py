import runpy
from pathlib import Path


def test_simple_line_report_contains_expected_strings():
    repo_root = Path(__file__).resolve().parents[1]
    example = repo_root / "examples" / "run_simple_line.py"
    assert example.exists(), f"Example script not found: {example}"

    # Execute the example to produce the report file
    runpy.run_path(str(example), run_name="__main__")

    report_file = repo_root / "simple_line_report.md"
    assert report_file.exists(), "Report file simple_line_report.md was not created"

    text = report_file.read_text(encoding="utf-8")

    assert "# Simple Line Scenario Report" in text
    assert "Best scenario: balanced line" in text
    assert "overloaded line" in text
