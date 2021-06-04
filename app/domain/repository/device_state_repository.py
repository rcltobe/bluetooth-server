from __future__ import annotations

import time
from abc import abstractmethod
from typing import List, Optional

from app.domain.models.bluetooth import DeviceState


class DeviceStateEntity:
    def __init__(self, address: str, state: DeviceState, created_at: Optional[float] = None):
        self.created_at: float = time.time() if created_at is None else created_at
        self.address: str = address
        self.state: DeviceState = state

    def to_json(self):
        return {
            "address": self.address,
            "state": self.state.name,
            "createdAt": int(self.created_at),
        }

    def to_csv(self) -> List[str]:
        return [self.address, self.state.value, int(self.created_at)]

    @classmethod
    def from_csv(cls, csv: List[str]) -> DeviceStateEntity:
        return DeviceStateEntity(
            address=csv[0],
            state=DeviceState.value_of(csv[1]),
            created_at=float(csv[2])
        )

    def next(self, states: List[DeviceStateEntity]) -> Optional[DeviceStateEntity]:
        after = [state for state
                 in states
                 if state.created_at > self.created_at
                 and state.address == self.address
                 and state.state.value != self.state.value
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
