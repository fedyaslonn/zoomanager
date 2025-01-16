from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.session_factory import get_async_session
from src.core.repositories.animals_repository import AnimalsRepository, AnimalsRepositoryProtocol, get_animals_repository

from typing import Protocol, Tuple, Optional, List, Annotated

from src.core.dtos.zoo_dto import CreateAnimal, AnimalSchema, UpdateAnimalRequest, UpdateAnimalResponse, DeleteAnimalRequest

from fastapi import HTTPException, status, Depends

from src.core.repositories.uow import IUnitOfWork, get_uow

import logging

logger = logging.getLogger(__name__)


class AnimalServiceProtocol(Protocol):
    async def create_animal(self, animal_data: CreateAnimal) -> AnimalSchema:
        ...

    async def update_animal(self, update_animal_data: UpdateAnimalRequest) -> UpdateAnimalResponse:
        ...

    async def get_animal_by_id(self, id: int) -> Optional[AnimalSchema]:
        ...

    async def get_animals_by_species(self, species: str) -> List[AnimalSchema]:
        ...

    async def delete_animal_by_id(self, id: int) -> bool:
        ...


class AnimalService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def create_animal(self, animal_data: CreateAnimal) -> AnimalSchema:
        async with self.uow as uow:
            search_exception = HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удалось создать животное"
            )

            try:
                animal_dict = animal_data.model_dump()
                animal_dict["created_at"] = datetime.utcnow()

                new_animal = await uow.animals.add_one(animal_dict)
                animal_response = AnimalSchema.model_validate(new_animal)

                await uow.commit()

            except Exception as e:
                await uow.rollback()
                raise search_exception

            return animal_response

    async def update_animal(self, animal_data: UpdateAnimalRequest) -> UpdateAnimalResponse:
        async with self.uow as uow:
            update_exception = HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не удалось обновить животное"
            )

            try:
                update_data = {}
                if animal_data.age is not None:
                    update_data["age"] = animal_data.age

                if animal_data.species is not None:
                    update_data["species"] = animal_data.species

                new_animal = await uow.animals.edit_one(data=update_data, inst_id=animal_data.id)
                await uow.commit()

                if not hasattr(new_animal, 'id'):
                    raise ValueError("Новая запись не содержит id")

                return UpdateAnimalResponse(
                                            species=new_animal.species,
                                            age=new_animal.age,
                                            updated_at=datetime.utcnow())

            except HTTPException as e:
                logger.error(f"Ошибка при попытке обновить животное {e.detail}")
                await uow.rollback()
                raise update_exception

            except Exception as e:
                logger.error(f"Неизвестная ошибка при попытке обновить животное {str(e)}")
                await uow.rollback()
                raise e

    async def get_animal_by_id(self, id: int) -> Optional[AnimalSchema]:
        search_exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не удалось найти животное по id"
        )

        async with self.uow as uow:
            animal = await uow.animals.find_one(inst_id=id)

            if not animal:
                raise search_exception

            return animal

    async def get_animals_by_species(self, species: str):
        search_exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не удалось найти животное по виду"
        )

        async with self.uow as uow:
            try:
                animals = await uow.animals.get_animals_by_species(species=species)

                if not animals:
                    raise search_exception

                return [AnimalSchema.model_validate(animal) for animal in animals]

            except HTTPException as e:
                logger.error(f"Ошибка при попытке получить список животных {e.detail}")
                raise search_exception

            except Exception as e:
                logger.error(f"Неизвестная ошибка при попытке получить список животных {e}")
                raise e

    async def delete_animal_by_id(self, id: int):
        delete_exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось удалить животное"
        )

        async with self.uow as uow:
            try:
                animal = await uow.animals.find_one(inst_id=id)

                if not animal:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Животное не найдено"
                    )

                logger.info(f"найденное животное {animal}")

                await uow.animals.delete_one(inst_id=animal.id)
                await uow.commit()

            except HTTPException as e:
                await uow.rollback()
                logger.error(f"Ошибка при попытке удалить животное {e.detail}")
                raise delete_exception

            except Exception as e:
                await uow.rollback()
                logger.error(f"Неизвестная ошибка при попытке удалить животное {str(e)}")
                raise e

async def get_animals_service(uow: IUnitOfWork = Depends(get_uow)) -> AnimalServiceProtocol:
    return AnimalService(uow=uow)

AnimServ = Annotated[AnimalServiceProtocol, Depends(get_animals_service)]