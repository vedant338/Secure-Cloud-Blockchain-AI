from typing import Dict, Optional

_users: Dict[str, str] = {}

def get_user_password(username: str) -> Optional[str]:
    return _users.get(username.lower())

def create_user(username: str, password_hash: str) -> bool:
    key = username.lower()
    if key in _users:
        return False
    _users[key] = password_hash
    return True
