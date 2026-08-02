# OS/Endpoint Detector — Metrics

**Owner:** Anshika

---

# 1. Baseline Detector Performance

The OS/Endpoint detector was trained using an Isolation Forest with a contamination value of **0.1** and evaluated on a held-out test set.

## Overall Performance

| Metric | Value |
|---|---:|
| Accuracy | 83% |
| Precision (Attack Class) | 0.30 |
| Recall (Attack Class) | 0.25 |
| F1-score (Attack Class) | 0.27 |

## Classification Report

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Normal (0) | 0.90 | 0.92 | 0.91 | 1042 |
| Attack (1) | 0.30 | 0.25 | 0.27 | 149 |
| **Accuracy** | | | **0.83** | **1191** |
| **Macro Average** | 0.60 | 0.58 | 0.59 | 1191 |
| **Weighted Average** | 0.82 | 0.83 | 0.83 | 1191 |

## Confusion Matrix

| Metric | Count |
|---|---:|
| True Positives (Caught Attacks) | 37 |
| False Negatives (Missed Attacks) | 112 |
| False Positives (False Alarms) | 87 |
| True Negatives (Correctly Identified Normal) | 955 |

### Derived Metrics

| Metric | Value |
|---|---:|
| Attack Recall | 24.83% |
| False Positive Rate | 8.35% |

---

# 2. Phase 3 — Adversarial Evaluation (Log Obfuscation)

## Objective

Evaluate the detector's robustness against simulated log obfuscation attacks.

## Attack Method

- Selected **30 attack samples** from the held-out test set.
- Computed the seven features with the largest difference between attack and normal samples.
- Reduced those feature values by **10% (×0.90)** to simulate log obfuscation.
- Evaluated the modified samples using the original Isolation Forest detector.

## Results

### Original Attack Samples

| Metric | Value |
|---|---:|
| Attack Samples | 30 |
| Attacks Detected | 6 |
| Attacks Missed | 24 |
| Detection Rate | **20.00%** |

### After Log Obfuscation

| Metric | Value |
|---|---:|
| Obfuscated Attack Samples | 30 |
| Attacks Detected | 6 |
| Attacks Missed | 24 |
| Detection Rate | **20.00%** |

---

# 3. Phase 4 — Adversarial Retraining

## Retraining Strategy

To improve robustness against log obfuscation:

- Selected attack samples from the training set.
- Generated three obfuscated versions of each attack sample using:
  - 90% feature values
  - 95% feature values
  - 80% feature values
- Added these adversarial samples to the original training dataset.
- Retrained an Isolation Forest using **contamination = 0.1**.

## Results After Retraining

The retrained model was evaluated on the same 30 obfuscated attack samples.

| Metric | Value |
|---|---:|
| Attack Samples | 30 |
| Attacks Detected | 5 |
| Attacks Missed | 25 |
| Detection Rate | **16.67%** |

### Confusion Matrix (Obfuscated Attack Set)

| Metric | Count |
|---|---:|
| True Positives | 5 |
| False Negatives | 25 |
| False Positives | 0* |
| True Negatives | 0* |

\*Only attack samples were evaluated during this phase, so no normal samples were present.

---

# 4. Comparison

| Stage | Attacks Detected | Detection Rate |
|---|---:|---:|
| Before Defenses | 6 / 30 | 20.00% |
| After Adversarial Retraining | 5 / 30 | 16.67% |

---

# 5. Observations

- The baseline detector achieved **83% overall accuracy** with an attack recall of **24.83%**.
- Simulated log obfuscation did not reduce detection performance; both the original and obfuscated attack sets resulted in **6 detections out of 30 attacks**.
- Retraining the Isolation Forest with additional obfuscated attack samples did **not** improve performance in this experiment. Detection decreased from **6/30** to **5/30**.

---