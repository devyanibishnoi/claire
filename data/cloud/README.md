# Cloud dataset

`raw/` is gitignored.

Synthetic CloudTrail-style logs — run `python3 generate_logs.py` to produce `raw/cloud_logs.json` (~5,000 normal entries + ~500 attack entries: unusual IAM permission changes, logins from new locations, privilege escalation).
