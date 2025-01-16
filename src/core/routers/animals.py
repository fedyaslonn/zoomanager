from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dtos.user_dto import UserSchema
from src.core.dtos.zoo_dto import *
from src.core.interactors.animals_interactors import *
from src.core.services.users_service import get_user_service, get_current_user_dependency

animal_router = APIRouter(prefix="/animals", tags=["animals"])

@animal_router.post("/create_animal", response_model=AnimalSchema)
async def create_animal(
        animal_data: CreateAnimal,
        create_animal_interactor: CreateAnimalInteractor = Depends(get_create_animal_interactor),
        current_user: UserSchema = Depends(get_current_user_dependency)
):
    try:
        animal = await create_animal_interactor.execute(animal_data)
        return animal

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла внутренняя ошибка сервера"
        )


@animal_router.post("/update_animal", response_model=UpdateAnimalResponse)
async def update_animal(
        animal_data: UpdateAnimalRequest,
        update_animal_interactor: UpdateAnimalInteractor = Depends(get_update_animal_interactor),
        current_user: UserSchema = Depends(get_current_user_dependency)
):
    try:
        animal = await update_animal_interactor.execute(animal_data)

        return animal

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла внутренняя ошибка сервера"
        )

@animal_router.get("/get_animal_by_id/{id}", response_model=Optional[AnimalSchema])
async def get_animal_by_id(
        id: int,
        get_animal_by_id_interactor: GetAnimalByIdInteractor = Depends(get_animal_by_id_interactor),
        current_user: UserSchema = Depends(get_current_user_dependency)
):
    try:
        animal = await get_animal_by_id_interactor.execute(id)

        return animal

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла внутренняя ошибка сервера"
        )

@animal_router.get("/get_animals_by_species", response_model=Optional[List[AnimalSchema]])
async def get_animals_by_species(
        species: str,
        get_animals_by_species_interactor: GetAnimalsBySpeciesInteractor = Depends(get_animals_by_species_interactor),
        current_user: UserSchema = Depends(get_current_user_dependency)
):
    try:
        animals = await get_animals_by_species_interactor.execute(species)

        return animals

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла внутренняя ошибка сервера",
        )

@animal_router.delete("/delete_animal_by_id/{id}")
async def delete_animal_by_id(
        id: int,
        get_delete_animal_by_id_interactor: DeleteAnimalByIdInteractor = Depends(get_delete_animal_by_id_interactor),
        current_user: UserSchema = Depends(get_current_user_dependency)
):
    try:
        await get_delete_animal_by_id_interactor.execute(id)

    except HTTPException as e:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла внутреняя ошибка сервера"
        )