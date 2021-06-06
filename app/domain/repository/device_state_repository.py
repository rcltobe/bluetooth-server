from __future__ import annotations

import time
from abc import abstractmethod
from typing import List, Optional


class DeviceStateEntity:
    def __init__(self, address: str, found: bool, created_at: Optional[float] = None):
        self.created_at: float = time.time() if created_at is None else created_at
        self.address: str = address
        self.found = found

    def to_json(self):
        return {
            "address": self.address,
            "found": 1 if self.found else 0,
            "createdAt": int(self.created_at),
        }

    def to_csv(self) -> List[str]:
        return [self.address, self.found, int(self.created_at)]

    @classmethod
    def from_csv(cls, csv: List[str]) -> Optional[DeviceStateEntity]:
        if len(csv) < 3:
            return None

        try:
            found = True if int(csv[1]) == 1 else False
        except ValueError:
            found = False

        return DeviceStateEntity(
            address=csv[0],
            found=found,
            created_at=float(csv[2])
        )

    def next(self, states: List[DeviceStateEntity]) -> Optional[DeviceStateEntity]:
        after = [state for state
                 in states
                 if state.created_at > self.created_at
                 and state.address == self.address
                 and state.found != self.found
                 ]
        if len(after) == 0:
            return None

        after = sorted(after, key=lambda state: state.created_at, reverse=True)

        return after[0]


class AbstractDeviceStateRepository:
    @abstractmethod
    async def find_all(self) -> List[DeviceStateEntity]:
        pass

    @abstractmethod
    async def find_last(self, address: str) -> Optional[DeviceStateEntity]:
        """
        更新日が最新の DeviceStateEntity を取得
        """
        pass

    @abstractmethod
    async def find_all_by_address(self, address: str) -> List[DeviceStateEntity]:
        pass

    @abstractmethod
    async def save(self, state: DeviceStateEntity):
        pass
