"""
Owner: Hridya (network layer)

Loads data/network/raw/*.csv, trains an anomaly detector (IsolationForest),
and writes flagged rows to detectors/network_detector/output/flags.json in the
shared format defined in docs/data_contract.md (layer = "network").

See coder_checklists.md > Hridya > Phase 2, Phase 8, Phase 9.
"""

import os
import random
import json
from datetime import datetime, timezone, timedelta
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest

# Paths relative to this script file -- works no matter which directory you run from
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.join(SCRIPT_DIR, "..", "..")
CSV_PATH = os.path.join(REPO_ROOT, "data", "network", "raw", "CICIDS2017.csv")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "output", "flags.json")

# ---- Phase 2: Train the detector ----

df = pd.read_csv(CSV_PATH, low_memory=False)
df = df.dropna()
df.columns = df.columns.str.strip()

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

users = [f"USR-{i:03d}" for i in range(1, 26)]
hosts = [f"HOST-{i:03d}" for i in range(1, 26)]

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

# ---- Phase 8: Feature Attribution ----
# For each real flagged row, find which single feature contributed most to its
# anomaly score using leave-one-feature-out against decision_function().

X_test_reset = X_test.reset_index(drop=True)
feature_names = list(X_test_reset.columns)
column_means = X_test_reset.mean()


def get_top_feature(row_series):
    """Replace one feature at a time with its column mean, re-score, find the
    feature whose removal drops the anomaly score the most."""
    # Pass as a single-row DataFrame to keep feature names -- avoids sklearn warning
    baseline = model.decision_function(row_series.to_frame().T)[0]
    max_drop = -float("inf")
    top_feat = None
    for col in feature_names:
        modified = row_series.copy()
        modified[col] = column_means[col]
        new_score = model.decision_function(modified.to_frame().T)[0]
        drop = baseline - new_score
        if drop > max_drop:
            max_drop = drop
            top_feat = col
    return top_feat


# Build flags -- top_feature computed automatically for every real flagged row
# Cap at 1000 rows for attribution: the paper needs the method demonstrated,
# not exhaustive attribution on every detection. Rows beyond the cap get top_feature=null.
ATTRIBUTION_CAP = 1000
total_flagged = flagged_mask.sum()
print(
    f"\nRunning feature attribution on {min(ATTRIBUTION_CAP, total_flagged)} of {total_flagged} flagged rows..."
)
flags = []
done = 0
for i in range(len(X_test_reset)):
    if flagged_mask[i]:
        row = X_test_reset.iloc[i]
        done += 1
        if done % 50 == 0 or done == min(ATTRIBUTION_CAP, total_flagged):
            print(
                f"  Attribution progress: {done}/{min(ATTRIBUTION_CAP, total_flagged)}"
            )
        if done <= ATTRIBUTION_CAP:
            top_feat = get_top_feature(row)
        else:
            top_feat = None  # beyond cap -- attribution not computed
        flags.append(
            {
                "entity": assigned_users[i],
                "host": assigned_hosts[i],
                "timestamp": assigned_timestamps[i],
                "anomaly_score": round(float(anomaly_scores[i]), 3),
                "layer": "network",
                "top_feature": top_feat,
            }
        )

# Synthetic coordination row from Phase 2 -- no real feature vector, so top_feature is null
flags.append(
    {
        "entity": "incident_demo_01",
        "host": "incident_demo_01",
        "timestamp": "2026-07-01T10:00:00Z",
        "anomaly_score": 0.95,
        "layer": "network",
        "top_feature": None,
    }
)

# ---- Phase 9: Additional multi-stage scenarios (network-layer rows only) ----
# Genuine chains: same entity+host across all 3 layers, timestamps within 10-min fusion window.
# Decoys: fusion should NOT group these -- either different entity+host per layer, or timestamps too far apart.

scenario_rows = [
    # Genuine chain 1 -- APT lateral movement
    {
        "entity": "chain_apt_02",
        "host": "HOST-CHAIN-02",
        "timestamp": "2026-07-02T09:00:00Z",
        "anomaly_score": 0.91,
        "layer": "network",
        "top_feature": None,
    },
    # Genuine chain 2 -- credential theft chain
    {
        "entity": "chain_cred_03",
        "host": "HOST-CHAIN-03",
        "timestamp": "2026-07-03T14:00:00Z",
        "anomaly_score": 0.87,
        "layer": "network",
        "top_feature": None,
    },
    # Decoy 1 -- close timestamps but DIFFERENT entity+host per layer; fusion should NOT group
    {
        "entity": "decoy_net_01",
        "host": "HOST-DECOY-N1",
        "timestamp": "2026-07-04T10:00:00Z",
        "anomaly_score": 0.74,
        "layer": "network",
        "top_feature": None,
    },
    # Decoy 2 -- same entity+host but timestamps 90+ min apart (outside fusion window); fusion should NOT group
    {
        "entity": "decoy_lag_02",
        "host": "HOST-DECOY-L2",
        "timestamp": "2026-07-05T08:00:00Z",
        "anomaly_score": 0.69,
        "layer": "network",
        "top_feature": None,
    },
]
flags.extend(scenario_rows)

# ---- Write output ----
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    json.dump(flags, f, indent=2)

print(f"\nWrote {len(flags)} rows to {OUTPUT_PATH}")
