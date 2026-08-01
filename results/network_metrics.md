# Network Detector — Metrics
### Owner: Hridya

## Baseline detection performance

| Metric | Value |
|---|---|
| True Positives (TP) | 13 |
| False Negatives (FN) | 17 |
| False Positives (FP) | 5 |
| True Negatives (TN) | 25 |
| Detection Rate (Recall) | 43.3% |
| Precision | 72.2% |

## Adversarial evaluation — evasion ("traffic padding")

| | Detection rate |
|---|---|
| Before defenses | 13/30 (43.3%) |
| After adversarial retraining | 20/30 (66.7%) |

## Full confusion matrix — before vs after hardening

| Metric | Before Hardening | After Hardening |
|---|---|---|
| TP | 13 | 20 |
| FN | 17 | 10 |
| FP | 5 | 20 |
| TN | 25 | 10 |
| Evasion success rate | 56.7% | 33.3% |
| Improvement | -- | +7 more caught |
