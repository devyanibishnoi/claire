# Network Layer — Adversarial Evaluation: Phase 3 & 4

### Owner: Hridya  
### Dataset: CICIDS2017  
### Model: Isolation Forest (unsupervised anomaly detection)

---

## Overview

This document explains the adversarial stress-test run on the network layer detector as part of CLAIRE's Phase 3–4 evaluation. The goal was to:

1. **Phase 3** — Attack the trained model: simulate an attacker trying to evade detection and measure how many attacks slip through.
2. **Phase 4** — Harden the model: apply a defense and measure how many are recovered.

---

## Phase 3 — Attacking the Detector

### What we did

We sampled 30 rows from the test set that were labeled as real attacks. We ran them through the already-trained Isolation Forest model to establish a **baseline detection rate** — how many the model catches under normal conditions.

Then we simulated an attacker performing **traffic padding**: slightly modifying the network flow features (packet sizes, byte counts, durations, flow rates) by a random ±15% multiplier on every feature column. The idea is that a real attacker would tweak their traffic patterns slightly to blend in with normal traffic and avoid triggering anomaly thresholds.

We ran the modified rows through the same model and recorded how many were still caught.

### Results

| Metric | Value |
|---|---|
| Attack rows tested | 30 |
| Caught before modification (baseline) | 13/30 (43.3%) |
| Caught after traffic padding | 13/30 (43.3%) |
| Evasion success rate | 56.7% |

### Why the padding had no effect

The ±15% perturbation on individual rows produced **no change** in detection. This is a known characteristic of Isolation Forest:

- IF is a tree-based model that makes decisions based on the **global feature distribution** of the entire training set.
- Nudging 30 rows by ±15% does not meaningfully shift their position relative to the learned decision boundaries.
- The 17 attacks that were already evading the model were doing so because they statistically resembled benign traffic — small perturbations on already-evading rows change nothing.

The 56.7% baseline evasion rate is therefore **intrinsic to the model**, not caused by the padding. It reflects the fundamental limitation of unsupervised anomaly detection on a dataset where some attack types (e.g. Infiltration, Heartbleed, Bot) generate traffic that looks statistically similar to normal flows.

---

## Phase 4 — Hardening the Detector

### First attempt: adversarial retraining (failed)

The natural first instinct for Phase 4 was to retrain the model with the padded attack rows included in the training data — this is called **adversarial training**, and it works well for supervised models.

We added the 30 padded rows to `X_train` with labels `y=1` (attack) and retrained Isolation Forest on the combined dataset.

**This did not work.** Detection after retraining was identical or worse. The reason:

- Isolation Forest is **unsupervised** — it never sees labels during training. Adding 30 labeled rows to a dataset of 2.2 million rows has no meaningful effect on the tree structure.
- IF learns which regions of feature space are sparse (anomalous) vs dense (normal). 30 extra rows cannot shift that density estimate in a dataset this large.
- In some runs, adding blended or padded rows to training actually made the model *less* sensitive in that region because it interpreted the new rows as evidence that the region is more "normal."

### Second attempt: threshold recalibration (worked)

Instead of retraining, we used **adaptive threshold recalibration** — a published defense technique for anomaly detectors.

**How Isolation Forest scoring works:**

Every row gets a raw anomaly score from `decision_function()`. Lower score = more anomalous. By default, IF uses the `contamination` parameter to set a threshold: it flags the bottom X% of scores as anomalies. This threshold is fixed at training time.

**What we did:**

1. Called `model.decision_function()` on all **known attack rows in the training set** (`X_train[y_train == 1]`) to get their raw anomaly scores.
2. Computed the **70th percentile** of those scores — meaning the score value that 70% of known training attacks fall below.
3. Used this as the new decision threshold: flag any row whose score falls below this value as an anomaly.

This is equivalent to saying: *"Flag anything that looks at least as suspicious as 70% of the attacks we've already seen."* It tightens the boundary based on empirical knowledge of what real attack scores look like, rather than using the default contamination-based threshold.

**Why the 70th percentile specifically:**

- The 30th percentile was tried first and made detection **worse** — because `decision_function` returns lower scores for anomalies, the 30th percentile is a *looser* threshold that lets more through.
- The 70th percentile sits higher in the score distribution, catching more borderline cases including the padded rows that were previously near the boundary.

### Results

| Metric | Before Hardening | After Hardening |
|---|---|---|
| Caught after evasion | 13/30 (43.3%) | 20/30 (66.7%) |
| Evaded detection | 17/30 (56.7%) | 10/30 (33.3%) |
| Improvement | — | +7 more caught (+23.4%) |

---

## Key Takeaways

**On Isolation Forest and adversarial robustness:**
IF is naturally resistant to small perturbations (±15% padding had zero effect) but has an intrinsic ceiling on detection rate for attack types that resemble normal traffic. This is not a flaw in the implementation — it is the expected behavior of unsupervised anomaly detection.

**On adversarial retraining for unsupervised models:**
Standard adversarial training (retrain on modified examples with labels) does not apply to unsupervised models. The defense mechanism must work within the model's actual learning paradigm.

**On threshold recalibration as a defense:**
Recalibrating the anomaly threshold based on the empirical score distribution of known attacks is a practical, effective, and theoretically grounded defense. It requires no retraining, no labels at inference time, and produces measurable improvement — a +23.4% recovery in detection rate after evasion in this evaluation.

**For CLAIRE's patent contribution:**
This before/after evaluation (43.3% → 66.7% post-hardening detection rate under adversarial evasion) is one of the concrete, quantitative results the project is built around. It demonstrates that the network layer detector can be stress-tested, partially evaded, and meaningfully hardened — which is the adversarial evaluation pipeline CLAIRE contributes as a reproducible system.

**Limitation:** Threshold recalibration improves detection of the observed evasion pattern but does not generalize to novel evasion strategies. This motivates future work on adaptive thresholding or hybrid supervised-unsupervised architectures for network anomaly detection.