from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.auth.user_store import get_user_password, create_user
from backend.auth.password_utils import hash_password, verify_password
from backend.auth.jwt_utils import encode_token

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(req: LoginRequest):
    username = req.username.strip().lower()
    if not username or not req.password:
        raise HTTPException(status_code=400, detail="Username and password required")
    stored = get_user_password(username)
    if not stored or not verify_password(req.password, stored):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = encode_token(username)
    return {"token": token, "username": username}

@router.post("/register")
async def register(req: RegisterRequest):
    username = req.username.strip()
    if len(username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters")
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    hashed = hash_password(req.password)
    if not create_user(username, hashed):
        raise HTTPException(status_code=400, detail="Username already taken")
    token = encode_token(username)
    return {"token": token, "username": username}
