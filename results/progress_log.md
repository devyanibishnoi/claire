# Progress Log

Running log of detection/robustness metrics as each of us completes phases, so the whole team can see how things evolve over time. This is shared across all three of us — **append your own row, never edit someone else's row.** This is a running history, not a final summary; `results/network_metrics.md`, `results/os_metrics.md`, and `results/cloud_llm_metrics.md` are still the place for each person's final polished before/after writeup.

| Date | Owner | Layer | Phase | Metric | Value | Notes |
|---|---|---|---|---|---|---|
| 2026-07-30 | Hridya | Network | Phase 2 (baseline) | Detection rate | 47.19% | CICIDS2017, contamination set to real attack proportion in data |
| 2026-07-30 | Hridya | Network | Phase 2 (baseline) | False alarm rate | 16.5% | |
| 2026-07-30 | Anshika | OS | Phase 2 (baseline) | Flags produced | 124 | ADFA-LD (real dataset), bag-of-syscalls features |
| 2026-07-30 | Devyani | Cloud | Phase 2 (baseline) | Detection rate | 100% (103/103) | Synthetic data; attacks deliberately obvious for this baseline — expect this to drop once Phase 5 makes them subtler |
| 2026-07-31 | Devyani | Cloud | Phase 5 (before defenses) | Detection rate under credential-mimicry evasion | 50% (15/30) | Redesigned data to include legitimate admin overlap so this evasion has real room to work; retraining (Phase 7) comes next |
