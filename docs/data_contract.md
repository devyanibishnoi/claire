# Data Contract

**Status: DRAFT — lock this together as a team on Day 1, then treat it as frozen.** If it ever needs to change, post in the team chat first — the Lead's fusion code depends on this matching exactly.

Every detector's `output/flags.json` must be a list of objects shaped like this:

```json
[
  {
    "entity": "user123 or 10.0.0.5 or an account ID",
    "host": "hostname or machine ID",
    "timestamp": "2026-07-25T14:32:00Z",
    "anomaly_score": 0.87,
    "layer": "network"
  }
]
```

| Field | Meaning |
|---|---|
| `entity` | Whatever identifies "who" (a user, an IP, an account) |
| `host` | Whatever identifies "where" (a machine or hostname) |
| `timestamp` | ISO 8601 format, so it sorts and compares correctly |
| `anomaly_score` | A number from 0.0 to 1.0, higher means more suspicious |
| `layer` | Always exactly `"network"`, `"os"`, or `"cloud"` depending on which detector wrote it |

As long as every detector writes this exact shape, `fusion/fuse.py` can read all three without ever opening anyone else's code.
