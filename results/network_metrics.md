# Network Detector — Metrics
### Owner: Hridya

## Baseline detection performance

| Metric | Value |
|---|---|
| True Positives (TP) | 469 |
| False Negatives (FN) | 531 |
| False Positives (FP) | 158 |
| True Negatives (TN) | 842 |
| Detection Rate (Recall) | 46.9% |
| Precision | 74.8% |

## Adversarial evaluation — evasion ("traffic padding")

| | Detection rate |
|---|---|
| Before defenses | 469/1000 (46.9%) |
| After adversarial retraining | 745/1000 (74.5%) |

## Full confusion matrix — before vs after hardening

| Metric | Before Hardening | After Hardening |
|---|---|---|
| TP | 469 | 745 |
| FN | 531 | 255 |
| FP | 158 | 623 |
| TN | 842 | 377 |
| Evasion success rate | 53.1% | 25.5% |
| Improvement | -- | +276 more caught |
