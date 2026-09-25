from pathlib import Path

import pandas as pd

INPUT_PATH = Path("data/processed/nyc311_q1_2025_analysis_ready.csv")
OUTPUT_DIRECTORY = Path("data/processed/overview")
CHUNK_SIZE = 100_000


def add_counts(total, current):
    return current if total is None else total.add(current, fill_value=0)


def save_count_table(counts, index_name, output_path):
    table = counts.rename("requests").rename_axis(index_name).reset_index()
    table["requests"] = table["requests"].astype(int)
    table["share_pct"] = (table["requests"] / table["requests"].sum() * 100).round(2)
    table.sort_values("requests", ascending=False).to_csv(output_path, index=False)


def main():
    if not INPUT_PATH.exists():
        raise SystemExit(f"Analysis-ready data file not found: {INPUT_PATH}")

    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)

    daily_counts = None
    borough_counts = None
    complaint_counts = None
    agency_counts = None
    non_closed_status_counts = None
    non_closed_complaint_counts = None

    columns = [
        "created_date",
        "borough",
        "complaint_type",
        "agency",
        "agency_name",
        "status",
        "status_is_closed",
    ]
    for chunk in pd.read_csv(INPUT_PATH, usecols=columns, chunksize=CHUNK_SIZE):
        dates = pd.to_datetime(chunk["created_date"]).dt.date
        daily_counts = add_counts(daily_counts, dates.value_counts())
        borough_counts = add_counts(borough_counts, chunk["borough"].value_counts())
        complaint_counts = add_counts(
            complaint_counts, chunk["complaint_type"].value_counts()
        )
        agency_counts = add_counts(
            agency_counts, chunk.groupby(["agency", "agency_name"]).size()
        )

        non_closed = chunk[chunk["status_is_closed"] == False]
        non_closed_status_counts = add_counts(
            non_closed_status_counts, non_closed["status"].value_counts()
        )
        non_closed_complaint_counts = add_counts(
            non_closed_complaint_counts, non_closed["complaint_type"].value_counts()
        )

    save_count_table(daily_counts, "created_date", OUTPUT_DIRECTORY / "daily_request_volume.csv")
    save_count_table(borough_counts, "borough", OUTPUT_DIRECTORY / "borough_request_volume.csv")
    save_count_table(
        complaint_counts,
        "complaint_type",
        OUTPUT_DIRECTORY / "complaint_type_volume.csv",
    )
    save_count_table(
        non_closed_status_counts,
        "status",
        OUTPUT_DIRECTORY / "non_closed_status_snapshot.csv",
    )
    save_count_table(
        non_closed_complaint_counts,
        "complaint_type",
        OUTPUT_DIRECTORY / "non_closed_complaint_types_snapshot.csv",
    )

    agency_table = agency_counts.rename("requests").reset_index()
    agency_table["requests"] = agency_table["requests"].astype(int)
    agency_table["share_pct"] = (
        agency_table["requests"] / agency_table["requests"].sum() * 100
    ).round(2)
    agency_table.sort_values("requests", ascending=False).to_csv(
        OUTPUT_DIRECTORY / "agency_volume.csv", index=False
    )

    resolution_data = pd.read_csv(
        INPUT_PATH,
        usecols=[
            "complaint_type",
            "has_valid_resolution_time",
            "resolution_hours",
        ],
    )
    valid_resolution_data = resolution_data[
        resolution_data["has_valid_resolution_time"] == True
    ]
    resolution_table = valid_resolution_data.groupby("complaint_type").agg(
        closed_requests=("resolution_hours", "size"),
        median_hours=("resolution_hours", "median"),
        p90_hours=("resolution_hours", lambda values: values.quantile(0.90)),
    )
    resolution_table["median_hours"] = resolution_table["median_hours"].round(2)
    resolution_table["p90_hours"] = resolution_table["p90_hours"].round(2)
    resolution_table.sort_values("closed_requests", ascending=False).to_csv(
        OUTPUT_DIRECTORY / "complaint_type_resolution.csv"
    )

    print("Saved overview tables to:", OUTPUT_DIRECTORY)
    print("Daily volume rows:", len(daily_counts))
    print("Complaint types:", len(complaint_counts))
    print("Agencies:", len(agency_table))


if __name__ == "__main__":
    main()
