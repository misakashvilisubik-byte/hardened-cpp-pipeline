import math
import sys
import os

def calculate_entropy(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    if not data: return 0
    
    entropy = 0
    for x in range(256):
        p_x = data.count(x) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log2(p_x)
    return entropy

path = sys.argv[1]
entropy = calculate_entropy(path)
print(f"Entropy of {path}: {entropy:.2f}")

if entropy > 7.5:
    print("SECURITY_ALERT: High entropy detected!")
    sys.exit(1)
