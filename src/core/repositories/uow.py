from typing import Protocol, Type, Optional

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.core.models.session_factory import async_session

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.core.repositories.user_repository import UserRepositoryProtocol, UserRepository
    from src.core.repositories.animals_repository import AnimalsRepositoryProtocol, AnimalsRepository

class IUnitOfWork(Protocol):
    users: "UserRepositoryProtocol"
    animals: "AnimalsRepositoryProtocol"

    async def __aenter__(self):
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    async def commit(self):
        ...

    async def rollback(self):
        ...

class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def __aenter__(self):
        from src.core.repositories.animals_repository import AnimalsRepositoryProtocol, AnimalsRepository
        from src.core.repositories.user_repository import UserRepositoryProtocol, UserRepository
        self.users = UserRepository(self.session)
        self.animals = AnimalsRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()

        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

async def get_uow() -> UnitOfWork:
    async with async_session() as session:
        yield UnitOfWork(session)