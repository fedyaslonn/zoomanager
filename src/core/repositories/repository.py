from typing import Protocol, Dict, List, Optional, TypeVar, Generic, Any, Annotated

from fastapi import Depends
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.session_factory import get_async_session
from src.core.repositories.uow import UnitOfWork

T = TypeVar("T")

class AbstractRepository(Protocol[T]):
    async def add_one(self, data: dict) -> T:
        ...

    async def edit_one(self, data: dict, inst_id: int) -> T:
        ...

    async def find_all(self) -> List[T]:
        ...

    async def find_one(self, inst_id: int) -> Optional[T]:
        ...

    async def delete_one(self, inst_id: int) -> bool:
        ...

class SQLAlchemyRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> T:
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def edit_one(self, data: dict, inst_id: int) -> T:
        stmt = update(self.model).values(**data).where(self.model.id == inst_id)
        res = await self.session.execute(stmt)

        stmt = select(self.model).where(self.model.id == inst_id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_all(self) -> List[T]:
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def find_one(self, inst_id: int) -> Optional[T]:
        stmt = select(self.model).where(self.model.id == inst_id)
        res = await self.session.execute(stmt)
        return res.scalars().one_or_none()

    async def delete_one(self, inst_id: int) -> bool:
        stmt = delete(self.model).where(self.model.id == inst_id)
        result = await self.session.execute(stmt)

        if result.rowcount == 0:
            raise ValueError("Объект не найден")

        return True

async def get_sql_rep(session: AsyncSession = Depends(get_async_session)) -> AbstractRepository:
    return SQLAlchemyRepository(session=session)

SQLRep = Annotated[AbstractRepository, Depends(get_sql_rep)]