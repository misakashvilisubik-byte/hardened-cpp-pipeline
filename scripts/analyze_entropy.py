import random
import sys

# Используем мощный метод проверки Миллера-Рабина
def is_prime(n, k=5): # k - количество тестов, чем больше, тем точнее
    if n < 2: return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
        if n % p == 0: return n == p
    
    # Тест Миллера-Рабина
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Генерируем число из 10 000 цифр
digits = 10000
# Первая цифра не должна быть нулем, последняя должна быть нечетной
large_num = random.randint(10**(digits-1), 10**digits)
if large_num % 2 == 0: large_num += 1

print(f"Checking if {digits}-digit number is prime...")
if is_prime(large_num):
    print("Found a probable prime!")
else:
    print("Not prime.")
