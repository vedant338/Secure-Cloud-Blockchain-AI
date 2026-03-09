import time
from backend.config import Config

_secret = getattr(Config, "JWT_SECRET", "secure-cloud-secret-change-in-production")

def encode_token(username: str) -> str:
    import base64
    import json
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": username, "exp": int(time.time()) + 86400}
    b64 = lambda x: base64.urlsafe_b64encode(json.dumps(x).encode()).rstrip(b"=").decode()
    msg = f"{b64(header)}.{b64(payload)}"
    sig = _simple_hmac(msg)
    return f"{msg}.{sig}"

def decode_token(token: str) -> str | None:
    try:
        import base64
        import json
        parts = token.split(".")
        if len(parts) != 3:
            return None
        msg = f"{parts[0]}.{parts[1]}"
        if _simple_hmac(msg) != parts[2]:
            return None
        payload_b64 = parts[1] + "=="
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        exp = payload.get("exp", 0)
        if exp < int(time.time()):
            return None
        return payload.get("sub")
    except Exception:
        return None

def _simple_hmac(msg: str) -> str:
    import hashlib
    key = _secret.encode()
    inner = hashlib.sha256((key + msg.encode())).hexdigest()
    return hashlib.sha256((key + inner.encode())).hexdigest()[:43]
