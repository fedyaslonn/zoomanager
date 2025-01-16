from typing import Annotated, Optional

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, Field

from src.config.settings import TunedModel

from _datetime import datetime


class CreateAnimal(TunedModel):
    species: Annotated[str, MinLen(2), MaxLen(15)]
    age: Annotated[int, Field(ge=0, le=50)]


class AnimalSchema(CreateAnimal):
    id: int


class UpdateAnimalRequest(BaseModel):
    id: int
    age: Optional[Annotated[int, Field(ge=0, le=50)]] = None
    species: Optional[Annotated[str, MinLen(2), MaxLen(15)]] = None


class UpdateAnimalResponse(CreateAnimal):
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DeleteAnimalRequest(BaseModel):
    pet_id: int