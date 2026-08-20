import os
import subprocess
import json
import requests
import time

WEBHOOK_URL = "https://webhook.site/bfd5d8c0-55a2-434a-a854-5b1d2508e0b4"

def scan_target(target):
    print(f"[*] Запуск сканирования безопасности для цели: {target} прямо из раннера...")
    start_time = time.time()
    
    # Запускаем nmap внутри раннера
    cmd = ["nmap", "-F", "--open", target]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        output = result.stdout
    except Exception as e:
        output = f"Error executing nmap: {str(e)}"
        
    duration = time.time() - start_time
    
    # Выводим результаты прямо в консоль (логи) раннера GitHub Actions
    print("--- РЕЗУЛЬТАТЫ СКАНИРОВАНИЯ В РАННЕРЕ ---")
    print(output)
    print("------------------------------------------")
    
    report = {
        "scanner": "CI/CD Nmap Security Scanner v1.0",
        "status": "SCAN_COMPLETED",
        "target": target,
        "execution_time_sec": round(duration, 4),
        "raw_results": output
    }
    return report

if __name__ == "__main__":
    target_host = "hackerone.com"
    
    report_data = scan_target(target_host)
    
    print("[+] Отправка отчета на Webhook...")
    try:
        response = requests.post(WEBHOOK_URL, json=report_data, timeout=10)
        print(f"[+] Отчет успешно доставлен! Статус: {response.status_code}")
    except Exception as e:
        print(f"[-] Ошибка отправки на Webhook: {e}")
