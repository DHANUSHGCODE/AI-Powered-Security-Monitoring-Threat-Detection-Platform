import time
import random
import csv
import os
from datetime import datetime

# Define output file
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "../data/generated_logs.csv")

# Ensure data directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Define headers if file doesn't exist
headers = ["timestamp", "source_ip", "destination_ip", "bytes", "protocol", "event_type", "details"]

# Check if file exists to write headers
file_exists = os.path.exists(LOG_FILE)

def generate_ip():
    return f"{random.randint(10, 192)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

def generate_log():
    protocols = ["TCP", "UDP", "ICMP", "HTTP", "HTTPS"]
    events = ["Normal", "Failed Login", "Port Scan", "Malware Detected", "File Access"]
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    src_ip = generate_ip()
    dst_ip = generate_ip()
    bytes_transferred = random.randint(100, 50000)
    protocol = random.choice(protocols)
    event_type = random.choices(events, weights=[0.7, 0.1, 0.1, 0.05, 0.05], k=1)[0]
    
    details = "Routine traffic"
    if event_type == "Failed Login":
        details = f"Failed attempt from {src_ip}"
    elif event_type == "Port Scan":
        details = f"Multiple ports scanned by {src_ip}"
    elif event_type == "Malware Detected":
        details = "Signature match: Trojan.Win32"
    elif event_type == "File Access":
        details = "Accessed /etc/passwd"

    return [timestamp, src_ip, dst_ip, bytes_transferred, protocol, event_type, details]

print(f"Starting log generation to {LOG_FILE}...")
print("Press Ctrl+C to stop.")

with open(LOG_FILE, "a", newline="") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(headers)
    
    try:
        while True:
            log_entry = generate_log()
            writer.writerow(log_entry)
            print(f"Logged: {log_entry}")
            f.flush()  # Ensure data is written immediately
            time.sleep(random.uniform(0.5, 2.0))
    except KeyboardInterrupt:
        print("\nLog generation stopped.")
