from __future__ import annotations

import time
import uuid
from abc import abstractmethod
from typing import List, Optional


class DeviceStateEntity:
    def __init__(self, address: str, found: bool, id: Optional[str] = None, created_at: Optional[float] = None):
        self.id = str(uuid.uuid4()) if id is None else id
        self.created_at: float = time.time() if created_at is None else created_at
        self.address: str = address
        self.found = found

    def to_json(self):
        return {
            "id": self.id,
            "address": self.address,
            "found": self.found,
            "createdAt": int(self.created_at),
        }

    def to_csv(self) -> List[str]:
        return [self.id, self.address, 1 if self.found else 0, int(self.created_at)]

    @classmethod
    def from_csv(cls, csv: List[str]) -> Optional[DeviceStateEntity]:
        if len(csv) < 4:
            return None

        try:
            found = True if int(csv[2]) == 1 else False
        except ValueError:
            found = False

        return DeviceStateEntity(
            id=csv[0],
            address=csv[1],
            found=found,
            created_at=float(csv[3])
        )


class AbstractDeviceStateRepository:
    @abstractmethod
    async def find_last(self, address: str) -> Optional[DeviceStateEntity]:
        """
        更新日が最新の DeviceStateEntity を取得
        """
        pass

    @abstractmethod
    async def save(self, state: DeviceStateEntity):
        """
        端末の検索結果を保存
        """
        pass
