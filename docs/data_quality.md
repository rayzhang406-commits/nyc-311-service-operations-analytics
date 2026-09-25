# Data Quality: NYC 311 Q1 2025 Extract

## Extract Overview

- Records: 884,765
- Columns: 13
- Created-date range: 2025-01-01 00:00:12 to 2025-03-31 23:59:57
- Invalid `created_date` values: 0
- Batch validation: 213 continuous batches, no duplicate `unique_key` values, and no invalid batch boundaries

## Missing Values

| Field | Missing records | Missing rate | Analytical handling |
| --- | ---: | ---: | --- |
| `closed_date` | 10,116 | 1.14% | Calculate closure time only for records with a valid closed date; report coverage. |
| `descriptor` | 16,789 | 1.90% | Retain as missing; exclude missing values only from descriptor-level summaries. |
| `due_date` | 880,616 | 99.53% | Exclude from operational timing metrics. It is also an expected agency update date, not a closure deadline. |
| `resolution_action_updated_date` | 3,499 | 0.40% | Retain as missing; do not use as a substitute for `closed_date`. |
| `resolution_description` | 11,404 | 1.29% | Retain as missing; use only in optional text-based exploration. |

The remaining extracted fields have no missing values.

## Resolution-Time Validity

- Records with a `closed_date`: 874,649
- Records with `status` equal to `Closed`: 877,281
- Records with a valid non-negative resolution time: 874,285
- Records with a negative resolution time: 364

The analysis-ready dataset retains all records. `has_closed_date` identifies records with a closure timestamp, while `status_is_closed` identifies records whose status is `Closed` in the extraction snapshot. These fields are not interchangeable: some records have a closed status but no closure timestamp. The dataset sets `resolution_hours` only when both timestamps are present and the computed duration is non-negative. The 364 negative-duration records are excluded from resolution-time summaries and remain available for data-quality review.

## Implications for Analysis

- Request-volume, agency, complaint-type, borough, status, and channel analyses can use the full extract.
- Resolution-time analysis uses only records with a valid non-negative `resolution_hours` value.
- The project does not use `due_date` to infer SLA compliance, priority, or a closure deadline.
