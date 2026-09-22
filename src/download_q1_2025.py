import argparse
import json
import time
from pathlib import Path

import pandas as pd
import requests

API_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
SELECTED_COLUMNS = [
    "unique_key",
    "created_date",
    "closed_date",
    "agency",
    "agency_name",
    "complaint_type",
    "descriptor",
    "status",
    "due_date",
    "resolution_action_updated_date",
    "resolution_description",
    "borough",
    "open_data_channel_type",
]
PERIOD_START = "2025-01-01T00:00:00.000"
PERIOD_END = "2025-04-01T00:00:00.000"
BATCH_SIZE = 1000
MAX_ATTEMPTS = 3
BATCH_DIRECTORY = Path("data/raw/q1_2025_batches")
CHECKPOINT_PATH = Path("data/raw/q1_2025_checkpoint.json")


def load_checkpoint():
    if not CHECKPOINT_PATH.exists():
        return {"last_created_date": None, "last_unique_key": None, "next_batch": 1}

    with CHECKPOINT_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def build_where(checkpoint):
    where = (
        f"created_date >= '{PERIOD_START}' "
        f"AND created_date < '{PERIOD_END}'"
    )

    if checkpoint["last_created_date"] is None:
        return where

    return (
        f"{where} AND ("
        f"created_date > '{checkpoint['last_created_date']}' "
        f"OR (created_date = '{checkpoint['last_created_date']}' "
        f"AND unique_key > '{checkpoint['last_unique_key']}')"
        ")"
    )


def download_one_batch(checkpoint):
    params = {
        "$select": ",".join(SELECTED_COLUMNS),
        "$where": build_where(checkpoint),
        "$order": "created_date ASC, unique_key ASC",
        "$limit": BATCH_SIZE,
    }

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(API_URL, params=params, timeout=30)
            response.raise_for_status()
            break
        except requests.RequestException as error:
            if attempt == MAX_ATTEMPTS:
                raise SystemExit(
                    f"API request failed after {MAX_ATTEMPTS} attempts: {error}"
                ) from error

            wait_seconds = 2 ** (attempt - 1)
            print(f"Request failed; retrying in {wait_seconds} second(s)...")
            time.sleep(wait_seconds)

    return pd.DataFrame(response.json()).reindex(columns=SELECTED_COLUMNS)


def save_checkpoint(checkpoint):
    with CHECKPOINT_PATH.open("w", encoding="utf-8") as file:
        json.dump(checkpoint, file, indent=2)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Download NYC 311 Q1 2025 data in resumable batches."
    )
    parser.add_argument(
        "--batches",
        type=int,
        default=1,
        help="Number of batches to download in this run (default: 1).",
    )
    arguments = parser.parse_args()

    if arguments.batches < 1:
        parser.error("--batches must be at least 1.")

    return arguments


def main():
    arguments = parse_arguments()
    BATCH_DIRECTORY.mkdir(parents=True, exist_ok=True)

    for _ in range(arguments.batches):
        checkpoint = load_checkpoint()
        batch = download_one_batch(checkpoint)

        if batch.empty:
            print("No more records found in the analysis period.")
            return

        batch_number = checkpoint["next_batch"]
        batch_path = BATCH_DIRECTORY / f"batch_{batch_number:04d}.csv"
        if batch_path.exists():
            raise SystemExit(f"Batch file already exists: {batch_path}")

        batch.to_csv(batch_path, index=False)

        last_row = batch.iloc[-1]
        updated_checkpoint = {
            "last_created_date": last_row["created_date"],
            "last_unique_key": last_row["unique_key"],
            "next_batch": batch_number + 1,
        }
        save_checkpoint(updated_checkpoint)

        print(f"Saved {len(batch)} rows to: {batch_path}")
        print("Next cursor:")
        print("created_date:", updated_checkpoint["last_created_date"])
        print("unique_key:", updated_checkpoint["last_unique_key"])


if __name__ == "__main__":
    main()
