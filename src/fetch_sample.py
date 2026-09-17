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
        "AND created_date < '2025-04-01T00:00:00.000'"
    ),
    "$order": "created_date ASC",
    "$limit": 100,
}

try:
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
except requests.RequestException as error:
    raise SystemExit(f"API request failed: {error}") from error

sample = pd.DataFrame(response.json()).reindex(columns=SELECTED_COLUMNS)
output_path = "data/raw/nyc311_q1_2025_sample.csv"
sample.to_csv(output_path, index=False)
print("Saved sample to:", output_path)

print("Shape:", sample.shape)
print("Columns:", sample.columns.tolist())
print(sample.head(3).to_string())