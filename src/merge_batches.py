import csv
from pathlib import Path

BATCH_DIRECTORY = Path("data/raw/q1_2025_batches")
OUTPUT_PATH = Path("data/processed/nyc311_q1_2025.csv")
TEMPORARY_OUTPUT_PATH = OUTPUT_PATH.with_suffix(".tmp")


def batch_number(path):
    return int(path.stem.split("_")[-1])


def main():
    batch_paths = sorted(BATCH_DIRECTORY.glob("batch_*.csv"), key=batch_number)
    if not batch_paths:
        raise SystemExit(f"No batch files found in: {BATCH_DIRECTORY}")

    if OUTPUT_PATH.exists():
        raise SystemExit(f"Output file already exists: {OUTPUT_PATH}")
    if TEMPORARY_OUTPUT_PATH.exists():
        raise SystemExit(f"Temporary output file already exists: {TEMPORARY_OUTPUT_PATH}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    row_count = 0

    with (
        batch_paths[0].open(newline="", encoding="utf-8") as first_batch,
        TEMPORARY_OUTPUT_PATH.open("w", newline="", encoding="utf-8") as output_file,
    ):
        first_reader = csv.DictReader(first_batch)
        fieldnames = first_reader.fieldnames
        if not fieldnames:
            raise SystemExit(f"No header found in: {batch_paths[0]}")

        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        for batch_path in batch_paths:
            with batch_path.open(newline="", encoding="utf-8") as batch_file:
                reader = csv.DictReader(batch_file)
                if reader.fieldnames != fieldnames:
                    raise SystemExit(f"Column mismatch in: {batch_path}")

                for row in reader:
                    writer.writerow(row)
                    row_count += 1

    TEMPORARY_OUTPUT_PATH.replace(OUTPUT_PATH)
    print(f"Merged {len(batch_paths)} batches and {row_count} rows.")
    print("Saved merged file to:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
