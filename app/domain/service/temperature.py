from typing import List

from app.domain.models.body_temperature import BodyTemperature
from app.domain.repository.body_temperature_repository import AbstractBodyTemperatureRepository
from app.infra.repository import RepositoryContainer


class BodyTemperatureService:
    def __init__(self,
                 body_temperature_repository: AbstractBodyTemperatureRepository
                 = RepositoryContainer.body_temperature_repository
                 ):
        self.body_temperature_repository = body_temperature_repository

    async def find_all(self) -> List[BodyTemperature]:
        return await self.body_temperature_repository.find_all()

    async def save(self, temperature: float, user_id: str):
        data = BodyTemperature(temperature, user_id)
        await self.body_temperature_repository.save(data)
