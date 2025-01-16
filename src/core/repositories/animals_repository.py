from typing import Protocol, Optional, Annotated, List

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from src.core.dtos.zoo_dto import CreateAnimal, AnimalSchema
from src.core.models.session_factory import get_async_session
from src.core.repositories.repository import SQLAlchemyRepository
from src.core.models.models import Animal


class AnimalsRepositoryProtocol(Protocol):
    async def get_animals_by_species(self, species: str):
        ...


class AnimalsRepository(SQLAlchemyRepository):
    model = Animal

    async def get_animals_by_species(self, species: str):
        result = await self.session.execute(select(Animal).where(Animal.species == species))
        animals = result.scalars().all()
        return animals

async def get_animals_repository(session: AsyncSession = Depends(get_async_session)) -> AnimalsRepositoryProtocol:
    return AnimalsRepository(session=session)

AnimalRep = Annotated[AnimalsRepositoryProtocol, Depends(get_animals_repository)]