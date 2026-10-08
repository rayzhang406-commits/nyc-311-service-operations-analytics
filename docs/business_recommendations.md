# What the Results Suggest

## What stands out in the data

- Brooklyn, Bronx, and Queens account for 77.65% of Q1 2025 requests. Residential noise and HEAT/HOT WATER are especially prominent in the Bronx, while Illegal Parking is the largest category in Brooklyn and Queens.
- Illegal Parking, HEAT/HOT WATER, and Noise - Residential together make up about 45% of all requests.
- Closure-time patterns vary substantially by complaint type. Parking and noise requests often close in hours, while housing-condition categories have longer median times and much longer tails.
- At extraction, 7,484 requests had a status other than `Closed`; most were marked `In Progress`.

## How these results could be used

- A follow-up analysis could begin with Brooklyn, the Bronx, and Queens, which together contain more than three quarters of the requests in this extract.
- For the three largest complaint types, volume and closure time should be shown separately. A category can be high-volume without having a long typical closure time.
- Housing-related categories should be compared with similar categories using median and 90th-percentile closure time. A citywide average would hide their longer tails relative to parking and noise requests.
- The non-`Closed` status count can be monitored as an extraction-date snapshot, but it should not be interpreted as the backlog at the end of Q1 2025.

See [data_quality.md](data_quality.md) for field limitations and handling decisions.
