from abc import abstractmethod
from typing import List

from app.domain.models.bluetooth import BluetoothDevice


class AbstractDeviceRepository:
    @abstractmethod
    async def find_all(self) -> List[BluetoothDevice]:
        """
        すべての端末を取得する
        """
        pass
