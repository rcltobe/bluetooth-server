from abc import abstractmethod
from typing import List

from app.domain.models.bluetooth import BluetoothDevice


class AbstractDeviceRepository:
    @abstractmethod
    async def find_all(self) -> List[BluetoothDevice]:
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> List[BluetoothDevice]:
        pass

    @abstractmethod
    async def save(self, device: BluetoothDevice):
        pass

    @abstractmethod
    async def delete(self, address: str):
        pass

    @abstractmethod
    async def delete_all_by_user_id(self, user_id: str):
        """
        user_id に紐づくすべての端末を削除
        """
        pass
