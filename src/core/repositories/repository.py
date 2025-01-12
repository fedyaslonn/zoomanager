from typing import Protocol, Dict, List, Optional, TypeVar, Generic, Any

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")

class AbstractRepository(Protocol[T]):
    async def add_one(self, data: dict) -> T:
        ...

    async def edit_one(self, data: dict, id: int) -> T:
        ...

    async def find_all(self) -> List[T]:
        ...

    async def find_one(self, id: str) -> Optional[T]:
        ...

    async def delete_by_one(self, id: str) -> None:
        ...

class SQLAlchemyRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> T:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        # await self.session.commit()
        return res.scalar_one()

    async def edit_one(self, data: dict, inst_id: str) -> T:
        stmt = update(self.model).values(**data).where(self.model.id == inst_id).returning(self.model.id)
        res = await self.session.execute(stmt)
        # await self.session.commit()
        return res.scalar_one()

    async def find_all(self) -> List[T]:
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def find_one(self, inst_id: str) -> Optional[T]:
        stmt = select(self.model).where(self.model.id == inst_id)
        res = await self.session.execute(stmt)
        return res.scalars().one_or_none()

    async def delete_one(self, inst_id: str) -> None:
        stmt = delete(self.model).where(self.model.id == inst_id)
        await self.session.execute(stmt)
        # await self.session.commit()

async def get_sql_alchemy_repository(session: AsyncSession) -> AbstractRepository:
    return SQLAlchemyRepository(session=session)

SQLAlchemyRep = Annotated[AbstractRepository, Depends(get_sql_alchemy_repository)]