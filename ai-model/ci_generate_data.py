"""CI Data Generator - generates a fixed batch of logs for model training in CI.
Runs once and exits (no infinite loop). Safe for GitHub Actions.
"""
import csv
import os
import random
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")
LOG_FILE = os.path.join(DATA_DIR, "generated_logs.csv")

os.makedirs(DATA_DIR, exist_ok=True)

headers = ["timestamp", "source_ip", "destination_ip", "bytes", "protocol", "event_type", "details"]

protocols = ["TCP", "UDP", "ICMP", "HTTP", "HTTPS"]
events = ["Normal", "Failed Login", "Port Scan", "Malware Detected", "File Access"]
weights = [0.7, 0.1, 0.1, 0.05, 0.05]


def generate_ip():
    return f"{random.randint(10,192)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"


def generate_row():
    event_type = random.choices(events, weights=weights, k=1)[0]
    src_ip = generate_ip()
    details_map = {
        "Failed Login": f"Failed attempt from {src_ip}",
        "Port Scan": f"Multiple ports scanned by {src_ip}",
        "Malware Detected": "Signature match: Trojan.Win32",
        "File Access": "Accessed /etc/passwd",
    }
    return [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        src_ip,
        generate_ip(),
        random.randint(100, 50000),
        random.choice(protocols),
        event_type,
        details_map.get(event_type, "Routine traffic"),
    ]


NUM_ROWS = 500
print(f"Generating {NUM_ROWS} log entries -> {LOG_FILE}")
with open(LOG_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for _ in range(NUM_ROWS):
        writer.writerow(generate_row())

print(f"Done. {NUM_ROWS} rows written to {LOG_FILE}")
