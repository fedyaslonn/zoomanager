from typing import Protocol, Optional, Annotated

from fastapi.params import Depends, Header

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.core.dtos.auth_dto import TokenResponse
from src.core.models.models import User, Animal
from src.core.models.session_factory import get_async_session
from src.core.repositories.repository import SQLAlchemyRepository


class UserRepositoryProtocol(Protocol):
    async def get_user_by_username(self, username: str) ->  User:
        ...

    async def adopt_animal(self, user_id: int, animal_id):
        ...

    async def release_animal(self, user_id: int, animal_id: int):
        ...

class TokenGeneratorProtocol(Protocol):
    async def generate_access_token(self, user_id: str) -> TokenResponse:
        ...

    async def generate_refresh_token(self, user_id: str) -> TokenResponse:
        ...

    def verify_token(self, token: str) -> Optional[str]:
        ...

class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_user_by_username(self, username: str) -> User:
        result = await self.session.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        return user

    async def adopt_animal(self, user_id: int, animal_id: int):
        user = await self.session.execute(select(User).where(User.id == user_id).options(selectinload(User.animals)))
        user = user.scalars().first()

        animal = await self.session.execute(select(Animal).where(Animal.id == animal_id))
        animal = animal.scalars().first()

        if not user or not animal:
            raise ValueError("Не удалось найти ни животное ни человека")

        if animal not in user.animals:
            user.animals.append(animal)

        else:
            raise ValueError("Нельзя дважды добавить к себе одно и то же животное")

        return user

    async def release_animal(self, user_id: int, animal_id: int):
        user = await self.session.execute(select(User).where(User.id == user_id).options(selectinload(User.animals)))
        user = user.scalars().first()

        animal = await self.session.execute(select(Animal).where(Animal.id == animal_id))
        animal = animal.scalars().first()

        if not user or not animal:
            raise ValueError("Не удалось найти ни животное ни человека")

        if animal not in user.animals:
            raise ValueError("Нельзя удалить у пользователя животное, которого у него нету")

        user.animals.remove(animal)
        return user

async def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepositoryProtocol:
    return UserRepository(session=session)

UserRep = Annotated[UserRepositoryProtocol, Depends(get_user_repository)]
