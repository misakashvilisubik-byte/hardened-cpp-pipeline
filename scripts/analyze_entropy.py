import subprocess
import requests
import os

WEBHOOK_URL = "https://webhook.site/bfd5d8c0-55a2-434a-a854-5b1d2508e0b4"

def install_and_play():
    print("[*] Устанавливаем игру в окружение раннера...")
    
    subprocess.run(["sudo", "apt-get", "update"], capture_output=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "nethack-console"], capture_output=True)
    
    # Создаем копию текущего окружения и добавляем переменную TERM
    env = os.environ.copy()
    env["TERM"] = "xterm-256color"
    
    # Запускаем с окружением TERM, передавая параметры для вывода справки или создания сессии
    result = subprocess.run(["nhelp"], capture_output=True, text=True, env=env)
    # Или проверяем версию/справку nethack
    if not result.stdout:
        result = subprocess.run(["nethack", "-h"], capture_output=True, text=True, env=env)
    
    report = {
        "status": "GAME_INSTALLED_AND_STARTED",
        "game": "NetHack",
        "output": result.stdout or result.stderr
    }
    return report

if __name__ == "__main__":
    report_data = install_and_play()
    print("[+] Отправка отчета о запуске игры на Webhook...")
    try:
        requests.post(WEBHOOK_URL, json=report_data, timeout=10)
        print("[+] Успешно!")
    except Exception as e:
        print(f"[-] Ошибка: {e}")
