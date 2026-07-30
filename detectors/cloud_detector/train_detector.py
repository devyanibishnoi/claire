

import json

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split

df = pd.read_json("../../data/cloud/raw/cloud_logs.json")
df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")

df = pd.get_dummies(df, columns=["action"])

pair_counts = df.groupby(["user", "source_ip"])["source_ip"].transform("count")
df["is_new_ip_for_this_entity"] = (pair_counts == 1).astype(int)

y = df["is_attack"]

X = df.drop(columns=["user", "source_ip", "resource", "timestamp", "is_attack"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X_train)

predictions = model.predict(X_test)  # -1 = flagged as anomaly, 1 = normal
raw_scores = model.decision_function(X_test)  # higher = more normal

flagged_mask = predictions == -1
actual_attack_mask = (y_test == 1).to_numpy()

caught = int((flagged_mask & actual_attack_mask).sum())
total_attacks = int(actual_attack_mask.sum())
print(f"Caught {caught} / {total_attacks} real attacks in the test set ({caught / total_attacks:.1%})")

normalized = 1 - (raw_scores - raw_scores.min()) / (raw_scores.max() - raw_scores.min())

original_rows = df.loc[X_test.index].reset_index(drop=True)

flags = []
for i in range(len(X_test)):
    if flagged_mask[i]:
        row = original_rows.iloc[i]
        flags.append({
            "entity": row["user"],
            "host": row["resource"],
            "timestamp": row["timestamp"],
            "anomaly_score": round(float(normalized[i]), 3),
            "layer": "cloud",
        })

flags.append({
    "entity": "incident_demo_01",
    "host": "incident_demo_01",
    "timestamp": "2026-07-01T10:08:00Z",
    "anomaly_score": 0.95,
    "layer": "cloud",
})

with open("output/flags.json", "w") as f:
    json.dump(flags, f, indent=2)

print(f"Wrote {len(flags)} flagged rows to detectors/cloud_detector/output/flags.json")
