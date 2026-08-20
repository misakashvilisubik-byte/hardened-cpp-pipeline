import subprocess
import requests

WEBHOOK_URL = "https://webhook.site/bfd5d8c0-55a2-434a-a854-5b1d2508e0b4"

def install_and_play():
    print("[*] Устанавливаем игру в окружение раннера...")
    
    # Устанавливаем классическую консольную игру (например, nethack или bsdgames)
    subprocess.run(["sudo", "apt-get", "update"], capture_output=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "nethack-console"], capture_output=True)
    
    # Проверяем, что игра запускается, и делаем снимок вывода (первые строчки игры)
    result = subprocess.run(["nethack", "--help"], capture_output=True, text=True)
    
    report = {
        "status": "GAME_INSTALLED",
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
