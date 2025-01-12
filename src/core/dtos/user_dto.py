import uuid
from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, Field

from src.config.settings import TunedModel

import datetime


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: str

class UserSchema(TunedModel):
    user_id: uuid.UUID
    username: str
    password: bytes

class UpdateUserRequest(CreateUser):
    pass

class UpdateUserResponse(BaseModel):
    username: str
    updated_at: datetime = Field(default_factory=datetime.datetime.utcnow)

class DeleteUserResponse(BaseModel):
    user_id: uuid.UUID