import json
import os
from datetime import timedelta

import pandas as pd

TIME_WINDOW = timedelta(minutes=10)


def load_flags(path):
    with open(path) as f:
        return json.load(f)


network_flags = load_flags("detectors/network_detector/output/flags.json")
os_flags = load_flags("detectors/os_detector/output/flags.json")
cloud_flags = load_flags("detectors/cloud_detector/output/flags.json")

all_records = network_flags + os_flags + cloud_flags

for i, record in enumerate(all_records):
    record["_id"] = i
    record["_ts"] = pd.to_datetime(record["timestamp"])

parent = list(range(len(all_records)))


def find(i):
    while parent[i] != i:
        parent[i] = parent[parent[i]]
        i = parent[i]
    return i


def union(i, j):
    root_i, root_j = find(i), find(j)
    if root_i != root_j:
        parent[root_i] = root_j


def link_matching_records(key):
    groups = {}
    for record in all_records:
        groups.setdefault(record[key], []).append(record)
    for group in groups.values():
        if len(group) < 2:
            continue
        group.sort(key=lambda r: r["_ts"])
        for i in range(len(group) - 1):
            if group[i + 1]["_ts"] - group[i]["_ts"] <= TIME_WINDOW:
                union(group[i]["_id"], group[i + 1]["_id"])


link_matching_records("entity")
link_matching_records("host")

chains = {}
for record in all_records:
    root = find(record["_id"])
    chains.setdefault(root, []).append(record)

attack_chains = [group for group in chains.values() if len(group) > 1]
attack_chains.sort(key=len, reverse=True)

for chain in attack_chains:
    for record in chain:
        del record["_id"]
        del record["_ts"]

cross_layer_chains = [chain for chain in attack_chains if len(set(r["layer"] for r in chain)) > 1]
three_layer_chains = [chain for chain in attack_chains if len(set(r["layer"] for r in chain)) == 3]

os.makedirs("fusion/output", exist_ok=True)
with open("fusion/output/attack_chains.json", "w") as f:
    json.dump(attack_chains, f, indent=2)
with open("fusion/output/cross_layer_chains.json", "w") as f:
    json.dump(cross_layer_chains, f, indent=2)
with open("fusion/output/three_layer_chains.json", "w") as f:
    json.dump(three_layer_chains, f, indent=2)

print(f"Found {len(attack_chains)} attack chains out of {len(all_records)} total flagged records")
print(f"Of those, {len(cross_layer_chains)} span more than one layer (see fusion/output/cross_layer_chains.json)")
print(f"Of those, {len(three_layer_chains)} span all three layers (see fusion/output/three_layer_chains.json)")
if attack_chains:
    print(f"Largest chain has {len(attack_chains[0])} records")
    layers_in_largest = set(r["layer"] for r in attack_chains[0])
    print(f"Layers in largest chain: {layers_in_largest}")
