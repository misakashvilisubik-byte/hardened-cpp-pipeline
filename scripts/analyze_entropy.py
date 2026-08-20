import os
import subprocess
import json
import requests
import time

WEBHOOK_URL = "https://webhook.site/bfd5d8c0-55a2-434a-a854-5b1d2508e0b4"

def scan_vulnerabilities(target):
    print(f"[*] Запуск сканирования уязвимостей (NSE Vuln scripts) для цели: {target}")
    start_time = time.time()
    
    # Используем nmap со скриптами проверки уязвимостей (категория vuln)
    # Примечание: сканирование через --script vuln может занять чуть больше времени
    cmd = ["nmap", "-p", "80,443", "--script", "vuln", target]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        output = result.stdout
    except Exception as e:
        output = f"Error executing vulnerability scan: {str(e)}"
        
    duration = time.time() - start_time
    
    print("--- РЕЗУЛЬТАТЫ СКАНИРОВАНИЯ УЯЗВИМОСТЕЙ ---")
    print(output)
    print("--------------------------------------------")
    
    report = {
        "scanner": "CI/CD Nmap Vulnerability Scanner v2.0",
        "status": "VULN_SCAN_COMPLETED",
        "target": target,
        "execution_time_sec": round(duration, 4),
        "vulnerability_report": output
    }
    return report

if __name__ == "__main__":
    target_host = "hackerone.com"
    
    report_data = scan_vulnerabilities(target_host)
    
    print("[+] Отправка отчета об уязвимостях на Webhook...")
    try:
        response = requests.post(WEBHOOK_URL, json=report_data, timeout=15)
        print(f"[+] Отчет успешно доставлен! Статус: {response.status_code}")
    except Exception as e:
        print(f"[-] Ошибка отправки на Webhook: {e}")
