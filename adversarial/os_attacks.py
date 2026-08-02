import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import random

random.seed(42)
df = pd.read_csv("data/os/raw/os_logs.csv")

y = df["class"]
X = df.drop(columns=["class"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X_train)

predictions = model.predict(X_test)
predictions = [1 if p == -1 else 0 for p in predictions]

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
    obfuscated_rows[col] = (obfuscated_rows[col] * 0.9)

evasion_predictions = model.predict(obfuscated_rows)
evaded_caught = (evasion_predictions == -1).sum()

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

print("=== Retraining with Multiple Obfuscated Samples ===")

attack_train = X_train[y_train == 1].sample(
    n=30,
    random_state=42
)

obfuscated_train_90 = attack_train.copy()
obfuscated_train_80 = attack_train.copy()
obfuscated_train_95 = attack_train.copy()

for col in columns_to_modify:

    obfuscated_train_90[col] = (
        obfuscated_train_90[col] * 0.90
    ).round()

    obfuscated_train_80[col] = (
        obfuscated_train_80[col] * 0.80
    ).round()

    obfuscated_train_95[col] = (
        obfuscated_train_95[col] * 0.95
    ).round()

X_train_retrained = pd.concat(
    [
        X_train,
        obfuscated_train_90,
        obfuscated_train_80,
        obfuscated_train_95
    ],
    ignore_index=True
)

retrained_model = IsolationForest(
    contamination=0.1,
    random_state=42
)

retrained_model.fit(X_train_retrained)

after_predictions = retrained_model.predict(
    obfuscated_rows
)

after_caught = int(
    (after_predictions == -1).sum()
)

print("\n=== Comparison ===")

print("Before defenses:")
print(f"Caught: {evaded_caught}/{len(obfuscated_rows)}")
print(f"Detection Rate: {evaded_caught / len(obfuscated_rows):.2%}")

print("\nAfter defenses:")
print(f"Caught: {after_caught}/{len(obfuscated_rows)}")
print(f"Detection Rate: {after_caught / len(obfuscated_rows):.2%}")

y_true = [1] * len(obfuscated_rows)

y_pred = [
    1 if pred == -1 else 0
    for pred in after_predictions
]

tn, fp, fn, tp = confusion_matrix(
    y_true,
    y_pred,
    labels=[0, 1]
).ravel()

print("\n=== Confusion Matrix (After Defenses) ===")
print(f"True Positives (Caught attacks): {tp}")
print(f"False Negatives (Missed attacks): {fn}")
print(f"False Positives: {fp}")
print(f"True Negatives: {tn}")

print("\n==============================")
print("Experimental Evaluation (Contamination = 0.30)")
print("==============================")

experimental_model = IsolationForest(
    contamination=0.30,
    random_state=42
)

experimental_model.fit(X_train)
experimental_predictions = experimental_model.predict(X_test)

experimental_predictions = [
    1 if p == -1 else 0
    for p in experimental_predictions
]

print(classification_report(
    y_test,
    experimental_predictions
))

cm = confusion_matrix(
    y_test,
    experimental_predictions
)

TN, FP, FN, TP = cm.ravel()

print("\nConfusion Matrix")
print(cm)

print(f"\nTrue Positives : {TP}")
print(f"False Negatives: {FN}")
print(f"False Positives: {FP}")
print(f"True Negatives : {TN}")

attack_recall = TP / (TP + FN)
false_positive_rate = FP / (FP + TN)

print(f"\nAttack Recall      : {attack_recall:.2%}")
print(f"False Positive Rate: {false_positive_rate:.2%}")