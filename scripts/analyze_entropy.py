import math
import sys

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

file_path = sys.argv[1]
entropy = calculate_entropy(file_path)
print(f"Entropy of {file_path}: {entropy:.2f}")
 
if entropy > 7.0:  
    print("SECURITY_ALERT: High entropy detected! Blocking build.")
    sys.exit(1) 
