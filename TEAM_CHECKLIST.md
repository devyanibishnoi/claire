# CLAIRE — Consolidated Team Checklist
### Where we actually stand, for the ICon INDIA 2026 push (Sept 22 – Sept 30)

This file merges `coder_checklists.md` (original Phase 0–7 work) and `coder_checklists_additions.md`
(new Phase 8+ work) into one status view, checked against what's actually in the repo right now
(commits, `flags.json` contents, `results/*.md`, `fusion/output/*.json`). Re-generate this by hand
as phases get finished — it won't update itself.

**Legend:** ✅ done and verified in repo · ⬜ not started · 🔲 partially done / needs a repo-external step (can't be verified from code alone)

---

## 1. The big picture

| Layer | Original detector + adversarial work (Phase 0–7) | New rigor work (Phase 8+) |
|---|---|---|
| Network (Hridya) | ✅ Done | ⬜ Not started |
| OS (Anshika) | ✅ Done | ⬜ Not started |
| Cloud + Fusion + LLM (Devyani) | ✅ Done | ⬜ Not started |

**Bottom line: the original submission (Phase 0–7 for all three, plus the first-pass consolidated
results table) is fully done and in the repo.** None of the new Sept 22–30 push (feature attribution,
extra fusion scenarios, cross-paradigm generalization, quantified prompt-injection testing, fusion
precision/recall, alert-reduction ratio) has been started yet — nothing in the additions checklist
has landed in code, data, or results files. That's the actual to-do list for this week, and it's
identical to `coder_checklists_additions.md` — nobody has a head start on any piece of it.

---

## 2. Master Timeline (unchanged from the additions file — still the plan)

| Day | Date | Hridya | Anshika | Devyani |
|---|---|---|---|---|
| 1 | Mon 22 Sep | Agree on new scenarios together. Start Phase 8 (feature attribution). | Same. Start Phase 8. | Same. Start Phase 8 (cross-paradigm retraining). |
| 2 | Tue 23 Sep | Finish Phase 8, push `top_feature` field. | Finish Phase 8, push `top_feature` field. | Finish cross-paradigm test. Start Phase 9 (LLM prompt-injection quantification). |
| 3 | Wed 24 Sep | Build Phase 9 scenario legs. | Build Phase 9 scenario legs. | Finish LLM quantification (15–20 variants). |
| 4 | Thu 25 Sep | Slack day — catch up / help others. | Slack day — catch up / help others. | Pull scenario legs, run fusion precision/recall (Phase 10). |
| 5 | Fri 26 Sep | — | — | Alert-reduction ratio (Phase 11). Start Phase 12 once `top_feature` is confirmed pushed by both. |
| 6 | Sat 27 Sep | Review `results/network_metrics.md`. | Review `results/os_metrics.md`. | Finish Phase 12. Consolidate into `results/cloud_llm_metrics.md`. |
| 7 | Sun 28 Sep | Whole team: read consolidated results, start paper draft. | Same. | Same, lead consolidation. |
| 8 | Mon 29 Sep | Whole team: finish paper draft, check every objective in `problem_statement.md` has a result. | Same. | Same. |
| 9 | Tue 30 Sep | Submit. | Submit. | Submit. |

---

## 3. Hridya — Network Detector

### Phase 0–7 (original) — ✅ all done
Detector trained on CICIDS2017, baseline recall 46.9% / precision 74.8%, traffic-padding evasion
tested (before 46.9% → after 74.5% via threshold recalibration, disclosed FP cost), results written
up in `results/network_metrics.md` and `results/network_adversarial_explanation.md`.

### Phase 8 — Feature attribution — ⬜ not started
- [ ] Compute `top_feature` per flagged row (leave-one-feature-out against `decision_function()`).
- [ ] Add `top_feature` to `detectors/network_detector/output/flags.json` — **checked: not present yet.**
- [ ] Update `docs/data_contract.md` to document the new field — **checked: still only has the original 5 fields.**
- [ ] Commit and push.

### Phase 9 — Extra fusion scenarios — ⬜ not started
- [ ] Agree on ≥2 genuine 3-layer chains + ≥2 decoys with Anshika and Devyani.
- [ ] Add your network-layer row for each into `flags.json` — **checked: only `incident_demo_01` exists right now, nothing beyond it.**
- [ ] Commit and push.

---

## 4. Anshika — OS/Endpoint Detector

### Phase 0–7 (original) — ✅ all done
Detector trained on ADFA-LD, baseline 83% accuracy / 24.83% attack recall, log-obfuscation evasion
tested (20.0% → 16.67% after retraining, honest negative result), written up in
`results/os_metrics.md` and `results/os_adversarial_explanation.md`.

### Phase 8 — Feature attribution — ⬜ not started
- [ ] Same leave-one-feature-out method as Hridya.
- [ ] Add `top_feature` to `detectors/os_detector/output/flags.json` — **checked: not present yet.**
- [ ] Confirm `docs/data_contract.md` has the field once Hridya adds it.
- [ ] Commit and push.

### Phase 9 — Extra fusion scenarios — ⬜ not started
- [ ] Use the same agreed scenario list as Hridya's Phase 9.
- [ ] Add your OS-layer row for each — **checked: only `incident_demo_01` exists right now.**
- [ ] Commit and push.

---

## 5. Devyani — Cloud Detector + Fusion + LLM Explanation

### Phase 0–7 (original) — ✅ all done
Cloud detector (100% baseline, admin-overlap redesign), credential-mimicry evasion tested through
two iterations (v1: 50%→20%, v2 with `is_unusual_hour`: 50%→30%, both honest negative results with
root-cause analysis), fusion layer built and validated on `incident_demo_01`, LLM explanation layer
built and prompt-injection tested (fooled before defenses, correctly flagged after). All written up
in `results/cloud_llm_metrics.md`.

### Original Phase 8 ("pull it together") — 🔲 partially done
- [x] Consolidated table across all three layers exists in `results/cloud_llm_metrics.md`.
- [ ] Send full draft to faculty guide (outside the repo — can't verify, check with the team).
- [ ] Review Diagrams & Claims Lead's draft (outside the repo — check with the team).
- [ ] Whole-team read-through (outside the repo — check with the team).

### Phase 8 — Cross-paradigm generalization test — ⬜ not started
- [ ] Repeat the credential-mimicry retraining experiment with `LocalOutlierFactor(novelty=True)` instead of `IsolationForest` — **checked: no `LocalOutlierFactor` anywhere in the repo yet.**
- [ ] Add a "Cross-paradigm generalization" section to `results/cloud_llm_metrics.md` — **checked: section doesn't exist yet.**
- [ ] Commit and push.

### Phase 9 — Quantify LLM prompt-injection robustness — ⬜ not started
- [ ] Write 15–20 varied injection attempts — **checked: `adversarial/llm_prompt_attacks.py` currently has exactly 1 hardcoded injection (the `entity`-field override), not a varied set.**
- [ ] Run each through both `VULNERABLE_SYSTEM_INSTRUCTION` and the real `SYSTEM_INSTRUCTION`, record compliance.
- [ ] Compute a before/after success rate, replace the single-example writeup in `results/cloud_llm_metrics.md` with the full table.
- [ ] Commit and push.

### Phase 10 — Fusion chain-reconstruction accuracy — ⬜ not started (blocked on Hridya/Anshika Phase 9)
- [ ] Pull Hridya's and Anshika's new scenario legs, add your cloud-layer rows.
- [ ] Run `fuse.py`, compute precision/recall on chain reconstruction — **checked: `fusion/output/` currently only reflects the single `incident_demo_01` chain plus unrelated existing chains, no "Fusion accuracy" section in `results/cloud_llm_metrics.md` yet.**
- [ ] Commit and push.

### Phase 11 — Alert-reduction ratio — ⬜ not started (same run as Phase 10)
- [ ] Count raw anomalies vs. fused incidents, record the reduction ratio — **checked: no such number in `results/cloud_llm_metrics.md` yet.**
- [ ] Commit and push.

### Phase 12 — Ground LLM explanation in feature attribution — ⬜ not started (blocked on Hridya/Anshika Phase 8)
- [ ] Add `top_feature` to the cloud detector's own `flags.json` — **checked: not present yet.**
- [ ] Update the `llm_explain.py` prompt to use it.
- [ ] Re-run the demo scenario, confirm the explanation names the actual driving feature.
- [ ] Commit and push.

### Phase 13 — Personal portfolio demo — ⬜ not started (optional, personal scope, do last)
- [ ] Single-page interactive walkthrough + "try to break it" LLM demo — **checked: no `index.html` or `demo` branch exists yet.**
- [ ] Not part of the paper submission — don't let this eat into Phase 8–12 time this week.

---

## 6. What actually needs to happen next

The critical path is: **Hridya + Anshika finish Phase 8 (feature attribution) and Phase 9 (scenarios)
first**, since Devyani's Phase 10, 11, and 12 are all blocked waiting on their `top_feature` field
and scenario rows landing in the shared `flags.json` files. Devyani's own Phase 8 (cross-paradigm)
and Phase 9 (LLM quantification) don't depend on anyone else and can start immediately, which is why
the timeline has her starting there on Day 1 while the other two do Phase 8.
