"""
Owner: Anshika (OS/endpoint layer)

Generates a synthetic OS/endpoint log dataset at data/os/raw/os_logs.csv.
Rows: {user, process_name, privilege_level, timestamp, is_attack}
~5,000 normal rows (common processes, normal privilege) +
~500 attack rows (unusual processes, privilege jumps, odd hours).

See coder_checklists.md > Anshika > Phase 1, Option B.
"""

# TODO: implement using Python's `random` module.
