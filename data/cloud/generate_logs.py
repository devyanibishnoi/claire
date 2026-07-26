"""
Owner: Devyani

Generates synthetic CloudTrail-style logs at data/cloud/raw/cloud_logs.json (or .csv).
Rows: {user, action, source_ip, timestamp, is_attack}
~5,000 normal entries (routine actions from known users/IPs) +
~500 attack entries (unusual IAM changes, new-location logins, privilege escalation).

See coder_checklists.md > Devyani > Phase 1.
"""

# TODO: implement synthetic log generator.
