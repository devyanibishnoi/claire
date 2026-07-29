import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import json

df = pd.read_csv("data/os/raw/os_logs.csv")

y = df["class"]
X = df.drop(columns=["class"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X_train)

predictions = model.predict(X_test)
predictions = [1 if p == -1 else 0 for p in predictions]

scores = model.decision_function(X_test)
flags = []

for idx, pred, score in zip(X_test.index, predictions, scores):
    if pred == 1:
        flag = {
            "entity": f"user_{idx}",
            "host": "host_01",
            "timestamp": "N/A",
            "anomaly_score": float(score),
            "layer": "os"
        }
        flags.append(flag)

with open("detectors/os_detector/output/flags.json", "w") as file:
    json.dump(flags, file, indent=4)