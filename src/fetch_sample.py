import pandas as pd
import requests

API_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"

params = {
    "$select": """
        unique_key,
        created_date,
        closed_date,
        agency,
        agency_name,
        complaint_type,
        descriptor,
        status,
        due_date,
        resolution_action_updated_date,
        resolution_description,
        borough,
        open_data_channel_type
    """,
    "$where": (
        "created_date >= '2025-01-01T00:00:00.000' "
        "AND created_date < '2025-04-01T00:00:00.000'"
    ),
    "$order": "created_date ASC",
    "$limit": 100,
}

response = requests.get(API_URL, params=params, timeout=30)
response.raise_for_status()

sample = pd.DataFrame(response.json())

print("Shape:", sample.shape)
print("Columns:", sample.columns.tolist())
print(sample.head(3).to_string())