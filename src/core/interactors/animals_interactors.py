from fastapi import HTTPException, status
from fastapi.params import Depends

from src.core.dtos.zoo_dto import *
from src.core.repositories.uow import get_uow

from src.core.services.animals_service import AnimalServiceProtocol, AnimalService, get_animals_repository, \
    get_animals_service

from typing import Protocol, Tuple, Optional, List


class CreateAnimalInteractor:
    def __init__(self, animal_service: AnimalServiceProtocol):
        self.animal_service = animal_service

    async def execute(self, animal_data: CreateAnimal) -> AnimalSchema:
        try:
            animal_info = await self.animal_service.create_animal(animal_data)

            return animal_info

        except HTTPException as e:
            raise e

class UpdateAnimalInteractor:
    def __init__(self, animal_service: AnimalServiceProtocol):
        self.animal_service = animal_service

    async def execute(self, animal_data: UpdateAnimalRequest) -> UpdateAnimalResponse:
        try:
            update_animal = await self.animal_service.update_animal(animal_data)

            return update_animal

        except HTTPException as e:
            raise e

class GetAnimalByIdInteractor:
    def __init__(self, animal_service: AnimalServiceProtocol):
        self.animal_service = animal_service

    async def execute(self, id: int) -> Optional[AnimalSchema]:
        try:
            animal = await self.animal_service.get_animal_by_id(id)

            return animal

        except HTTPException as e:
            raise e

class GetAnimalsBySpeciesInteractor:
    def __init__(self, animal_service: AnimalServiceProtocol):
        self.animal_service = animal_service

    async def execute(self, species: str) -> List[AnimalSchema]:
        try:
            animals = await self.animal_service.get_animals_by_species(species)

            return animals

        except HTTPException as e:
            raise e

class DeleteAnimalByIdInteractor:
    def __init__(self, animal_service: AnimalServiceProtocol) -> bool:
        self.animal_service = animal_service

    async def execute(self, id: int):
        try:
            await self.animal_service.delete_animal_by_id(id)

        except HTTPException as e:
            raise e

async def get_create_animal_interactor(
        animal_service: AnimalServiceProtocol = Depends(get_animals_service)
) -> CreateAnimalInteractor:
    return CreateAnimalInteractor(animal_service=animal_service)

async def get_update_animal_interactor(
        animal_service: AnimalServiceProtocol = Depends(get_animals_service)
) -> UpdateAnimalInteractor:
    return UpdateAnimalInteractor(animal_service=animal_service)

async def get_animal_by_id_interactor(
        animal_service: AnimalServiceProtocol = Depends(get_animals_service)
) -> GetAnimalByIdInteractor:
    return GetAnimalByIdInteractor(animal_service=animal_service)

async def get_animals_by_species_interactor(
        animal_service: AnimalServiceProtocol = Depends(get_animals_service)
) -> GetAnimalsBySpeciesInteractor:
    return GetAnimalsBySpeciesInteractor(animal_service=animal_service)

async def get_delete_animal_by_id_interactor(
        animal_service: AnimalServiceProtocol = Depends(get_animals_service)
) -> DeleteAnimalByIdInteractor:
    return DeleteAnimalByIdInteractor(animal_service=animal_service)
