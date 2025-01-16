from src.core.repositories.uow import IUnitOfWork, get_uow
from src.core.repositories.user_repository import UserRepository


from typing import Protocol, Tuple, Optional, Annotated

from src.core.dtos.user_dto import CreateUser, UserSchema, UserResponse, AnimalResponse, AdoptAnimalResponse
from src.core.dtos.auth_dto import TokenResponse
from src.core.repositories.user_repository import UserRepositoryProtocol, get_user_repository

from src.core.utils.jwt_handler import Hasher, JWTHandler, oauth2_scheme, get_jwt_handler

from fastapi import HTTPException, status, Depends

import logging

logger = logging.getLogger(__name__)


class UserServiceProtocol(Protocol):
    async def register_user(self, user_data: CreateUser) -> Tuple[UserSchema, TokenResponse]:
        ...

    async def authenticate_user(self, username: str, password: str) -> Optional[TokenResponse]:
        ...

    async def adopt_animal(self, user_id: int, animal_id: int):
        ...

    async def release_animal(self, user_id: int, animal_id: int):
        ...

    async def get_current_user(self, auth_token: Optional[str]):
        ...

class UserService:
    def __init__(self, jwt_handler: JWTHandler, uow: IUnitOfWork):
        self.jwt_handler = jwt_handler
        self.uow = uow

    async def authenticate_user(self, username: str, password: str):
        async with self.uow as uow:
            authentication_exception = HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Username или пароль не верны",
            )
            user = await uow.users.get_user_by_username(username)

            if not user:
                raise authentication_exception

            if user and Hasher.verify_password(password, user.hashed_password):

                access_token = await self.jwt_handler.generate_access_token(data={ "username": user.username, "user_id": str(user.id) })
                refresh_token = await self.jwt_handler.generate_refresh_token(data={ "username": user.username, "user_id": str(user.id) })

                return (TokenResponse(access_token=access_token, refresh_token=refresh_token, token_type="Bearer"))

            return None

    async def register_user(self, user_data: CreateUser):
        async with self.uow as uow:
            authentication_exception = HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удалось зарегистрировать пользователя"
            )

            existing_user = await uow.users.get_user_by_username(user_data.username)

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Пользователь с таким именем уже существует"
                )
            try:
                new_user = await uow.users.add_one({"username": user_data.username,
                                                           "hashed_password": Hasher.hash_password(user_data.password)
                                                           })


                access_token = await self.jwt_handler.generate_access_token(
                    data={"username": new_user.username, "user_id": str(new_user.id)}
                )

                refresh_token = await self.jwt_handler.generate_refresh_token(
                    data={"username": new_user.username, "user_id": str(new_user.id)}
                )
                await uow.commit()

            except Exception as e:
                await uow.rollback()
                raise authentication_exception

            return (new_user, TokenResponse(access_token=access_token, refresh_token=refresh_token, token_type="Bearer"))

    async def get_current_user(self, auth_token: Optional[str] = Depends(oauth2_scheme)):
        token_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидные данные для входа",
        )
        if not auth_token:
            raise token_exception

        username = await self.jwt_handler.verify_token(auth_token, token_type="access")

        if not username:
            raise token_exception


        async with self.uow as uow:
            user = await uow.users.get_user_by_username(username)

            if not user:
                raise token_exception

            return user

    async def adopt_animal(self, user_id: int, animal_id: int):
        exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверные данные"
        )

        async with self.uow as uow:
            try:
                adopt_request = await uow.users.adopt_animal(user_id, animal_id)

                if not adopt_request:
                    raise exception

                await uow.commit()

                user_response = UserResponse(
                    id=adopt_request.id,
                    username=adopt_request.username
                )

                animals_response = [
                    AnimalResponse(
                        id=animal.id,
                        species=animal.species,
                        age=animal.age,
                        created_at=animal.created_at,
                        master_id=animal.master_id
                    )
                    for animal in adopt_request.animals
                ]

                return AdoptAnimalResponse(
                    master=user_response,
                    animals=animals_response
                )

            except HTTPException as e:
                await uow.rollback()
                logger.error(f"Ошибка при попытке приручить животное {e.detail}")
                raise e

            except Exception as e:
                await uow.rollback()
                logger.error(f"Неизвестная ошибка при попытке приручить животное {str(e)}")
                raise e

    async def release_animal(self, user_id: int, animal_id: int):
        exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверные данные"
        )

        async with self.uow as uow:
            try:
                release_request = await uow.users.release_animal(user_id, animal_id)

                if not release_request:
                    raise exception

                await uow.commit()
                return release_request

            except HTTPException as e:
                await uow.rollback()
                logger.error((f"Ошибка при попытке отпустить животное {e.detail}"))
                raise e

            except Exception as e:
                await uow.rollback()
                logger.error(f"Неизвестная ошибка при попытке отпустить животное {str(e)}")
                raise e


async def get_user_service(
    jwt_handler: JWTHandler =  Depends(get_jwt_handler),
    uow: IUnitOfWork = Depends(get_uow)
) -> UserServiceProtocol:
    return UserService(uow=uow, jwt_handler=jwt_handler)

UserServ = Annotated[UserServiceProtocol, Depends(get_user_service)]

async def get_current_user_dependency(
        auth_token: str = Depends(oauth2_scheme),
        user_service: UserServiceProtocol = Depends(get_user_service)
):
    return await user_service.get_current_user(auth_token)