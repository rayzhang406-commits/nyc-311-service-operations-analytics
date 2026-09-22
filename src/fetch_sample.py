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

params = {
    "$select": ",".join(SELECTED_COLUMNS),
    "$where": (
    "created_date >= '2025-01-01T00:00:00.000' "
    "AND created_date < '2025-04-01T00:00:00.000' "
    "AND ("
    "created_date > '2025-01-01T01:24:02.000' "
    "OR (created_date = '2025-01-01T01:24:02.000' "
    "AND unique_key > '63581103')"
    ")"
),
    "$order": "created_date ASC, unique_key ASC",
    "$limit": 1000,
}

try:
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
except requests.RequestException as error:
    raise SystemExit(f"API request failed: {error}") from error

sample = pd.DataFrame(response.json()).reindex(columns=SELECTED_COLUMNS)
output_path = "data/raw/nyc311_q1_2025_page_002.csv"
sample.to_csv(output_path, index=False)
print("Saved sample to:", output_path)

print("Shape:", sample.shape)
print("Columns:", sample.columns.tolist())
print(sample.head(3).to_string())
last_row = sample.iloc[-1]
print("\nLast cursor:")
print("created_date:", last_row["created_date"])
print("unique_key:", last_row["unique_key"])