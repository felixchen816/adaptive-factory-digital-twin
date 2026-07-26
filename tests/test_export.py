import csv

from factory_twin.export import write_rows_to_csv


def test_write_rows_to_csv_creates_file(tmp_path):
    output_path = tmp_path / "results.csv"
    rows = [
        {
            "scenario": "balanced line",
            "machine": "standard cutter",
            "line_status": "stable",
        },
        {
            "scenario": "overloaded line",
            "machine": "slow press",
            "line_status": "overloaded",
        },
    ]

    write_rows_to_csv(rows, output_path)

    assert output_path.exists()


def test_write_rows_to_csv_writes_header_and_rows(tmp_path):
    output_path = tmp_path / "results.csv"
    rows = [
        {
            "scenario": "balanced line",
            "machine": "standard cutter",
            "line_status": "stable",
        },
        {
            "scenario": "overloaded line",
            "machine": "slow press",
            "line_status": "overloaded",
        },
    ]

    write_rows_to_csv(rows, output_path)

    with open(output_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        written_rows = list(reader)

    assert reader.fieldnames == ["scenario", "machine", "line_status"]
    assert written_rows[0]["scenario"] == "balanced line"
    assert written_rows[1]["line_status"] == "overloaded"
