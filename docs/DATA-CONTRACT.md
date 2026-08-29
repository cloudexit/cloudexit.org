# Public data contract

Every public dataset under `static/data/` must be immutable by version and ship
with the following files:

```text
<dataset>/<version>/
├── data.csv or data.yaml
├── schema.json
├── sources.csv
├── methodology.md
├── checksums.txt
└── README.md
```

## Required record metadata

- dataset ID and version;
- published, collected-from, and collected-to dates;
- source URL, publisher, source tier, and access date;
- product, region, plan, currency, unit, and commercial term where applicable;
- raw value, normalized value, and the formula or transform version;
- applicability boundary, exclusions, uncertainty, and status;
- license or reuse note;
- correction or withdrawal reference.

## Lifecycle states

`draft → internal-review → public-current → public-stale → corrected | withdrawn`

Published bytes are not overwritten. A correction produces a new revision and
links the previous one. The site may change which revision it calls current,
but old URLs and checksums remain resolvable.

## No silent joins

When a chart combines provider prices, hardware inputs, exchange rates, or
first-party case data, the join keys and dates are part of the method. A human
reader must be able to trace every plotted value back to a row and source.

