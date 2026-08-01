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

scores = model.decision_function(X_test)
min_score = scores.min()
max_score = scores.max()
normalized_scores = 1 - ((scores - min_score) / (max_score - min_score))

'''print(classification_report(y_test, predictions))

cm = confusion_matrix(y_test, predictions)

TN, FP, FN, TP = cm.ravel()

print(f"True Positives (Caught attacks): {TP}")
print(f"False Negatives (Missed attacks): {FN}")
print(f"False Positives (False alarms): {FP}")
print(f"True Negatives (Correctly identified normal): {TN}")'''

users = [
    "USR-001", "USR-002", "USR-003", "USR-004", "USR-005",
    "USR-006", "USR-007", "USR-008", "USR-009", "USR-010",
    "USR-011", "USR-012", "USR-013", "USR-014", "USR-015",
    "USR-016", "USR-017", "USR-018", "USR-019", "USR-020",
    "USR-021", "USR-022", "USR-023", "USR-024", "USR-025"
]

hosts = [
    "HOST-001", "HOST-002", "HOST-003", "HOST-004", "HOST-005",
    "HOST-006", "HOST-007", "HOST-008", "HOST-009", "HOST-010",
    "HOST-011", "HOST-012", "HOST-013", "HOST-014", "HOST-015",
    "HOST-016", "HOST-017", "HOST-018", "HOST-019", "HOST-020",
    "HOST-021", "HOST-022", "HOST-023", "HOST-024", "HOST-025"
]


start = datetime(2026, 6, 1, 0, 0, 0)
end = datetime(2026, 6, 30, 23, 59, 59)
def random_timestamp():
    delta = end - start
    random_seconds = random.randint(0,int(delta.total_seconds()))

    return (start + timedelta(seconds=random_seconds)).strftime("%Y-%m-%dT%H:%M:%SZ")


flags = []
f_val = {
    "entity": "incident_demo_01", 
    "host": "incident_demo_01", 
    "timestamp": "2026-07-01T10:04:00Z", 
    "anomaly_score": 0.95, 
    "layer": "os"
}
flags.append(f_val)

for pred, score in zip(predictions, normalized_scores):
    if pred == 1:
        flag = {
            "entity": random.choice(users),
            "host": random.choice(hosts),
            "timestamp": random_timestamp(),
            "anomaly_score": round(float(score), 4),
            "layer": "os"
        }
        flags.append(flag)

with open("detectors/os_detector/output/flags.json", "w") as file:
    json.dump(flags, file, indent=2)