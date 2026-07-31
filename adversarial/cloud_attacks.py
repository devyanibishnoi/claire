import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split

df = pd.read_json("../data/cloud/raw/cloud_logs.json")
df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")

df = pd.get_dummies(df, columns=["action"])

pair_counts = df.groupby(["user", "source_ip"])["source_ip"].transform("count")
df["is_new_ip_for_this_entity"] = (pair_counts == 1).astype(int)

y = df["is_attack"]

X = df.drop(columns=["user", "source_ip", "resource", "timestamp", "is_attack"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X_train)

attack_rows = X_test[y_test == 1].sample(n=30, random_state=42)

baseline_predictions = model.predict(attack_rows)
baseline_caught = int((baseline_predictions == -1).sum())

mimicry_rows = attack_rows.copy()
mimicry_rows["is_new_ip_for_this_entity"] = 0

evasion_predictions = model.predict(mimicry_rows)
evaded_caught = int((evasion_predictions == -1).sum())

print(f"Baseline: {baseline_caught} / {len(attack_rows)} caught before any modification")
print(f"After credential-use mimicry: {evaded_caught} / {len(attack_rows)} still caught")
print(f"Evasion success rate: {(len(attack_rows) - evaded_caught) / len(attack_rows):.1%}")
