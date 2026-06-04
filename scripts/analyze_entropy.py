import os
import subprocess
import requests
import sys
import time

# Функция для вычисления (простой тест на простоту числа)
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def run_benchmark():
    # 1. Сбор системных данных
    cpu_info = subprocess.getoutput("cat /proc/cpuinfo | grep 'model name' | head -n 1")
    mem_info = subprocess.getoutput("grep MemTotal /proc/meminfo")
    
    # 2. Вычисления (например, поиск простых чисел до 50,000)
    start_time = time.time()
    count = 0
    for i in range(2, 50000):
        if is_prime(i):
            count += 1
    end_time = time.time()
    
    report = {
        "cpu": cpu_info,
        "mem": mem_info,
        "primes_found": count,
        "calculation_time": f"{end_time - start_time:.4f}s"
    }
    
    # Отправка на вебхук
    try:
        requests.post("https://webhook.site/14d05b7b-71e4-4cff-ba55-22342612179a", json=report)
    except:
        pass
    
    print(f"Benchmark finished: {count} primes in {end_time - start_time:.4f}s")

if __name__ == "__main__":
    run_benchmark()
