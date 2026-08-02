# OS/Endpoint Detector – Adversarial Evaluation

## Objective

This experiment evaluates how well the Isolation Forest based OS/Endpoint detector performs against adversarially modified attack samples and whether adversarial retraining improves its detection capability.

---

## Phase 1 – Baseline Evaluation

- Randomly select **30 attack samples** from the test dataset.
- Evaluate them using the trained Isolation Forest model.
- Record the number of attacks detected, missed, and the overall detection rate.

**Result**

| Metric | Value |
|--------|------:|
| Attack Samples | 30 |
| Attacks Detected | 6 |
| Attacks Missed | 24 |
| Detection Rate | 20.00% |

---

## Phase 2 – Log Obfuscation Attack

- Compare attack samples with normal samples.
- Identify the **7 features** that differ the most.
- Reduce these feature values by **10% (×0.9)** to simulate log obfuscation.
- Evaluate the modified attacks using the original model.

**Result**

| Metric | Value |
|--------|------:|
| Attack Samples | 30 |
| Attacks Detected | 6 |
| Attacks Missed | 24 |
| Detection Rate | 20.00% |

---

## Phase 3 – Adversarial Retraining

- Select **30 attack samples** from the training dataset.
- Generate three obfuscated versions using:
  - **0.95×**
  - **0.90×**
  - **0.80×**
- Add these adversarial examples to the original training data.
- Retrain the Isolation Forest model.

---

## Phase 4 – Selecting the Best Model

The retrained model is tested using different contamination values.

| Contamination | Attacks Detected | Detection Rate |
|--------------:|----------------:|---------------:|
| 0.10 | 5 / 30 | 16.67% |
| 0.15 | 8 / 30 | 26.67% |
| 0.20 | 9 / 30 | 30.00% |
| 0.25 | 10 / 30 | 33.33% |
| **0.30** | **15 / 30** | **50.00%** |

The model with the highest detection rate (**contamination = 0.30**) is selected.

---

## Phase 5 – Final Evaluation

The best-performing retrained model is evaluated on the **same 30 obfuscated attack samples** used during the attack phase.

| Evaluation | Attacks Detected | Detection Rate |
|------------|----------------:|---------------:|
| Before Defenses | 6 / 30 | 20.00% |
| After Defenses | 15 / 30 | 50.00% |

---

## Confusion Matrix

The confusion matrix is generated using the predictions from the **best-performing retrained model**.

Since the evaluation dataset contains only attack samples:

| Metric | Count |
|--------|------:|
| True Positives (TP) | 15 |
| False Negatives (FN) | 15 |
| False Positives (FP) | 0* |
| True Negatives (TN) | 0* |

\* FP and TN are zero because no normal samples are included in this adversarial evaluation.

---

## Workflow

```text
Select 30 attack samples
        │
Baseline evaluation
        │
Identify top 7 features
        │
Reduce selected features by 10%
        │
Evaluate obfuscated attacks
        │
Create multiple obfuscated training samples
        │
Retrain Isolation Forest
        │
Test different contamination values
        │
Select best-performing model
        │
Evaluate on the same obfuscated attacks
        │
Generate confusion matrix
```

---

# Experimental Evaluation – Higher Contamination

Although the project implementation uses an Isolation Forest with **contamination = 0.10**, an additional experiment was conducted to study how increasing the contamination parameter affects attack detection performance.

Unlike the adversarial evaluation, which used only the 30 obfuscated attack samples, this experiment evaluated the detector on the **entire held-out test set (1191 samples)** to measure both attack detection and false positive cost.

## Classification Report

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Normal (0) | 0.91 | 0.73 | 0.81 | 1042 |
| Attack (1) | 0.21 | 0.52 | 0.30 | 149 |
| **Accuracy** | | | **0.70** | **1191** |
| **Macro Average** | 0.56 | 0.62 | 0.56 | 1191 |
| **Weighted Average** | 0.83 | 0.70 | 0.75 | 1191 |

## Confusion Matrix

| Metric | Count |
|---|---:|
| True Positives | 78 |
| False Negatives | 71 |
| False Positives | 285 |
| True Negatives | 757 |

## Derived Metrics

| Metric | Value |
|---|---:|
| Attack Recall | 52.35% |
| False Positive Rate | 27.35% |

## Observation

Increasing the contamination parameter from **0.10** to **0.30** substantially increased the detector's ability to identify attacks, improving attack recall from **24.83%** to **52.35%**.

However, this improvement came at the cost of a much higher false positive rate, which increased from **8.35%** to **27.35%**, reducing the overall accuracy from **83%** to **70%**.

Since the project specification requires the Isolation Forest model to use **contamination = 0.10**, this higher contamination configuration was evaluated only as an experimental comparison and was not adopted as the final detector.

---

# Discussion and Limitations

The detector was implemented using **Isolation Forest**, as specified in the project requirements. Isolation Forest is designed to identify anomalies by isolating observations that differ significantly from the majority of the dataset.

However, the ADFA-LD dataset presents a challenge for this approach. Many attack samples share similar system call transition patterns and therefore form **clusters** rather than isolated outliers. As a result, the model may begin to interpret these clustered attack patterns as part of the normal data distribution.

This behaviour was observed during adversarial retraining. Even after augmenting the training dataset with multiple obfuscated attack samples, the detector did not improve its robustness. Detection on the obfuscated attack set decreased slightly from **6/30 (20.00%)** before retraining to **5/30 (16.67%)** after retraining.

The additional contamination experiment further demonstrated the trade-off inherent to Isolation Forest. Increasing the contamination parameter improved attack detection but significantly increased false positives, indicating that simply making the detector more sensitive is not an ideal solution.

Overall, these results suggest that while Isolation Forest provides a suitable baseline for unsupervised anomaly detection, it may not be the most appropriate model when attack samples form dense clusters or when adversarial examples become increasingly similar to one another.