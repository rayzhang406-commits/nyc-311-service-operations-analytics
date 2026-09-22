# Data Source

- Dataset: NYC 311 Service Requests from 2020 to Present
- Provider: NYC 311
- Platform: NYC Open Data
- Dataset ID: `erm2-nwe9`
- Update frequency: Daily
- Unit of observation: One public 311 service request per row
- Data dictionary version: Updated 2025
- Analysis period: January 1, 2025 to March 31, 2025
- Record count at scope check: 884,765
- Scope check date: September 8, 2026
- Extraction completed: September 22, 2026
- Extracted record count: 884,765
- Extraction method: Deterministic keyset pagination by `created_date` and `unique_key`

Dataset URL: https://data.cityofnewyork.us/resource/erm2-nwe9.json

## Important limitations

- Field values and request statuses may change because the dataset is updated daily.
- `Due Date` represents an expected agency update date, not necessarily a closure deadline.
- Agency comparisons require caution because agencies handle different types of requests.
- Exact addresses and coordinates will not be used in the initial analysis.
