import math
from collections import Counter

def calculate_entropy(data: bytes) -> float:
    if not data:
        return 0.0

    counter = Counter(data)
    length = len(data)

    entropy = 0.0
    for count in counter.values():
        p = count / length
        entropy -= p * math.log2(p)

    return entropy


def extract_features(
    file_bytes: bytes,
    file_hash: str,
    is_verified: bool
):
    return {
        "file_size": len(file_bytes),
        "hash_length": len(file_hash),
        "entropy": calculate_entropy(file_bytes),
        "verified": int(is_verified)
    }