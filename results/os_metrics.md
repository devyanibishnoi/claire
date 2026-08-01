
# OS/Endpoint Detector — Metrics

**Owner:** Anshika

## Baseline Detection Performance

| Metric | Value |
|---|---:|
| Accuracy | 83% |
| Precision (Attack Class) | 0.30 |
| Recall (Attack Class) | 0.25 |
| F1-score (Attack Class) | 0.27 |

---

## Adversarial Evaluation — Log Obfuscation

### Detection Rate

| Evaluation Stage | Detection Rate |
|---|---:|
| Before Defenses | 20.0% (6/30 attacks detected) |
| After Adversarial Retraining | 16.67% (5/30 attacks detected) |

---

## Before Defenses — Classification Report

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| 0 | 0.90 | 0.92 | 0.91 | 1042 |
| 1 | 0.30 | 0.25 | 0.27 | 149 |
| **Accuracy** | | | **0.83** | **1191** |
| **Macro Avg** | 0.60 | 0.58 | 0.59 | 1191 |
| **Weighted Avg** | 0.82 | 0.83 | 0.83 | 1191 |

---

## Confusion Matrix Metrics

| Metric | Count |
|---|---:|
| True Positives (Caught attacks) | 37 |
| False Negatives (Missed attacks) | 112 |
| False Positives (False alarms) | 87 |
| True Negatives (Correctly identified normal) | 955 |

---

## Adversarial Evaluation Details

- Attack samples selected: **30**
- Attack samples were selected from the attack-labeled test data.
- Obfuscation method: The seven features with the largest difference between attack and normal traffic were modified by multiplying their values by **0.9**, simulating a 10% reduction in suspicious log features.
- The modified attack samples were evaluated against the original detector.

### Results Before Defenses

| Metric | Value |
|---|---:|
| Attack Samples Tested | 30 |
| Attacks Detected | 6 |
| Attacks Missed | 24 |
| Detection Rate | 20.0% |

---

# After Adversarial Retraining

## Retraining Approach

- Obfuscated attack examples were added to the training dataset.
- The Isolation Forest model was retrained using the augmented training data.
- The retrained model was evaluated on the same set of 30 obfuscated attack samples.

## Results After Defenses

| Metric | Value |
|---|---:|
| Obfuscated Attack Samples Tested | 30 |
| Attacks Detected | 5 |
| Attacks Missed | 25 |
| Detection Rate | 16.67% |

---

## Comparison

| Stage | Detection |
|---|---:|
| Before Defenses | 6/30 (20.0%) |
| After Adversarial Retraining | 5/30 (16.67%) |

---

## Observation

The adversarial retraining approach did not improve detection performance in this experiment. The retrained Isolation Forest model detected 5 out of 30 obfuscated attacks compared to 6 out of 30 detected by the original model.

This indicates that the current retraining strategy was not sufficient to improve robustness against the simulated log obfuscation attack. Further improvements may require additional adversarial examples, feature engineering, or a different detection approach.