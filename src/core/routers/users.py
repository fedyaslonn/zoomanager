from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import logging

from src.core.dtos.auth_dto import TokenResponse, LoginRequest
from src.core.dtos.user_dto import CreateUser, AdoptAnimalResponse, UserSchema
from src.core.interactors.users_interactors import RegisterUserInteractor, get_register_user_interactor, \
    AuthenticateUserInteractor, get_authenticate_user_interactor, AdoptAnimalInteractor, get_adopt_animal_interactor, \
    get_release_animal_interactor, ReleaseAnimalInteractor
from src.core.services.users_service import get_current_user_dependency

logger = logging.getLogger(__name__)

user_router = APIRouter(prefix="/auth", tags=["auth"])


@user_router.post("/register", response_model=TokenResponse)
async def register_user(
    user_data: CreateUser,
    register_user_interactor: RegisterUserInteractor = Depends(get_register_user_interactor),
):
    try:
        user, tokens = await register_user_interactor.execute(user_data)
        return tokens

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"Неизвестная ошибка при регистрации пользователя: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла внутренняя ошибка сервера",
        )


@user_router.post("/login", response_model=TokenResponse)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        authenticate_user_interactor: AuthenticateUserInteractor = Depends(get_authenticate_user_interactor)
):
    try:
        credentials = LoginRequest(username=form_data.username, password=form_data.password)
        result = await authenticate_user_interactor.execute(credentials)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный username или пароль",
            )
        tokens = result
        return tokens

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"Неизвестная ошибка при аутентификации пользователя: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла внутренняя ошибка сервера",
        )


@user_router.post("/adopt_animal/{user_id}/{animal_id}", response_model=AdoptAnimalResponse)
async def adopt_animal(
        user_id: int,
        animal_id: int,
        adopt_animal_interactor: AdoptAnimalInteractor = Depends(get_adopt_animal_interactor),
        current_user: UserSchema = Depends(get_current_user_dependency)
):
    try:
        adopt_request = await adopt_animal_interactor.execute(user_id, animal_id)
        return adopt_request

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"Неизвестная ошибка при попытке приручить животное: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла внутренняя ошибка сервера",
        )


@user_router.post("/release_animal/{user_id}/{animal_id}")
async def adopt_animal(
        user_id: int,
        animal_id: int,
        release_animal_interactor: ReleaseAnimalInteractor = Depends(get_release_animal_interactor),
        current_user: UserSchema = Depends(get_current_user_dependency)
):
    try:
        release_request = await release_animal_interactor.execute(user_id, animal_id)

        return release_request

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.error(f"Неизвестная ошибка при попытке отпустить животное: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла внутренняя ошибка сервера",
        )
