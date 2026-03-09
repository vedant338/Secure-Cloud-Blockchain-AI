import hashlib
import math 

from collections import Counter
def sha256_hash(data: bytes) -> str:
    """
    Generate SHA-256 hash of given data.
    Returns hex string.
    """
    sha = hashlib.sha256()
    sha.update(data)
    return sha.hexdigest()

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