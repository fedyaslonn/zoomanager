import uuid
from typing import Annotated, List, Optional

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, Field, ConfigDict

from src.config.settings import TunedModel

from _datetime import datetime

from src.core.models.models import User, Animal

class CreateUser(TunedModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: str


class UserSchema(TunedModel):
    id: int
    username: str
    password: bytes

class UpdateUserRequest(CreateUser):
    pass

class UpdateUserResponse(BaseModel):
    username: str
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DeleteUserRequest(BaseModel):
    user_id: int

class UserResponse(BaseModel):
    id: int
    username: str

class AnimalResponse(BaseModel):
    id: int
    species: str
    age: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    master_id: Optional[int]

class AdoptAnimalResponse(BaseModel):
    master: UserResponse
    animals: List[AnimalResponse]
