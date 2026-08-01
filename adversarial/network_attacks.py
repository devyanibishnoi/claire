"""
Owner: Hridya (network layer)

Simulates evasion ("traffic padding") against the trained network detector:
slightly perturbs byte-count/duration fields on known-attack rows and checks
detection rate before/after adversarial retraining.

See coder_checklists.md > Hridya > Phase 3-4.
"""

# TODO: implement evasion attack + before/after evaluation.

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

attack_rows = X_test[y_test == 1].sample(n=25, random_state=42)

baseline_preds = model.predict(attack_rows)
baseline_caught = int((baseline_preds == -1).sum())

padding_cols = [
    "Flow Duration",
    "Total Length of Fwd Packets",
    "Total Length of Bwd Packets",
    "Fwd Packet Length Mean",
    "Bwd Packet Length Mean",
    "Flow Bytes/s",
    "Flow Packets/s",
    "Fwd Packets/s",
    "Bwd Packets/s",
    "Average Packet Size",
]

rng = np.random.default_rng(42)
padded_rows = attack_rows.copy()

for col in padding_cols:
    if col in padded_rows.columns:
        noise = rng.uniform(0.95, 1.05, size=len(padded_rows))  # ±5%
        padded_rows[col] = padded_rows[col] * noise

evasion_predictions = model.predict(padded_rows)
evaded_caught = int((evasion_predictions == -1).sum())

print(
    f"Baseline: {baseline_caught} / {len(attack_rows)} caught before any modification"
)
print(f"After traffic padding: {evaded_caught} / {len(attack_rows)} still caught")
print(
    f"Evasion success rate: {(len(attack_rows) - evaded_caught) / len(attack_rows):.1%}"
)

# ── PHASE 4: ADVERSARIAL RETRAINING ──────────────────────────────────────────

X_train_hardened = pd.concat([X_train, padded_rows], ignore_index=True)
y_train_hardened = pd.concat(
    [
        y_train,
        pd.Series([1] * len(padded_rows)),  # they are still attacks
    ],
    ignore_index=True,
)

hardened_model = IsolationForest(contamination=contamination, random_state=42)
hardened_model.fit(X_train_hardened)

hardened_preds = hardened_model.predict(padded_rows)
hardened_caught = int((hardened_preds == -1).sum())

print("\n -- Phase 4: After Adversarial Retraining --")
print(f"Before hardening:  {evaded_caught}/{len(attack_rows)} caught after evasion")
print(f"After hardening:   {hardened_caught}/{len(attack_rows)} caught after evasion")
print(f"Improvement:       +{hardened_caught - evaded_caught} more caught")
