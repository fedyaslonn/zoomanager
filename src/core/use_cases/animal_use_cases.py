from typing import Annotated, Protocol, Optional, Tuple, Type, TypeVar

from src.core.dtos.zoo_dto import *

from src.core.services.animals_service import AnimalServiceProtocol

animal_input = TypeVar('animal_input', contravariant=True)
animal_output = TypeVar('animal_output', contravariant=True)

class AnimalUseCaseProtocol(Protocol[animal_input, animal_output]):
    async def __call__(self, data: animal_input) -> animal_output:
        ...

class CreateAnimalUseCase:
    def __init__(self, animal_service: AnimalServiceProtocol):
        self.animal_service = animal_service

    async def __call__(self, animal_data: CreateAnimal) -> AnimalSchema:
        return await self.animal_service.create_animal(animal_data)

class UpdateAnimalUseCase:
    def __init__(self, animal_service: AnimalServiceProtocol):
        self.animal_service = animal_service

    async def __call__(self, animal_data: UpdateAnimalRequest) -> UpdateAnimalResponse:
        return await self.animal_service.update_animal(animal_data)

class DeleteAnimalUseCase:
    def __init__(self, animal_service: AnimalServiceProtocol):
        self.animal_service = animal_service

    async def __call__(self, id: int):
        return await self.animal_service.delete_animal_by_id(id)

