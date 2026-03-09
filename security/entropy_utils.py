import math
from collections import Counter

def calculate_entropy(data: bytes) -> float:
    if not data:
        return 0.0

    counts = Counter(data)
    entropy = 0.0
    length = len(data)

    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)

    return round(entropy, 4)