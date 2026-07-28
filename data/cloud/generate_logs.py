"""
Owner: Devyani

Generates synthetic CloudTrail-style logs at data/cloud/raw/cloud_logs.json.
Rows: {user, action, source_ip, resource, timestamp, is_attack}
~5,000 normal entries (routine actions from known users/home IPs) +
~500 attack entries (unusual IAM actions, new-location logins, odd-hour activity).

See coder_checklists.md > Devyani > Phase 1.
"""

import json
import random
from datetime import datetime, timedelta

random.seed(42)

NUM_USERS = 30
NORMAL_ROWS = 5000
ATTACK_ROWS = 500

ROUTINE_ACTIONS = ["ConsoleLogin", "GetObject", "PutObject", "DescribeInstances", "ListBuckets"]
SENSITIVE_ACTIONS = ["AttachUserPolicy", "CreateAccessKey", "PutUserPolicy", "DeleteTrail", "AssumeRole"]
RESOURCES = [
    "arn:aws:s3:::reports-bucket",
    "arn:aws:s3:::user-uploads",
    "arn:aws:iam::123456789012:role/Analyst",
    "arn:aws:ec2:us-east-1:123456789012:instance/i-0abc123",
]


def random_ip():
    return f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def random_timestamp(start_hour, end_hour):
    day_offset = random.randint(0, 29)
    hour = random.randint(start_hour, end_hour)
    minute = random.randint(0, 59)
    dt = datetime(2026, 6, 1) + timedelta(days=day_offset, hours=hour, minutes=minute)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

users = []
for i in range(NUM_USERS):
    users.append({
        "name": f"user{i + 1}",
        "home_ips": [random_ip() for _ in range(random.randint(2, 3))],
        "routine_actions": random.sample(ROUTINE_ACTIONS, k=random.randint(2, 3)),
    })

rows = []

for _ in range(NORMAL_ROWS):
    user = random.choice(users)
    rows.append({
        "user": user["name"],
        "action": random.choice(user["routine_actions"]),
        "source_ip": random.choice(user["home_ips"]),
        "resource": random.choice(RESOURCES),
        "timestamp": random_timestamp(9, 18),
        "is_attack": 0,
    })

for _ in range(ATTACK_ROWS):
    user = random.choice(users)
    rows.append({
        "user": user["name"],
        "action": random.choice(SENSITIVE_ACTIONS),
        "source_ip": random_ip(),
        "resource": random.choice(RESOURCES),
        "timestamp": random_timestamp(1, 4),
        "is_attack": 1,
    })

random.shuffle(rows)

with open("data/cloud/raw/cloud_logs.json", "w") as f:
    json.dump(rows, f, indent=2)

print(f"Wrote {len(rows)} rows ({NORMAL_ROWS} normal, {ATTACK_ROWS} attack) to data/cloud/raw/cloud_logs.json")
