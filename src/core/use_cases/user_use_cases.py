from typing import Annotated, Protocol, Optional, Tuple

from fastapi import Depends

from src.core.dtos.auth_dto import TokenResponse, RefreshTokenRequest, LoginRequest
from src.core.dtos.user_dto import UserSchema, UpdateUserRequest, CreateUser, UpdateUserResponse, DeleteUserResponse
from src.core.repositories.user_repository import UserRepositoryProtocol


class UserUseCaseProtocol(Protocol):
    async def register_user(self, user_data: CreateUser) -> Tuple[UserSchema, TokenResponse]:
        ...

    async def authenticate_user(self, username: str, password: str) -> Optional[Tuple[UserSchema, TokenResponse]]:
        ...

    async def adopt_animal(self, user_id: str, animal_id: str):
        ...

    async def release_animal(self, user_id: str, animal_id: str):
        ...

    async def get_current_user(self, auth_token: Optional[str]):
        ...


class UserUseCase:
    def __init__(self, repo: UserRepositoryProtocol, ):
        self.repo = repo

    def register_user(self):
