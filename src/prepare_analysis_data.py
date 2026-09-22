from pathlib import Path

import pandas as pd

INPUT_PATH = Path("data/processed/nyc311_q1_2025.csv")
OUTPUT_PATH = Path("data/processed/nyc311_q1_2025_analysis_ready.csv")
TEMPORARY_OUTPUT_PATH = OUTPUT_PATH.with_suffix(".tmp")
CHUNK_SIZE = 100_000


def main():
    if not INPUT_PATH.exists():
        raise SystemExit(f"Merged data file not found: {INPUT_PATH}")
    if OUTPUT_PATH.exists():
        raise SystemExit(f"Output file already exists: {OUTPUT_PATH}")
    if TEMPORARY_OUTPUT_PATH.exists():
        raise SystemExit(f"Temporary output file already exists: {TEMPORARY_OUTPUT_PATH}")

    rows_written = 0
    closed_records = 0
    valid_resolution_records = 0
    negative_resolution_records = 0
    first_chunk = True

    for chunk in pd.read_csv(INPUT_PATH, chunksize=CHUNK_SIZE):
        created_datetime = pd.to_datetime(chunk["created_date"], errors="coerce")
        closed_datetime = pd.to_datetime(chunk["closed_date"], errors="coerce")
        resolution_hours = (closed_datetime - created_datetime).dt.total_seconds() / 3600

        is_closed = closed_datetime.notna()
        has_valid_resolution_time = is_closed & created_datetime.notna() & (resolution_hours >= 0)
        has_negative_resolution_time = is_closed & created_datetime.notna() & (resolution_hours < 0)

        chunk["is_closed"] = is_closed
        chunk["has_valid_resolution_time"] = has_valid_resolution_time
        chunk["resolution_hours"] = resolution_hours.where(has_valid_resolution_time)

        chunk.to_csv(
            TEMPORARY_OUTPUT_PATH,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False,
        )

        rows_written += len(chunk)
        closed_records += is_closed.sum()
        valid_resolution_records += has_valid_resolution_time.sum()
        negative_resolution_records += has_negative_resolution_time.sum()
        first_chunk = False

    TEMPORARY_OUTPUT_PATH.replace(OUTPUT_PATH)

    print("Rows written:", rows_written)
    print("Records with closed_date:", closed_records)
    print("Records with valid resolution time:", valid_resolution_records)
    print("Records with negative resolution time:", negative_resolution_records)
    print("Saved analysis-ready data to:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
