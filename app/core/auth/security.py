from http.client import HTTPException
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import hashlib
import base64
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

import re

def validate_password_strength(password: str):
    if len(password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")

    if not re.search(r"[A-Z]", password):
        raise HTTPException(400, "Password must contain one uppercase letter")

    if not re.search(r"[a-z]", password):
        raise HTTPException(400, "Password must contain one lowercase letter")

    if not re.search(r"\d", password):
        raise HTTPException(400, "Password must contain one number")

    if not re.search(r"[@$!%*?&#]", password):
        raise HTTPException(400, "Password must contain one special character")

def _prehash(password: str) -> str:
    # produce a fixed-length, bcrypt-safe string from the password
    # use SHA-256 digest then base64-encode -> 44 chars (always < 72 bytes)

    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.b64encode(digest).decode("ascii")


def hash_password(password: str) -> str:

    # validate_password_strength(password)
    pre = _prehash(password)
    return pwd_context.hash(pre)


def verify_password(password: str, hashed_password: str) -> bool:
    pre = _prehash(password)
    return pwd_context.verify(pre, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
