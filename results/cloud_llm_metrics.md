# Cloud Detector + LLM Explanation — Metrics
### Owner: Devyani

## Baseline cloud detector performance
Detection rate: 100% (105/105 real attacks caught on held-out test set). `IsolationForest(contamination=0.1)` on one-hot `action` + engineered `is_new_ip_for_this_entity`.

## Adversarial evaluation — credential-use mimicry (cloud detector)

Attack: flip `is_new_ip_for_this_entity` from 1 to 0 on real attack rows, simulating a stolen session/IP already recognized as trusted for that user, without changing the actual malicious action performed.

| | Detection rate |
|---|---|
| Before defenses | 50% (15/30 still caught) |
| After adversarial retraining | _TODO_ |

## Adversarial evaluation — prompt injection (LLM explanation layer)

| | Fooled? |
|---|---|
| Before "untrusted data" rule | _TODO_ |
| After "untrusted data" rule | _TODO_ |

## Consolidated results (network + os + cloud/llm)
_TODO: pull in results/network_metrics.md and results/os_metrics.md for the patent's "Experimental Validation Results" section._
