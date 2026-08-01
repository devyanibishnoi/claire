import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import random
from datetime import datetime, timedelta

random.seed(42)
df = pd.read_csv("data/os/raw/os_logs.csv")

y = df["class"]
X = df.drop(columns=["class"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X_train)

predictions = model.predict(X_test)
predictions = [1 if p == -1 else 0 for p in predictions]

#Attack Begins

attack_rows = X_test[y_test == 1].sample(n=30, random_state=42)

baseline_predictions = model.predict(attack_rows)
baseline_caught = int((baseline_predictions == -1).sum())

normal_rows = X_test[y_test == 0]

attack_normal_difference = (
    attack_rows.mean() - normal_rows.mean()
).abs().sort_values(ascending=False)

columns_to_modify = attack_normal_difference.head(7).index.tolist()

obfuscated_rows = attack_rows.copy()
for col in columns_to_modify:
    obfuscated_rows[col] = (obfuscated_rows[col] * 0.9).round()

evasion_predictions = model.predict(obfuscated_rows)
evaded_caught = (evasion_predictions == -1).sum()

#Results

print("=== Baseline ===")
print(f"Attack samples: {len(attack_rows)}")
print(f"Caught: {baseline_caught}")
print(f"Missed: {len(attack_rows) - baseline_caught}")
print(f"Detection Rate: {baseline_caught / len(attack_rows):.2%}")

print("=== After Log Obfuscation ===")
print(f"Attack samples: {len(obfuscated_rows)}")
print(f"Caught: {evaded_caught}")
print(f"Missed: {len(obfuscated_rows) - evaded_caught}")
print(f"Detection Rate: {evaded_caught / len(obfuscated_rows):.2%}")
#Attack End

print("=== Retraining with Obfuscated Samples ===")

# Create obfuscated training examples from training attacks
attack_train = X_train[y_train == 1].sample(
    n=15,
    random_state=42
)

obfuscated_train = attack_train.copy()

for col in columns_to_modify:
    obfuscated_train[col] = (obfuscated_train[col] * 0.9).round()

# Add to training
X_train_retrained = pd.concat(
    [
        X_train,
        obfuscated_train
    ],
    ignore_index=True
)

retrained_model = IsolationForest(
    contamination=0.1,
    random_state=42
)

retrained_model.fit(X_train_retrained)

# Test on the original 30 obfuscated attacks
after_predictions = retrained_model.predict(obfuscated_rows)

after_caught = int((after_predictions == -1).sum())

print("\n=== Comparison ===")

print("Before defenses:")
print(f"Caught: {evaded_caught}/{len(obfuscated_rows)}")
print(f"Detection Rate: {evaded_caught / len(obfuscated_rows):.2%}")

print("\nAfter defenses:")
print(f"Caught: {after_caught}/{len(obfuscated_rows)}")
print(f"Detection Rate: {after_caught / len(obfuscated_rows):.2%}")