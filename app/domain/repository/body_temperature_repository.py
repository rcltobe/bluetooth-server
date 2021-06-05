from abc import abstractmethod
from typing import List

from app.domain.models.body_temperature import BodyTemperature


class AbstractBodyTemperatureRepository:
    @abstractmethod
    async def find_all(self) -> List[BodyTemperature]:
        pass

    @abstractmethod
    async def save(self, data: BodyTemperature):
        pass
