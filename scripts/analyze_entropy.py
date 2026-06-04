import random
import requests
import time
import multiprocessing
import os

WEBHOOK_URL = "https://webhook.site/14d05b7b-71e4-4cff-ba55-22342612179a"

def is_prime_miller_rabin(n, k=5):
    if n < 2: return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
        if n % p == 0: return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def worker(instance_id):
    digits = 10000
    large_num = random.randint(10**(digits-1), 10**digits)
    if large_num % 2 == 0: large_num += 1
    
    start = time.time()
    result = is_prime_miller_rabin(large_num)
    duration = time.time() - start
    
    payload = {
        "instance": instance_id,
        "prime_found": result,
        "duration": f"{duration:.4f}s",
        "cpu_worker": os.getpid()
    }
    
    try:
        requests.post(WEBHOOK_URL, json=payload)
        return f"Instance {instance_id} done."
    except Exception as e:
        return f"Error {instance_id}: {e}"

if __name__ == "__main__":
    # Запуск 10 процессов параллельно
    print("Starting parallel benchmark...")
    with multiprocessing.Pool(processes=10) as pool:
        results = pool.map(worker, range(1, 11))
    
    print("\n".join(results))
