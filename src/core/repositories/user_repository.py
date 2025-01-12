from typing import Protocol, Optional, Annotated

from fastapi.params import Depends, Header

from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dtos.auth_dto import TokenResponse
from src.core.dtos.user_dto import UserSchema
from src.core.models.models import User


class UserRepositoryProtocol(Protocol):
    async def get_user_by_username(self, username: str) ->  User:
        ...

class Toke0nGeneratorProtocol(Protocol):
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

async def get_user_repository(session: AsyncSession) -> UserRepositoryProtocol:
    return UserRepository(session=session)

UserRep = Annotated[UserRepositoryProtocol, Depends(get_user_repository)]
