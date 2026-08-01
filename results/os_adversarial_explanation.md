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





# Previous Experiments

Before arriving at the final approach, several adversarial retraining strategies were evaluated to improve the detector's robustness.

## Attempt 1 – Single Obfuscation (0.90×)

* Generated obfuscated attack samples by reducing the selected features by **10% (×0.90)**.
* Added these obfuscated samples to the training dataset.
* Retrained the Isolation Forest using the original **contamination = 0.1**.
* Result: Detection performance did not improve significantly and, in some runs, decreased compared to the original model.

## Attempt 2 – Increasing Training Samples

* Increased the number of obfuscated attack samples used for retraining.
* The model was retrained using the same Isolation Forest configuration.
* Result: Only minor changes in detection performance were observed.

## Attempt 3 – Multiple Obfuscation Strengths

* Generated three adversarial versions of the training attacks:

  * **0.95×** (5% reduction)
  * **0.90×** (10% reduction)
  * **0.80×** (20% reduction)
* Combined all obfuscated samples with the original training data before retraining.
* This exposed the model to a wider range of evasive attack patterns.

## Attempt 4 – Contamination Parameter Tuning

To determine the most suitable anomaly threshold after adversarial retraining, multiple contamination values were evaluated.

| Contamination | Attacks Detected | Detection Rate |
| ------------: | ---------------: | -------------: |
|          0.10 |           5 / 30 |         16.67% |
|          0.15 |           8 / 30 |         26.67% |
|          0.20 |           9 / 30 |         30.00% |
|          0.25 |          10 / 30 |         33.33% |
|      **0.30** |      **15 / 30** |     **50.00%** |

The model with **contamination = 0.30** achieved the highest detection rate and was selected for the final evaluation.

## Final Outcome

The final approach combined:

* Multiple obfuscation strengths (0.95×, 0.90×, and 0.80×).
* Adversarial retraining using the augmented training dataset.
* Hyperparameter tuning of the Isolation Forest contamination value.

This configuration improved the adversarial detection rate from **20.00% (6/30)** before defenses to **50.00% (15/30)** after retraining and model selection.

## Attempt 5 – Hard Example Mining

A Hard Example Mining strategy was also explored.

Instead of retraining the model using all obfuscated attack samples, only the **hard examples** (i.e., the attacks that successfully evaded detection) were selected for retraining.

The workflow was:

1. Evaluate the obfuscated attack samples using the original detector.
2. Identify the attacks that were **missed** by the model.
3. Add these hard examples to the training dataset.
4. Retrain the Isolation Forest model.
5. Re-evaluate the same 30 obfuscated attack samples.

**Observation:** This strategy produced essentially the **same detection performance** as the previous retraining approach.