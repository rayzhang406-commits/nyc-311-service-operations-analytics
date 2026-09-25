from pathlib import Path

import pandas as pd

INPUT_PATH = Path("data/processed/nyc311_q1_2025_analysis_ready.csv")
OUTPUT_DIRECTORY = Path("data/processed/overview")
CHUNK_SIZE = 100_000


def main():
    if not INPUT_PATH.exists():
        raise SystemExit(f"Analysis-ready data file not found: {INPUT_PATH}")

    borough_complaint_counts = None
    for chunk in pd.read_csv(
        INPUT_PATH,
        usecols=["borough", "complaint_type"],
        chunksize=CHUNK_SIZE,
    ):
        current_counts = chunk.groupby(["borough", "complaint_type"]).size()
        borough_complaint_counts = (
            current_counts
            if borough_complaint_counts is None
            else borough_complaint_counts.add(current_counts, fill_value=0)
        )

    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    mix = borough_complaint_counts.rename("requests").reset_index()
    mix["requests"] = mix["requests"].astype(int)
    mix["borough_total_requests"] = mix.groupby("borough")["requests"].transform("sum")
    mix["borough_share_pct"] = (
        mix["requests"] / mix["borough_total_requests"] * 100
    ).round(2)
    mix = mix.sort_values(["borough", "requests"], ascending=[True, False])

    top_three = mix.groupby("borough", group_keys=False).head(3)
    mix.to_csv(OUTPUT_DIRECTORY / "borough_complaint_mix.csv", index=False)
    top_three.to_csv(OUTPUT_DIRECTORY / "top_complaints_by_borough.csv", index=False)

    print("Saved borough-complaint tables to:", OUTPUT_DIRECTORY)
    print("\nTop three complaint types in each borough:")
    print(
        top_three[
            ["borough", "complaint_type", "requests", "borough_share_pct"]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
