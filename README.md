# CLAIRE — Cross-Layer AI-driven Incident Response & Explanation

*(Formal problem statement title: "AI-Assisted Cross-Layer Threat Detection & Explanation System" — see `problem_statement.pdf`.)*

A patent-track research project that detects security threats independently across three layers — network, OS/endpoint, and cloud — correlates them into a single multi-stage attack narrative, explains that narrative in plain English via an LLM, and then deliberately stress-tests the whole pipeline against adversarial evasion.

## Background

Modern cyberattacks rarely stay confined to one layer. A typical intrusion touches unusual network traffic, suspicious OS-level activity (privilege escalation, process injection), and anomalous cloud access (compromised credentials, unusual IAM changes) — often as one continuous attack, but caught (if at all) by separate, siloed tools: NIDS for network, EDR for endpoints, CSPM for cloud. Correlating those separate alerts into one coherent picture is still largely manual and expertise-dependent today, which drives alert fatigue and slows incident response.

## The problem

There is no lightweight, extensible system that (a) detects anomalies independently across network, OS, and cloud layers using ML, (b) correlates those anomalies into a single multi-stage attack narrative, and (c) uses an LLM to turn that correlated evidence into a clear, prioritized, human-readable explanation for an analyst — while also being evaluated for its own robustness against adversarial evasion at every layer, including the LLM layer itself. Most existing work either detects at a single layer in isolation, or builds LLM-based security assistants without rigorously testing whether the underlying pipeline can be evaded. CLAIRE targets that gap.

## What CLAIRE does

1. Independent ML-based anomaly detectors for network traffic, OS/endpoint logs, and cloud access logs.
2. A fusion mechanism that correlates anomalies flagged across all three layers into one attack chain.
3. An LLM explanation layer that converts correlated evidence into a prioritized, human-readable analyst alert with a severity rating.
4. Realistic multi-stage attack scenarios spanning all three layers, used to red-team the full pipeline — adversarial evasion at each detection layer, plus prompt-level attacks on the LLM layer.
5. Quantitative before/after metrics comparing detection and explanation reliability, undefended vs. hardened.

The core contribution isn't a new detection algorithm in isolation — it's the reproducible cross-layer pipeline plus the adversarial stress-test of the *entire* system, including the LLM explanation layer, which is rarely evaluated adversarially in existing work. That before/after comparison is the concrete, measurable result the whole project is building toward.

## Pipeline

```
network_detector ─┐
os_detector       ─┼─→ fusion/fuse.py ─→ explanation/llm_explain.py
cloud_detector    ─┘
```

Each detector independently flags anomalies in its own layer and writes them to its own `output/flags.json`, in the shared format defined in [`docs/data_contract.md`](docs/data_contract.md). Fusion correlates flags across layers by shared entity/host and a shared time window into "attack chains." The explanation layer turns each attack chain into a plain-language, severity-rated summary. Every detector and the LLM layer also goes through an attack-and-harden cycle (adversarial evasion → retrain/defend → re-test), producing the before/after numbers in `results/`.

For a fully diagrammed, step-by-step walkthrough of this pipeline (including mermaid diagrams of the full data flow, the adversarial hardening loop, and the original motivating attack scenario traced end to end), see [`LEARNING.md`](LEARNING.md).

## Repo map — which doc is for what

| Doc | What it's for |
|---|---|
| `problem_statement.pdf` | The original research problem statement — background, objectives, methodology, novelty. Source of truth for scope. |
| `README.md` (this file) | Project overview and orientation. |
| `repo_guide.md` | Folder structure, who owns what, and the git workflow that keeps three people from ever conflicting. |
| `coder_checklists.md` | Literal, step-by-step checklist per person, phase by phase. |
| `docs/data_contract.md` | The one shared, locked data format every detector's `flags.json` must match. |
| `LEARNING.md` | Concept explanations and diagrams for the whole pipeline — shared concepts plus a section per person. |
| `results/*.md` | Each layer's detection metrics and before/after adversarial evaluation numbers. |

## Team & ownership

| Layer | Owner |
|---|---|
| Network detector | Hridya |
| OS/endpoint detector | Anshika |
| Cloud detector + Fusion + LLM explanation | Devyani |

See `repo_guide.md` for the full folder structure and git workflow, and `coder_checklists.md` for step-by-step instructions per person.

## Getting started

1. Read `repo_guide.md` once.
2. Follow your section of `coder_checklists.md` in order.
3. Never edit a file inside someone else's folder.
