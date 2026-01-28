from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import hashlib
import base64

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def _prehash(password: str) -> str:
    # produce a fixed-length, bcrypt-safe string from the password
    # use SHA-256 digest then base64-encode -> 44 chars (always < 72 bytes)
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    return base64.b64encode(digest).decode("ascii")


def hash_password(password: str) -> str:
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
