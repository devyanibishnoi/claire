# Problem Statement
### AI-Assisted Cross-Layer Threat Detection and Explanation System (CLAIRE)

**Revision note:** this version extends the original faculty-issued problem statement with the objectives, methodology, and novelty framing needed for the ICon INDIA 2026 submission (Networking, Security and Blockchain Systems track, AI-driven cybersecurity). Sections 1 to 3 are carried over largely unchanged, since the original background and gap analysis still hold. Sections 4 to 7 are revised to reflect the additional rigor the team is adding before the September 30 deadline.

---

## 1. Background and Motivation

Modern cyberattacks rarely stay confined to a single layer of an organization's infrastructure. A typical multi-stage attack might involve unusual network traffic (reconnaissance or exfiltration), suspicious operating system activity (privilege escalation, process injection), and anomalous cloud access patterns (compromised credentials, unusual IAM permission changes), often occurring within the same intrusion but detected, if at all, by separate, siloed tools.

Modern Security Operations Centers (SOCs) rely heavily on layer-specific tools: network intrusion detection systems (NIDS), endpoint detection and response (EDR), and cloud security posture management (CSPM) platforms. Each generates its own alerts, but correlating those alerts into a single coherent picture of an attack is still largely a manual, expertise-dependent process. This contributes directly to alert fatigue and delayed incident response, two of the most cited pain points in current industry security reports. The security industry is actively moving toward autonomous SOC and extended detection and response (XDR) models that attempt to solve exactly this problem, making this both a timely and practically relevant research direction.

## 2. Problem Statement

There is no lightweight, extensible system that (a) detects anomalies independently across network, OS, and cloud layers using machine learning, (b) correlates those anomalies into a single multi-stage attack narrative, (c) uses a large language model to translate that correlated evidence into a clear, prioritized, human-readable explanation for a security analyst, while also being evaluated for its own robustness against adversarial evasion at each layer, including the explanation layer itself, and (d) demonstrates that its findings hold beyond a single model implementation rather than reflecting an artifact of one specific algorithm.

Most existing academic work addresses detection at a single layer in isolation, or proposes LLM-based security assistants without rigorously testing whether the underlying detection pipeline can itself be evaded. This leaves a gap between detection accuracy on a clean dataset and detection reliability against a motivated attacker, a gap that matters far more in practice than in a benchmark. A further, narrower gap exists even within the adversarial-evaluation literature that does exist: robustness findings are typically reported for a single detection algorithm, leaving open whether an observed defense (or an observed defense failure) is a property of the underlying detection paradigm or an artifact of the specific implementation tested.

## 3. Research Gap

- Cross-layer correlation of security signals is addressed more in industry tooling than in reproducible academic research.
- LLM-based alert summarization and explanation for SOC analysts is an emerging area with limited adversarial evaluation.
- Few studies stress-test the full detection pipeline (all layers plus the LLM explanation layer) as a single adversarial target, rather than evaluating each component separately.
- Adversarial robustness results for anomaly detectors are rarely tested for generalization across more than one unsupervised model, leaving it unclear whether reported findings reflect a structural property of the detection paradigm or a quirk of one implementation.
- Existing systems in this space rarely report the practical operator-facing metric that motivates their design in the first place: how much raw alert volume the correlation step actually removes.

## 4. Objectives

1. Design and implement independent, unsupervised ML-based anomaly detectors for network traffic, OS/endpoint logs, and cloud access logs, so that genuinely novel attack patterns can be flagged without requiring labeled examples of every attack type in advance.
2. Build a fusion mechanism that correlates anomalies flagged across the three layers into unified multi-stage attack scenarios, using shared entity or host identity and time-window proximity, and evaluate that mechanism quantitatively against both genuine multi-stage chains and decoy, unrelated anomalies.
3. Integrate a large language model layer that converts correlated technical evidence into a prioritized, human-readable analyst alert, grounded in the specific features that drove each underlying detection rather than in identifying metadata alone.
4. Design realistic multi-stage attack scenarios spanning all three layers, including scenarios deliberately constructed to test whether fusion over-correlates unrelated events, and use them to red-team the complete pipeline: adversarial evasion at each detection layer, and prompt-level attacks against the LLM explanation layer.
5. Evaluate detection performance and robustness before and after hardening, with quantitative before/after metrics applied with the same rigor to every component of the pipeline, including the explanation layer, not only the ML detectors.
6. Test whether the adversarial hardening findings generalize across more than one unsupervised anomaly detection paradigm, rather than reporting a result specific to a single model implementation.
7. Quantify the pipeline's practical operational value directly, by measuring the reduction in raw alert volume achieved through cross-layer correlation.

## 5. Proposed Methodology

- **Data:** publicly available benchmark datasets for network traffic (CICIDS2017) and OS/endpoint activity (ADFA-LD), combined with a project-generated synthetic dataset for cloud access logs, and synthetic multi-stage attack chains constructed where realistic public data spanning all three layers is unavailable.
- **Detection layer:** independent, unsupervised anomaly detectors trained per layer. Each detector reports, for every flagged event, both an anomaly score and the single feature that contributed most to that score, so downstream explanation can be grounded in cause rather than metadata alone.
- **Fusion layer:** anomalies are correlated across layers using timestamp and entity-based linking (same user, same host, same time window) to reconstruct attack chains. Fusion is evaluated against a constructed set of scenarios that includes both genuine multi-stage attacks and decoy, unrelated anomalies occurring close together in time, with precision and recall reported for correct chain reconstruction.
- **Explanation layer:** a large language model generates a natural-language summary and severity ranking from the correlated evidence, using the per-event feature attribution from the detection layer to ground its explanation in the actual cause of each flag.
- **Adversarial evaluation:** evasion attacks are attempted against each detector (traffic padding, log obfuscation, credential-use mimicry), and a varied set of prompt-based attacks is attempted against the LLM explanation layer, with detection and explanation degradation measured quantitatively before and after applying defenses.
- **Generalization check:** the adversarial retraining experiment is repeated on at least one detector using a second, distinct unsupervised anomaly detection method, to establish whether an observed hardening result (positive or negative) is a property of the underlying detection paradigm or specific to the first model tested.
- **Impact quantification:** raw per-layer alert counts are compared against post-fusion incident counts across the full evaluation run, to report a concrete alert-reduction ratio as direct evidence of the system's operational value.

## 6. Novelty and Contribution

The core contribution is not a new detection algorithm in isolation, but a reproducible cross-layer pipeline combined with an adversarial stress-test of the entire system, including the LLM explanation layer, applied with the same quantitative rigor at every stage. Three elements distinguish this work from existing single-layer or single-component evaluations:

- A fusion mechanism evaluated on measured precision and recall against constructed decoy scenarios, rather than demonstrated on a single example.
- An explanation layer whose robustness against prompt manipulation is reported as a quantitative rate across a varied attack set, and whose narratives are grounded in per-event feature attribution rather than identifying metadata.
- Empirical evidence, tested across more than one unsupervised detection paradigm, on whether naive adversarial retraining of density-based anomaly detectors reliably improves robustness. If the finding replicates across paradigms, it constitutes a structural property of unsupervised anomaly detection rather than an artifact of one implementation, and is the project's most citable result.

## 7. Expected Outcome

A working, quantitatively evaluated prototype demonstrating cross-layer attack detection, correlation, and explanation, producing: detection and adversarial robustness metrics for each layer; measured precision and recall for multi-stage attack chain reconstruction; a quantified robustness rate for the LLM explanation layer under prompt injection; a quantified alert-reduction ratio demonstrating operational value; and evidence for or against the generalizability of the retraining-robustness finding across more than one unsupervised detection paradigm. Together these form the results section of the conference paper submitted to ICon INDIA 2026.
