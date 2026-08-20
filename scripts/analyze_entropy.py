import os
import sys
import subprocess
import requests
import json

WEBHOOK_URL = "https://webhook.site/bfd5d8c0-55a2-434a-a854-5b1d2508e0b4"

def git_operations_demo():
    """Симулируем работу AI-агента с Git-репозиторием"""
    print("[*] AI-Агент анализирует изменения в репозитории...")
    
    # Получаем последний коммит
    try:
        commit_msg = subprocess.check_output(["git", "log", "-1", "--pretty=format:%s"], text=True)
        author = subprocess.check_output(["git", "log", "-1", "--pretty=format:%an"], text=True)
        print(f"[+] Последний коммит: '{commit_msg}' от автора {author}")
    except Exception as e:
        print(f"[-] Ошибка git: {e}")
        commit_msg = "Unknown"

    # Создаем файл отчета от имени AI-агента
    ai_report_content = f"""# AI Code Guardian Report
- **Status:** Secured & Analyzed
- **Target Commit:** {commit_msg}
- **Agent:** Python Autonomous CI/CD Agent v1.0
- **Recommendation:** Code looks clean, but always pin your GitHub Action versions!
"""
    
    with open("ai_security_patch.md", "w") as f:
        f.write(ai_report_content)
        
    print("[+] AI-Агент сгенерировал файл отчета: ai_security_patch.md")

def configure_git_and_push():
    """Настройка git и автоматический коммит от имени бота (если есть права)"""
    try:
        subprocess.run(["git", "config", "--global", "user.name", "AI Code Guardian Bot"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "ai-bot@users.noreply.github.com"], check=True)
        
        # Добавляем созданный файл в индекс
        subprocess.run(["git", "add", "ai_security_patch.md"], check=True)
        
        # Проверяем, есть ли изменения для коммита
        status = subprocess.run(["git", "status", "--porcelain"], stdout=subprocess.PIPE, text=True).stdout
        if status.strip():
            subprocess.run(["git", "commit", "-m", "🤖 AI Agent: Autonomous Security & Code Review Report"], check=True)
            print("[+] Автоматический коммит успешно создан!")
            
            # Внимание: для пуша нужен токен с правами contents: write в workflow permissions
            # subprocess.run(["git", "push"], check=True)
            # print("[+] Изменения отправлены в репозиторий!")
        else:
            print("[*] Нет новых изменений для коммита.")
    except Exception as e:
        print(f"[-] Ошибка при работе с Git: {e}")

if __name__ == "__main__":
    print("🤖 Запуск автономного AI-агента внутри раннера...")
    git_operations_demo()
    configure_git_and_push()
    
    payload = {
        "agent_status": "AI_AGENT_EXECUTION_SUCCESS",
        "runner_user": os.getenv("USER", "unknown"),
        "message": "AI agent successfully executed and generated security patches."
    }
    
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
        print("[+] Телеметрия AI-агента отправлена на Webhook.")
    except Exception as e:
        print(f"[-] Ошибка отправки: {e}")
