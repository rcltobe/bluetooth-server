from abc import abstractmethod
from typing import List

from app.domain.models.device_state import DeviceState


class AbstractDeviceStateRepository:
    @abstractmethod
    async def find_all(self) -> List[DeviceState]:
        """
        すべての端末の検索結果を取得
        """
        pass

    @abstractmethod
    async def save_all(self, states: List[DeviceState]):
        """
        端末の検索結果を保存
        """
        pass

    async def delete_before(self, time_in_mills: int):
        """
        指定された時刻以前の、検索結果を削除する
        """
        pass
