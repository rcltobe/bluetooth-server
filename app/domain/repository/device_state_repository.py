import time
from abc import abstractmethod
from typing import List

from app.domain.models.bluetooth import DeviceState


class DeviceStateEntity:
    def __init__(self, address: str, state: DeviceState, created_at: float = time.time()):
        self.address = address
        self.state = state
        self.created_at = created_at


class AbstractDeviceStateRepository:
    @abstractmethod
    async def find_all(self) -> List[DeviceStateEntity]:
        pass

    @abstractmethod
    async def save(self, state: DeviceStateEntity):
        pass
