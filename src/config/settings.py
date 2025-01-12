import os
from dataclasses import dataclass
from dotenv import load_dotenv
import sys
from pydantic import BaseModel
from pydantic.v1 import BaseSettings, Field

load_dotenv()

class DBSettings(BaseSettings):
    host: str = Field(env="DB_HOST")
    port: int = Field(env="DB_PORT", default=5432)
    user: str = Field(env="DB_USER")
    password: str = Field(env="DB_PASS")
    name: str = Field(env="DB_NAME")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

@dataclass
class Settings:
    SECRET_KEY: str = os.getenv("")
    TOKEN_TYPE: str = os.getenv("TOKEN_TYPE")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int =  30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60*24*15


pythonpath = os.getenv('PYTHONPATH')

if pythonpath:
    sys.path.append(pythonpath)

class TunedModel(BaseModel):
    class Config:
        orm_mode = True


settings = Settings()
db = DBSettings()