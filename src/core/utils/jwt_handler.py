import jwt
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from src.config.settings import settings
from passlib.context import CryptContext


class JWTHandler:
    def __init__(self, access_secret_key: str, refresh_secret_key: str, access_token_expiration_minutes: int, refresh_token_expiration_minutes: int):
        self.access_secret_key = access_secret_key
        self.refresh_secret_key = refresh_secret_key
        self.algorithm = settings.ALGORITHM
        self.access_token_expiration = timedelta(minutes=access_token_expiration_minutes)
        self.refresh_token_expiration = timedelta(minutes=refresh_token_expiration_minutes)

    async def generate_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()

        expire = datetime.utcnow() + (expires_delta if expires_delta else self.access_token_expiration)
        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, self.access_secret_key, algorithm=self.algorithm)


    async def generate_refresh_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()

        expire = datetime.utcnow() + (expires_delta if expires_delta else self.refresh_token_expiration)
        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, self.refresh_secret_key, algorithm=self.algorithm)


    async def verify_token(self, token: str, token_type: str = ''):
        try:
            secret_key = self.access_secret_key if token_type == 'access' else self.refresh_secret_key
            payload = jwt.decode(token, secret_key, algorithms=[self.algorithm])
            return payload.get('username')

        except jwt.PyJWTError as e:
            return None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class Hasher:
    @staticmethod
    def verify_password(planned_password: str, hashed_password: bytes):
        return pwd_context.verify(planned_password, hashed_password)

    @staticmethod
    def hash_password(password: str):
        return pwd_context.hash(password)


async def get_jwt_handler() -> JWTHandler:
    return JWTHandler(
        access_secret_key=settings.SECRET_KEY,
        refresh_secret_key=settings.REFRESH_SECRET_KEY,
        access_token_expiration_minutes=30,
        refresh_token_expiration_minutes=1440
    )