from pathlib import Path

import pandas as pd

BATCH_DIRECTORY = Path("data/raw/q1_2025_batches")
REQUIRED_COLUMNS = ["unique_key", "created_date"]


def batch_number(path):
    return int(path.stem.split("_")[-1])


def main():
    paths = sorted(BATCH_DIRECTORY.glob("batch_*.csv"), key=batch_number)
    if not paths:
        raise SystemExit(f"No batch files found in: {BATCH_DIRECTORY}")

    numbers = [batch_number(path) for path in paths]
    expected_numbers = list(range(1, numbers[-1] + 1))
    missing_numbers = sorted(set(expected_numbers) - set(numbers))

    batches = [
        pd.read_csv(path, usecols=REQUIRED_COLUMNS, dtype={"unique_key": "string"})
        for path in paths
    ]
    data = pd.concat(batches, ignore_index=True)
    duplicate_keys = data["unique_key"].duplicated().sum()

    invalid_boundaries = []
    for previous, current, previous_path, current_path in zip(
        batches, batches[1:], paths, paths[1:]
    ):
        previous_cursor = (
            previous.iloc[-1]["created_date"],
            previous.iloc[-1]["unique_key"],
        )
        current_cursor = (
            current.iloc[0]["created_date"],
            current.iloc[0]["unique_key"],
        )
        if current_cursor <= previous_cursor:
            invalid_boundaries.append(f"{previous_path.name} -> {current_path.name}")

    print("Batch files:", len(paths))
    print("Total rows:", len(data))
    print("Duplicate unique_key values:", duplicate_keys)
    print("Missing batch numbers:", missing_numbers or "None")
    print("Invalid boundaries:", invalid_boundaries or "None")
    print("First batch:", paths[0].name)
    print("Latest batch:", paths[-1].name)

    if duplicate_keys or missing_numbers or invalid_boundaries:
        raise SystemExit("Batch validation failed.")

    print("Batch validation passed.")


if __name__ == "__main__":
    main()
