# AI-Assisted Cross-Layer Threat Detection & Explanation System

A patent-track project that detects security threats across three layers — network, OS/endpoint, and cloud — and correlates them into unified, LLM-explained attack chains.

## Pipeline

```
network_detector ─┐
os_detector       ─┼─→ fusion/fuse.py ─→ explanation/llm_explain.py
cloud_detector    ─┘
```

Each detector independently flags anomalies in its layer and writes them to its own `output/flags.json` in the shared format defined in [`docs/data_contract.md`](docs/data_contract.md). The fusion layer correlates flags across layers by shared entity/host and time window into "attack chains." The explanation layer summarizes each attack chain in plain language with a severity rating.

## Team & ownership

See [`REPO_GUIDE.md`](REPO_GUIDE.md) for the full folder structure, who owns what, and git workflow. See [`coder_checklists.md`](coder_checklists.md) for step-by-step instructions per person.

| Layer | Owner |
|---|---|
| Network detector | Hridya |
| OS/endpoint detector | Anshika |
| Cloud detector + Fusion + LLM explanation | Devyani |

## Getting started

1. Read `REPO_GUIDE.md` once.
2. Follow your section of `coder_checklists.md` in order.
3. Never edit a file inside someone else's folder.
