from fastapi import HTTPException, status
from fastapi.params import Depends

from src.core.dtos.auth_dto import TokenResponse, LoginRequest
from src.core.dtos.user_dto import CreateUser, UserSchema

from src.core.services.users_service import UserServiceProtocol, UserService, get_user_service
from src.core.repositories.user_repository import UserRepository, UserRepositoryProtocol

from typing import Protocol, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class RegisterUserInteractor:
    def __init__(self, user_service: UserServiceProtocol):
        self.user_service = user_service

    async def execute(self, user_data: CreateUser) -> Tuple[UserSchema, TokenResponse]:
        try:
            user_info = await self.user_service.register_user(user_data)

            return user_info

        except HTTPException as e:
            logger.error(f"Ошибка при регистрации пользователя: {e.detail}")
            raise e

class AuthenticateUserInteractor:
    def __init__(self, user_service: UserServiceProtocol):
        self.user_service = user_service

    async def execute(self, credentials: LoginRequest) -> Optional[Tuple[UserSchema, TokenResponse]]:
        try:
            result = await self.user_service.authenticate_user(credentials.username, credentials.password)

            return result

        except HTTPException as e:
            logger.error(f"Ошибка при аутентификации пользователя: {e.detail}")
            raise e


class AdoptAnimalInteractor:
    def __init__(self, user_service: UserServiceProtocol):
        self.user_service = user_service

    async def execute(self, animal_id: int, user_id: int):
        try:
            result = await self.user_service.adopt_animal(animal_id, user_id)

            return result

        except HTTPException as e:
            logger.error(f"Ошибка при попытке приручить животное: {e.detail}")
            raise e


class ReleaseAnimalInteractor:
    def __init__(self, user_service: UserServiceProtocol):
        self.user_service = user_service

    async def execute(self, animal_id: int, user_id: int):
        try:
            result = await self.user_service.release_animal(animal_id, user_id)

            return result

        except HTTPException as e:
            logger.error(f"Ошибка при попытке отпустить животное: {e.detail}")
            raise e


async def get_register_user_interactor(
        user_service: UserServiceProtocol = Depends(get_user_service),
) -> RegisterUserInteractor:
    return RegisterUserInteractor(user_service=user_service)


async def get_authenticate_user_interactor(
    user_service: UserServiceProtocol = Depends(get_user_service),
) -> AuthenticateUserInteractor:
    return AuthenticateUserInteractor(user_service=user_service)

async def get_adopt_animal_interactor(
    user_service: UserServiceProtocol = Depends(get_user_service)
) -> AdoptAnimalInteractor:
    return AdoptAnimalInteractor(user_service=user_service)

async def get_release_animal_interactor(
    user_service: UserServiceProtocol = Depends(get_user_service)
) -> ReleaseAnimalInteractor:
    return ReleaseAnimalInteractor(user_service=user_service)