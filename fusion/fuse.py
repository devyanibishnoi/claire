"""
Owner: Devyani

Reads detectors/{network,os,cloud}_detector/output/flags.json (never edits
them) and groups records into "attack chains": records that share an entity
or host AND whose timestamps fall within a shared time window (e.g. 10 min).

See coder_checklists.md > Devyani > Phase 3.
"""

# TODO: implement correlation logic.
