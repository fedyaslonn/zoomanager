from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

session_engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(bind=session_engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session():
    async with async_session() as session:
        yield session