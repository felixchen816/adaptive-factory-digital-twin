import csv


def write_rows_to_csv(rows, output_path):
    """Write comparison rows to a CSV file."""
    if not rows:
        return

    fieldnames = rows[0].keys()

    with open(output_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
