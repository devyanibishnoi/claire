# Project Repo Guide
### CLAIRE — Cross-Layer AI-driven Incident Response & Explanation

This file explains the folder structure, who owns what, and the git rules everyone follows so pushes never conflict. Read it once before writing any code. Put this file at the root of the repo as `repo_guide.md` so anyone can find it.

---

## 1. The golden rule

**Everyone works only inside their own folder(s). Nobody edits a file inside someone else's folder — ever.** This one rule is what prevents almost all merge conflicts. You don't need clever git tricks if two people never touch the same file.

The only file everyone shares is `docs/data_contract.md` (explained in Section 3) — and even that one is only edited once, together, on Day 1.

---

## 2. Folder structure

```
repo/
├── problem_statement.pdf            (shared — the original research problem statement)
├── README.md                        (shared — project overview, edited rarely)
├── repo_guide.md                    (this file)
├── coder_checklists.md              (shared — literal step-by-step checklist per person)
├── LEARNING.md                      (shared — concept notes + pipeline diagrams, see Section 3)
├── docs/
│   └── data_contract.md             (shared — the ONE agreed data format, see Section 3)
│
├── data/
│   ├── network/                     ← Hridya only
│   │   ├── README.md                (where to get the dataset)
│   │   └── raw/                     (downloaded dataset files — see .gitignore note below)
│   ├── os/                          ← Anshika only
│   │   ├── README.md
│   │   ├── generate_logs.py         (synthetic-data option, see coder_checklists.md)
│   │   └── raw/
│   └── cloud/                       ← Devyani only
│       ├── README.md
│       ├── generate_logs.py
│       └── raw/
│
├── detectors/
│   ├── network_detector/            ← Hridya only
│   │   ├── train_detector.py
│   │   └── output/flags.json
│   ├── os_detector/                 ← Anshika only
│   │   ├── train_detector.py
│   │   └── output/flags.json
│   └── cloud_detector/              ← Devyani only
│       ├── train_detector.py
│       └── output/flags.json
│
├── fusion/                          ← Devyani only
│   └── fuse.py                      (reads all three flags.json files — never edits them)
│
├── explanation/                     ← Devyani only
│   └── llm_explain.py
│
├── adversarial/
│   ├── network_attacks.py           ← Hridya only
│   ├── os_attacks.py                ← Anshika only
│   ├── cloud_attacks.py             ← Devyani only
│   └── llm_prompt_attacks.py        ← Devyani only
│
└── results/
    ├── network_metrics.md           ← Hridya only
    ├── os_metrics.md                ← Anshika only
    └── cloud_llm_metrics.md         ← Devyani only
```

---

## 3. Who owns what

| Folder / file | Owner | What goes in it |
|---|---|---|
| `data/network/`, `detectors/network_detector/`, `adversarial/network_attacks.py`, `results/network_metrics.md` | **Hridya** | Everything about the network detector, start to finish |
| `data/os/`, `detectors/os_detector/`, `adversarial/os_attacks.py`, `results/os_metrics.md` | **Anshika** | Everything about the OS/endpoint detector, start to finish |
| `data/cloud/`, `detectors/cloud_detector/`, `fusion/`, `explanation/`, `adversarial/cloud_attacks.py`, `adversarial/llm_prompt_attacks.py`, `results/cloud_llm_metrics.md` | **Devyani** | The cloud detector, plus fusion, plus the LLM explanation layer, plus their adversarial testing |
| `README.md`, `docs/data_contract.md`, `problem_statement.pdf`, `coder_checklists.md` | **Everyone** (rarely) | Shared reference — see rules below |
| `LEARNING.md` | **Devyani** (written for everyone) | Concept notes and pipeline diagrams, organized so Hridya/Anshika-relevant material lives in their own sections — read-only for the other two, updated by Devyani as the project progresses |

**Each detector folder produces exactly one output file the rest of the team depends on: `output/flags.json`.** That's the handoff point. Fusion only ever *reads* those three files — it never edits them, and the detector owners never touch `fusion/`.

---

## 4. The data contract (`docs/data_contract.md`)

Before anyone writes real code, the whole team agrees — together, in one sitting — on the exact shape of every detector's output file. Once agreed, put it in `docs/data_contract.md` and treat it as locked. If it ever needs to change, whoever needs the change posts in the team chat first — don't silently change it, since Devyani's fusion code depends on it exactly matching.

Suggested contract — each `flags.json` is a list of objects shaped like this:

```json
[
  {
    "entity": "user123 or 10.0.0.5 or an account ID",
    "host": "hostname or machine ID",
    "timestamp": "2026-07-25T14:32:00Z",
    "anomaly_score": 0.87,
    "layer": "network"
  }
]
```

- `entity` — whatever identifies "who" (a user, an IP, an account)
- `host` — whatever identifies "where" (a machine or hostname)
- `timestamp` — ISO 8601 format, so it sorts and compares correctly
- `anomaly_score` — a number from 0.0 to 1.0, higher means more suspicious
- `layer` — always exactly `"network"`, `"os"`, or `"cloud"` depending on which detector wrote it

As long as every detector writes this exact shape, Devyani's fusion script can read all three without ever opening anyone else's code.

---

## 5. Git rules

### One-time setup (everyone does this once)
1. Install git if you don't have it (check with `git --version` in a terminal).
2. Set your identity (only needed once per computer):
   ```
   git config --global user.name "Your Name"
   git config --global user.email "your@email.com"
   ```
3. Clone the repo:
   ```
   git clone <repo-url>
   cd <repo-folder-name>
   ```

### Every time you sit down to work
1. Pull the latest changes first, always:
   ```
   git pull
   ```
2. Do your work — but only inside your own folder(s).
3. Commit in small chunks as you go, not one giant commit at the end:
   ```
   git add <your folder>
   git commit -m "network: clean data and train first model"
   ```
4. Push right away:
   ```
   git push
   ```

### Commit message convention
Start every commit message with your area, then a short description:
- `network: add evasion attack script`
- `os: retrain with adversarial examples`
- `cloud: wire up fusion output`
- `fusion: initial timestamp/entity linking`
- `llm: add prompt-injection defense`

### Why this avoids conflicts
Since nobody edits another person's folder, git almost never sees two people's changes touching the same lines — so there's nothing to conflict over. Direct pushes to `main` are fine here; you don't need branches or pull requests for a repo this size with folder-based ownership.

### If a conflict happens anyway (rare — only possible on shared files)
1. Run `git pull` — git will tell you if there's a conflict and mark it inside the file with `<<<<<<<`, `=======`, and `>>>>>>>` symbols.
2. Open the file, decide together (message the team) which version to keep, or combine both.
3. Delete the `<<<<<<<` / `=======` / `>>>>>>>` marker lines once resolved.
4. Save, then:
   ```
   git add <the file>
   git commit -m "resolve conflict in data_contract.md"
   git push
   ```

### `.gitignore` — don't commit these
Create a `.gitignore` file at the repo root with:
```
venv/
__pycache__/
*.pyc
.DS_Store
data/*/raw/
```
Large dataset files shouldn't go in the repo at all — GitHub isn't built for that, and it slows every future `git pull` down for the whole team. Instead, if your `raw/` folder is ignored, write a short note in `data/<yourlayer>/README.md` explaining where to download the dataset from, so anyone can get it themselves.

---


