from typing import Annotated, Protocol, Optional, Tuple, TypeVar

from fastapi import Depends

from src.core.dtos.auth_dto import TokenResponse, RefreshTokenRequest, LoginRequest
from src.core.dtos.user_dto import UserSchema, UpdateUserRequest, CreateUser, UpdateUserResponse, DeleteUserResponse
from src.core.repositories.user_repository import UserRepositoryProtocol
from src.core.services.users_service import UserServiceProtocol

user_input = TypeVar('user_input', contravariant=True)
user_output = TypeVar('user_output', covariant=True)


class UserUseCaseProtocol(Protocol[user_input, user_output]):
    async def __call__(self, data: user_input) -> user_output:
        ...

class RegisterUserUseCase:
    def __init__(self, users_service: 'UserServiceProtocol'):
        self.users_service = users_service

    async def __call__(self, user_data: CreateUser) -> Tuple[UserSchema, TokenResponse]:
        return await self.users_service.register_user(user_data)


class AuthenticateUserUseCase:
    def __init__(self, users_service: 'UserServiceProtocol'):
        self.user_service = users_service

    async def __call__(self, credentials: LoginRequest) -> Optional[Tuple[UserSchema, TokenResponse]]:
        return await self.user_service.authenticate_user(credentials.username, credentials.password)


class AdoptAnimalUseCase:
    def __init__(self, users_service: 'UserServiceProtocol'):
        self.users_service = users_service

    async def __call__(self, user_id: int, animal_id: int) -> None:
        return await self.users_service.adopt_animal(user_id, animal_id)


class ReleaseAnimalUseCase:
    def __init__(self, users_service: 'UserServiceProtocol'):
        self.users_service = users_service

    async def __call__(self, user_id: int, animal_id: int) -> None:
        return await self.users_service.release_animal(user_id, animal_id)
