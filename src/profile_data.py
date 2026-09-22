from pathlib import Path

import pandas as pd

DATA_PATH = Path("data/processed/nyc311_q1_2025.csv")
CHUNK_SIZE = 100_000


def main():
    if not DATA_PATH.exists():
        raise SystemExit(f"Merged data file not found: {DATA_PATH}")

    total_rows = 0
    missing_counts = None
    min_created_date = None
    max_created_date = None
    invalid_created_dates = 0

    for chunk in pd.read_csv(DATA_PATH, chunksize=CHUNK_SIZE):
        total_rows += len(chunk)

        chunk_missing = chunk.isna().sum()
        if missing_counts is None:
            missing_counts = chunk_missing
        else:
            missing_counts = missing_counts.add(chunk_missing, fill_value=0)

        created_dates = pd.to_datetime(chunk["created_date"], errors="coerce")
        invalid_created_dates += created_dates.isna().sum()

        chunk_min = created_dates.min()
        chunk_max = created_dates.max()
        min_created_date = chunk_min if min_created_date is None else min(min_created_date, chunk_min)
        max_created_date = chunk_max if max_created_date is None else max(max_created_date, chunk_max)

    print("Rows:", total_rows)
    print("Columns:", len(missing_counts))
    print("Created-date range:", min_created_date, "to", max_created_date)
    print("Invalid created_date values:", invalid_created_dates)
    print("\nMissing values:")
    for column, count in missing_counts.items():
        percentage = count / total_rows * 100
        print(f"{column}: {int(count)} ({percentage:.2f}%)")


if __name__ == "__main__":
    main()
