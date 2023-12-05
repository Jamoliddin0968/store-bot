from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from src.config import REFRESH_SECRET_KEY, SECRET_KEY

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = SECRET_KEY   # should be kept secret
JWT_REFRESH_SECRET_KEY = REFRESH_SECRET_KEY

# Constants for hashing
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    access_token_expires = (
        expires_delta or datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {"exp": access_token_expires, "sub": str(subject)}
    return jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    refresh_token_expires = (
        expires_delta or datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {"exp": refresh_token_expires, "sub": str(subject)}
    return jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)
