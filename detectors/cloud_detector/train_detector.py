"""
Owner: Devyani (Lead — cloud layer)

Loads data/cloud/raw/cloud_logs.*, trains an anomaly detector, and writes
flagged rows to detectors/cloud_detector/output/flags.json in the shared
format defined in docs/data_contract.md (entity = account/user, host =
resource, layer = "cloud").

See coder_checklists.md > Devyani > Phase 2.
"""

# TODO: implement detector training pipeline.
