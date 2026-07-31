"""
Owner: Hridya (network layer)

Loads data/network/raw/*.csv, trains an anomaly detector (e.g. IsolationForest),
and writes flagged rows to detectors/network_detector/output/flags.json in the
shared format defined in docs/data_contract.md (layer = "network").

See coder_checklists.md > Hridya > Phase 2.
"""

# TODO: implement detector training pipeline.
import os
import random
import json
from datetime import datetime, timezone, timedelta
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest

df = pd.read_csv("claire/data/network/raw/CICIDS2017.csv", low_memory=False)

# print(df.head(5))
# print(df.info())

df = df.dropna()

df.columns = df.columns.str.strip()

# print(df['Label'].value_counts())

y = (df["Label"] != "BENIGN").astype(int)  # 0=normal, 1=attack
contamination = round(float(y.mean()), 2)

X = df.drop(columns=["Label"]).copy()
X["Destination Port"] = pd.to_numeric(X["Destination Port"], errors="coerce").fillna(0)
X.replace([np.inf, -np.inf], np.nan, inplace=True)
X.fillna(0, inplace=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = IsolationForest(contamination=contamination, random_state=42)
model.fit(X_train)

raw_preds = model.predict(X_test)
raw_scores = model.decision_function(X_test)

# Normalize scores to [0.0, 1.0]
min_s, max_s = raw_scores.min(), raw_scores.max()
anomaly_scores = 1 - (raw_scores - min_s) / (max_s - min_s)

y_pred = (raw_preds == -1).astype(int)

caught = ((y_pred == 1) & (y_test == 1)).sum()
missed = ((y_pred == 0) & (y_test == 1)).sum()
fp = ((y_pred == 1) & (y_test == 0)).sum()
tn = ((y_pred == 0) & (y_test == 0)).sum()

print(f"\nAttacks caught  (TP): {caught:,}")
print(f"Attacks missed  (FN): {missed:,}")
print(f"False alarms    (FP): {fp:,}")
print(f"Detection Rate:       {caught / (caught + missed):.2%}")
print(f"False Alarm Rate:     {fp / (fp + tn):.2%}")
print(classification_report(y_test, y_pred, target_names=["BENIGN", "ATTACK"]))

users = [
    "USR-001",
    "USR-002",
    "USR-003",
    "USR-004",
    "USR-005",
    "USR-006",
    "USR-007",
    "USR-008",
    "USR-009",
    "USR-010",
    "USR-011",
    "USR-012",
    "USR-013",
    "USR-014",
    "USR-015",
    "USR-016",
    "USR-017",
    "USR-018",
    "USR-019",
    "USR-020",
    "USR-021",
    "USR-022",
    "USR-023",
    "USR-024",
    "USR-025",
]
hosts = [
    "HOST-001",
    "HOST-002",
    "HOST-003",
    "HOST-004",
    "HOST-005",
    "HOST-006",
    "HOST-007",
    "HOST-008",
    "HOST-009",
    "HOST-010",
    "HOST-011",
    "HOST-012",
    "HOST-013",
    "HOST-014",
    "HOST-015",
    "HOST-016",
    "HOST-017",
    "HOST-018",
    "HOST-019",
    "HOST-020",
    "HOST-021",
    "HOST-022",
    "HOST-023",
    "HOST-024",
    "HOST-025",
]

start = datetime(2026, 6, 1, 0, 0, 0, tzinfo=timezone.utc)
end = datetime(2026, 6, 30, 23, 59, 59, tzinfo=timezone.utc)
delta_seconds = int((end - start).total_seconds())


def random_timestamp():
    return (start + timedelta(seconds=random.randint(0, delta_seconds))).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


flagged_mask = y_pred == 1

random.seed(42)
assigned_users = [random.choice(users) for _ in range(len(X_test))]
assigned_hosts = [random.choice(hosts) for _ in range(len(X_test))]
assigned_timestamps = [random_timestamp() for _ in range(len(X_test))]

flags = []
for i in range(len(X_test)):
    if flagged_mask[i]:
        flags.append(
            {
                "entity": assigned_users[i],
                "host": assigned_hosts[i],
                "timestamp": assigned_timestamps[i],
                "anomaly_score": round(float(anomaly_scores[i]), 3),
                "layer": "network",
            }
        )

flags.append(
    {
        "entity": "incident_demo_01",
        "host": "incident_demo_01",
        "timestamp": "2026-07-01T10:08:00Z",
        "anomaly_score": 0.95,
        "layer": "cloud",
    }
)

with open("claire/detectors/network_detector/output/flags.json", "w") as f:
    json.dump(flags, f, indent=2)

print(
    f"Wrote {len(flags)} flagged rows to detectors/network_detector/output/flags.json"
)
