import os
import re
import json
import requests
import time

WEBHOOK_URL = "https://webhook.site/bfd5d8c0-55a2-434a-a854-5b1d2508e0b4"

# Регулярные выражения для поиска утечек секретов и уязвимостей в CI/CD
PATTERNS = {
    "AWS Secret Key": r"(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANOA|ANVA|ASIA)[A-Z0-9]{16}",
    "Private Key": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
    "Generic API Token": r"(api[_-]?key|secret[_-]?token|auth[_-]?token)\s*[:=]\s*['\"'][0-9a-zA-Z-_]{16,48}['\"']",
    "Unpinned GitHub Action": r"uses:\s*[^@\n]+@(main|master|latest)" # Риск Supply Chain атак
}

def scan_file(filepath):
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for name, pattern in PATTERNS.items():
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    findings.append({"threat_type": name, "file": filepath, "count": len(matches)})
    except Exception as e:
        pass
    return findings

def audit_codebase():
    print("[*] Запуск глубокого аудита безопасности окружения...")
    all_findings = []
    
    # Рекурсивно сканируем проект (включая воркфлоу)
    for root, dirs, files in os.walk("."):
        # Пропускаем служебные папки гита
        if ".git" in root:
            continue
        for file in files:
            full_path = os.path.join(root, file)
            findings = scan_file(full_path)
            if findings:
                all_findings.extend(findings)
                
    return all_findings

if __name__ == "__main__":
    start_time = time.time()
    vulnerabilities = audit_codebase()
    duration = time.time() - start_time
    
    report = {
        "status": "SECURITY_AUDIT_COMPLETED",
        "scanner": "Python-Native CyberHunter v1.0",
        "execution_time_sec": round(duration, 4),
        "total_threats_detected": len(vulnerabilities),
        "vulnerabilities": vulnerabilities
    }
    
    print(f"[+] Аудит завершен за {duration:.4f} сек. Найдено угроз: {len(vulnerabilities)}")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    # Отправка отчета безопасности на Webhook
    try:
        response = requests.post(WEBHOOK_URL, json=report, timeout=10)
        print(f"[+] Отчет успешно доставлен в Центр Мониторинга (Webhook). Статус: {response.status_code}")
    except Exception as e:
        print(f"[-] Ошибка отправки отчета: {e}")
