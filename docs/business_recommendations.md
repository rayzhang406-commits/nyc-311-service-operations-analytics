# Operational Interpretation and Recommendations

## Evidence-Based Observations

1. Request demand is concentrated. Brooklyn, Bronx, and Queens account for 77.65% of Q1 2025 requests.
2. Demand mix differs by borough. Residential noise and HEAT/HOT WATER dominate the Bronx; Illegal Parking is the largest category in Brooklyn and Queens; Street Condition is relatively prominent in Staten Island's top-three mix.
3. Closure-time distributions differ sharply by complaint type. High-volume parking and noise categories typically close in hours, while housing-condition categories have much longer median and tail durations.
4. The extraction snapshot contains 7,484 requests whose status is not `Closed`. Most are marked `In Progress`.

## Recommended Uses

- Use daily request-volume monitoring to identify demand peaks and plan intake, triage, or communications capacity. The Q1 peak is descriptive evidence, not a forecast by itself.
- Review demand by borough and complaint type together when planning operational attention. A single citywide ranking hides material differences in local request mix.
- Monitor median and 90th-percentile resolution time within comparable complaint types. Do not compare agency-level durations without accounting for the mix and complexity of work.
- Separate status-based snapshot monitoring from closure-time reporting. `status` and `closed_date` are not fully interchangeable in this public extract.

## Interpretation Limits

- Request counts are not adjusted for population, land area, reporting behavior, or service eligibility.
- The dataset does not establish causes for volume peaks or duration differences.
- Status is observed at the September 22, 2026 extraction snapshot; it cannot reconstruct a historical backlog at the end of Q1 2025.
- `due_date` is missing for 99.53% of records and is not a closure deadline. This project makes no SLA, priority, or compliance claim from that field.
- The results describe public 311 service-request records only; they do not include confidential employer, vendor, or operational data.
