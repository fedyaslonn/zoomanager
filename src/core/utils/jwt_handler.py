import bcrypt
import jwt
import os
from typing import Optional
from datetime import datetime, timedelta
from config.settings import settings
from domain.protocols.auth_protocol import TokenGenerator
import uuid
from passlib.context import CryptoContext
from typing_extensions import deprecated
from jose import jwt
from fastapi import Request

class JWTHandler(TokenGenerator):
    def __init__(self, access_secret_key: str, refresh_secret_key: str, algorithm: str, access_token_expiration_minutes: int, refresh_token_expiration_minutes: int):
        self.access_secret_key = access_secret_key
        self.refresh_secret_key = refresh_secret_key
        self.algorithm = algorithm
        self.access_token_expiration_minutes = access_token_expiration_minutes
        self.refresh_token_expiration_minutes = refresh_token_expiration_minutes

    async def generate_access_token(self, data: dict, expires_time: timedelta | None = None):
        to_encode = data.copy()
        if expires_time:
            expire = datetime.utcnow() + expires_time
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expiration_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.access_secret_key, algorithm=ALGORITHM)


    async def generate_refresh_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.refresh_token_expiration_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.refresh_secret_key, self.algorithm)


    async def verify_token(self, token: str, key: Optional[str] = None, toke_type: str = ''):
        try:
            secret_key = self.access_secret_key if token_type == 'access' else self.refresh_secret_key
            payload = jwt.decode(token, secret_key, algorithms=[self.algorithm])
            return payload.get(key) if key else payload.get('sub')
        except JWTError as e:
            return None

pwd_context = CryptoContext(schemas=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    async def verify_password(planned_password: str, hashed_password: bytes):
        return pwd_context.verify(planned_password, hashed_password)

    @staticmethod
    async def hash_password(password: str):
        return pwd_context.hash(password)

async def check_cookie(request: Request):
    cookie = request.cookies

    if not cookie:
        return None

    if cookie.get('refresh-Token'):
        return cookie.get('refresh-Token')
