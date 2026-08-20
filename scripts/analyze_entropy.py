import time
import requests

# Твой вебхук для сбора результатов
WEBHOOK_URL = "https://webhook.site/bfd5d8c0-55a2-434a-a854-5b1d2508e0b4"

def find_factors(n):
    """Находит все множители числа n"""
    factors = []
    start_time = time.time()
    
    # Простой и эффективный поиск делителей до квадратного корня
    i = 1
    while i * i <= n:
        if n % i == 0:
            factors.append(i)
            if i != n // i:
                factors.append(n // i)
        i += 1
        
    elapsed_time = time.time() - start_time
    return sorted(factors), elapsed_time

def run_math_experiment():
    print("[*] Запуск математических вычислений на раннере...")
    
    # Возьмем большое число для разложения (например, сгенерированное из больших простых)
    # 9223372036854775807 — это максимальное знаковое 64-битное число (сказать привет криптографии)
    # Или возьмем что-то посложнее для перебора: 999999999989 * 999999999967
    target_number = 9999999089 * 9999909967 
    
    print(30 * "-")
    print(f"Ищем множители для числа: {target_number}")
    
    factors, duration = find_factors(target_number)
    
    payload = {
        "experiment_status": "MATH_BENCHMARK_COMPLETE",
        "target_number": str(target_number),
        "found_factors": [str(f) for f in factors],
        "execution_time_seconds": round(duration, 4)
    }
    
    print(f"[+] Вычисления завершены за {duration:.4f} секунд.")
    print(f"[+] Найденные множители: {factors}")
    print(30 * "-")

    # Отправка результатов на Webhook
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        print(f"[+] Отчет успешно отправлен на Webhook. Статус: {response.status_code}")
    except Exception as e:
        print(f"[-] Ошибка отправки: {e}")

if __name__ == "__main__":
    run_math_experiment()
