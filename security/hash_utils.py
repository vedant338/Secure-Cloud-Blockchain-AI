import hashlib

def sha256_hash(data: bytes) -> str:
    """
    Generate SHA-256 hash of given data.
    Returns hex string.
    """
    sha = hashlib.sha256()
    sha.update(data)
    return sha.hexdigest()